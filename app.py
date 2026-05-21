import streamlit as st

from auth_common import apply_styles, get_supabase_client, restore_session, user_field, user_metadata
from signin import render_signin
from signup import render_signup


st.set_page_config(page_title="StudyFlow", page_icon="🎓", layout="wide")

apply_styles()


client = get_supabase_client()

if "supabase_user" not in st.session_state:
    st.session_state.supabase_user = None

if "supabase_session" not in st.session_state:
    st.session_state.supabase_session = None

if client is not None and st.session_state.supabase_user is None:
    st.session_state.supabase_user = restore_session(client)

is_authenticated = st.session_state.supabase_user is not None

st.markdown(
    """
    <div class="bg-hero shadow-hero tw-rounded-hero p-8 text-white mb-6">
        <h1 class="m-0 text-4xl leading-tight font-semibold">Welcome to StudyFlow</h1>
        <p class="mt-3 max-w-4xl text-base opacity-90">
            Sign up first, then sign in with Supabase authentication. Your logged-in session stays available in Streamlit until you log out.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if client is None:
    st.error("Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY to your .env file, and install the supabase package.")
    st.info("Run streamlit after setting the Supabase credentials.")
    st.stop()

st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.account-access-card) {
            max-width: 720px;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="account-access-card bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-5">', unsafe_allow_html=True)
st.subheader("Account access")
tab_signin, tab_signup = st.tabs(["Sign in", "Sign up"])

with tab_signin:
    render_signin(client)

with tab_signup:
    render_signup(client)

st.markdown('</div>', unsafe_allow_html=True)

if is_authenticated:
    user = st.session_state.supabase_user
    metadata = user_metadata(user)
    display_name = metadata.get("name") or user_field(user, "email") or "Signed in user"
    email_value = user_field(user, "email")

    st.success(f"Signed in as {display_name}")
    st.markdown(
        f"""
        <div class="bg-gradient-to-b from-white to-blue-50 ring-panel shadow-panel tw-rounded-panel p-4">
            <p><strong>Name:</strong> {metadata.get('name', 'Not set')}</p>
            <p><strong>University:</strong> {metadata.get('university_name', 'Not set')}</p>
            <p><strong>Subject:</strong> {metadata.get('subject', 'Not set')}</p>
            <p><strong>Email:</strong> {email_value or 'Not set'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        st.session_state.supabase_user = None
        st.session_state.supabase_session = None
        st.rerun()

st.markdown(
    '<div class="text-soft mt-4 text-center text-sm">Built with Streamlit and Supabase authentication for a clean student login flow.</div>',
    unsafe_allow_html=True,
)
