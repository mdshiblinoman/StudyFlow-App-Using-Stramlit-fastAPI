import streamlit as st
from pathlib import Path
from auth_common import clear_supabase_state, user_field, user_metadata
from subjects import CSE_SUBJECTS, EEE_SUBJECTS, PROGRAMMING_LANGUAGES


LOGO_PATH = Path(__file__).resolve().parent / "assets" / "studyflow-logo.svg"
ALL_SEARCHABLE_SUBJECTS = list(dict.fromkeys(CSE_SUBJECTS + EEE_SUBJECTS + PROGRAMMING_LANGUAGES))


def _ensure_search_history_state():
    if "search_history" not in st.session_state:
        st.session_state.search_history = []


def _log_search(query, source):
    _ensure_search_history_state()

    entry = {
        "query": query,
        "source": source,
    }

    history = st.session_state.search_history
    if not history or history[0] != entry:
        history.insert(0, entry)
        st.session_state.search_history = history[:20]


def _open_subject_from_search(subject_name):
    if subject_name in PROGRAMMING_LANGUAGES:
        st.session_state.selected_subject = "Programming Languages"
        st.session_state.selected_language = subject_name
        st.session_state.selected_department = "CSE"
    else:
        st.session_state.selected_subject = subject_name
        st.session_state.selected_language = None
        st.session_state.selected_department = "EEE" if subject_name in EEE_SUBJECTS else "CSE"

    _log_search(subject_name, "Subject search")
    st.session_state.current_view = "subject"
    st.rerun()


def _render_profile_panel(client, user, include_search_history=True):
    metadata = user_metadata(user)
    full_name = metadata.get("name") or user_field(user, "email", "Learner").split("@")[0]
    email = user_field(user, "email", "Not available")
    user_id = user_field(user, "id", "N/A")
    university = metadata.get("university_name", "Not provided")
    session = metadata.get("session", "Not provided")
    subject = metadata.get("subject", "Not provided")
    initials = "".join(part[0].upper() for part in full_name.split()[:2]) or "SF"

    st.markdown(
        f"""
        <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-4">
            <div style="display:flex;align-items:center;gap:0.8rem;">
                <div style="width:48px;height:48px;border-radius:14px;background:linear-gradient(135deg,#0ea5e9 0%,#2563eb 60%,#1d4ed8 100%);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;">
                    {initials}
                </div>
                <div>
                    <h4 class="m-0">{full_name}</h4>
                    <p class="m-0 text-soft text-sm">{email}</p>
                </div>
            </div>
            <div class="mt-3" style="display:grid;grid-template-columns:1fr;gap:0.4rem;">
                <p class="m-0 text-sm"><strong>User ID:</strong> {user_id}</p>
                <p class="m-0 text-sm"><strong>University:</strong> {university}</p>
                <p class="m-0 text-sm"><strong>Session:</strong> {session}</p>
                <p class="m-0 text-sm"><strong>Department:</strong> {subject}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if include_search_history:
        st.markdown('<div class="mt-3"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-4">
                <h4 class="m-0 mb-3">Search History</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        history = st.session_state.get("search_history", [])
        if not history:
            st.caption("No searches yet. Your selected subjects and languages will appear here.")
        else:
            for item in history[:10]:
                st.markdown(
                    f"""
                    <div class="bg-card ring-panel shadow-panel tw-rounded-panel p-4 mb-4">
                        <p class="m-0"><strong>{item['query']}</strong></p>
                        <p class="m-0 text-soft text-sm">Source: {item['source']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if st.button("Clear search history", key="clear_search_history", use_container_width=True):
            st.session_state.search_history = []
            st.rerun()

    if st.button("Logout", key="profile_logout_btn", use_container_width=True):
        try:
            client.auth.sign_out()
        except Exception:
            pass
        clear_supabase_state(reset_client=True)
        st.session_state.current_view = "auth"
        st.rerun()


def render_home_page(client, user):
    _ensure_search_history_state()

    logo_col, title_col, profile_icon_col = st.columns([1, 8, 1], gap="small")

    with logo_col:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=56)
        else:
            st.markdown(
                """
                <div style="width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#06b6d4 0%,#1d4ed8 55%,#1e3a8a 100%);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.3rem;font-weight:700;box-shadow:0 10px 30px rgba(29,78,216,0.25);">
                    SF
                </div>
                """,
                unsafe_allow_html=True,
            )

    with title_col:
        st.markdown(
            """
            <h2 class="m-0 text-center" style="display:inline-block;padding:0.45rem 0.9rem;background:linear-gradient(90deg,#06b6d4 0%,#1d4ed8 60%,#1e3a8a 100%);color:#fff;border-radius:10px;">StudyFlow</h2>
            """,
            unsafe_allow_html=True,
        )

    with profile_icon_col:
        if st.button("👤 Profile", key="profile_nav_btn", use_container_width=True, help="Open profile page"):
            st.session_state.current_view = "profile"
            st.rerun()

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)

    st.markdown("### Search by Subject")
    with st.form("subject_search_form", clear_on_submit=False):
        search_query = st.text_input(
            "Type a subject or language",
            key="subject_search_query",
            placeholder="e.g. Data Structures, Operating Systems, Python",
        )
        search_submitted = st.form_submit_button("Search", use_container_width=True)

    normalized_query = search_query.strip().lower()
    matching_subjects = [item for item in ALL_SEARCHABLE_SUBJECTS if normalized_query and normalized_query in item.lower()]

    if search_submitted:
        exact_match = next((item for item in ALL_SEARCHABLE_SUBJECTS if item.lower() == normalized_query), None)
        if exact_match:
            _open_subject_from_search(exact_match)
        elif not matching_subjects:
            st.warning("No matching subject found. Try another keyword.")

    if normalized_query and matching_subjects:
        st.caption("Matching subjects")
        match_cols = st.columns(3)
        for index, subject_name in enumerate(matching_subjects[:12]):
            col = match_cols[index % 3]
            if col.button(subject_name, key=f"subject_search_match_{index}"):
                _open_subject_from_search(subject_name)

    st.markdown("### CSE Subjects")

    # Render CSE subjects as buttons
    cols = st.columns(3)
    for i, subj in enumerate(CSE_SUBJECTS):
        col = cols[i % 3]
        if col.button(subj, key=f"cse_subject_{i}"):
            st.session_state.selected_subject = subj
            st.session_state.selected_department = "CSE"
            _log_search(subj, "CSE subject")
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
                _log_search(lang, "Programming language")
                st.session_state.current_view = "subject"
                st.rerun()

        if st.button("Back to subjects"):
            st.session_state.selected_subject = None
            st.session_state.selected_language = None
            st.rerun()


def render_profile_page(client, user):
    _ensure_search_history_state()

    top_col, back_col = st.columns([6, 1], gap="small")
    with top_col:
        st.markdown(
            """
            <div class="bg-card ring-card shadow-card backdrop-blur-12 tw-rounded-card p-4">
                <h2 class="m-0">Profile</h2>
                <p class="m-0 text-soft">Your account details and activity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with back_col:
        if st.button("⬅ Home", key="back_home_from_profile", use_container_width=True):
            st.session_state.current_view = "home"
            st.rerun()

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)
    _render_profile_panel(client, user, include_search_history=True)
