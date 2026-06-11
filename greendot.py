import os
from datetime import date
from typing import List

import streamlit as st
from db import (
    DB_CONFIGURED,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    initialize_database,
    list_applications,
    save_application,
    delete_application,
    get_application_by_id,
)
from utils import (
    generate_excel_bytes,
    sanitize_text,
    validate_email,
    save_uploaded_file,
)

st.set_page_config(
    page_title="ClaimFlow Intake",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLE = """
<style>
:root {
    color-scheme: light;
    --brand-dark: #0b2d56;
    --brand-cyan: #12b886;
    --surface: #ffffff;
    --surface-soft: #f4fbf8;
    --text-muted: #5b6f84;
}

body {
    background: linear-gradient(180deg, #eff9f3 0%, #f6fbf8 100%);
    color: var(--brand-dark);
}

.stApp {
    background: transparent;
}

section {
    padding: 4rem 0;
}

.header-section {
    padding-top: 1rem;
}

.section-card {
    background: var(--surface);
    border-radius: 30px;
    padding: 2rem;
    border: 1px solid rgba(11, 45, 86, 0.08);
    box-shadow: 0 32px 66px rgba(11, 45, 86, 0.08);
}

.hero-panel {
    border-radius: 36px;
    padding: 3rem;
    background: linear-gradient(135deg, #0b2d56 0%, #12b886 100%);
    color: white;
    box-shadow: 0 60px 140px rgba(0, 145, 89, 0.18);
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 999px;
    padding: 0.75rem 1rem;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.18);
    font-weight: 700;
}

.hero-button,
.cta-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    padding: 1rem 1.8rem;
    color: white !important;
    background: var(--brand-dark);
    text-decoration: none;
    transition: transform 0.2s ease, background-color 0.2s ease;
    font-weight: 700;
}

.hero-button:hover,
.cta-button:hover {
    background: #083352;
    transform: translateY(-1px);
}

.card-panel {
    border-radius: 28px;
    background: white;
    border: 1px solid rgba(11, 45, 86, 0.08);
    box-shadow: 0 22px 50px rgba(15, 45, 70, 0.06);
    padding: 2rem;
}

.card-panel h3 {
    color: var(--brand-dark);
}

.card-panel p,
.card-panel li {
    color: var(--text-muted);
}

.stButton>button {
    border-radius: 999px;
    background-color: var(--brand-dark);
    color: white;
    padding: 0.85rem 1.8rem;
    font-weight: 700;
}

.stButton>button:hover {
    background-color: #083352;
}

input,
textarea {
    border-radius: 16px !important;
}

[data-testid="stForm"] .stButton>button {
    width: auto;
}

@media (max-width: 900px) {
    .hero-panel {
        padding: 2rem;
    }
}

.nav-links {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.nav-link {
    color: var(--brand-dark);
    font-weight: 700;
    text-decoration: none;
}

.nav-link:hover {
    color: var(--brand-cyan);
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

NAV = """
<div class='nav-links'>
    <a class='nav-link' href='#home'>Home</a>
    <a class='nav-link' href='#benefits'>Benefits</a>
    <a class='nav-link' href='#workflow'>How it works</a>
    <a class='nav-link' href='#faq'>FAQ</a>
    <a class='nav-link' href='#contact'>Contact</a>
    <a class='nav-link' href='#apply'>Apply</a>
</div>
"""

st.markdown(NAV, unsafe_allow_html=True)

initialize_database()


def render_hero() -> None:
    st.markdown(
        """
        <section id='home' class='hero-panel'>
            <div style='display:flex; flex-wrap:wrap; gap:2rem; align-items:center;'>
                <div style='flex:1; min-width:320px; max-width:640px;'>
                    <div class='hero-pill'>Claim intake designed for modern financial teams</div>
                    <h1 style='font-size:3.4rem; line-height:1.05; margin-top:1rem;'>A premium customer intake experience for every claim.</h1>
                    <p style='font-size:1.05rem; margin-top:1.5rem; max-width:630px; color: rgba(255,255,255,0.92);'>Collect claim details, validate submissions, and manage records securely with a high-performing intake platform built for fast growth.</p>
                    <div style='margin-top:2rem; display:flex; flex-wrap:wrap; gap:1rem;'>
                        <a class='hero-button' href='#apply'>Start application</a>
                        <a class='hero-button' style='background: rgba(255,255,255,0.14);' href='#contact'>Contact sales</a>
                    </div>
                </div>
                <div style='flex:1; min-width:320px;'>
                    <div class='card-panel'>
                        <p style='margin-bottom:0.75rem; font-weight:700; color:#12b886;'>Trusted workflow</p>
                        <h2 style='margin:0 0 1rem;'>Secure customer intake with visibility.</h2>
                        <ul style='padding-left:1.2rem; line-height:1.8;'>
                            <li>Clear submission tracking for every request</li>
                            <li>Safe file attachment handling</li>
                            <li>Authenticated admin review and exports</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_benefits() -> None:
    st.write(" ")
    st.markdown("<section id='benefits'><div class='section-card'><h2>Benefits</h2><p>Built to deliver a premium intake journey with enterprise-grade security.</p></div></section>", unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    cols[0].markdown(
        """
        <div class='card-panel'>
            <h3>Customer-first experience</h3>
            <p>Clean forms, fast validation, and clear feedback across desktop and mobile.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class='card-panel'>
            <h3>Secure storage</h3>
            <p>Submissions are saved in Supabase PostgreSQL with safe upload handling.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class='card-panel'>
            <h3>Actionable admin insights</h3>
            <p>Search, filter, export, and manage claims from a secure dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow() -> None:
    st.write(" ")
    st.markdown("<section id='workflow'><div class='section-card'><h2>How it works</h2><p>A straight-forward process for customers and administrators.</p></div></section>", unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    cols[0].markdown(
        """
        <div class='card-panel'>
            <h3>1. Submit claim</h3>
            <p>Customers complete the form with claim details and attach supporting documents.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class='card-panel'>
            <h3>2. Store securely</h3>
            <p>Each submission is saved to the database and made available to authorized staff.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class='card-panel'>
            <h3>3. Manage and export</h3>
            <p>Admins review claims, filter records, export Excel reports, and delete entries if needed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_faq() -> None:
    st.write(" ")
    st.markdown("<section id='faq'><div class='section-card'><h2>Frequently asked questions</h2></div></section>", unsafe_allow_html=True)
    faq_items = [
        (
            "How is my claim information stored?",
            "Claim details are stored in Supabase PostgreSQL. Uploaded attachments are saved securely to a protected uploads folder and registered with a safe link."
        ),
        (
            "Can admins export records?",
            "Yes. Admins can export both CSV and Excel (.xlsx) reports for all submitted claims."
        ),
        (
            "What credentials are required for admin access?",
            "Admin email and password are configured through environment variables for secure access."
        ),
        (
            "Is the intake form mobile friendly?",
            "Yes. The layout is responsive and optimized for both mobile and desktop browsers."
        ),
    ]
    for question, answer in faq_items:
        with st.expander(question):
            st.write(answer)


def render_contact() -> None:
    st.write(" ")
    st.markdown("<section id='contact'><div class='section-card'><h2>Contact</h2><p>Send a message and our team will follow up with more information.</p></div></section>", unsafe_allow_html=True)
    with st.form("contact_form"):
        contact_name = st.text_input("Full Name")
        contact_email = st.text_input("Email Address")
        contact_message = st.text_area("Message", height=120)
        if st.form_submit_button("Send message"):
            if not contact_name or not contact_email or not contact_message:
                st.error("Please provide your full name, email, and a brief message.")
            elif not validate_email(contact_email):
                st.error("Please enter a valid email address.")
            else:
                st.success("Your message has been received. We will respond soon.")


def render_application_form() -> None:
    st.markdown("<section id='apply'><div class='section-card'><h2>Application form</h2><p>Submit your claim details below to begin the process.</p></div></section>", unsafe_allow_html=True)
    if not DB_CONFIGURED:
        st.warning("The application form is disabled because database configuration is missing. Set SUPABASE_DB_URL or DATABASE_URL in environment variables.")
        return

    with st.form("claim_application_form"):
        col1, col2 = st.columns(2)
        full_name = col1.text_input("Full Name")
        phone = col1.text_input("Phone Number")
        email = col1.text_input("Email Address")
        address = col2.text_input("Address")
        city = col2.text_input("City")
        state = col1.text_input("State")
        zip_code = col2.text_input("ZIP Code")
        date_of_birth = col1.date_input("Date of Birth", max_value=date.today())
        claim_reference = col2.text_input("Claim Reference Number")
        claim_description = st.text_area("Description of Claim", height=140)
        notes = st.text_area("Supporting Notes (optional)", height=120)
        uploaded_file = st.file_uploader("Optional supporting file", type=["pdf", "png", "jpg", "jpeg"], help="PDF or image files only")
        submitted = st.form_submit_button("Submit claim")

        if submitted:
            if not full_name or not phone or not email or not address or not city or not state or not zip_code or not claim_reference or not claim_description:
                st.error("Please complete all required fields before submitting.")
                return

            if not validate_email(email):
                st.error("Please provide a valid email address.")
                return

            try:
                file_url = save_uploaded_file(uploaded_file)
                save_application(
                    {
                        "full_name": sanitize_text(full_name),
                        "phone": sanitize_text(phone),
                        "email": sanitize_text(email),
                        "address": sanitize_text(address),
                        "city": sanitize_text(city),
                        "state": sanitize_text(state),
                        "zip_code": sanitize_text(zip_code),
                        "date_of_birth": date_of_birth,
                        "claim_reference": sanitize_text(claim_reference),
                        "claim_description": sanitize_text(claim_description),
                        "notes": sanitize_text(notes),
                        "uploaded_file_url": file_url,
                    }
                )
                st.success("Your claim has been submitted successfully.")
                st.info("A secure copy of your submission is now stored in the intake platform.")
            except Exception as exc:
                st.error(f"Unable to save your claim right now: {exc}")


def render_admin_login() -> None:
    st.markdown("<section id='admin'><div class='section-card'><h2>Admin login</h2><p>Sign in with secure credentials to view submitted claims.</p></div></section>", unsafe_allow_html=True)
    if not DB_CONFIGURED:
        st.warning("Admin panel is disabled until database configuration is available.")
        return
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        st.error("ADMIN_EMAIL and ADMIN_PASSWORD must be configured in environment variables.")
        return

    with st.form("admin_login_form"):
        admin_email = st.text_input("Admin Email")
        admin_password = st.text_input("Admin Password", type="password")
        if st.form_submit_button("Log in"):
            if admin_email.strip().lower() == ADMIN_EMAIL.strip().lower() and admin_password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Admin signed in successfully.")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")


def render_admin_dashboard() -> None:
    st.markdown("<section id='admin'><div class='section-card'><h2>Admin dashboard</h2><p>Search, filter, export, and manage customer claims securely.</p></div></section>", unsafe_allow_html=True)

    search_text = st.text_input("Search by name, email, phone, or claim reference")
    col1, col2, col3 = st.columns(3)
    start_date = col1.date_input("From", date.today().replace(day=1))
    end_date = col2.date_input("To", date.today())
    sort_order = col3.selectbox("Sort by date", ["Newest first", "Oldest first"])
    sort_desc = sort_order == "Newest first"

    if start_date > end_date:
        st.error("The start date cannot be after the end date.")
        return

    applications = list_applications(search=search_text, start_date=start_date, end_date=end_date, sort_desc=sort_desc)
    if not applications:
        st.warning("No claim submissions match the current filters.")
        return

    st.markdown(f"<p><strong>{len(applications)}</strong> application(s) found.</p>", unsafe_allow_html=True)
    df = st.dataframe(applications, use_container_width=True)

    export_cols = [
        "id",
        "full_name",
        "phone",
        "email",
        "address",
        "city",
        "state",
        "zip_code",
        "created_at",
        "claim_reference",
        "notes",
    ]
    excel_bytes = generate_excel_bytes(applications)
    st.download_button("Download Excel report", data=excel_bytes, file_name="claims_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    csv_data = st.session_state.get("csv_data")
    if csv_data is None:
        import pandas as pd

        csv_data = pd.DataFrame(applications).to_csv(index=False).encode("utf-8")
        st.session_state["csv_data"] = csv_data

    st.download_button("Download CSV", data=csv_data, file_name="claims_report.csv", mime="text/csv")

    with st.expander("Application details and management"):
        ids = [app["id"] for app in applications]
        selected_id = st.selectbox("Select application ID", ids)
        if selected_id:
            record = get_application_by_id(selected_id)
            if record:
                st.markdown("<div class='card-panel'>", unsafe_allow_html=True)
                st.write(record)
                st.markdown("</div>", unsafe_allow_html=True)
                if record.get("uploaded_file_url"):
                    st.markdown(f"**Attachment:** {record['uploaded_file_url']}")
                if st.button("Delete this application"):
                    delete_application(selected_id)
                    st.success("Application deleted.")
                    st.experimental_rerun()

    if st.button("Log out"):
        st.session_state.admin_authenticated = False
        st.experimental_rerun()


def main() -> None:
    st.title("ClaimFlow Intake Platform")
    page = st.sidebar.radio("Navigate", ["Home", "Apply", "Admin"], index=0)
    if page == "Home":
        render_hero()
        render_benefits()
        render_workflow()
        render_faq()
        render_contact()
    elif page == "Apply":
        render_application_form()
    elif page == "Admin":
        if st.session_state.admin_authenticated:
            render_admin_dashboard()
        else:
            render_admin_login()

    if not DB_CONFIGURED:
        st.warning("Database is not configured. Set SUPABASE_DB_URL or DATABASE_URL to enable claim intake and admin features.")


if __name__ == "__main__":
    main()
