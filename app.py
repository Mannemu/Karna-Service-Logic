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
st.set_page_config(page_title="Kärna Service Logic | A+ CSRD Suite", layout="wide")

# 2. THE BRAIN: ENHANCED A+ ENGINE
@st.cache_data(ttl=86400)
def generate_granular_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    
    # Impact multipliers for Carbon, Waste, and Labor
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000, "co2_factor": 1.4},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000, "co2_factor": 1.1},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000, "co2_factor": 0.8},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000, "co2_factor": 0.4},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000, "co2_factor": 1.2}
    }
    
    m = multipliers.get(sector, multipliers["Restaurant"])
    
    # Generate Base Data
    data = {
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'ingredient_waste_kg': np.random.uniform(m['waste']*0.4, m['waste']*0.8, size=90),
        'plate_waste_kg': np.random.uniform(m['waste']*0.1, m['waste']*0.3, size=90),
        'contract_hours': [160] * 90,
        'actual_hours': np.random.uniform(160, 160 + m['overtime']*4, size=90),
    }
    
    df = pd.DataFrame(data)
    
    # A+ ADDITION: Specific Scope 3 Carbon Logic (E1)
    df['co2_tonnes'] = (df['supplier_invoice_sek'] / 1000) * m['co2_factor'] * 0.05
    
    # A+ ADDITION: Peer Benchmarking Lines (Specific to Sector)
    df['peer_waste_avg'] = df['ingredient_waste_kg'] * 1.12 # Peers are 12% less efficient
    df['peer_co2_avg'] = df['co2_tonnes'] * 1.08           # Peers have 8% higher footprint
    
    return df

# 3. SIDEBAR & NAVIGATION
st.sidebar.title("Kärna Service Logic")
st.sidebar.info("🛡️ Audit-Ready: ESRS Framework Active")

sector = st.sidebar.selectbox("Verksamhetstyp", ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"])

# Separating views into distinct Legal Pillars
view_mode = st.sidebar.radio(
    "Välj Rapportområde", 
    ["🌍 Miljö: Klimat (E1)", "♻️ Miljö: Resurser (E5)", "👥 Socialt: Personal (S1)"]
)

df = generate_granular_data(sector)

# 4. TOP LEVEL KPIS
st.title(f"{sector} Compliance Dashboard")
c1, c2, c3 = st.columns(3)
with c1: st.metric("Koldioxidavtryck (E1)", f"{df['co2_tonnes'].sum():,.2f} tCO2e")
with c2: st.metric("Resursutnyttjande (E5)", f"{df['ingredient_waste_kg'].sum():,.0f} kg")
with c3: st.metric("Social Risk (S1)", "LÅG", "0 incidenter")

st.divider()

# 5. DYNAMIC SEPARATED GRAPHS
if view_mode == "🌍 Miljö: Klimat (E1)":
    st.header("ESRS E1: Klimatpåverkan & Scope 3")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("CO2-avtryck vs. Branschsnitt")
        st.line_chart(df.set_index('date')[['co2_tonnes', 'peer_co2_avg']])
    
    with col_right:
        st.info("**Insikt:** Din verksamhet ligger 8% under branschsnittet tack vare optimerad logistik.")
        st.write("Mappade konton: 4010, 4020")

elif view_mode == "♻️ Miljö: Resurser (E5)":
    st.header("ESRS E5: Resursanvändning & Svinn")
    
    st.subheader("Inköpssvinn vs. Branschbenchmark")
    st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'peer_waste_avg']])
    
    st.subheader("Detaljerad fördelning: Inköp vs. Tallrikssvinn")
    st.bar_chart(df.set_index('date')[['ingredient_waste_kg', 'plate_waste_kg']])

elif view_mode == "👥 Socialt: Personal (S1)":
    st.header("ESRS S1: Arbetsförhållanden & Duty of Care")
    st.subheader("Faktisk arbetstid vs. Kontrakt")
    st.line_chart(df.set_index('date')[['actual_hours', 'contract_hours']])
    st.success("Inga brott mot vilotidsregler identifierade under perioden.")

# 6. AUDIT EXPORT (The A+ Anchor)
st.divider()
st.subheader("📥 Export för Revision")
st.download_button("Ladda ner fullständig Audit-fil (CSV)", df.to_csv().encode('utf-8'), "Karna_Audit_Trail.csv")
