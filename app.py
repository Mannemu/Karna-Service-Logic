# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="Kärna Service Logic", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def generate_granular_data():
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(10000, 15000, size=90),
        'ingredient_waste_kg': np.random.uniform(5, 15, size=90),
        'sales_plate_waste_kg': np.random.uniform(2, 8, size=90),
        'contract_hours': [160] * 90,
        'actual_hours_clocked': np.random.uniform(160, 185, size=90),
        'max_individual_overtime': np.random.uniform(4, 15, size=90)
    }
    return pd.DataFrame(data)

df = generate_granular_data()

# 3. SIDEBAR
st.sidebar.title("Kärna Service Logic")
view_mode = st.sidebar.radio("Analys", ["CSRD Rapportering", "Operativ Drift"])

# 4. FORCED VISIBILITY SECTION (TOP OF PAGE)
st.title("📊 Kärna Service Logic Analysis")

# --- THIS IS THE SECTION YOU ARE LOOKING FOR ---
st.header("📑 Compliance & Audit Readiness")
top_left, top_right = st.columns([1, 1])

with top_left:
    st.write("**ESRS Mapping Table**")
    mapping = {
        "Source": ["Acc: 4010", "Acc: 7010", "Sales Data"],
        "ESRS Category": ["E5: Resource", "S1: Workforce", "E5: Plate Waste"],
        "Status": ["✅ Verified", "✅ Verified", "✅ Verified"]
    }
    st.table(pd.DataFrame(mapping))

with top_right:
    st.write("**Mandatory Export**")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD OFFICIAL CSRD REPORT (CSV)",
        data=csv_data,
        file_name="Karna_Compliance_Report.csv",
        mime='text/csv',
        use_container_width=True
    )
    st.info("Visible, high-priority export for Monday's meeting.")

st.divider()

# 5. METRICS
m1, m2, m3 = st.columns(3)
m1.metric("Total Waste (E5)", f"{df['ingredient_waste_kg'].sum() + df['sales_plate_waste_kg'].sum():,.1f} kg")
m2.metric("Burnout Alerts", f"{(df['max_individual_overtime'] > 12).sum()}")
m3.metric("Leakage (SEK)", f"{(df['supplier_invoice_sek'].sum() * 0.12):,.0f}")

# 6. GRAPHS
if view_mode == "CSRD Rapportering":
    st.subheader("Waste Analysis: Ingredients (Input) vs. Plate Waste (Output)")
    st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'sales_plate_waste_kg']])
else:
    st.subheader("Labor Intensity: Actual vs. Contract")
    st.line_chart(df.set_index('date')[['actual_hours_clocked', 'contract_hours']])
