from sqlalchemy.orm import sessionmaker
from database import engine
from models import Customer, Usage, Transaction, Feedback
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Establish database session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_prepare_data():
    """
    Fetch and merge customer-related data from the database, preparing it for modeling.

    Returns:
        DataFrame: Cleaned and combined data for modeling.
    """
    # Fetch customers
    customers = session.query(Customer).all()
    customers_df = pd.DataFrame([{
        'customer_id': c.customer_id,
        'age': c.age,
        'gender': c.gender,
        'location': c.location,
        'churn_prediction': c.churn_prediction
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
    data = customers_df.merge(usage_df, on="customer_id", how="left")
    data = data.merge(transactions_df, on="customer_id", how="left")

    # Fill missing values and encode categorical data
    data['plan_type'] = data['plan_type'].fillna('Unknown')
    data['amount'] = data['amount'].fillna(0)
    data['usage_frequency'] = data['usage_frequency'].fillna(0)

    # One-hot encode categorical features
    data = pd.get_dummies(data, columns=['gender', 'plan_type', 'location'], drop_first=True)
    return data

def train_model(data):
    """
    Train a machine learning model to predict churn.

    Args:
        data (DataFrame): Cleaned data prepared for modeling.

    Returns:
        RandomForestClassifier: Trained machine learning model.
        DataFrame: Updated DataFrame with churn predictions.
    """
    # Features and target
    features = [col for col in data.columns if col not in ['customer_id', 'churn_prediction']]
    target = 'churn_prediction'

    X = data[features]
    y = data[target]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))

    # Predict for all customers
    data['predicted_churn'] = model.predict(X)
    return model, data

def update_predictions_in_database(data):
    """
    Update churn predictions in the Customer table.

    Args:
        data (DataFrame): DataFrame containing customer features and churn predictions.
    """
    for _, row in data.iterrows():
        customer = session.query(Customer).filter_by(customer_id=row['customer_id']).first()
        if customer:
            customer.churn_prediction = int(row['predicted_churn'])
            session.commit()

def save_model(model, filename="final_model.pkl"):
    """
    Save the trained model to a file.

    Args:
        model: Trained machine learning model.
        filename (str): Path to save the model file.
    """
    joblib.dump(model, filename)
    print(f"Model saved to {filename}.")

if __name__ == "__main__":
    """
    Main execution for the data science model.

    Steps:
    1. Fetch and prepare data from the database.
    2. Train a machine learning model to predict churn.
    3. Update predictions in the database.
    4. Save the trained model for future use.
    """
    print("Fetching and preparing data...")
    data = fetch_and_prepare_data()

    print("Training the model...")
    model, data_with_predictions = train_model(data)

    print("Updating predictions in the database...")
    update_predictions_in_database(data_with_predictions)

    print("Saving the model...")
    save_model(model)

    print("Model training and prediction process completed successfully!")
