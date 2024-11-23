from faker import Faker
import pandas as pd
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

# Generate Customers
def generate_customer(customer_id):
    """Generate a single customer record."""
    return {
        "customer_id": customer_id,
        "name": fake.name(),
        "age": random.randint(18, 80),
        "gender": random.choice(["Male", "Female", "Other"]),
        "location": fake.city()
    }

# Generate Usage
def generate_usage(usage_id, customer_id):
    """Generate a single usage record."""
    return {
        "usage_id": usage_id,
        "customer_id": customer_id,
        "feature_name": random.choice(["Feature A", "Feature B", "Feature C", "Feature D"]),
        "usage_frequency": random.randint(1, 500),  # Number of times a feature was used
        "last_used_date": fake.date_between(start_date='-1y', end_date='today')
    }

# Generate Transactions
def generate_transaction(transaction_id, customer_id):
    """Generate a single transaction record."""
    plan_types = ["Basic", "Premium", "Enterprise"]
    plan_prices = {"Basic": 9.99, "Premium": 19.99, "Enterprise": 49.99}
    plan_type = random.choice(plan_types)
    amount = plan_prices[plan_type] + round(random.uniform(-2.0, 2.0), 2)  # Add minor price variation

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "payment_date": fake.date_between(start_date='-1y', end_date='today'),
        "amount": amount,
        "plan_type": plan_type
    }

# Generate Feedback
def generate_feedback(feedback_id, customer_id):
    """Generate a single feedback record."""
    return {
        "feedback_id": feedback_id,
        "customer_id": customer_id,
        "feedback_text": fake.sentence(),
        "rating": random.randint(1, 5)
    }
