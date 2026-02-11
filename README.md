# Customer Segmentation & Product Recommendation System

## 📌 Project Overview

This project analyzes real-world e-commerce transaction data to:

- Clean and preprocess transactional records
- Perform exploratory data analysis (EDA)
- Construct invoice-level product baskets
- Generate association rules using the Apriori algorithm
- Build a simple interactive product recommendation interface (Streamlit)

The goal is to simulate a real-world retail analytics workflow where insights are transformed into actionable product recommendations.

---

## 📊 Dataset

- Source: Online Retail dataset
- ~525,000 transaction records
- 8 variables (Invoice, StockCode, Description, Quantity, Price, Customer ID, Country, InvoiceDate)

After cleaning:
- Removed missing customer IDs
- Filtered invalid (non-positive) quantities
- Standardized product descriptions

---

## 🔎 Exploratory Analysis

The notebook includes:

- Top-selling products visualization
- Basket size distribution
- Product pair frequency analysis
- Support vs Confidence rule visualization

---

## 🛒 Basket Construction Strategy

To improve computational efficiency for association rule mining:

- Only the top 300 most frequently purchased products were included.
- Invoice × Product basket matrix was constructed.
- Binary transformation applied for Apriori algorithm.

---

## 🤖 Association Rules

Apriori algorithm was applied to extract:

- Frequent itemsets
- Association rules
- Support, confidence, and lift metrics

Rules are exported to `rules.csv` for downstream usage.

---

## 💡 Product Recommendation App

A simple Streamlit-based interface (`app.py`) was developed to demonstrate how association rules can power a product recommendation system.

### How it works:
1. Select a product
2. System filters relevant association rules
3. Displays recommended products sorted by confidence

Run locally:

```bash
🛠 Technologies Used

Python

Pandas

Matplotlib

Mlxtend (Apriori)

Streamlit

🎯 Key Takeaways

Demonstrates end-to-end analytics pipeline

Converts association rules into a usable product recommendation workflow

Balances computational efficiency with analytical depth

Bridges data analysis and applied product implementation

👩‍💻 Author

Eylem Yılmaz
Master’s in Computer Engineering (Non-thesis)
Focused on Data Analytics & Business Intelligence
pip install -r requirements.txt
streamlit run app.py
