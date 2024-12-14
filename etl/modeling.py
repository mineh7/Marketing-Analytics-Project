from database import SessionLocal
from models import Result, Customer, Usage, Transaction
import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Fetch Combined Data for Predictions
def fetch_data_for_predictions():
    """
    Fetch and combine data from the database for training and prediction purposes.
    """
    session = SessionLocal()
    try:
        customers = session.query(Customer).all()
        usage = session.query(Usage).all()
        transactions = session.query(Transaction).all()

        customers_df = pd.DataFrame(
            [{"customer_id": c.customer_id, "age": c.age, "location": c.location} for c in customers]
        )
        usage_df = pd.DataFrame(
            [{"customer_id": u.customer_id, "usage_frequency": u.usage_frequency} for u in usage]
        )
        transactions_df = pd.DataFrame(
            [{"customer_id": t.customer_id, "amount": t.amount} for t in transactions]
        )

        data = customers_df.merge(usage_df, on="customer_id", how="left")
        data = data.merge(transactions_df, on="customer_id", how="left")
        return data
    finally:
        session.close()

# Train Model and Predict
def train_and_predict(data):
    """
    Train a machine learning model and predict churn probabilities.
    """
    data["churn"] = (data["usage_frequency"] < 5).astype(int)
    features = ["age", "usage_frequency", "amount"]
    X = data[features].fillna(0)
    y = data["churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    logger.info("Model Classification Report:")
    logger.info(classification_report(y_test, y_pred))

    data["predicted_churn"] = model.predict(X)
    data["churn_probability"] = model.predict_proba(X)[:, 1]
    return data

# Populate Results Table
def populate_results_table(data):
    """
    Populate the results table with prediction data.
    """
    session = SessionLocal()
    try:
        for _, row in data.iterrows():
            result = Result(
                customer_id=row["customer_id"],
                prediction="Churn" if row["predicted_churn"] == 1 else "No Churn",
                probability=row["churn_probability"],
                created_at=pd.Timestamp.now(),
            )
            session.add(result)
        session.commit()
        logger.info("Results table populated.")
    except Exception as e:
        logger.error(f"Error populating results table: {e}")
    finally:
        session.close()
