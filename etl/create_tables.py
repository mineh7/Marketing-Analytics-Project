import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configure logging for SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Define the base class
Base = declarative_base()

# Define the Customers table
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    subscription_start_date = Column(Date)
    subscription_end_date = Column(Date)
    transactions = relationship("Transaction", back_populates="customer")
    usage = relationship("Usage", back_populates="customer")

# Define the Usage table
class Usage(Base):
    __tablename__ = 'usage'
    usage_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    feature_name = Column(String, nullable=False)
    usage_frequency = Column(Integer)
    last_used_date = Column(Date)
    customer = relationship("Customer", back_populates="usage")

# Define the Transactions table
class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    payment_date = Column(Date)
    amount = Column(Float)
    plan_type = Column(String)
    customer = relationship("Customer", back_populates="transactions")

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/postgres")

# Create database engine
engine = create_engine(DATABASE_URL)

# Test database connection
try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Create all tables
try:
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
    exit()
