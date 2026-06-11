import os
import re
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st

PAGE_TITLE = "GreenDot"

st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="collapsed")

STYLE = """
<style>
:root {
    color-scheme: light;
    --brand-dark: #0c2d56;
    --brand-green: #00c853;
    --surface: #ffffff;
    --surface-soft: #f6fbf8;
    --text-muted: #526c83;
}

body {
    background: linear-gradient(180deg, #eff9f3 0%, #f6fbf8 100%);
    color: var(--brand-dark);
}

.stApp {
    background: transparent;
}

section {
    padding: 3rem 0;
}

.section-card {
    background: var(--surface);
    border-radius: 28px;
    padding: 2rem;
    border: 1px solid rgba(14, 50, 88, 0.08);
    box-shadow: 0 32px 80px rgba(11, 45, 82, 0.08);
}

.hero-panel {
    border-radius: 36px;
    padding: 3rem;
    background: linear-gradient(135deg, #0c2d56 0%, #00c853 100%);
    color: white;
    box-shadow: 0 50px 120px rgba(0, 128, 78, 0.18);
}

.hero-panel h1,
.hero-panel h2,
.hero-panel p {
    margin: 0;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    border-radius: 999px;
    padding: 0.7rem 1rem;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
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
    font-weight: 700;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

.hero-button:hover,
.cta-button:hover {
    background: #083352;
    transform: translateY(-1px);
}

.card-highlight {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 24px;
    padding: 1.6rem;
    color: white;
}

.card-panel {
    border-radius: 28px;
    background: white;
    border: 1px solid rgba(14, 50, 88, 0.08);
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
</style>
"""

