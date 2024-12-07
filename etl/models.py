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
