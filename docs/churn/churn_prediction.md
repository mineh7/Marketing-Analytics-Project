# Churn Prediction

## Prediction Logic
The churn prediction process relies on a combination of business rules and machine learning models.

---

### **Churn Labeling**
1. **Low Usage**: Usage frequency < 5 leads to a churn flag.  
2. **Negative Feedback**: Feedback rating < 3 results in a churn flag.  
3. **No Transactions**: Customers with no transactions are flagged as potential churn.  

These rules are applied in the **ETL process**, and the result is stored as a **churn_prediction** field in the customer table.

---

### **Machine Learning Model**
1. **Model Used**: RandomForestClassifier  
2. **Features Used**:  
   - Age  
   - Location (One-hot encoded)  
   - Usage Frequency  
   - Amount (Transaction data)  

3. **Labels**:  
   - **Churn (1)**: Indicates a customer has churned.  
   - **No Churn (0)**: Indicates a customer has not churned.  

---

### **Training the Model**
1. **Train-Test Split**: The data is split into 70% training and 30% testing sets.  
2. **Model Training**: A RandomForestClassifier is trained on customer data, and the model is saved as `final_model.pkl`.  
3. **Evaluation**:  
   - Accuracy, Precision, Recall, and F1 scores are calculated.  
   - The results are stored in `model_metrics.txt`.  
4. **Predictions**:  
   - Churn predictions are saved in `final_predictions.csv`.  
   - Churn probability is also calculated and stored.  

---
