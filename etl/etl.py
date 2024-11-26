# Loading modules and packages
from models import *
from database import engine, Base
import pandas as pd
from os import path
import glob
from data_generator import (
    generate_customer,
    generate_usage,
    generate_transaction,
    generate_feedback,
)
from loguru import logger
import os
import random  # Required for generating random data
from sqlalchemy.orm import sessionmaker
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Constants
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_USAGE_RECORDS = 5000
NUMBER_OF_TRANSACTIONS = 3000
NUMBER_OF_FEEDBACK_RECORDS = 1000
DATA_FOLDER = "data/"

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

# Data generation
def generate_and_save_data():
    """Generate data and save as CSV files."""
    # Generate customers
    customers = pd.DataFrame([generate_customer(customer_id) for customer_id in range(1, NUMBER_OF_CUSTOMERS + 1)])
    customers.to_csv(f"{DATA_FOLDER}customers.csv", index=False)
    logger.info(f"Generated customers.csv with {len(customers)} records.")

    # Generate usage
    usage = pd.DataFrame([
        generate_usage(usage_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for usage_id in range(1, NUMBER_OF_USAGE_RECORDS + 1)
    ])
    usage.to_csv(f"{DATA_FOLDER}usage.csv", index=False)
    logger.info(f"Generated usage.csv with {len(usage)} records.")

    # Generate transactions
    transactions = pd.DataFrame([
        generate_transaction(transaction_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for transaction_id in range(1, NUMBER_OF_TRANSACTIONS + 1)
    ])
    transactions.to_csv(f"{DATA_FOLDER}transactions.csv", index=False)
    logger.info(f"Generated transactions.csv with {len(transactions)} records.")

    # Generate feedback
    feedback = pd.DataFrame([
        generate_feedback(feedback_id, random.randint(1, NUMBER_OF_CUSTOMERS))
        for feedback_id in range(1, NUMBER_OF_FEEDBACK_RECORDS + 1)
    ])
    feedback.to_csv(f"{DATA_FOLDER}feedback.csv", index=False)
    logger.info(f"Generated feedback.csv with {len(feedback)} records.")

# Load data into the database
def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.

    Args:
    - table_name: Name of the database table.
    - csv_path: Path to the CSV file containing data.

    Returns:
    - None
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f'Loaded {table_name} into the database.')

# Fetch data for predictions
def fetch_data_for_predictions():
    """
    Fetch and combine data from the database for prediction purposes.
    """
    customers = session.query(Customer).all()
    usage = session.query(Usage).all()
    transactions = session.query(Transaction).all()

    customers_df = pd.DataFrame([{
        'customer_id': c.customer_id,
        'age': c.age,
        'location': c.location
    } for c in customers])

    usage_df = pd.DataFrame([{
        'customer_id': u.customer_id,
        'usage_frequency': u.usage_frequency,
        'last_used_date': u.last_used_date
    } for u in usage])

    transactions_df = pd.DataFrame([{
        'customer_id': t.customer_id,
        'amount': t.amount,
        'plan_type': t.plan_type
    } for t in transactions])

    # Merge datasets
    data = customers_df.merge(usage_df, on="customer_id", how="left")
    data = data.merge(transactions_df, on="customer_id", how="left")
    return data

# Prediction function
def train_and_predict(data):
    """
    Train a model and predict churn based on customer data.

    Args:
    - data: Combined customer data (DataFrame).

    Returns:
    - Updated DataFrame with predictions.
    """
    # Simulate churn column
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

    # Predict for all customers
    data['predicted_churn'] = model.predict(X)
    return data

# Update predictions in the database
def update_predictions_in_database(data):
    """
    Update churn predictions in the database.

    Args:
    - data: DataFrame with predictions.
    """
    for _, row in data.iterrows():
        customer = session.query(Customer).filter_by(customer_id=row['customer_id']).first()
        if customer:
            customer.churn_prediction = int(row['predicted_churn'])
            session.commit()

if __name__ == "__main__":
    # Step 1: Data generation
    logger.info("Starting data generation...")
    generate_and_save_data()
    logger.info("Data generation completed.")

    # Step 2: Load data into the database
    folder_path = "data/*.csv"
    files = glob.glob(folder_path)
    for file_path in files:
        table_name = path.splitext(path.basename(file_path))[0]
        try:
            load_csv_to_table(table_name, file_path)
        except Exception as e:
            logger.error(f"Failed to load table {table_name}: {e}")

    # Step 3: Perform predictions
    logger.info("Fetching data for predictions...")
    data_for_predictions = fetch_data_for_predictions()

    logger.info("Training model and making predictions...")
    data_with_predictions = train_and_predict(data_for_predictions)

    logger.info("Updating predictions in the database...")
    update_predictions_in_database(data_with_predictions)

    logger.info("ETL process with predictions completed.")
