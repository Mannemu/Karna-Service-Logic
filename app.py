# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:31:50 2026

@author: Manna
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 1. PAGE CONFIG (Must be at the very top)
st.set_page_config(page_title="Kärna Service Logic | TEST VERSION 0.1", layout="wide")
def login_page():
    st.title("Welcome to Kärna Service Logic")
    st.write("The first-mover engine for ESRS & CSRD compliance.")
    st.divider()

    # The Connection Button
    if st.button("Connect with Fortnox", type="primary"):
        st.session_state.authenticated = True
        st.rerun()
    
    # The GDPR "Trust" Notice
    st.caption("""
    **🔒 Data Privacy & GDPR Notice** By connecting, Kärna will receive read-only access to your Fortnox accounting and personal data. 
    We use this strictly to generate your sustainability insights. No data is modified, 
    and we never share your information with third parties.
    """)

# 2. THE SYNC BRAIN (Backend Logic)
@st.cache_data(ttl=86400) 
def fetch_and_sync_fortnox_data(sector):
    dates = pd.date_range(end=datetime.today(), periods=90, freq='D')
    multipliers = {
        "Event Center": {"waste": 45, "overtime": 12, "vol": 20000, "co2": 1.4},
        "Hotel (F&B)": {"waste": 30, "overtime": 8, "vol": 15000, "co2": 1.1},
        "Restaurant": {"waste": 20, "overtime": 5, "vol": 10000, "co2": 0.8},
        "Café/Bistro": {"waste": 10, "overtime": 2, "vol": 5000, "co2": 0.4},
        "Fast Food": {"waste": 15, "overtime": 4, "vol": 12000, "co2": 1.2}
    }
    m = multipliers.get(sector, multipliers["Restaurant"])
    df = pd.DataFrame({
        'date': dates,
        'supplier_invoice_sek': np.random.uniform(m['vol']*0.8, m['vol']*1.2, size=90),
        'ingredient_waste_kg': np.random.uniform(m['waste']*0.4, m['waste']*0.8, size=90),
        'plate_waste_kg': np.random.uniform(m['waste']*0.1, m['waste']*0.3, size=90),
        'contract_hours': [160] * 90,
        'actual_hours': np.random.uniform(160, 160 + m['overtime']*4, size=90),
    })
    df['co2_tonnes'] = (df['supplier_invoice_sek'] / 1000) * m['co2'] * 0.05
    df['peer_waste_avg'] = df['ingredient_waste_kg'] * 1.12 
    df['peer_co2_avg'] = df['co2_tonnes'] * 1.08           
    return df

# 3. SIDEBAR NAVIGATION
st.sidebar.title("Kärna Service Logic")
st.sidebar.success("🛡️ Audit-Ready: ESRS Active")
st.sidebar.info("🔄 Sync: 24h Cycle Verified")

# Primary Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Support", "Integritetspolicy"])

# 4. PAGE ROUTING (The "Logic Switch")

if page == "Dashboard":
    # Authentication Check
    if "authenticated" not in st.session_state:
        st.title("Welcome to Kärna Service Logic")
        st.write("The first-mover engine for ESRS & CSRD compliance.")
        if st.button("Connect with Fortnox"):
            st.session_state.authenticated = True
            st.rerun()
    else:
        # ALL DASHBOARD CODE IS INDENTED HERE
        st.sidebar.markdown("---")
        sector = st.sidebar.selectbox("Verksamhetstyp", ["Event Center", "Hotel (F&B)", "Restaurant", "Café/Bistro", "Fast Food"])
        view_mode = st.sidebar.radio("Välj Rapportområde", ["🌍 Miljö: Klimat (E1)", "♻️ Miljö: Resurser (E5)", "👥 Socialt: Personal (S1)"])
        
        df = fetch_and_sync_fortnox_data(sector)
        st.title(f"{sector} | {view_mode}")

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Koldioxidavtryck (E1)", f"{df['co2_tonnes'].sum():,.2f} tCO2e")
        with m2: st.metric("Total Waste (E5)", f"{df['ingredient_waste_kg'].sum() + df['plate_waste_kg'].sum():,.0f} kg")
        with m3: st.metric("Burnout Incidents (S1)", "0", "Safe")
        
        st.divider()

        if view_mode == "🌍 Miljö: Klimat (E1)":
            st.subheader("CO2-avtryck vs. Branschsnitt")
            st.line_chart(df.set_index('date')[['co2_tonnes', 'peer_co2_avg']])
        elif view_mode == "♻️ Miljö: Resurser (E5)":
            st.subheader("Resursutnyttjande: Inköpt råvara vs. Benchmark")
            st.area_chart(df.set_index('date')[['ingredient_waste_kg', 'peer_waste_avg']])
        else:
            st.subheader("Arbetstidsanalys (Duty of Care)")
            st.line_chart(df.set_index('date')[['actual_hours', 'contract_hours']])

elif page == "Support":
    # Everything else is hidden when this runs
    st.title("📞 Support & Integration")
    st.markdown("""
    ### Behöver du hjälp?
    Kärna Service Logic är designad för att vara sömlös, men vi finns här om du har frågor.
    
    * **E-post:** support@karna.se
    * **Installation:** Aktivera integrationen i Fortnox Marketplace.
    * **FAQ:** Vi mappar automatiskt 4000-4010 och personal-data.
    """)

elif page == "Integritetspolicy":
    st.title("🔒 Integritetspolicy (Privacy Policy)")
    st.write("""
    **Behandling av personuppgifter**
    Kärna Service Logic läser data från Fortnox via säkra API-anrop. 
    1. **Data:** Bokföring, personal och företagsinfo.
    2. **Syfte:** Generera ESG-rapporter (CSRD/ESRS).
    3. **Säkerhet:** Vi lagrar inget permanent och skriver aldrig till din bokföring.
    """)
