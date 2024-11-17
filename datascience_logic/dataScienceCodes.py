import pandas as pd
import sqlite3
import sklearn as sk
#functions to test crud operations
# insertions
def add_customer(cursor, conn, customer_data):
    cursor.execute("""
        INSERT INTO Customers (CustomerID, Name, Age, Gender, Location, SubscriptionStartDate, SubscriptionEndDate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, customer_data)
    conn.commit()

#reading the data
def get_customers(cursor):
    cursor.execute("SELECT * FROM Customers")
    return cursor.fetchall()

# write operations
def update_customer_age(cursor, conn, customer_id, new_age):
    cursor.execute("""
        UPDATE Customers
        SET Age = ?
        WHERE CustomerID = ?
    """, (new_age, customer_id))
    conn.commit()

# deleting data
def delete_customer(cursor, conn, customer_id):
    cursor.execute("DELETE FROM Customers WHERE CustomerID = ?", (customer_id,))
    conn.commit()


if __name__ == "__main__":
    import sqlite3

    # establishing the connection with the db
    conn = sqlite3.connect('customer_retention.db')
    cursor = conn.cursor()

    # testing
    add_customer(cursor, conn, (101, 'John Doe', 30, 'Male', 'New York', '2023-01-01', '2023-12-31'))
    print("All customers:", get_customers(cursor))
    update_customer_age(cursor, conn, 101, 35)
    print("Updated customers:", get_customers(cursor))
    delete_customer(cursor, conn, 101)
    print("Remaining customers:", get_customers(cursor))

    conn.close()

conn = sqlite3.connect('customer_retention.db')

# load data into dataframes
customers_df = pd.read_sql_query("SELECT * FROM Customers", conn)
print(customers_df.head())

conn.close()

# customer charn predictions
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# simulating a column
customers_df['Churn'] = (customers_df['Age'] > 30).astype(int)  # Simulated churn flag

X = customers_df[['Age']]
y = customers_df['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
