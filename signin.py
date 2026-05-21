import streamlit as st

from auth_common import extract_session, extract_user, normalize_session


def render_signin(client):
    with st.form("signin_form", clear_on_submit=False):
        signin_email = st.text_input("Email", placeholder="you@example.com", key="signin_email")
        signin_password = st.text_input("Password", type="password", placeholder="Your password", key="signin_password")
        signin_submit = st.form_submit_button("Sign in", use_container_width=True)

    if not signin_submit:
        return

    if not signin_email.strip() or not signin_password:
        st.error("Email and password are required.")
        return

    try:
        result = client.auth.sign_in_with_password(
            {
                "email": signin_email.strip(),
                "password": signin_password,
            }
        )
        session = extract_session(result)
        user = extract_user(result)
        st.session_state.supabase_session = normalize_session(session)
        if user is None:
            user = client.auth.get_user().user
        st.session_state.supabase_user = user
        st.success("Signed in successfully.")
        st.rerun()
    except Exception as exc:
        st.error(str(exc))