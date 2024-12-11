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
    churn_prediction = Column(Integer, nullable=True)  # Churn prediction flag (0 or 1) to indicate churn status
    transactions = relationship("Transaction", back_populates="customer")
    usage = relationship("Usage", back_populates="customer")
    feedback = relationship("Feedback", back_populates="customer")
    results = relationship("Result", back_populates="customer")
    predictions = relationship("Prediction", back_populates="customer")  # Relationship for predictions
    segments = relationship("Segment", back_populates="customer")  # Relationship for segments

# Usage Model
class Usage(Base):
    __tablename__ = 'usage'
    usage_id = Column(Integer, primary_key=True)
    feature_name = Column(String)
    usage_frequency = Column(Integer)  # Tracks how often a feature is used
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_used_date = Column(DateTime, default=datetime.datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="usage")

# Transaction Model
class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Float)  # Amount paid in this transaction
    plan_type = Column(String)  # Type of plan (Basic, Premium, etc.)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_used_date = Column(DateTime, default=datetime.datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="transactions")

# Feedback Model
class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True)
    feedback_text = Column(String)  # Customer feedback text
    rating = Column(Integer)  # Rating given by the customer (1-5)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    customer = relationship("Customer", back_populates="feedback")

# Results Model
class Result(Base):
    __tablename__ = 'results'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    prediction = Column(String, nullable=False)  # Churn prediction result
    probability = Column(Float, nullable=False)  # Probability of the prediction 
    customer = relationship("Customer", back_populates="results")

# Campaigns Model
class Campaign(Base):
    __tablename__ = 'campaigns'
    campaign_id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    churn_rate_before = Column(Float, nullable=False)
    churn_rate_after = Column(Float, nullable=False)
    churn_reduction = Column(Float, nullable=False)

# Predictions Model
class Prediction(Base):
    __tablename__ = 'predictions'
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    predicted_churn = Column(Integer, nullable=False)
    churn_probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    customer = relationship("Customer", back_populates="predictions")

# Segment Model
class Segment(Base):
    __tablename__ = 'segments'
    segment_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    segment_label = Column(String, nullable=False)
    engagement_score = Column(Float, nullable=False)
    spending_score = Column(Float, nullable=False)
    customer = relationship("Customer", back_populates="segments")

# Create all tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)
