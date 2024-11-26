from sqlalchemy.orm import sessionmaker
from database import engine
from models import Customer, Usage, Transaction, Feedback
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Establish database session
Session = sessionmaker(bind=engine)
session = Session()

# Step 1: Fetch data from database
def fetch_data():
    # Fetch customers
    customers = session.query(Customer).all()
    customers_df = pd.DataFrame([{
        'customer_id': c.customer_id,
        'age': c.age,
        'location': c.location
    } for c in customers])

    # Fetch usage
    usage = session.query(Usage).all()
    usage_df = pd.DataFrame([{
        'customer_id': u.customer_id,
        'usage_frequency': u.usage_frequency,
        'last_used_date': u.last_used_date
    } for u in usage])

    # Fetch transactions
    transactions = session.query(Transaction).all()
    transactions_df = pd.DataFrame([{
        'customer_id': t.customer_id,
        'amount': t.amount,
        'plan_type': t.plan_type
    } for t in transactions])

    # Merge datasets on customer_id
    merged_df = customers_df.merge(usage_df, on="customer_id", how="left")
    merged_df = merged_df.merge(transactions_df, on="customer_id", how="left")
    return merged_df

# Step 2: Train and predict
def train_and_predict(data):
    # Simulate a churn column (e.g., churn if usage frequency < 5 or low rating)
    data['churn'] = (data['usage_frequency'] < 5).astype(int)

    # Features and target
    features = ['age', 'usage_frequency', 'amount']  # Example features
    target = 'churn'

    X = data[features].fillna(0)  # Fill missing values
    y = data[target]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Predict for all data
    data['predicted_churn'] = model.predict(X)
    return data

# Step 3: Update predictions back to the database
def update_predictions(data):
    for _, row in data.iterrows():
        customer = session.query(Customer).filter_by(customer_id=row['customer_id']).first()
        if customer:
            customer.churn_prediction = int(row['predicted_churn'])
            session.commit()

if __name__ == "__main__":
    # Fetch data
    print("Fetching data...")
    data = fetch_data()

    # Train model and predict
    print("Training model and making predictions")
    data_with_predictions = train_and_predict(data)

    # Update predictions in the database
    print("Updating predictions in the database")
    update_predictions(data_with_predictions)

    print("Predictions successfully integrated!")
