from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base, engine
import datetime

Base = declarative_base()

# Customer Model
class Customer(Base):
    """
    Represents a customer in the database.

    Attributes:
        customer_id (int): Unique identifier for the customer.
        name (str): Full name of the customer.
        age (int): Age of the customer.
        gender (str): Gender of the customer.
        location (str): City or location of the customer.
        churn_prediction (int): Predicted churn status for the customer (nullable).
        transactions (list): List of related transactions for the customer.
        usage (list): List of related usage records for the customer.
        feedback (list): List of related feedback entries for the customer.
        results (list): List of related prediction results for the customer.
    """
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    churn_prediction = Column(Integer, nullable=True)
    transactions = relationship("Transaction", back_populates="customer")
    usage = relationship("Usage", back_populates="customer")
    feedback = relationship("Feedback", back_populates="customer")
    results = relationship("Result", back_populates="customer")


# Usage Model
class Usage(Base):
    """
    Represents usage data for a customer.

    Attributes:
        usage_id (int): Primary key for the usage record.
        feature_name (str): Name of the feature used.
        usage_frequency (int): Frequency of usage.
        payment_date (datetime): Date of payment for the feature.
        last_used_date (datetime): Last date the feature was used.
        customer_id (int): Foreign key referencing the associated customer.
        customer (Customer): Relationship to the associated customer.
    """
    __tablename__ = 'usage'
    usage_id = Column(Integer, primary_key=True)
    feature_name = Column(String)
    usage_frequency = Column(Integer)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_used_date = Column(DateTime, default=datetime.datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="usage")


# Transaction Model
class Transaction(Base):
    """
    Represents a transaction made by a customer.

    Attributes:
        transaction_id (int): Primary key for the transaction.
        amount (float): Amount paid in the transaction.
        plan_type (str): Type of plan (e.g., Basic, Premium).
        payment_date (datetime): Date of the payment.
        last_used_date (datetime): Last date of usage for the transaction.
        customer_id (int): Foreign key referencing the associated customer.
        customer (Customer): Relationship to the associated customer.
    """
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Float)
    plan_type = Column(String)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_used_date = Column(DateTime, default=datetime.datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="transactions")


# Feedback Model
class Feedback(Base):
    """
    Represents customer feedback.

    Attributes:
        feedback_id (int): Primary key for the feedback record.
        feedback_text (str): Feedback provided by the customer.
        rating (int): Rating given by the customer.
        customer_id (int): Foreign key referencing the associated customer.
        customer (Customer): Relationship to the associated customer.
    """
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True)
    feedback_text = Column(String)
    rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="feedback")


# Results Model
class Result(Base):
    """
    Represents predictions or results for a customer.

    Attributes:
        result_id (int): Primary key for the result record.
        customer_id (int): Foreign key referencing the associated customer.
        prediction (str): The model's prediction outcome (e.g., "Churn").
        probability (float): Probability score of the prediction.
        created_at (datetime): Timestamp when the result was generated.
        customer (Customer): Relationship to the associated customer.
    """
    __tablename__ = 'results'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    prediction = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="results")


# Create all tables
Base.metadata.create_all(engine)
