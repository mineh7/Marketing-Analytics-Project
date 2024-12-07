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
    customers = session.query(Customer).all()
    customers_df = pd.DataFrame([{
        'customer_id': c.customer_id,
        'age': c.age,
        'gender': c.gender,
        'location': c.location,
        'churn_prediction': c.churn_prediction
    } for c in customers])

    usage = session.query(Usage).all()
    usage_df = pd.DataFrame([{
        'customer_id': u.customer_id,
        'usage_frequency': u.usage_frequency,
        'last_used_date': u.last_used_date
    } for u in usage])

    transactions = session.query(Transaction).all()
    transactions_df = pd.DataFrame([{
        'customer_id': t.customer_id,
        'amount': t.amount,
        'plan_type': t.plan_type
    } for t in transactions])

    data = customers_df.merge(usage_df, on="customer_id", how="left")
    data = data.merge(transactions_df, on="customer_id", how="left")

    data['plan_type'] = data['plan_type'].fillna('Unknown')
    data['amount'] = data['amount'].fillna(0)
    data['usage_frequency'] = data['usage_frequency'].fillna(0)

    data = pd.get_dummies(data, columns=['gender', 'plan_type', 'location'], drop_first=True)
    return data

def train_model(data):
    features = [col for col in data.columns if col not in ['customer_id', 'churn_prediction']]
    target = 'churn_prediction'

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(random_state=42, n_estimators=200, max_depth=10)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("Model Evaluation:")
    print(report)

    with open("model_metrics.txt", "w") as f:
        f.write("Model Evaluation Metrics:\n")
        f.write(report)

    data['predicted_churn'] = model.predict(X)
    data['churn_probability'] = model.predict_proba(X)[:, 1]
    return model, data

def update_predictions_in_database(data):
    try:
        print("Updating churn predictions in the database...")
        for _, row in data.iterrows():
            # Fetch the customer from the database
            customer = session.query(Customer).filter_by(customer_id=row['customer_id']).first()
            
            if customer:
                # Update churn_prediction field
                customer.churn_prediction = int(row['predicted_churn'])
            else:
                print(f"Customer with ID {row['customer_id']} not found in the database.")

        # Commit all updates
        session.commit()
        print("Churn predictions successfully updated in the database.")
    except Exception as e:
        # Rollback in case of any failure
        session.rollback()
        print(f"Error updating database: {e}")


def save_model(model, filename="final_model.pkl"):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}.")

def save_predictions_to_csv(data, filename="final_predictions.csv"):
    final_output = data[['customer_id', 'predicted_churn', 'churn_probability']]
    final_output.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}.")

if __name__ == "__main__":
    print("Fetching and preparing data...")
    data = fetch_and_prepare_data()

    print("Training the model...")
    model, data_with_predictions = train_model(data)

    print("Updating predictions in the database...")
    update_predictions_in_database(data_with_predictions)

    print("Saving the model...")
    save_model(model)

    print("Saving predictions to a CSV file...")
    save_predictions_to_csv(data_with_predictions)

    print("Model training and prediction process completed successfully!")
