# Marketing Analytics Project
**Customer Retention: Reducing Churn in Subscription-Based Businesses**

## Overview
High churn rates within the first three months pose a significant challenge for subscription-based businesses. This project focuses on identifying the key drivers of churn, leveraging data analytics to predict customer behavior, and implementing actionable strategies to enhance customer retention. By reducing churn, businesses can achieve sustainable growth, improve customer loyalty, and maximize profitability.

---

## Problem Statement
Subscription-based businesses often lose a significant number of customers within the initial months. This leads to:
- Loss of potential long-term revenue.
- Increased costs for acquiring new customers.
- Reduced brand loyalty.

The challenge is to understand **why customers churn** and implement data-driven strategies to **reduce churn rates effectively**.

---

## Project Objectives
1. **Identify churn drivers**: Analyze customer demographics, usage behavior, payment history, and feedback to determine factors contributing to churn.
2. **Predict churn**: Build predictive models to classify customers into low-risk and high-risk categories.
3. **Enhance retention**: Implement and test tailored interventions to improve customer satisfaction and loyalty.

---

## Key Features of the Project
1. **Feedback Analysis**:
   - Analyzes customer feedback to identify dissatisfaction and pain points.
2. **Churn Drivers**:
   - Pinpoints key factors (e.g., usage behavior, feedback ratings, and transaction history) leading to churn.
3. **Churn Prediction**:
   - Uses machine learning to classify customers into high-risk and low-risk categories.
4. **Visual Analytics**:
   - Provides actionable insights through visualizations (e.g., churn trends and churn reasons).

---

## Solution Approach

### 1. Data Collection
- **Sources**:
  - CRM systems for customer demographics and payment history.
  - Usage analytics for engagement patterns.
  - Customer feedback surveys for dissatisfaction insights.
- **Preprocessing**: Handle missing values, outliers, and ensure data is analysis-ready.

### 2. Data Analysis
- **Descriptive Analytics**: Identify trends and patterns in customer behavior.
- **Predictive Modeling**:
  - Use machine learning to predict churn likelihood.
  - Evaluate models using metrics like precision, recall, and ROC-AUC.
- **Customer Segmentation**: Group customers based on engagement, demographics, and churn risk.

### 3. Strategy Development
- Tailored strategies, including:
  - Discounts for at-risk customers.
  - Personalized engagement campaigns.
  - Improved onboarding processes.
- Pilot strategies and measure impact.

### 4. Success Metrics
- **Retention Rate**: Percentage of customers retained over a specific period.
- **Customer Lifetime Value (CLV)**: Revenue generated per customer.
- **Model Performance**: Reduction in churn prediction errors.

---

## Installation and Setup

### Prerequisites
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Steps to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/marketing-analytics-project.git
   cd marketing-analytics-project
   ```

2. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - **pgAdmin**: [http://localhost:5050](http://localhost:5050)
     - Email: `admin@admin.com`
     - Password: `password`
   - **Documentation (MkDocs)**: [http://localhost:8000](http://localhost:8000)

---

## Weblinks

## Weblinks

- **[MkDocs Documentation](https://mineh7.github.io/Marketing-Analytics-Project/)**:
- **[pgAdmin Interface](http://localhost:5050)**: 


---

## Project Structure

Here’s an overview of the project’s file structure:

```bash
.
├── README.md             # Project documentation
├── .env                  # Environment variables
├── docker-compose.yml    # Docker Compose configuration
├── data/                 # Folder containing synthetic datasets
├── docs/                 # Documentation files
├── etl/                  # ETL pipeline scripts
├── models.py             # Database schema
├── requirements.txt      # Python dependencies
└── scripts/              # Supporting Python scripts
```

---

## How It Works

### Data Pipeline
1. **ETL Process**:
   - Generates synthetic customer, usage, and feedback data.
   - Loads data into PostgreSQL via the ETL pipeline (`etl.py`).

2. **Machine Learning**:
   - Trains a RandomForest model to predict churn probabilities.
   - Outputs predictions to the `Results` table.

3. **Visual Analytics**:
   - Displays churn drivers, trends, and customer feedback through dynamic visualizations.

### Schema Design
The database schema stores all required data for churn analytics. For details, refer to:
- **ERD**: Accessible in the [MkDocs Documentation](http://localhost:8000).

---

## Contributing

We welcome contributions! Please open an issue or submit a pull request to contribute to this project.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
