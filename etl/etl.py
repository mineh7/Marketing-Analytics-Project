# Loading modules and packages
from models import *


import time

# Pause code execution for 10 seconds
print("Pausing for 20 seconds...")
time.sleep(60)
print("Resuming execution.")


from database import engine, Base
import pandas as pd
from data_generator import (
    generate_customer,
    generate_usage,
    generate_transaction,
    generate_feedback,
)
from loguru import logger
import os
import random  # <--- Add this import

# Constants
NUMBER_OF_CUSTOMERS = 2000
NUMBER_OF_USAGE_RECORDS = 5000
NUMBER_OF_TRANSACTIONS = 3000
NUMBER_OF_FEEDBACK_RECORDS = 1000
DATA_FOLDER = "data/"

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

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

if __name__ == "__main__":
    logger.info("Starting data generation...")
    generate_and_save_data()
    logger.info("Data generation completed.")



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
    logger.info(f'loading {table_name}')


import glob
from os import path


# Specify the path to the folder, using "*" to match all files
folder_path = "data/*.csv"

# Use glob to get a list of file paths in the specified folder
files = glob.glob(folder_path)
base_names = [path.splitext(path.basename(file))[0] for file in files]
# Print the list of files
for table in base_names:
    try:
        load_csv_to_table(table, path.join("data/", f"{table}.csv"))
    except Exception as e:
        print(f"Failed to ingest table {table}. Moving to the next!")

print("Tables are populated.")
