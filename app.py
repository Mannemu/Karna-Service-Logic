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

# THE BRAIN: GRANULAR INDUSTRY DATA 
@st.cache_data
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000}
    }
    
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'waste_kg': np.random.uniform(m['waste']*0.5, m['waste']*1.5, size=90),
        'ingredient_yield_gap': np.random.uniform(0.05, 0.25, size=90),
        'max_individual_overtime': np.random.uniform(m['overtime']*0.8, m['overtime']*2, size=90)
    }
    return pd.DataFrame(data)

# SIDEBAR START 
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=50)
st.sidebar.title("Kärna Service Logic")

# Operational Controls
sector = st.sidebar.selectbox(
    "Välj verksamhetstyp", 
    ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"]
)

view_mode = st.sidebar.radio("Analysnivå", ["Organisatorisk (CSRD)", "Operativ (Duty of Care)"])

st.sidebar.divider()

#  BOTTOM: Legal & Agreement 
with st.sidebar.expander("⚖️ Juridiska villkor & Avtal"):
    st.markdown("### ANVÄNDARAVTAL")
    st.caption("Senast uppdaterad: April 2026")
    
    st.markdown("""
    Detta avtal reglerar förhållandet mellan Slutanvändaren och App-utvecklaren (Kärna Service Logic). 
    Genom att aktivera tjänsten via Fortnox App-market godkänner du nedanstående villkor.
    """)

    st.markdown("#### KOMPLETTERANDE AVTAL")
    st.info("""
    **1. TJÄNSTENS SYFTE:** Appen är ett verktyg för analys och beslutsstöd. Kärna ansvarar inte för affärsbeslut. Slutanvändaren ansvarar för att kontrollera siffror mot originaldata i Fortnox.

    **2. TILLGÄNGLIGHET:** Underhåll sker söndagar 22:00 – måndagar 04:00. Support ges helgfria vardagar 09:00 – 17:00.

    **3. BENCHMARKING:** Kärna har rätt att använda anonymiserad data för branschjämförelser. Inga personuppgifter delas.

    **4. PRIS:** 199 SEK/mån (exkl. moms). Debiteras via Fortnox.
    """)

    st.markdown("#### STANDARDVILLKOR (FORTNOX)")
    st.write("""
    Slutanvändaren erhåller en icke-exklusiv rätt att använda Appen. 
    Uppsägning sker senast en (1) månad före nästa fakturering via Fortnox.
    """)

# DATA PROCESSING 
df = generate_granular_data(sector)
financial_leakage = df['supplier_invoice_sek'].sum() * df['ingredient_yield_gap'].mean()
burnout_risk_count = (df['max_individual_overtime'] > 12).sum()

# MAIN DASHBOARD 
st.title(f"{sector} | {view_mode}")

# Metrics Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Waste (E5)", f"{df['waste_kg'].sum():,.1f} kg", "-2% vs Peer Avg")
with c2:
    risk_status = "CRITICAL" if burnout_risk_count > 10 else "STABLE"
    st.metric("Burnout Risk (S1)", risk_status, f"{burnout_risk_count} incidents")
with c3:
    st.metric("Financial Leakage", f"{financial_leakage:,.0f} SEK", "Based on Yield Analysis")

# Visuals
if view_mode == "Operativ (Duty of Care)":
    st.subheader("Individual Staff Overtime Trends")
    st.line_chart(df.set_index('date')['max_individual_overtime'])
else:
    st.subheader("Resource Inflow vs. Waste")
    st.area_chart(df.set_index('date')[['waste_kg', 'supplier_invoice_sek']])

st.success(f"Strategy: Addressing ingredient yield gaps could recover **{financial_leakage*0.5:,.0f} SEK** this quarter.")
