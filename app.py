# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

#  PAGE CONFIG & THEME 
st.set_page_config(page_title="Kärna Service Logic | CSRD Compliance", layout="wide")

#  THE BRAIN: GRANULAR INDUSTRY DATA
@st.cache_data
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    multipliers = {
        "Event Center": {"waste": 45, "overtime_max": 12, "vol": 20000, "staff_base": 160},
        "Hotel (F&B)": {"waste": 30, "overtime_max": 8, "vol": 15000, "staff_base": 160},
        "Restaurant": {"waste": 20, "overtime_max": 5, "vol": 10000, "staff_base": 160},
        "Café/Bistro": {"waste": 10, "overtime_max": 2, "vol": 5000, "staff_base": 160},
        "Fast Food": {"waste": 15, "overtime_max": 4, "vol": 12000, "staff_base": 160}
    }
    
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'waste_kg': np.random.uniform(m['waste']*0.5, m['waste']*1.5, size=90),
        'ingredient_yield_gap': np.random.uniform(0.05, 0.25, size=90),
        'contract_hours': [m['staff_base']] * 90,
        'actual_hours_clocked': np.random.uniform(m['staff_base'], m['staff_base'] + (m['overtime_max']*5), size=90),
        'max_individual_overtime': np.random.uniform(m['overtime_max']*0.8, m['overtime_max']*2, size=90)
    }
    return pd.DataFrame(data)

#  SIDEBAR
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=50)
st.sidebar.title("Kärna Service Logic")

sector = st.sidebar.selectbox(
    "Välj verksamhetstyp", 
    ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"]
)

view_mode = st.sidebar.radio("Analysnivå", ["Organisatorisk (CSRD)", "Operativ (Duty of Care)"])

st.sidebar.divider()

with st.sidebar.expander(" Juridiska villkor & Avtal"):
    st.markdown("### ANVÄNDARAVTAL")
    st.caption("Senast uppdaterad: April 2026")
    st.info("**Pris:** 199 SEK/mån. **Benchmarking:** Anonymiserad data delas för branschinsikter.")

#  DATA PROCESSING
df = generate_granular_data(sector)
financial_leakage = df['supplier_invoice_sek'].sum() * df['ingredient_yield_gap'].mean()
burnout_risk_count = (df['max_individual_overtime'] > 12).sum()
total_overtime = df['actual_hours_clocked'].sum() - df['contract_hours'].sum()

#  MAIN DASHBOARD
st.title(f"{sector} | {view_mode}")

# Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Waste (E5)", f"{df['waste_kg'].sum():,.1f} kg", "-2% vs Peer Avg")
with c2:
    risk_status = "CRITICAL" if burnout_risk_count > 10 else "STABLE"
    st.metric("Burnout Risk (S1)", risk_status, f"{burnout_risk_count} incidents")
with c3:
    st.metric("Labor Variance", f"+{total_overtime:,.0f} hrs", "Above Contract")
with c4:
    st.metric("Leakage (SEK)", f"{financial_leakage:,.0f}", "Yield Gap")

# COMPLIANCE MAPPING 
with st.expander(" ESRS & Fortnox Data Mapping (Auditor View)"):
    mapping_data = {
        "Fortnox Source": ["4010 (Inköp)", "7010 (Löner)", "Tidrapportering", "Avfallshantering"],
        "ESRS Category": ["E5: Resource Use", "S1: Workforce Impact", "S1: Working Conditions", "E5: Waste Management"],
        "Audit Logic": ["Line-item Yield Analysis", "Burnout Probability", "Contract vs Actual Delta", "Packaging Benchmarks"]
    }
    st.table(pd.DataFrame(mapping_data))

# EXPORT SECTION
st.divider()
col_a, col_b = st.columns([1, 2])
with col_a:
    st.subheader("Compliance Export")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f" Download {sector} Audit Report (CSV)",
        data=csv,
        file_name=f"Karna_{sector.replace(' ', '_')}_Compliance.csv",
        mime='text/csv',
    )
with col_b:
    st.dataframe(df.head(5), use_container_width=True)

st.divider()

# VISUALS
if view_mode == "Operativ (Duty of Care)":
    st.subheader("Labor Intensity: Actual Clock-ins vs. Contract")
    st.line_chart(df.set_index('date')[['actual_hours_clocked', 'contract_hours']])
else:
    st.subheader("Resource Flow vs. Financial Leakage")
    st.area_chart(df.set_index('date')[['waste_kg', 'supplier_invoice_sek']])

st.success(f"Strategy: Closing yield gaps and stabilizing labor hours could recover **{financial_leakage*0.6:,.0f} SEK** annually.")
