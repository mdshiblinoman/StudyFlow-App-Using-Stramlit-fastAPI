import streamlit as st
from auth_common import clear_supabase_state, user_field, user_metadata
from subjects import CSE_SUBJECTS, EEE_SUBJECTS, PROGRAMMING_LANGUAGES


def render_home_page(client, user):

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)

    # Render CSE subjects as buttons
    cols = st.columns(3)
    for i, subj in enumerate(CSE_SUBJECTS):
        col = cols[i % 3]
        if col.button(subj, key=f"cse_subject_{i}"):
            st.session_state.selected_subject = subj
            st.session_state.selected_department = "CSE"
            st.info(f"Selected subject: {subj}")

    st.markdown('<div class="mt-3"></div>', unsafe_allow_html=True)

    # If Programming Languages is selected, show language group
    selected = st.session_state.get("selected_subject")
    if selected == "Programming Languages":
        st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-4">
            <h4 class="m-0 mb-3">Programming Languages</h4>
            <p class="m-0 text-soft">Choose a language to explore topics and resources.</p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, lang in enumerate(PROGRAMMING_LANGUAGES):
            col = cols[i % 3]
            if col.button(lang, key=f"lang_{i}"):
                st.session_state.selected_language = lang
                st.session_state.selected_department = "CSE"
                st.session_state.current_view = "subject"
                st.rerun()

        if st.button("Back to subjects"):
            st.session_state.selected_subject = None
            st.session_state.selected_language = None
            st.rerun()

    if st.button("Logout", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        clear_supabase_state(reset_client=True)
        st.session_state.current_view = "auth"
        st.rerun()