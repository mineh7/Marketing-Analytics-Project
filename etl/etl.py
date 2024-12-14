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
from sqlalchemy.exc import IntegrityError
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

# Log and check for duplicate customer IDs
duplicate_ids = customers[customers.duplicated(subset=["customer_id"], keep=False)]
if not duplicate_ids.empty:
    logger.warning("Duplicate customer IDs detected:")
    logger.warning(duplicate_ids)
else:
    logger.info("No duplicate customer IDs detected.")

# Remove duplicate customer IDs
customers = customers.drop_duplicates(subset=["customer_id"])
logger.info(f"Customer Data cleaned. Shape after removing duplicates: {customers.shape}")

# Save the cleaned data to CSV
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

# Load CSV to Database Table using SQLAlchemy

def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.

    Parameters:
    - table_name (str): The name of the database table.
    - csv_path (str): The path to the CSV file containing data.
    """
    session = SessionLocal()
    try:
        # Clear existing data
        session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        session.commit()

        # Load new data
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        logger.info(f"Successfully loaded data into table: {table_name}")
    except IntegrityError as e:
        logger.error(f"Integrity error while loading data into table {table_name}: {e}")
    except Exception as e:
        logger.error(f"Failed to load data into table {table_name}: {e}")
    finally:
        session.close()


# Fetch Combined Data for Predictions
def fetch_data_for_predictions():
    """
    Fetch and combine data from the database for training and prediction purposes.
    """
    session = SessionLocal()
    try:
        customers = session.query(Customer).all()
        usage = session.query(Usage).all()
        transactions = session.query(Transaction).all()

        customers_df = pd.DataFrame(
            [{"customer_id": c.customer_id, "age": c.age, "location": c.location} for c in customers]
        )
        usage_df = pd.DataFrame(
            [{"customer_id": u.customer_id, "usage_frequency": u.usage_frequency} for u in usage]
        )
        transactions_df = pd.DataFrame(
            [{"customer_id": t.customer_id, "amount": t.amount} for t in transactions]
        )

        data = customers_df.merge(usage_df, on="customer_id", how="left")
        data = data.merge(transactions_df, on="customer_id", how="left")
        return data
    finally:
        session.close()

# Train Model and Predict
def train_and_predict(data):
    """
    Train a machine learning model and predict churn probabilities.
    """
    data["churn"] = (data["usage_frequency"] < 5).astype(int)
    features = ["age", "usage_frequency", "amount"]
    X = data[features].fillna(0)
    y = data["churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    logger.info("Model Classification Report:")
    logger.info(classification_report(y_test, y_pred))

    data["predicted_churn"] = model.predict(X)
    data["churn_probability"] = model.predict_proba(X)[:, 1]
    return data

# Populate Results Table
def populate_results_table(data):
    """
    Populate the results table with prediction data.
    """
    session = SessionLocal()
    try:
        for _, row in data.iterrows():
            result = Result(
                customer_id=row["customer_id"],
                prediction="Churn" if row["predicted_churn"] == 1 else "No Churn",
                probability=row["churn_probability"],
                created_at=pd.Timestamp.now(),
            )
            session.add(result)
        session.commit()
        logger.info("Results table populated.")
    finally:
        session.close()

# Main ETL Process
if __name__ == "__main__":
    logger.info("Starting ETL process...")
    folder_path = f"{DATA_FOLDER}*.csv"
    files = glob.glob(folder_path)

    for file_path in files:
        table_name = path.splitext(path.basename(file_path))[0]
        load_csv_to_table(table_name, file_path)

    data_for_predictions = fetch_data_for_predictions()
    data_with_predictions = train_and_predict(data_for_predictions)
    populate_results_table(data_with_predictions)
    logger.info("ETL process completed.")
