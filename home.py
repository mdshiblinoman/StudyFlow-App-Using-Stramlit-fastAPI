import streamlit as st
from auth_common import clear_supabase_state, user_field, user_metadata

def render_home_page(client, user):

    # CSE subjects list (rendered as buttons)
    CSE_SUBJECTS = [
        "Programming Languages",
        "Data Structures",
        "Algorithms",
        "Discrete Mathematics",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Software Engineering",
        "Artificial Intelligence",
    ]

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-4">
        <h4 class="m-0 mb-3">Common CSE Subjects</h4>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, subj in enumerate(CSE_SUBJECTS):
        col = cols[i % 3]
        if col.button(subj, key=f"subject_{i}"):
            st.session_state.selected_subject = subj
            st.info(f"Selected subject: {subj}")

    # extra button for other/advanced subjects
    if st.button("Other CSE subjects"):
        st.session_state.selected_subject = "Other CSE subjects"
        st.info("Selected: Other CSE subjects")

    if st.button("Logout", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        clear_supabase_state(reset_client=True)
        st.session_state.current_view = "auth"
        st.rerun()