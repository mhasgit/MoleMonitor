"""MoleMonitor entry point. Sets config, nav, and dispatches to page modules."""

import streamlit as st

from src import config
from src.db import database
from src.pages import about, forgot_password, history, home, instructions, login, register, dashboard
from src.state import session_store


def main() -> None:
    st.set_page_config(page_title=config.APP_TITLE, page_icon=config.PAGE_ICON)
    database.init_db()
    session_store.init_history()

    # Sidebar: app header and nav as proper buttons
    st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebar"] .sidebar-app-header {
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }
        [data-testid="stSidebar"] .sidebar-nav-title {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            opacity: 0.85;
            margin-bottom: 0.5rem;
            padding-left: 0.25rem;
        }
        /* Nav buttons: full width, block style */
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            justify-content: flex-start;
            padding: 0.5rem 0.85rem;
            font-weight: 500;
            border-radius: 0.5rem;
            transition: background-color 0.2s ease, box-shadow 0.15s ease;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f'<p class="sidebar-app-header">{config.APP_TITLE}</p>',
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    st.sidebar.markdown('<p class="sidebar-nav-title">Navigation</p>', unsafe_allow_html=True)

    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "Home"
    current = st.session_state["nav_page"]

    for nav_page in config.NAV_PAGES:
        is_active = nav_page == current
        label = f"► {nav_page}" if is_active else nav_page
        if st.sidebar.button(
            label,
            key=f"nav_{nav_page}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            if not is_active:
                st.session_state["nav_page"] = nav_page
                st.rerun()

    page = st.session_state["nav_page"]

    if page == "Home":
        home.render()
    elif page == "Register":
        register.render()
    elif page == "Login":
        login.render()
    elif page == "Forgot Password":
        forgot_password.render()
    elif page == "Instructions":
        instructions.render()
    elif page == "Image History":
        history.render()
    elif page == "About":
        about.render()
    else:
        home.render()


if __name__ == "__main__":
    main()