NAV_STYLE = """
<style>
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
    color: var(--brand-green);
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)
st.markdown(NAV_STYLE, unsafe_allow_html=True)

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DB_CONFIGURED = bool(SUPABASE_DB_URL)

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "application_submitted" not in st.session_state:
    st.session_state.application_submitted = False


@st.cache_resource
def get_db_connection():
    if not DB_CONFIGURED:
        raise RuntimeError("SUPABASE_DB_URL or DATABASE_URL environment variable is required.")
    return psycopg2.connect(
        SUPABASE_DB_URL,
        sslmode="require",
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def initialize_database():
    if not DB_CONFIGURED:
        return
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
        connection.commit()


def validate_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value.strip()))


def sanitize_text(value: Optional[str]) -> str:
    return value.strip() if isinstance(value, str) else ""


def save_application(form_data: Dict[str, str]) -> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO applications (
                    full_name,
                    phone,
                    email,
                    address,
                    city,
                    state,
                    zip_code,
                    notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    form_data["full_name"],
                    form_data["phone"],
                    form_data["email"],
                    form_data["address"],
                    form_data["city"],
                    form_data["state"],
                    form_data["zip_code"],
                    form_data["notes"],
                ),
            )
        connection.commit()


def load_applications(search: str = "", start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict]:
    query = "SELECT * FROM applications"
    conditions = []
    params = []

    if search:
        conditions.append("(LOWER(full_name) LIKE %s OR LOWER(email) LIKE %s OR LOWER(phone) LIKE %s)")
        wildcard = f"%{search.lower()}%"
        params.extend([wildcard, wildcard, wildcard])

    if start_date:
        conditions.append("created_at >= %s")
        params.append(datetime.combine(start_date, datetime.min.time()))

    if end_date:
        conditions.append("created_at < %s")
        params.append(datetime.combine(end_date + timedelta(days=1), datetime.min.time()))

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


def delete_application(application_id: int) -> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
        connection.commit()


def format_timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M") if isinstance(value, datetime) else ""


def render_nav():
    st.markdown(
        """
        <div class='nav-links'>
            <a class='nav-link' href='#apply'>Apply Now</a>
            <a class='nav-link' href='#contact'>Contact</a>
            <a class='nav-link' href='#faq'>FAQ</a>
            <a class='nav-link' href='#admin'>Admin</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <section class='hero-panel'>
            <div style='display:flex; flex-wrap:wrap; gap:2rem; align-items:center;'>
                <div style='flex:1; min-width:320px; max-width:640px;'>
                    <div class='hero-pill'>Trusted fintech for premium applicants</div>
                    <h1 style='font-size:3.4rem; line-height:1.05; margin-top:1rem;'>Apply with confidence, get results faster.</h1>
                    <p style='font-size:1.05rem; margin-top:1.5rem; max-width:620px; color: rgba(255,255,255,0.92);'>GreenDot brings a premium customer journey for modern financial applications. Built for speed, security, and clarity across desktop and mobile.</p>
                    <div style='margin-top:2rem; display:flex; flex-wrap:wrap; gap:1rem;'>
                        <a class='hero-button' href='#apply'>Start application</a>
                        <a class='hero-button' style='background: rgba(255,255,255,0.14);' href='#contact'>Talk with sales</a>
                    </div>
                </div>
                <div style='flex:1; min-width:320px;'>
                    <div class='card-highlight'>
                        <p style='margin-bottom:0.75rem; font-weight:700;'>Secure onboarding</p>
                        <h2 style='margin:0 0 1rem;'>Identity verification in minutes</h2>
                        <ul style='padding-left:1.25rem; color: rgba(255,255,255,0.95);'>
                            <li>Encrypted submission channels</li>
                            <li>Fast review with clear status updates</li>
                            <li>Mobile-first experience for every application</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_benefits():
    st.write(" ")
    st.markdown("<section><div class='section-card'><h2>Why customers choose GreenDot</h2><p>Modern fintech tools and premium service built for fast, confident decisions.</p></div></section>", unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    cols[0].markdown(
        """
        <div class='card-panel'>
            <h3>Speed</h3>
            <p>Modern processes that reduce friction and move applicants ahead in hours, not days.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        """
        <div class='card-panel'>
            <h3>Security</h3>
            <p>Enterprise-grade protections for every submission, with encrypted storage and access controls.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        """
        <div class='card-panel'>
            <h3>Support</h3>
            <p>Responsive teams and transparent updates keep every applicant informed and empowered.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_faq_section():
    st.write(" ")
    st.markdown("<section id='faq'><div class='section-card'><h2>Frequently asked questions</h2></div></section>", unsafe_allow_html=True)
    faqs = [
        (
            "How do I submit an application?",
            "Complete the application form with your full contact details and notes. We store submissions securely and notify you by email."
        ),
        (
            "Is my personal information safe?",
            "Yes. Every record is stored in Supabase PostgreSQL and transmitted over encrypted channels for maximum protection."
        ),
        (
            "How long does approval take?",
            "Most applications are reviewed within 24 to 48 hours after submission, depending on the volume and any follow-up needed."
        ),
        (
            "Can I update my application?",
            "If you need to revise details after submission, contact the support team through the contact form."
        ),
    ]
    for question, answer in faqs:
        with st.expander(question):
            st.write(answer)


def render_contact_section():
    st.write(" ")
    st.markdown("<section id='contact'><div class='section-card'><h2>Contact</h2><p>Share your details and our team will respond with next steps.</p></div></section>", unsafe_allow_html=True)
    with st.form("contact_form"):
        contact_name = st.text_input("Full Name")
        contact_email = st.text_input("Email Address")
        contact_message = st.text_area("Message")
        contact_submit = st.form_submit_button("Send message")
        if contact_submit:
            if contact_name and contact_email and contact_message and validate_email(contact_email):
                st.success("Thanks! Your message has been sent to our team.")
            else:
                st.error("Please enter a valid full name, email address, and message.")


def render_apply_form():
    st.markdown("<section id='apply'><div class='section-card'><h2>Application form</h2><p>Submit your details below to start the process.</p></div></section>", unsafe_allow_html=True)
    if not DB_CONFIGURED:
        st.warning("The application form is disabled because the database is not configured. Set SUPABASE_DB_URL or DATABASE_URL in your deployment environment.")
        return
    with st.form("application_form"):
        col1, col2 = st.columns(2)
        full_name = col1.text_input("Full Name")
        phone = col1.text_input("Phone Number")
        email = col1.text_input("Email Address")
        address = col2.text_input("Address")
        city = col2.text_input("City")
        state = col1.text_input("State")
        zip_code = col2.text_input("Zip Code")
        notes = st.text_area("Notes", height=110)
        submit = st.form_submit_button("Submit application")

        if submit:
            form_data = {
                "full_name": sanitize_text(full_name),
                "phone": sanitize_text(phone),
                "email": sanitize_text(email),
                "address": sanitize_text(address),
                "city": sanitize_text(city),
                "state": sanitize_text(state),
                "zip_code": sanitize_text(zip_code),
                "notes": sanitize_text(notes),
            }
            missing = [
                label for label, value in [
                    ("Full Name", form_data["full_name"]),
                    ("Phone Number", form_data["phone"]),
                    ("Email Address", form_data["email"]),
                    ("Address", form_data["address"]),
                    ("City", form_data["city"]),
                    ("State", form_data["state"]),
                    ("Zip Code", form_data["zip_code"]),
                ] if not value
            ]
            if missing:
                st.error(f"Please complete these fields: {', '.join(missing)}")
            elif not validate_email(form_data["email"]):
                st.error("Enter a valid email address.")
            else:
                try:
                    save_application(form_data)
                    st.success("Your application has been submitted successfully.")
                    st.info("A confirmation has been stored and we will reach out soon.")
                    st.session_state.application_submitted = True
                except Exception as exc:
                    st.error(f"Unable to save your application right now. {exc}")


def authenticate_admin(email: str, password: str) -> bool:
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return False
    return email.strip().lower() == ADMIN_EMAIL.strip().lower() and password == ADMIN_PASSWORD


def render_admin_login():
    st.markdown("<section id='admin'><div class='section-card'><h2>Admin login</h2><p>Secured access for application management.</p></div></section>", unsafe_allow_html=True)
    if not DB_CONFIGURED:
        st.warning("Database is not configured. Set SUPABASE_DB_URL or DATABASE_URL before using admin features.")
        return
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        st.error("Admin credentials must be configured in environment variables: ADMIN_EMAIL and ADMIN_PASSWORD.")
        return
    with st.form("admin_login"):
        admin_email = st.text_input("Admin Email")
        admin_password = st.text_input("Admin Password", type="password")
        admin_submit = st.form_submit_button("Log in")
        if admin_submit:
            if authenticate_admin(admin_email, admin_password):
                st.session_state.admin_authenticated = True
                st.success("Admin authenticated successfully.")
                st.experimental_rerun()
            else:
                st.error("Invalid admin credentials.")


def render_admin_panel():
    st.markdown("<section id='admin'><div class='section-card'><h2>Admin dashboard</h2><p>View, filter, export, and manage submissions.</p></div></section>", unsafe_allow_html=True)
    search = st.text_input("Search by name, email, or phone")
    col1, col2 = st.columns(2)
    start_date = col1.date_input("From", date.today() - timedelta(days=30))
    end_date = col2.date_input("To", date.today())
    if start_date > end_date:
        st.error("Start date cannot be after end date.")
        return
    applications = load_applications(search=search, start_date=start_date, end_date=end_date)
    if not applications:
        st.warning("No applications found for the selected filters.")
        return
    df = pd.DataFrame(applications)
    df["created_at"] = df["created_at"].apply(format_timestamp)
    st.dataframe(df, use_container_width=True)
    csv_payload = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export CSV",
        data=csv_payload,
        file_name=f"greendot_applications_{date.today().isoformat()}.csv",
        mime="text/csv",
    )
    with st.expander("Delete application by ID"):
        delete_id = st.number_input("Application ID", min_value=1, step=1)
        if st.button("Delete application"):
            try:
                delete_application(int(delete_id))
                st.success(f"Deleted application {delete_id}.")
                st.experimental_rerun()
            except Exception as exc:
                st.error(f"Unable to delete application: {exc}")
    if st.button("Log out"):
        st.session_state.admin_authenticated = False
        st.experimental_rerun()


def main():
    try:
        initialize_database()
    except Exception as exc:
        st.error(f"Database initialization failed. Check SUPABASE_DB_URL. {exc}")
        return

    render_nav()
    render_hero()
    render_benefits()
    render_faq_section()
    render_contact_section()
    render_apply_form()

    admin_tabs = st.tabs(["Application portal", "Admin portal"])
    with admin_tabs[0]:
        st.write("Manage your brand experience with secure admin access.")
    with admin_tabs[1]:
        if st.session_state.admin_authenticated:
            render_admin_panel()
        else:
            render_admin_login()


if __name__ == "__main__":
    main()
