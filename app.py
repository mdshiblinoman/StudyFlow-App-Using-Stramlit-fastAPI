import streamlit as st

from auth_common import apply_styles, get_supabase_client, restore_session, user_field, user_metadata
from home import render_home_page
from subject import render_subject_page
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

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"

if "current_view" not in st.session_state:
    st.session_state.current_view = "home" if st.session_state.supabase_user is not None else "auth"

if st.session_state.supabase_user is not None:
    st.session_state.current_view = "home"
else:
    st.session_state.current_view = "auth"

is_authenticated = st.session_state.supabase_user is not None

st.markdown(
    """
    <div class="bg-hero shadow-hero tw-rounded-hero p-8 text-white mb-6">
        <h1 class="m-0 text-4xl leading-tight font-semibold">Welcome to StudyFlow</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

if client is None:
    st.error("Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY to your .env file, and install the supabase package.")
    st.info("Run streamlit after setting the Supabase credentials.")
    st.stop()

if st.session_state.current_view == "home" and is_authenticated:
    render_home_page(client, st.session_state.supabase_user)
elif st.session_state.current_view == "subject" and is_authenticated:
    render_subject_page(client)
else:
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
    if st.session_state.auth_mode == "signin":
        render_signin(client)
    else:
        render_signup(client)

    st.markdown('</div>', unsafe_allow_html=True)

