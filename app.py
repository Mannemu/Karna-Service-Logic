# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pickle
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="Retail Intelligence Dashboard", layout="wide")

st.title(" Retail Demand & Inventory Forecaster")
st.markdown("""
This dashboard predicts future inventory needs based on historical sales, seasonality, and price points.
*Built with Python, Scikit-Learn, and SQLite.*
""")

# 2. Data & Model Loaders
@st.cache_data
def load_data():
    engine = create_engine('sqlite:///retail_inventory.db')
    with engine.connect() as conn:
        df = pd.read_sql('sales_data', conn)
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_model():
    with open('forecaster_model.pkl', 'rb') as f:
        return pickle.load(f)

# Initialize data and model
df = load_data()
model = load_model()

# 3. Sidebar Filters
st.sidebar.header("Filter Analytics")
category = st.sidebar.selectbox("Select Product Category", df['category'].unique())
filtered_df = df[df['category'] == category].sort_values('date')

# 4. Main Dashboard Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Units Sold", f"{int(filtered_df['units_sold'].sum()):,}")
with col2:
    avg_price = f"${filtered_df['unit_price'].mean():.2f}"
    st.metric("Avg Unit Price", avg_price)
with col3:
    current_stock = filtered_df['stock_level'].iloc[-1]
    st.metric("Current Stock Level", f"{int(current_stock):,}")

# 5. Visualizing Historical Sales
st.subheader(f"Historical Sales Trend: {category}")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered_df['date'], filtered_df['units_sold'], color='#1f77b4', linewidth=2)
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# 6. The "Predictive" Piece (What-If Analysis)
st.divider()
st.subheader("🔮 Demand Forecaster (What-If Scenario)")
st.write("Adjust the variables below to see the predicted demand for next week.")

# User Inputs for Prediction
price_input = st.slider("Target Unit Price ($)", 10.0, 200.0, float(filtered_df['unit_price'].iloc[-1]))
is_weekend_input = st.checkbox("Is this for a Weekend?")
lag_sales = filtered_df['units_sold'].iloc[-1] # Simplification for the demo

# Prepare the data for the model
# Feature order: ['day_of_week', 'month', 'is_weekend', 'sales_lag_7', 'unit_price']
input_features = np.array([[1, 3, int(is_weekend_input), lag_sales, price_input]])
prediction = model.predict(input_features)[0]

st.success(f"### Predicted Demand: **{int(prediction)} units**")

if prediction > current_stock:
    st.warning(" Warning: Predicted demand exceeds current stock. Reorder recommended.")
else:
    st.info(" Inventory levels appear sufficient for predicted demand.")