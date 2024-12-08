## Main ETL Process (`etl.py`)

# Loading modules and packages
from models import *  # Import all models
from database import engine, SessionLocal
from data_generator import (
    generate_customer,
    generate_usage,
    generate_transaction,
    generate_feedback,
)
import pandas as pd
from loguru import logger
import random
import glob
from os import path
import os
from sqlalchemy import text
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Declaring Constants
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_USAGE_RECORDS = 5000
NUMBER_OF_TRANSACTIONS = 3000
NUMBER_OF_FEEDBACK_RECORDS = 1000

# Ensure data folder exists
DATA_FOLDER = "data/"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Generating Customer Data
customers = pd.DataFrame(
    [generate_customer(customer_id) for customer_id in range(NUMBER_OF_CUSTOMERS)]
)
logger.info("Customer Data")
logger.info(customers.head(1))
customers.to_csv(f"{DATA_FOLDER}customers.csv", index=False)
logger.info(f"Customer Data saved to CSV: {customers.shape}")

# Generating Usage Data
usage = pd.DataFrame(
    [
        generate_usage(usage_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for usage_id in range(NUMBER_OF_USAGE_RECORDS)
    ]
)
logger.info("Usage Data")
logger.info(usage.head(1))
usage.to_csv(f"{DATA_FOLDER}usage.csv", index=False)
logger.info(f"Usage Data saved to CSV: {usage.shape}")

# Generating Transaction Data
transactions = pd.DataFrame(
    [
        generate_transaction(transaction_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for transaction_id in range(NUMBER_OF_TRANSACTIONS)
    ]
)
logger.info("Transaction Data")
logger.info(transactions.head(1))
transactions.to_csv(f"{DATA_FOLDER}transactions.csv", index=False)
logger.info(f"Transaction Data saved to CSV: {transactions.shape}")

# Generating Feedback Data
feedback = pd.DataFrame(
    [
        generate_feedback(feedback_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for feedback_id in range(NUMBER_OF_FEEDBACK_RECORDS)
    ]
)
logger.info("Feedback Data")
logger.info(feedback.head(1))
feedback.to_csv(f"{DATA_FOLDER}feedback.csv", index=False)
logger.info(f"Feedback Data saved to CSV: {feedback.shape}")

# Load CSV to Database Table with Duplicate Handling
def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.
    Skips rows with duplicate primary keys using ON CONFLICT DO NOTHING.

    Args:
        table_name (str): Name of the database table.
        csv_path (str): Path to the CSV file containing data.
    """
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_path)

        # Use SQLAlchemy to insert rows with conflict handling
        with engine.connect() as connection:
            for _, row in df.iterrows():
                # Build INSERT query with ON CONFLICT DO NOTHING
                query = text(f"""
                    INSERT INTO {table_name} ({', '.join(df.columns)})
                    VALUES ({', '.join([':{}'.format(col) for col in df.columns])})
                    ON CONFLICT DO NOTHING;
                """)
                connection.execute(query, row.to_dict())
        logger.info(f"Loaded {table_name} into the database (skipping duplicates).")
    except Exception as e:
        logger.error(f"Failed to load {table_name}: {e}")

# Fetch Combined Data for Predictions
def fetch_data_for_predictions():
    """
    Fetch and combine data from the database for training and prediction purposes.

    Returns:
        DataFrame: Combined customer data.
    """
    session = SessionLocal()
    try:
        customers = session.query(Customer).all()
        usage = session.query(Usage).all()
        transactions = session.query(Transaction).all()

        # Convert data into DataFrames
        customers_df = pd.DataFrame([{
            'customer_id': c.customer_id,
            'age': c.age,
            'location': c.location
        } for c in customers])

        usage_df = pd.DataFrame([{
            'customer_id': u.customer_id,
            'usage_frequency': u.usage_frequency
        } for u in usage])

        transactions_df = pd.DataFrame([{
            'customer_id': t.customer_id,
            'amount': t.amount
        } for t in transactions])

        # Merge data into one DataFrame
        data = customers_df.merge(usage_df, on="customer_id", how="left")
        data = data.merge(transactions_df, on="customer_id", how="left")
        return data
    finally:
        session.close()

# Train Model and Predict
def train_and_predict(data):
    """
    Train a machine learning model and predict churn probabilities.

    Args:
        data (DataFrame): Combined customer data.

    Returns:
        DataFrame: Updated DataFrame with predictions and probabilities.
    """
    data['churn'] = (data['usage_frequency'] < 5).astype(int)

    # Features and target
    features = ['age', 'usage_frequency', 'amount']
    X = data[features].fillna(0)
    y = data['churn']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Predict probabilities
    data['predicted_churn'] = model.predict(X)
    data['churn_probability'] = model.predict_proba(X)[:, 1]
    return data

# Populate Results Table
def populate_results_table(data):
    """
    Populate the results table with prediction data.

    Args:
        data (DataFrame): DataFrame containing prediction results.
    """
    session = SessionLocal()
    try:
        for _, row in data.iterrows():
            result = Result(
                customer_id=row['customer_id'],
                prediction="Churn" if row['predicted_churn'] == 1 else "No Churn",
                probability=row['churn_probability'],
                created_at=pd.Timestamp.now()
            )
            session.add(result)
        session.commit()
        logger.info("Results table populated.")
    finally:
        session.close()

# Main ETL Process
if __name__ == "__main__":
    logger.info("Starting ETL process...")

    # Load data into database
    folder_path = f"{DATA_FOLDER}*.csv"
    files = glob.glob(folder_path)
    for file_path in files:
        table_name = path.splitext(path.basename(file_path))[0]
        load_csv_to_table(table_name, file_path)

    # Fetch data for predictions
    data_for_predictions = fetch_data_for_predictions()

    # Train model and generate predictions
    data_with_predictions = train_and_predict(data_for_predictions)

    # Populate results table
    populate_results_table(data_with_predictions)

    logger.info("ETL process completed.")

## Data Generation (`data_generator.py`)

from faker import Faker
import pandas as pd
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

def generate_customer(customer_id):
    """
    Generate a single customer record.

    Args:
        customer_id (int): Unique identifier for the customer.

    Returns:
        dict: A dictionary representing the customer's details.
            - customer_id (int): Customer's unique ID.
            - name (str): Full name of the customer.
            - age (int): Age of the customer (18-80).
            - gender (str): Gender of the customer.
            - location (str): City of residence.
    """
    return {
        "customer_id": customer_id,
        "name": fake.name(),
        "age": random.randint(18, 80),
        "gender": random.choice(["Male", "Female", "Other"]),
        "location": fake.city()
    }

def generate_usage(usage_id, customer_id):
    """
    Generate a single usage record.

    Args:
        usage_id (int): Unique identifier for the usage record.
        customer_id (int): Unique identifier for the associated customer.

    Returns:
        dict: A dictionary representing the usage record.
            - usage_id (int): Usage record's unique ID.
            - customer_id (int): Customer's unique ID.
            - feature_name (str): Name of the feature used.
            - usage_frequency (int): Number of times the feature was used (1-500).
            - last_used_date (date): The last date the feature was used (up to 1 year ago).
    """
    return {
        "usage_id": usage_id,
        "customer_id": customer_id,
        "feature_name": random.choice(["Feature A", "Feature B", "Feature C", "Feature D"]),
        "usage_frequency": random.randint(1, 500),
        "last_used_date": fake.date_between(start_date='-1y', end_date='today')
    }

def generate_transaction(transaction_id, customer_id):
    """
    Generate a single transaction record.

    Args:
        transaction_id (int): Unique identifier for the transaction record.
        customer_id (int): Unique identifier for the associated customer.

    Returns:
        dict: A dictionary representing the transaction record.
            - transaction_id (int): Transaction's unique ID.
            - customer_id (int): Customer's unique ID.
            - payment_date (date): The date of the payment (up to 1 year ago).
            - amount (float): The amount paid for the plan with minor price variations.
            - plan_type (str): Type of plan purchased (Basic, Premium, Enterprise).
    """
    plan_types = ["Basic", "Premium", "Enterprise"]
    plan_prices = {"Basic": 9.99, "Premium": 19.99, "Enterprise": 49.99}
    plan_type = random.choice(plan_types)
    amount = plan_prices[plan_type] + round(random.uniform(-2.0, 2.0), 2)

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "payment_date": fake.date_between(start_date='-1y', end_date='today'),
        "amount": amount,
        "plan_type": plan_type
    }

def generate_feedback(feedback_id, customer_id):
    """
    Generate a single feedback record.

    Args:
        feedback_id (int): Unique identifier for the feedback record.
        customer_id (int): Unique identifier for the associated customer.

    Returns:
        dict: A dictionary representing the feedback record.
            - feedback_id (int): Feedback record's unique ID.
            - customer_id (int): Customer's unique ID.
            - feedback_text (str): Randomly generated feedback text.
            - rating (int): Rating given by the customer (1-5).
    """
    return {
        "feedback_id": feedback_id,
        "customer_id": customer_id,
        "feedback_text": fake.sentence(),
        "rating": random.randint(1, 5)
    }


## Machine Learning Model (`data_science_model.py`)

from sqlalchemy.orm import sessionmaker
from database import engine
from models import Customer, Usage, Transaction, Feedback
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Establish database session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_prepare_data():
    customers = session.query(Customer).all()
    customers_df = pd.DataFrame([{
        'customer_id': c.customer_id,
        'age': c.age,
        'gender': c.gender,
        'location': c.location,
        'churn_prediction': c.churn_prediction
    } for c in customers])

    usage = session.query(Usage).all()
    usage_df = pd.DataFrame([{
        'customer_id': u.customer_id,
        'usage_frequency': u.usage_frequency,
        'last_used_date': u.last_used_date
    } for u in usage])

    transactions = session.query(Transaction).all()
    transactions_df = pd.DataFrame([{
        'customer_id': t.customer_id,
        'amount': t.amount,
        'plan_type': t.plan_type
    } for t in transactions])

    data = customers_df.merge(usage_df, on="customer_id", how="left")
    data = data.merge(transactions_df, on="customer_id", how="left")

    data['plan_type'] = data['plan_type'].fillna('Unknown')
    data['amount'] = data['amount'].fillna(0)
    data['usage_frequency'] = data['usage_frequency'].fillna(0)

    data = pd.get_dummies(data, columns=['gender', 'plan_type', 'location'], drop_first=True)
    return data

def train_model(data):
    features = [col for col in data.columns if col not in ['customer_id', 'churn_prediction']]
    target = 'churn_prediction'

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(random_state=42, n_estimators=200, max_depth=10)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("Model Evaluation:")
    print(report)

    with open("model_metrics.txt", "w") as f:
        f.write("Model Evaluation Metrics:\n")
        f.write(report)

    data['predicted_churn'] = model.predict(X)
    data['churn_probability'] = model.predict_proba(X)[:, 1]
    return model, data

def update_predictions_in_database(data):
    try:
        print("Updating churn predictions in the database...")
        for _, row in data.iterrows():
            # Fetch the customer from the database
            customer = session.query(Customer).filter_by(customer_id=row['customer_id']).first()
            
            if customer:
                # Update churn_prediction field
                customer.churn_prediction = int(row['predicted_churn'])
            else:
                print(f"Customer with ID {row['customer_id']} not found in the database.")

        # Commit all updates
        session.commit()
        print("Churn predictions successfully updated in the database.")
    except Exception as e:
        # Rollback in case of any failure
        session.rollback()
        print(f"Error updating database: {e}")


def save_model(model, filename="final_model.pkl"):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}.")

def save_predictions_to_csv(data, filename="final_predictions.csv"):
    final_output = data[['customer_id', 'predicted_churn', 'churn_probability']]
    final_output.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}.")

if __name__ == "__main__":
    print("Fetching and preparing data...")
    data = fetch_and_prepare_data()

    print("Training the model...")
    model, data_with_predictions = train_model(data)

    print("Updating predictions in the database...")
    update_predictions_in_database(data_with_predictions)

    print("Saving the model...")
    save_model(model)

    print("Saving predictions to a CSV file...")
    save_predictions_to_csv(data_with_predictions)

    print("Model training and prediction process completed successfully!")
