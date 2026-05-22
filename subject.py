import streamlit as st
from auth_common import user_field
from resources import get_resources_for, make_search_link
from urllib.parse import quote_plus


def _link(name, site=None):
    # return a tuple (display, url)
    if site == "youtube":
        return name, make_search_link(name, site="youtube")
    return name, make_search_link(name, site="google")


def render_subject_page(client):
    """Render subject detail page showing curated resources."""
    subject = st.session_state.get("selected_subject") or st.session_state.get("selected_language")
    department = st.session_state.get("selected_department")

    if not subject:
        st.warning("No subject selected.")
        if st.button("Back to home"):
            st.session_state.current_view = "home"
            st.rerun()
        return

    st.markdown(
        f"""
        <div class="bg-hero shadow-hero tw-rounded-hero p-6 text-white mb-6">
            <h1 class="m-0 text-3xl leading-tight font-semibold">{subject}</h1>
            <p class="mt-2 text-base opacity-90">Department: {department or 'N/A'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    resources = get_resources_for(subject)

    # helper to render anchor as button
    def render_button(label, url):
        href = url.replace('"', '%22')
        btn = f'<a href="{href}" target="_blank" rel="noopener" style="display:inline-block;padding:8px 12px;margin:6px;border-radius:8px;background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%);color:#fff;text-decoration:none;font-weight:600;">{label}</a>'
        st.markdown(btn, unsafe_allow_html=True)

    # If user arrived by selecting a specific language, show category buttons first
    is_language = bool(st.session_state.get("selected_language"))
    selected_category = st.session_state.get("resource_category")

    if is_language and not selected_category:
        st.markdown('<div class="mt-2"></div>', unsafe_allow_html=True)
        st.markdown("**Choose a resource type**")
        c1, c2, c3 = st.columns(3)
        if c1.button("YouTube"):
            st.session_state.resource_category = "youtube"
            st.rerun()
        if c2.button("Books"):
            st.session_state.resource_category = "books"
            st.rerun()
        if c3.button("Blogs"):
            st.session_state.resource_category = "blogs"
            st.rerun()

        st.markdown('<div class="mt-2"></div>', unsafe_allow_html=True)
        if st.button("Back to subjects"):
            # clear language and category state
            st.session_state.selected_language = None
            st.session_state.resource_category = None
            st.session_state.current_view = "home"
            st.rerun()

        return

    # If a category is selected (either from language-page or general subject page), show those resources
    if selected_category:
        st.markdown('<div class="mt-2"></div>', unsafe_allow_html=True)
        cat = selected_category
        items = []
        if resources:
            items = resources.get(cat, [])

        if not items:
            # fallback to search link
            if cat == "youtube":
                render_button(f"Search {subject} on YouTube", make_search_link(subject, site="youtube"))
            else:
                render_button(f"Search {subject}", make_search_link(subject))
        else:
            for name in items:
                _, url = _link(name, site=("youtube" if cat == "youtube" else None))
                render_button(name, url)

        st.markdown('<div class="mt-3"></div>', unsafe_allow_html=True)
        if st.button("Back to resource types"):
            st.session_state.resource_category = None
            st.rerun()

        if st.button("Back to home"):
            st.session_state.current_view = "home"
            st.session_state.selected_subject = None
            st.session_state.selected_language = None
            st.session_state.resource_category = None
            st.rerun()

        return

    # Default: show all categories for non-language subjects
    if not resources:
        st.info("No curated resources available for this subject yet. Here are search results you can try:")
        st.markdown(f"- YouTube: [{subject}]({make_search_link(subject, site='youtube')})")
        st.markdown(f"- Web search: [{subject}]({make_search_link(subject)})")
        return

    st.markdown('<div class="mt-2"></div>', unsafe_allow_html=True)

    # YouTube channels / playlists
    yts = resources.get("youtube", [])
    if yts:
        st.markdown("**YouTube channels / playlists**")
        for name in yts:
            _, url = _link(name, site="youtube")
            render_button(name, url)

    # Books
    books = resources.get("books", [])
    if books:
        st.markdown("**Books**")
        for name in books:
            _, url = _link(name + " book")
            render_button(name, url)

    # Blogs
    blogs = resources.get("blogs", [])
    if blogs:
        st.markdown("**Blogs / Articles**")
        for name in blogs:
            _, url = _link(name)
            render_button(name, url)

    st.markdown('<div class="mt-4"></div>', unsafe_allow_html=True)
    if st.button("Back to home"):
        st.session_state.current_view = "home"
        st.rerun()
