import streamlit as st

from auth_common import extract_session, extract_user, normalize_session


def render_signup(client):
    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input("Name", placeholder="Your full name", key="signup_name")
        university_name = st.text_input("University name", placeholder="Your university", key="signup_university")
        session_name = st.text_input("Session", placeholder="2023-2027", key="signup_session")
        subject = st.text_input("Subject", placeholder="Computer Science", key="signup_subject")
        signup_email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
        signup_password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
        confirm_password = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="signup_confirm_password")
        signup_submit = st.form_submit_button("Create account", use_container_width=True)

    if not signup_submit:
        return

    errors = []

    if not name.strip():
        errors.append("Name is required.")
    if not university_name.strip():
        errors.append("University name is required.")
    if not session_name.strip():
        errors.append("Session is required.")
    if not subject.strip():
        errors.append("Subject is required.")
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
                        "university_name": university_name.strip(),
                        "session": session_name.strip(),
                        "subject": subject.strip(),
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