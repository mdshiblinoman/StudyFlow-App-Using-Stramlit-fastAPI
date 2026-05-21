import os

import streamlit as st
from dotenv import load_dotenv

try:
    from supabase import create_client
except ImportError:
    create_client = None


load_dotenv()

TAILWIND_INSPIRED_CSS = """
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 30%),
            linear-gradient(135deg, #eef4ff 0%, #f7fbff 45%, #ffffff 100%);
    }
    .tw-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 52%, #2563eb 100%);
        padding: 2.2rem;
        border-radius: 28px;
        color: white;
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.22);
        margin-bottom: 1.5rem;
    }
    .tw-hero h1 {
        margin: 0;
        font-size: 2.4rem;
        line-height: 1.05;
    }
    .tw-hero p {
        margin: 0.75rem 0 0;
        opacity: 0.92;
        font-size: 1.02rem;
        max-width: 52rem;
    }
    .tw-card {
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 24px;
        padding: 1.2rem 1.2rem 0.6rem;
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(12px);
    }
    .tw-badge {
        display: inline-block;
        background: rgba(219, 234, 254, 0.96);
        color: #1d4ed8;
        padding: 0.38rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }
    div[data-testid="stForm"] {
        background: transparent;
    }
    .tw-footer {
        color: #64748b;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 1rem;
    }
    .tw-panel {
        border-radius: 18px;
        padding: 1rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(239,246,255,0.92));
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }
</style>
"""


def apply_styles():
    st.markdown(TAILWIND_INSPIRED_CSS, unsafe_allow_html=True)


def get_supabase_client():
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key or create_client is None:
        return None

    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(url, key)

    return st.session_state.supabase_client


def extract_session(result):
    session = getattr(result, "session", None)
    if session is not None:
        return session

    data = getattr(result, "data", None)
    if isinstance(data, dict):
        return data.get("session")

    return None


def extract_user(result):
    user = getattr(result, "user", None)
    if user is not None:
        return user

    data = getattr(result, "data", None)
    if isinstance(data, dict):
        return data.get("user")

    return None


def normalize_session(session):
    if session is None:
        return None

    return {
        "access_token": getattr(session, "access_token", None) or session.get("access_token"),
        "refresh_token": getattr(session, "refresh_token", None) or session.get("refresh_token"),
    }


def restore_session(client):
    stored_session = st.session_state.get("supabase_session")
    if not stored_session:
        return None

    access_token = stored_session.get("access_token")
    refresh_token = stored_session.get("refresh_token")
    if not access_token or not refresh_token:
        return None

    try:
        client.auth.set_session(access_token, refresh_token)
    except Exception:
        st.session_state.supabase_session = None
        st.session_state.supabase_user = None
        return None

    try:
        return client.auth.get_user().user
    except Exception:
        return st.session_state.get("supabase_user")


def user_metadata(user):
    if not user:
        return {}

    return getattr(user, "user_metadata", None) or user.get("user_metadata", {}) or {}


def user_field(user, field_name, default=None):
    if user is None:
        return default

    if isinstance(user, dict):
        return user.get(field_name, default)

    return getattr(user, field_name, default)