from models import *  # Import all models
from database import engine, SessionLocal
from data_generator import (
    generate_customer,
    generate_usage,
    generate_transaction,
    generate_feedback,
)
from modeling import fetch_data_for_predictions, train_and_predict, populate_results_table
import pandas as pd
from loguru import logger
import random
import glob
from os import path
import os
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

# Declaring Constants
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_USAGE_RECORDS = 5000
NUMBER_OF_TRANSACTIONS = 3000
NUMBER_OF_FEEDBACK_RECORDS = 1000

# Ensure data folder exists
DATA_FOLDER = "data/"
os.makedirs(DATA_FOLDER, exist_ok=True)

# (Data generation code remains the same...)

# Load CSV to Database Table using SQLAlchemy
def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.
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

# Main ETL Process
if __name__ == "__main__":
    logger.info("Starting ETL process...")
    folder_path = f"{DATA_FOLDER}*.csv"
    files = glob.glob(folder_path)

    for file_path in files:
        table_name = path.splitext(path.basename(file_path))[0]
        load_csv_to_table(table_name, file_path)

    # Modeling part (delegated to modeling.py)
    data_for_predictions = fetch_data_for_predictions()
    data_with_predictions = train_and_predict(data_for_predictions)
    populate_results_table(data_with_predictions)
    logger.info("ETL process completed.")
