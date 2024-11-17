import sqlite3
import pandas as pd

# Creating a database connection

conn = sqlite3.connect('customer_retention.db')
cursor = conn.cursor()

print("Database connected successfully!")

# Creating respective tables
create_customers_table = """
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Age INTEGER,
    Gender TEXT,
    Location TEXT,
    SubscriptionStartDate DATE,
    SubscriptionEndDate DATE
);
"""

create_transactions_table = """
CREATE TABLE IF NOT EXISTS Transactions (
    TransactionID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    PaymentDate DATE,
    Amount REAL,
    PlanType TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
"""

create_usage_table = """
CREATE TABLE IF NOT EXISTS Usage (
    UsageID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    FeatureName TEXT,
    UsageFrequency INTEGER,
    LastUsedDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
"""

create_feedback_table = """
CREATE TABLE IF NOT EXISTS Feedback (
    FeedbackID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    FeedbackText TEXT,
    Rating INTEGER,
    SubmissionDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
"""

# execute the queries to create the tables
cursor.execute(create_customers_table)
cursor.execute(create_transactions_table)
cursor.execute(create_usage_table)
cursor.execute(create_feedback_table)

print("Tables created successfully!")
conn.commit()

# Load data from flat files (Synthetic data is used)
customers_df = pd.read_csv('customers.csv')
transactions_df = pd.read_csv('transactions.csv')
usage_df = pd.read_csv('usage.csv')
feedback_df = pd.read_csv('feedback.csv')

# Insert data into the database
customers_df.to_sql('Customers', conn, if_exists='append', index=False)
transactions_df.to_sql('Transactions', conn, if_exists='append', index=False)
usage_df.to_sql('Usage', conn, if_exists='append', index=False)
feedback_df.to_sql('Feedback', conn, if_exists='append', index=False)

print("Data inserted successfully!")


def get_high_risk_customers():
    query = """
    SELECT c.CustomerID, c.Name, c.Location, f.Rating, u.UsageFrequency
    FROM Customers c
    LEFT JOIN Feedback f ON c.CustomerID = f.CustomerID
    LEFT JOIN Usage u ON c.CustomerID = u.CustomerID
    WHERE f.Rating < 3 OR u.UsageFrequency < 5;
    """
    results = cursor.execute(query).fetchall()
    return results

high_risk_customers = get_high_risk_customers()
print("High-risk customers:", high_risk_customers)