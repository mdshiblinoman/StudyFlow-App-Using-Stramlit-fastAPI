import streamlit as st

from auth_common import user_field, user_metadata


def render_home_page(client, user):
    metadata = user_metadata(user)
    display_name = metadata.get("name") or user_field(user, "email") or "Signed in user"

    st.markdown(
        """
        <div class="bg-hero shadow-hero tw-rounded-hero p-8 text-white mb-6">
            <div class="bg-badge text-badge inline-block rounded-full px-3 py-1 text-sm font-bold mb-4">StudyFlow Home</div>
            <h1 class="m-0 text-4xl leading-tight font-semibold">Welcome back!</h1>
            <p class="mt-3 max-w-4xl text-base opacity-90">
                You are signed in and ready to continue your StudyFlow experience.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-6">
            <h3 class="m-0 mb-3">Hello, {display_name}</h3>
            <p class="m-0 text-soft">Your home page is now open automatically after sign in.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        st.session_state.supabase_user = None
        st.session_state.supabase_session = None
        st.session_state.current_view = "auth"
        st.rerun()