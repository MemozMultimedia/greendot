import os
import re
import uuid
from datetime import datetime, date
from io import BytesIO
from typing import Any, Dict, List, Optional

import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st
#from openpyxl import Workbook
#from openpyxl.utils.dataframe import dataframe_to_rows

DATABASE_URL = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
DB_CONFIGURED = bool(DATABASE_URL)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
ALLOWED_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png"}

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

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


@st.cache_resource
def get_connection():
    if not DB_CONFIGURED:
        return None
    try:
        return psycopg2.connect(
            DATABASE_URL,
            sslmode="require",
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


def initialize_database() -> None:
    if not DB_CONFIGURED:
        return
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code TEXT NOT NULL,
                    date_of_birth DATE NOT NULL,
                    claim_reference TEXT NOT NULL,
                    claim_description TEXT NOT NULL,
                    notes TEXT,
                    uploaded_file_url TEXT
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_applications_created_at ON applications(created_at DESC);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_applications_email ON applications(LOWER(email));")
        conn.commit()
    except Exception as e:
        st.warning(f"Database initialization: {e}")
    finally:
        if conn:
            conn.close()


def sanitize_text(value: Optional[str]) -> str:
    return value.strip() if isinstance(value, str) else ""


def validate_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value.strip()))


def sanitize_filename(filename: str) -> str:
    name = os.path.basename(filename)
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    return name[:120]


def save_uploaded_file(uploaded_file: Optional[Any]) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported file type.")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = sanitize_filename(uploaded_file.name)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def save_application(application: Dict[str, Any]) -> None:
    if not DB_CONFIGURED:
        raise RuntimeError("Database not configured.")
    conn = get_connection()
    if not conn:
        raise RuntimeError("Database connection failed.")
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO applications (
                    full_name, phone, email, address, city, state, zip_code,
                    date_of_birth, claim_reference, claim_description, notes, uploaded_file_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    application["full_name"],
                    application["phone"],
                    application["email"],
                    application["address"],
                    application["city"],
                    application["state"],
                    application["zip_code"],
                    application["date_of_birth"],
                    application["claim_reference"],
                    application["claim_description"],
                    application["notes"],
                    application["uploaded_file_url"],
                ),
            )
        conn.commit()
    finally:
        if conn:
            conn.close()


def list_applications(
    search: str = "",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    sort_desc: bool = True,
) -> List[Dict[str, Any]]:
    if not DB_CONFIGURED:
        return []
    conn = get_connection()
    if not conn:
        return []
    try:
        query = "SELECT * FROM applications"
        conditions = []
        params = []
        if search:
            conditions.append("(LOWER(full_name) LIKE %s OR LOWER(email) LIKE %s OR LOWER(phone) LIKE %s OR LOWER(claim_reference) LIKE %s)")
            term = f"%{search.lower()}%"
            params.extend([term, term, term, term])
        if start_date:
            conditions.append("created_at >= %s")
            params.append(datetime.combine(start_date, datetime.min.time()))
        if end_date:
            conditions.append("created_at < %s")
            params.append(datetime.combine(end_date, datetime.max.time()))
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at " + ("DESC" if sort_desc else "ASC")
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall() or []
    finally:
        if conn:
            conn.close()


def get_application_by_id(application_id: int) -> Optional[Dict[str, Any]]:
    if not DB_CONFIGURED:
        return None
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM applications WHERE id = %s", (application_id,))
            return cursor.fetchone()
    finally:
        if conn:
            conn.close()


def delete_application(application_id: int) -> None:
    if not DB_CONFIGURED:
        return
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()


def generate_excel_bytes(applications: List[Dict[str, Any]]) -> bytes:
    if not applications:
        return b""
    try:
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows
        df = pd.DataFrame(applications)
        df = df.rename(columns={
            "id": "Submission ID",
            "full_name": "Full Name",
            "phone": "Phone",
            "email": "Email",
            "address": "Address",
            "city": "City",
            "state": "State",
            "zip_code": "ZIP",
            "created_at": "Date Submitted",
            "claim_reference": "Claim Reference",
            "notes": "Notes",
        })
        df = df[[
            "Submission ID",
            "Full Name",
            "Phone",
            "Email",
            "Address",
            "City",
            "State",
            "ZIP",
            "Date Submitted",
            "Claim Reference",
            "Notes",
        ]]
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Applications"
        for r in dataframe_to_rows(df, index=False, header=True):
            worksheet.append(r)
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value or "")) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(length + 2, 40)
        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        return buffer.read()
    except ImportError:
        return b""


def render_nav():
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.image("logo.svg", use_column_width=True)
    with col2:
        st.markdown(
            """
            <div class='nav-links'>
                <a class='nav-link' href='#home'>Home</a>
                <a class='nav-link' href='#benefits'>Benefits</a>
                <a class='nav-link' href='#workflow'>How it works</a>
                <a class='nav-link' href='#faq'>FAQ</a>
                <a class='nav-link' href='#contact'>Contact</a>
                <a class='nav-link' href='#apply'>Apply</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_hero():
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


def render_benefits():
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


def render_workflow():
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


def render_faq():
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


def render_contact():
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


def render_application_form():
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
        uploaded_file = st.file_uploader("Optional supporting file", type=["pdf", "png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Submit claim")
        if submitted:
            if not full_name or not phone or not email or not address or not city or not state or not zip_code or not claim_reference or not claim_description:
                st.error("Please complete all required fields before submitting.")
                return
            if not validate_email(email):
                st.error("Please provide a valid email address.")
                return
            try:
                file_url = save_uploaded_file(uploaded_file) if uploaded_file else ""
                save_application({
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
                })
                st.success("Your claim has been submitted successfully.")
                st.info("A secure copy of your submission is now stored in the intake platform.")
            except Exception as exc:
                st.error(f"Unable to save your claim right now: {exc}")


def render_admin_login():
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


def render_admin_dashboard():
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
    st.dataframe(applications, use_container_width=True)
    excel_bytes = generate_excel_bytes(applications)
    if excel_bytes:
        st.download_button("Download Excel report", data=excel_bytes, file_name="claims_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    csv_data = pd.DataFrame(applications).to_csv(index=False).encode("utf-8")
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


def main():
    render_nav()
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
    initialize_database()
    main()
# Force redeploy
