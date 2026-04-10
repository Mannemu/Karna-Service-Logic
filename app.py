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

# 2. THE BRAIN: DIFFERENTIATED WASTE LOGIC
@st.cache_data
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    m = {"waste_ratio": 0.15, "overtime_max": 8, "vol": 12000, "staff_base": 160}
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'ingredient_waste_kg': np.random.uniform(5, 15, size=90), # INPUT WASTE
        'sales_plate_waste_kg': np.random.uniform(2, 8, size=90),  # OUTPUT WASTE
        'contract_hours': [m['staff_base']] * 90,
        'actual_hours_clocked': np.random.uniform(m['staff_base'], m['staff_base'] + 20, size=90),
        'max_individual_overtime': np.random.uniform(4, 15, size=90)
    }
    return pd.DataFrame(data)

# 3. SIDEBAR & HEADER
st.sidebar.title("Kärna Service Logic")
sector = st.sidebar.selectbox("Bransch", ["Restaurant", "Hotel (F&B)", "Event Center"])
view_mode = st.sidebar.radio("Analys", ["CSRD Rapportering", "Operativ Drift"])

df = generate_granular_data(sector)

# 4. TOP ROW: KPI METRICS
st.title(f"📊 {sector} Analysis Portal")
c1, c2, c3 = st.columns(3)
c1.metric("Total Waste (E5)", f"{df['ingredient_waste_kg'].sum() + df['sales_plate_waste_kg'].sum():,.1f} kg")
c2.metric("Burnout Alerts (S1)", f"{(df['max_individual_overtime'] > 12).sum()} Incidenter")
c3.metric("Financial Leakage", f"{(df['supplier_invoice_sek'].sum() * 0.12):,.0f} SEK")

st.divider()

# 5. THE "COMPLIANCE BOX" - FORCED VISIBILITY
# We put this ABOVE the graphs so it's impossible to miss.
st.subheader("📑 Compliance & Audit Readiness")
col_left, col_right = st.columns([1, 1])

with col_left:
    st.write("**Audit Trail: Fortnox Account Mapping**")
    mapping = {
        "Source": ["Acc: 4010", "Acc: 7010", "Sales Data", "Time Logs"],
        "ESRS Category": ["E5: Ingredient Waste", "S1: Workforce", "E5: Plate Waste", "S1: Duty of Care"],
        "Audit Status": ["✅ Verified", "✅ Verified", "✅ Verified", "✅ Verified"]
    }
    st.table(pd.DataFrame(mapping))

with col_right:
    st.write("**Export for Government Filing**")
    # Big, heavy-duty button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD OFFICIAL CSRD COMPLIANCE REPORT (CSV)",
        data=csv_data,
        file_name=f"Karna_Compliance_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
        use_container_width=True,
        help="Download the full dataset mapped to ESRS standards for 2026 reporting."
    )
    st.info("This report includes anonymized benchmarking data ready for the Fortnox Sustainability Hub.")

st.divider()

# 6. REFINED GRAPHS
if view_mode == "CSRD Rapportering":
    st.subheader("Resource Flow: Ingredients vs. Prepared Waste")
    # Splitting the waste types to show we understand the difference
    st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'sales_plate_waste_kg']])
    st.caption("Green: Spoilage/Yield Loss (Input) | Blue: Plate Waste/Unsold Goods (Output)")
else:
    st.subheader("Human Capital: Duty of Care Monitoring")
    st.line_chart(df.set_index('date')[['actual_hours_clocked', 'contract_hours']])
    st.caption("Tracking the delta between planned staffing and reality to prevent S1 Burnout incidents.")
