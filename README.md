# retail-intelligence-orchestrator
An end-to-end Data Science product that automates retail data engineering, predictive demand forecasting, and inventory optimisation via an interactive Streamlit dashboard
#  AI-Driven Retail Inventory Orchestrator
An End-to-End Data Science Solution for Demand Forecasting & Inventory Management.

#  Overview
This project solves a common retail pain point: Inventory Optimisation. I have built a complete pipeline that transforms raw, unorganised sales data into an interactive predictive dashboard.

#  The Architecture
1. Data Engineering (`data_engine.py`): 
   - Automated ETL pipeline using Python and SQLite.
   - Includes a Data Quality Auditor to handle missing values, negative prices, and outliers.
2. Machine Learning (`forecaster.py`): 
   - Feature Engineering: Time-series lag features ($t-7$) to capture weekly cycles.
   - Model: Scikit-Learn Linear Regression baseline for demand prediction.
3. User Interface (`app.py`): 
   - Interactive Streamlit dashboard.
   - "What-If" scenario simulator for price-to-demand elasticity.

#  Key Results
- Resilience: The pipeline handles corrupted data inputs without crashing.
- Actionability: Provides a "Reorder Warning" when predicted demand exceeds current stock.

#  Installation & Usage
1. Clone the repo: `git clone [YOUR_REPO_URL]`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialise the database: `python data_engine.py`
4. Train the model: `python forecaster.py`
5. Launch the app: `streamlit run app.py`

---
Created as a demonstration of full-stack data science capabilities for Upwork 2026.
