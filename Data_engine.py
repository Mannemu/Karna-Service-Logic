# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:15:46 2026

@author: Manna
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta

def generate_retail_data():
    # 1. Generate Base Data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    date_rng = pd.date_range(start=start_date, end=end_date, freq='D')
    categories = ['Footwear', 'Outerwear', 'Accessories', 'Denim']
    
    data_list = []
    for date in date_rng:
        for cat in categories:
            month_factor = 1.5 if date.month in [7, 12] else 1.0
            base_sales = np.random.randint(50, 200)
            sales = int(base_sales * month_factor)
            
            data_list.append({
                'date': date,
                'category': cat,
                'units_sold': sales,
                'unit_price': np.random.choice([25.0, 50.0, 80.0, 120.0]),
                'stock_level': np.random.randint(100, 1000)
            })

    df = pd.DataFrame(data_list)
    
    # 2. Inject "Real World" Mess (The Portfolio Flex)
    df.loc[10:15, 'units_sold'] = np.nan       # Missing values
    df.loc[20:22, 'unit_price'] = -50.0        # Bad data (negative price)
    df.loc[30:32, 'units_sold'] = 5000         # Outliers (impossible spike)
    
    return df

def audit_data(df):
    print("---  DATA QUALITY AUDIT STARTING ---")
    
    # Check 1: Missing Values
    null_count = df['units_sold'].isnull().sum()
    if null_count > 0:
        print(f"  Found {null_count} missing sales records. Imputing with median.")
        df['units_sold'] = df['units_sold'].fillna(df['units_sold'].median())
        
    # Check 2: Negative Prices
    neg_prices = (df['unit_price'] < 0).sum()
    if neg_prices > 0:
        print(f"  Found {neg_prices} negative prices. Correcting to absolute values.")
        df['unit_price'] = df['unit_price'].abs()
        
    # Check 3: Outliers (Simplified Z-Score)
    limit = df['units_sold'].mean() + (3 * df['units_sold'].std())
    outliers = (df['units_sold'] > limit).sum()
    if outliers > 0:
        print(f"  Detected {outliers} sales outliers. Capping at 95th percentile.")
        cap = df['units_sold'].quantile(0.95)
        df.loc[df['units_sold'] > limit, 'units_sold'] = cap

    print("---  AUDIT COMPLETE: DATA IS CLEAN ---")
    return df

def save_to_db(df):
    engine = create_engine('sqlite:///retail_inventory.db')
    df.to_sql('sales_data', engine, if_exists='replace', index=False)
    print(" Database Updated: retail_inventory.db")

if __name__ == "__main__":
    raw_data = generate_retail_data()
    clean_data = audit_data(raw_data)
    save_to_db(clean_data)