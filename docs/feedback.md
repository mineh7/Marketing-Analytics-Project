## Feedback Processing

### Overview
Feedback data plays a vital role in understanding why customers churn. It captures customer sentiment, experiences, and satisfaction levels.

### Data Flow
1. Feedback is generated using synthetic data (via `generate_feedback` in `etl.py`).
2. The data is saved as `feedback.csv` and loaded into the database.
3. Feedback includes:
   - **FeedbackID**: Unique identifier.
   - **CustomerID**: Links to the customer table.
   - **FeedbackText**: Text input from customers.
   - **Rating**: A numerical rating (1–5).

### Insights Derived
- Negative feedback (ratings < 3) often correlates with churn.
- Common issues include poor service quality, high prices, and product dissatisfaction.