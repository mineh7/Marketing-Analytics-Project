import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Use SQLAlchemy's declarative_base
Base = declarative_base()

# Define the Customers table
class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Age = Column(Integer)
    Gender = Column(String)
    Location = Column(String)
    SubscriptionStartDate = Column(Date)
    SubscriptionEndDate = Column(Date)
    feedback = relationship("Feedback", back_populates="customer")

# Define the Transactions table
class Transaction(Base):
    __tablename__ = 'transactions'
    TransactionID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    PaymentDate = Column(Date)
    Amount = Column(Float)
    PlanType = Column(String)

# Define the Usage table
class Usage(Base):
    __tablename__ = 'usage'
    UsageID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    FeatureName = Column(String)
    UsageFrequency = Column(Integer)
    LastUsedDate = Column(Date)

# Define the Feedback table
class Feedback(Base):
    __tablename__ = 'feedback'
    FeedbackID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    FeedbackText = Column(String)
    Rating = Column(Integer)
    SubmissionDate = Column(Date)
    customer = relationship("Customer", back_populates="feedback")

# Get the database URL from the environment variable
database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db_name")

# Create the database engine
engine = create_engine(database_url)

# Create all tables
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()
