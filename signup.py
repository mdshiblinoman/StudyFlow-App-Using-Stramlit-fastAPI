import streamlit as st

from auth_common import extract_session, extract_user, normalize_session


PUBLIC_UNIVERSITIES = [
    "University of Dhaka",
    "University of Rajshahi",
    "University of Chittagong",
    "Jahangirnagar University",
    "Bangladesh University of Engineering and Technology (BUET)",
    "Khulna University",
    "Shahjalal University of Science and Technology",
    "Jagannath University",
    "Jashore University of Science and Technology",
    "Comilla University",
    "Pabna University of Science and Technology",
    "Mawlana Bhashani Science and Technology University",
    "Noakhali Science and Technology University",
    "Patuakhali Science and Technology University",
    "Bangabandhu Sheikh Mujibur Rahman Science and Technology University",
    "Bangabandhu Sheikh Mujibur Rahman Agricultural University",
    "Sher-e-Bangla Agricultural University",
    "Hajee Mohammad Danesh Science and Technology University",
    "Mymensingh Engineering College",
    "Bangladesh University of Professionals",
    "University of Barishal",
    "Rabindra University",
    "Bangamata Sheikh Fojilatunnesa Mujib Science and Technology University",
    "Bangabandhu Sheikh Mujib Medical University",
    "National University",
]


PRIVATE_UNIVERSITIES = [
    "BRAC University",
    "North South University",
    "Independent University, Bangladesh",
    "East West University",
    "Ahsanullah University of Science and Technology",
    "American International University-Bangladesh",
    "Daffodil International University",
    "University of Asia Pacific",
    "United International University",
    "BRAC University",
    "Stamford University Bangladesh",
    "Southeast University",
    "City University",
    "Green University of Bangladesh",
    "IUBAT — International University of Business Agriculture and Technology",
    "International University of Business Agriculture and Technology",
    "Manarat International University",
    "Primeasia University",
    "Northern University Bangladesh",
    "Premier University",
    "Varendra University",
    "Bangladesh University",
    "BGC Trust University Bangladesh",
    "Lalmatia Housing Society Ltd. University",
    "Canadian University of Bangladesh",
    "Central Women's University",
    "World University of Bangladesh",
    "Eastern University",
    "Notre Dame University Bangladesh",
    "Presidency University",
    "Southeast University",
    "Sonargaon University",
    "University of Development Alternative",
    "University of Liberal Arts Bangladesh",
    "Uttara University",
    "The People's University of Bangladesh",
]


SESSION_OPTIONS = [
    "Select session",
    "2025-2026",
    "2024-2025",
    "2023-2024",
    "2022-2023",
    "2021-2022",
    "2020-2021",
    "2019-2020",
]


UNIVERSITY_OPTIONS = ["Select university"] + list(dict.fromkeys(PUBLIC_UNIVERSITIES + PRIVATE_UNIVERSITIES))


ENGINEERING_SUBJECT_OPTIONS = [
    "Select engineering department",
    "Computer Science and Engineering (CSE)",
    "Electrical and Electronic Engineering (EEE)",
    "Mechanical Engineering (ME)",
    "Civil Engineering (CE)",
    "Industrial and Production Engineering (IPE)",
    "Textile Engineering",
    "Materials and Metallurgical Engineering",
    "Chemical Engineering",
    "Petroleum and Mining Engineering",
    "Architecture",
    "Biomedical Engineering",
    "Mechatronics Engineering",
    "Software Engineering",
    "Information and Communication Engineering",
    "Biomedical Physics and Technology",
    "Environmental Engineering",
    "Naval Architecture and Marine Engineering",
    "Aerospace Engineering",
]


def render_signup(client):
    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input("Name", placeholder="Your full name", key="signup_name")
        university_name = st.selectbox("University name", UNIVERSITY_OPTIONS, index=0, key="signup_university")
        session_name = st.selectbox("Session", SESSION_OPTIONS, index=0, key="signup_session")
        subject = st.selectbox("Engineering department", ENGINEERING_SUBJECT_OPTIONS, index=0, key="signup_subject")
        signup_email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            help="Use 12+ characters with letters, numbers, and symbols.",
            key="signup_password",
        )
        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Re-enter your strong password",
            key="signup_confirm_password",
        )
        signup_submit = st.form_submit_button("Create account", use_container_width=True)

    if not signup_submit:
        return

    errors = []

    if not name.strip():
        errors.append("Name is required.")
    if university_name == "Select university":
        errors.append("University name is required.")
    if session_name == "Select session":
        errors.append("Session is required.")
    if subject == "Select engineering department":
        errors.append("Engineering department is required.")
    if not signup_email.strip():
        errors.append("Email is required.")
    if not signup_password:
        errors.append("Password is required.")
    if signup_password != confirm_password:
        errors.append("Passwords do not match.")
    if "@" not in signup_email or "." not in signup_email:
        errors.append("Enter a valid email address.")

    if errors:
        for error in errors:
            st.error(error)
        return

    try:
        result = client.auth.sign_up(
            {
                "email": signup_email.strip(),
                "password": signup_password,
                "options": {
                    "data": {
                        "name": name.strip(),
                        "university_name": university_name,
                        "session": session_name,
                        "subject": subject,
                    }
                },
            }
        )
        session = extract_session(result)
        user = extract_user(result)

        if user is None:
            st.success("Account created. Check your email to confirm your account, then sign in.")
            return

        st.session_state.supabase_session = normalize_session(session)
        st.session_state.supabase_user = user
        st.success("Account created and signed in successfully.")
        st.rerun()
    except Exception as exc:
        st.error(str(exc))