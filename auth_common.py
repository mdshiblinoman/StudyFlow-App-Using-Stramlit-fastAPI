import os
from pathlib import Path

import streamlit as st

try:
    from supabase import create_client
except ImportError:
    create_client = None


def load_env_file(env_path=".env"):
    env_file = Path(env_path)
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

TAILWIND_UTILITY_CSS = """
<style>
    .bg-page {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 30%),
            linear-gradient(135deg, #eef4ff 0%, #f7fbff 45%, #ffffff 100%);
    }
    .bg-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 52%, #2563eb 100%);
    }
    .shadow-hero {
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.22);
    }
    .shadow-card {
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.08);
    }
    .shadow-panel {
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }
    .backdrop-blur-12 {
        backdrop-filter: blur(12px);
    }
    .bg-card {
        background: rgba(255, 255, 255, 0.84);
    }
    .bg-badge {
        background: rgba(219, 234, 254, 0.96);
    }
    .bg-gradient-to-b {
        background-image: linear-gradient(to bottom, var(--tw-gradient-from, #ffffff), var(--tw-gradient-to, #eff6ff));
    }
    .from-white {
        --tw-gradient-from: #ffffff;
    }
    .to-blue-50 {
        --tw-gradient-to: #eff6ff;
    }
    .text-badge {
        color: #1d4ed8;
    }
    .text-soft {
        color: #64748b;
    }
    .text-white {
        color: #ffffff;
    }
    .text-sm {
        font-size: 0.875rem;
        line-height: 1.25rem;
    }
    .text-base {
        font-size: 1rem;
        line-height: 1.5rem;
    }
    .text-4xl {
        font-size: 2.25rem;
        line-height: 2.5rem;
    }
    .font-semibold {
        font-weight: 600;
    }
    .font-bold {
        font-weight: 700;
    }
    .leading-tight {
        line-height: 1.25;
    }
    .m-0 {
        margin: 0;
    }
    .mt-3 {
        margin-top: 0.75rem;
    }
    .mt-4 {
        margin-top: 1rem;
    }
    .mb-4 {
        margin-bottom: 1rem;
    }
    .mb-6 {
        margin-bottom: 1.5rem;
    }
    .p-4 {
        padding: 1rem;
    }
    .p-5 {
        padding: 1.25rem;
    }
    .p-8 {
        padding: 2rem;
    }
    .px-3 {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    .py-1 {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    .inline-block {
        display: inline-block;
    }
    .rounded-full {
        border-radius: 9999px;
    }
    .max-w-4xl {
        max-width: 56rem;
    }
    .opacity-90 {
        opacity: 0.9;
    }
    .text-center {
        text-align: center;
    }
    .ring-card {
        border: 1px solid rgba(148, 163, 184, 0.20);
    }
    .ring-panel {
        border: 1px solid rgba(148, 163, 184, 0.18);
    }
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: #ffffff;
        border: none;
        border-radius: 14px;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
        transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        filter: brightness(1.03);
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.28);
        transform: translateY(-1px);
    }
    div[data-testid="stButton"] > button:focus,
    div[data-testid="stFormSubmitButton"] > button:focus {
        box-shadow: 0 0 0 3px rgba(147, 197, 253, 0.45), 0 14px 30px rgba(37, 99, 235, 0.28);
    }
    div[data-testid="stButton"] > button:disabled,
    div[data-testid="stFormSubmitButton"] > button:disabled {
        background: linear-gradient(135deg, #94a3b8 0%, #cbd5e1 100%);
        color: rgba(255, 255, 255, 0.85);
        box-shadow: none;
        transform: none;
    }
    .tw-rounded-hero {
        border-radius: 28px;
    }
    .tw-rounded-card {
        border-radius: 24px;
    }
    .tw-rounded-panel {
        border-radius: 18px;
    }
    div[data-testid="stForm"] {
        background: transparent;
    }
</style>
"""


def apply_styles():
    st.markdown(TAILWIND_UTILITY_CSS, unsafe_allow_html=True)


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