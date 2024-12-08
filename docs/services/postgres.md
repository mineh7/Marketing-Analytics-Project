## Database Models (`models.py`)

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
import datetime

# Customer Model
class Customer(Base):
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
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True)
    feedback_text = Column(String)
    rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="feedback")

# Results Model
class Result(Base):
    __tablename__ = 'results'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    prediction = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    customer = relationship("Customer", back_populates="results")

# Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)


## Database Connection (`database.py`)


"""
Database Configuration

This module sets up the database connection, engine, and session management
using SQLAlchemy. It loads configuration from environment variables defined in
a `.env` file.
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

def get_db():
    """
    Provides a database session for interacting with the database.

    This function is used to yield a SQLAlchemy session object (`SessionLocal`) 
    for performing database operations. The session is automatically closed 
    after use to prevent connection leaks.

    Yields:
        SessionLocal: A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Load environment variables from the `.env` file
load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
"""
str: The database connection URL. This value is loaded from the `.env` file
and is used to configure the SQLAlchemy engine. Example format:
`postgresql+psycopg2://user:password@host:port/database`
"""

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)
"""
Engine: SQLAlchemy engine object used to manage the connection pool and 
execute SQL statements. Configured using the `DATABASE_URL`.
"""

# Base class for declarative models
Base = declarative.declarative_base()
"""
DeclarativeMeta: Base class for all ORM models. All models should inherit from this
to define database tables.
"""

# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Session: Configured sessionmaker object for creating session instances. Sessions
are used to interact with the database and manage transactions.
"""

# Test the database connection when run directly
if __name__ == "__main__":
    """
    When this script is executed directly, it attempts to establish a connection 
    to the database and outputs the status. This is useful for verifying the 
    database configuration.
    """
    try:
        with engine.connect() as connection:
            print("Connected to the new database successfully!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
