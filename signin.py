import streamlit as st

from auth_common import extract_session, extract_user, normalize_session

def render_signin(client):
    with st.form("signin_form", clear_on_submit=False):
        signin_email = st.text_input("Email", key="signin_email")
        signin_password = st.text_input("Password", type="password", key="signin_password")
        signin_submit = st.form_submit_button("Sign in", use_container_width=True)

    if st.button("Don't have an account? Sign up", key="signin_to_signup"):
        st.session_state.auth_mode = "signup"
        st.rerun()

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
        st.session_state.auth_mode = "signin"
        st.session_state.current_view = "home"
        st.success("Signed in successfully.")
        st.rerun()
    except Exception as exc:
        error_message = str(exc)
        if "invalid login credentials" in error_message.lower():
            st.error("Invalid login credentials.")
            st.info("If you just created the account, confirm your email first. If email confirmation is disabled, verify the email and password exactly as entered.")
            return
        if "email not confirmed" in error_message.lower() or "email_confirmation" in error_message.lower():
            st.error("Email not confirmed.")
            st.info("Check your inbox and confirm your account before signing in. If you want to skip email confirmation, disable it in the Supabase dashboard under Authentication > Providers > Email.")
            return

        st.error(error_message)