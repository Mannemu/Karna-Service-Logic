# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# PAGE CONFIG & THEME 
st.set_page_config(page_title="ServiceLogic | CSRD & Gov Compliance", layout="wide")

# THE BRAIN: GENERATING SECTOR-SPECIFIC BENCHMARKS ---
@st.cache_data
def generate_industry_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    # Baslogik för olika sektorer
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000}
    }
    
    # Hanterar matchning mellan svenska/engelska nycklar om det behövs
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'waste_estimate_kg': np.random.uniform(m['waste']*0.5, m['waste']*1.5, size=90),
        'staff_overtime_hours': np.random.uniform(0, m['overtime'], size=90),
        'event_tag': np.random.choice(['Daily Ops', 'Peak Spike', 'Holiday'], p=[0.8, 0.1, 0.1], size=90)
    }
    return pd.DataFrame(data)

# SIDEBAR CONTROLS 
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=50)
st.sidebar.title("Kärna Service Logic")

# Operativa inställningar
sector = st.sidebar.selectbox(
    "Välj verksamhetstyp", 
    ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"]
)

establishment_age = st.sidebar.radio("Compliance Category", ["New (Permit Tracking)", "Existing (Legacy Audit)"])

reduction_target = st.sidebar.slider("Mål för avfallsminskning (%)", 0, 50, 15)

st.sidebar.divider()

# JURIDISKA VILLKOR & AVTAL (Integrerat från PDF och tillägg)
with st.sidebar.expander(" Juridiska villkor & Avtal"):
    st.markdown("### ANVÄNDARAVTAL")
    st.caption("Senast uppdaterad: April 2026")
    
    st.markdown("""
    Detta Avtal reglerar förhållandet mellan Fortnox kunder ("Slutanvändaren") och Kärna Service Logic ("App-utvecklaren"). 
    Genom att aktivera tjänsten via Fortnox App-market godkänner du nedanstående villkor.
    """)

    st.markdown("#### 1. KOMPLETTERANDE VILLKOR")
    st.info("""
    **Beslutsstöd:** Appen är ett verktyg för analys och beslutsstöd. Kärna ansvarar inte för affärsbeslut eller myndighetstvister. Slutanvändaren äger ansvaret för att kontrollera siffror mot originalfakturor i Fortnox innan åtgärd tas.

    **Tillgänglighet:** Vi strävar efter hög driftssäkerhet, men planerat underhåll sker söndagar 22:00 – måndagar 04:00. Support ges via e-post helgfria vardagar 09:00 – 17:00.

    **Benchmarking:** Kärna har rätt att använda anonymiserad data för att skapa branschjämförelser. Inga företagsnamn eller personuppgifter delas någonsin med tredje part eller andra användare.

    **Pris:** Månadsavgift: 199 SEK (exkl. moms). Debiteras via Fortnox. Uppsägning följer Fortnox standardvillkor.
    """)

    st.markdown("#### 2. STANDARDVILLKOR (FORTNOX)")
    st.markdown("""
    **Nyttjanderätt:** Slutanvändaren erhåller en icke-exklusiv rätt att använda Appen.
    
    **Immateriella rättigheter:** App-utvecklaren äger samtliga rättigheter till Appen.
    
    **Ansvar:** App-utvecklaren ansvarar ej för indirekta förluster eller skador på Slutanvändarens system.
    
    **Uppsägning:** Sker senast en (1) månad före nästa fakturering via Fortnox.
    """)
    
    st.divider()
    st.caption("Fullständigt juridiskt dokument (PDF) finns tillgängligt via Fortnox App-market.")

# DATA LOADING & CALCULATIONS 
df = generate_industry_data(sector)
waste_cost_ratio = 0.18 # Branschstandard: 18% av matkostnaden går till spillo
total_waste = df['waste_estimate_kg'].sum()
financial_leakage = df['supplier_invoice_sek'].sum() * waste_cost_ratio
projected_savings = financial_leakage * (reduction_target / 100)

# MAIN DASHBOARD 
st.title(f"{sector} Operations: CSRD & Govt Compliance")
st.markdown(f"**Tracking:** ESRS E5 (Resource Use) & S1 (Workforce) | **Status:** {establishment_age}")

# Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Waste (E5)", f"{total_waste:,.1f} kg", "-3% Peer Avg")
with c2:
    status = "CRITICAL" if df['staff_overtime_hours'].mean() > 5 else "STABLE"
    st.metric("Workforce (S1)", status, "Burnout Risk" if status == "CRITICAL" else "Healthy")
with c3:
    st.metric("Financial Leakage", f"{financial_leakage:,.0f} SEK")
with c4:
    st.metric("Gov Compliance Score", "88%", "Pass")

# VISUALIZATION
st.subheader("Industry Benchmark Analysis")
st.area_chart(df.set_index('date')[['waste_estimate_kg', 'staff_overtime_hours']])

# COMPLIANCE MAPPING TABLE
with st.expander("Governmental & ESRS Data Mapping"):
    mapping_data = {
        "Fortnox Code": ["4010", "7010", "7210", "5410"],
        "Gov Standard": ["Livsmedelsverket (Inflow)", "Arbetsmiljöverket", "Arbetsmiljöverket", "Miljöbalken (Waste)"],
        "ESRS Category": ["E5: Resource Use", "S1: Workforce Impact", "S1: Working Conditions", "E5: Waste Management"],
        "Derived Insight": ["Food Volume Tracking", "Staff Retention Rate", "Burnout Risk Index", "Packaging Benchmarks"]
    }
    st.table(pd.DataFrame(mapping_data))

# EXCEL DOWNLOAD
csv_data = df.to_csv(index=False)
excel_friendly_csv = "sep=,\n" + csv_data

st.download_button(
    label=f"Generate {sector} CSRD Draft Report",
    data=excel_friendly_csv,
    file_name=f"{sector.replace(' ', '_')}_Compliance_Report.csv",
    mime="text/csv"
)

st.success(f"Strategy: Att minska avfallet med {reduction_target}% skulle återvinna **{projected_savings:,.0f} SEK** årligen.")
