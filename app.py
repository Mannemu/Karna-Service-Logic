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

# 2. THE BRAIN: 24-HOUR SYNC CYCLE (Option 2)
# ttl=86400 ensures the data only "refreshes" once every 24 hours
@st.cache_data(ttl=86400)
def sync_fortnox_data():
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    # Logic: Distinguishing Input (Ingredients) from Output (Sales/Ready-made)
    data = {
        'date': dates,
        'supplier_spend_sek': np.random.uniform(10000, 15000, size=90),
        'ingredient_waste_kg': np.random.uniform(5, 15, size=90), # INPUT WASTE
        'plate_waste_kg': np.random.uniform(2, 8, size=90),      # OUTPUT WASTE
        'contract_hrs': [160] * 90,
        'actual_hrs_clocked': np.random.uniform(160, 185, size=90),
        'max_individual_overtime': np.random.uniform(4, 15, size=90)
    }
    return pd.DataFrame(data)

df = sync_fortnox_data()

# 3. SIDEBAR & LOGS
st.sidebar.title("Kärna Service Logic")
st.sidebar.info(f"Last Fortnox Sync: {datetime.now().strftime('%Y-%m-%d')} 02:00 AM")
view_mode = st.sidebar.radio("Analysnivå", ["CSRD Rapportering (E5/S1)", "Operativ Drift"])

# 4. MAIN HEADER & COMPLIANCE TABLE (FORCED VISIBILITY)
st.title("📊 Kärna: Operational Intelligence")

st.subheader("📑 Compliance & Audit Readiness")
col_map, col_btn = st.columns([2, 1])

with col_map:
    # Explicitly showing how we track Ready-made (Output) vs Ingredients (Input)
    mapping = {
        "Data Source": ["Acc: 4010 (Invoices)", "POS/Sales Data", "Fortnox Time"],
        "ESRS Category": ["E5: Ingredient Waste", "E5: Plate Waste", "S1: Workforce Impact"],
        "Logic": ["Input (Yield Gap)", "Output (Unsold)", "Duty of Care Audit"]
    }
    st.table(pd.DataFrame(mapping))

with col_btn:
    st.write("**Audit Trail**")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD AUDIT REPORT (CSV)",
        data=csv_data,
        file_name="Karna_Audit_Compliance.csv",
        mime='text/csv',
        use_container_width=True
    )

st.divider()

# 5. METRICS
m1, m2, m3 = st.columns(3)
m1.metric("Waste (Input + Output)", f"{df['ingredient_waste_kg'].sum() + df['plate_waste_kg'].sum():,.1f} kg")
m2.metric("S1 Burnout Alerts", f"{(df['max_individual_overtime'] > 12).sum()}")
m3.metric("Financial Recovery", f"{(df['supplier_spend_sek'].sum() * 0.12):,.0f} SEK")

# 6. REFINED GRAPHS (INPUT vs OUTPUT)
if view_mode == "CSRD Rapportering (E5/S1)":
    st.subheader("E5: Resource Usage (Ingredients vs. Plate Waste)")
    # This chart explicitly separates the two waste types you asked for
    st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'plate_waste_kg']])
    st.caption("Layer 1: Ingredient Yield Loss (Input) | Layer 2: Ready-made/Unsold Goods (Output)")
else:
    st.subheader("S1: Human Capital (Contract vs. Actual)")
    st.line_chart(df.set_index('date')[['actual_hrs_clocked', 'contract_hrs']])
    st.caption("Monitoring labor delta to fulfill ESRS Duty of Care requirements.")
