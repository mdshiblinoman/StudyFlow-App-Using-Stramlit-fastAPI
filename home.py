import streamlit as st
from auth_common import clear_supabase_state, user_field, user_metadata

def render_home_page(client, user):

    # Expanded subject lists (CSE and EEE) rendered as buttons
    CSE_SUBJECTS = [
        "Programming Languages",
        "Data Structures",
        "Algorithms",
        "Object-Oriented Programming (OOP)",
        "Database Management Systems (DBMS)",
        "Operating Systems",
        "Computer Networks",
        "Software Engineering",
        "Computer Architecture",
        "Microprocessors & Microcontrollers",
        "Discrete Mathematics",
        "Theory of Computation",
        "Compiler Design",
        "Artificial Intelligence (AI)",
        "Machine Learning",
        "Web Development",
        "Mobile Application Development",
        "Cyber Security",
        "Data Mining",
        "Computer Graphics",
        "Communication Systems",
        "Digital Signal Processing (DSP)",
        "Microprocessor & Embedded Systems",
        "Renewable Energy Systems",
        "VLSI Design",
        "Signals and Systems",
    ]

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, subj in enumerate(CSE_SUBJECTS):
        col = cols[i % 3]
        if col.button(subj, key=f"cse_subject_{i}"):
            st.session_state.selected_subject = subj
            st.session_state.selected_department = "CSE"
            st.info(f"Selected subject: {subj}")

    st.markdown('<div class="mt-3"></div>', unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        clear_supabase_state(reset_client=True)
        st.session_state.current_view = "auth"
        st.rerun()