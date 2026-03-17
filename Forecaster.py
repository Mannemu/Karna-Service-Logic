# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:20:15 2026

@author: Manna
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import pickle

def load_and_prep_data():
    # 1. Connect to the SQL spine
    engine = create_engine('sqlite:///retail_inventory.db')
    
    # We use a context manager (with) to ensure the connection closes properly
    with engine.connect() as conn:
        df = pd.read_sql('sales_data', conn)
    
    # CRITICAL FIX: Convert all column names to standard strings immediately
    df.columns = [str(col) for col in df.columns]
    
    # 2. Convert date string to datetime object
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Create 'Lag Features'
    df['sales_lag_7'] = df.groupby('category')['units_sold'].transform(lambda x: x.shift(7))
    
    # Drop rows with NaN from the lag
    df = df.dropna() 
    
    return df

def train_model(df):
    print("\n---  TRAINING FORECASTING MODEL ---")
    
    # Define features (X) and target (y)
    features = ['day_of_week', 'month', 'is_weekend', 'sales_lag_7', 'unit_price']
    
    # Ensure X is clean and columns are strings one last time before Scikit-learn sees them
    X = df[features].copy()
    X.columns = X.columns.astype(str)
    
    y = df['units_sold']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and fit
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 4. Evaluation
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    
    print(" Model Training Successful!")
    print(f" Accuracy Metric (MAE): {round(mae, 2)} units")
    
    # 5. Serialization
    with open('forecaster_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print(" Model saved as: forecaster_model.pkl")

if __name__ == "__main__":
    try:
        data = load_and_prep_data()
        if not data.empty:
            train_model(data)
        else:
            print(" Error: DataFrame is empty. Check Phase 1.")
    except Exception as e:
        print(f" Error occurred: {e}")