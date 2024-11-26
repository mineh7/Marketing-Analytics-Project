from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base, engine

Base = declarative_base()

# Customer Model
class Customer(Base):
    __tablename__ = 'customers' 
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    transactions = relationship("Transaction", back_populates="customer")
    usage = relationship("Usage", back_populates="customer")
    feedback = relationship("Feedback", back_populates="customer")

# Usage Model
class Usage(Base):
    __tablename__ = 'usage'  
    usage_id = Column(Integer, primary_key=True)
    feature_name = Column(String)
    usage_frequency = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))  
    customer = relationship("Customer", back_populates="usage")

# Transaction Model
class Transaction(Base):
    __tablename__ = 'transactions' 
    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Float)
    plan_type = Column(String)
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

# Create all tables
Base.metadata.create_all(engine)
