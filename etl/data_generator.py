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
