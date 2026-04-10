# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="ServiceLogic | CSRD & Gov Compliance", layout="wide")

# --- 2. THE BRAIN: GRANULAR INDUSTRY DATA ---
@st.cache_data
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    # Sector multipliers for ingredients and labor
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000}
    }
    
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    # Simulating individual staff data (Anonymous IDs for Duty of Care)
    staff_ids = [f"Staff_{i}" for i in range(1, 11)]
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'waste_kg': np.random.uniform(m['waste']*0.5, m['waste']*1.5, size=90),
        'ingredient_yield_gap': np.random.uniform(0.05, 0.25, size=90), # % of specific high-value items lost
        'avg_overtime_hours': np.random.uniform(0, m['overtime'], size=90),
        'max_individual_overtime': np.random.uniform(m['overtime']*0.8, m['overtime']*2, size=90)
    }
    return pd.DataFrame(data)

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=50)
st.sidebar.title("Kärna Service Logic")

sector = st.sidebar.selectbox(
    "Välj verksamhetstyp", 
    ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"]
)

view_mode = st.sidebar.radio("Analysnivå", ["Organisatorisk (CSRD)", "Operativ (Duty of Care)"])

st.sidebar.divider()

# JURIDISKA VILLKOR & AVTAL
with st.sidebar.expander("⚖️ Juridiska villkor & Avtal"):
    st.markdown("### ANVÄNDARAVTAL")
    st.caption("Senast uppdaterad: April 2026")
    
    st.markdown("""
    Detta Avtal reglerar förhållandet mellan Slutanvändaren och Kärna Service Logic ("App-utvecklaren").
    """)

    st.markdown("#### 1. KOMPLETTERANDE VILLKOR")
    st.info("""
    **Beslutsstöd:** Appen är ett verktyg för analys. Kärna ansvarar inte för affärsbeslut. Slutanvändaren ansvarar för att kontrollera siffror mot originaldata i Fortnox.

    **Tillgänglighet:** Planerat underhåll sker söndagar 22:00 – måndagar 04:00. Support ges helgfria vardagar 09:00 – 17:00.

    **Benchmarking:** Kärna har rätt att använda anonymiserad data för branschjämförelser. Inga identifierbara person- eller företagsuppgifter delas.

    **Pris:** 199 SEK/mån (exkl. moms). Debiteras via Fortnox.
    """)

    st.markdown("#### 2. STANDARDVILLKOR (FORTNOX)")
    st.markdown("""
    **Nyttjanderätt:** Slutanvändaren erhåller en icke-exklusiv rätt att använda Appen.
    **Ansvar:** App-utvecklaren ansvarar ej för indirekta förluster.
    """)

# --- 4. DATA PROCESSING ---
df = generate_granular_data(sector)
financial_leakage = df['supplier_invoice_sek'].sum() * df['ingredient_yield_gap'].mean()
burnout_risk_count = (df['max_individual_overtime'] > 12).sum() # Example threshold

# --- 5. MAIN DASHBOARD ---
st.title(f"{sector} | {view_mode}")
st.markdown(f"**Status:** Aktuella mätvärden för ESRS E5 & S1 rapportering")

# Metrics Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Waste (E5)", f"{df['waste_kg'].sum():,.1f} kg", "-2% mot branschsnitt")
with c2:
    risk_status = "HÖG" if burnout_risk_count > 10 else "NORMAL"
    st.metric("Burnout Risk (S1)", f"{risk_status}", f"{burnout_risk_count} kritiska incidenter")
with c3:
    st.metric("Ekonomiskt läckage", f"{financial_leakage:,.0f} SEK", "Baserat på ingrediensanalys")

# Visuals based on View Mode
if view_mode == "Operativ (Duty of Care)":
    st.subheader("Individuell belastningsanalys (Anonymiserad)")
    st.line_chart(df.set_index('date')['max_individual_overtime'])
    st.info("Systemet flaggar för 'Duty of Care'-intervention när enskild personal överskrider 12 timmar övertid per vecka.")
else:
    st.subheader("Ingrediens- och resursflöde")
    st.area_chart(df.set_index('date')[['waste_kg', 'supplier_invoice_sek']])

# EXCEL REPORT
csv_data = df.to_csv(index=False)
st.download_button(
    label=f"Exportera CSRD-rapport för {sector}",
    data=csv_data,
    file_name=f"Karna_{sector}_Report.csv",
    mime="text/csv"
)

st.success(f"Genom att åtgärda identifierade yield-gaps på ingrediensnivå kan verksamheten spara ca **{financial_leakage*0.5:,.0f} SEK** nästa kvartal.")
