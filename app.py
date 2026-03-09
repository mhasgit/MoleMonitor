"""MoleMonitor entry point. Sets config, nav, and dispatches to page modules."""

import streamlit as st

from src import config
from src.db import database
from src.ui import theme
from src.pages import (
    about,
    dashboard,
    forgot_password,
    history,
    home,
    instructions,
    login,
    register,
)
from src.state import session_store


def _hide_sidebar() -> None:
    """Inject CSS to hide sidebar and collapse control when showing auth pages."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    database.init_db()
    session_store.init_history()

    # Auth state: any login lets user in (mock)
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "Demo User"
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"

    if not st.session_state["authenticated"]:
        _hide_sidebar()
        auth_page = st.session_state.get("auth_page", "login")
        if auth_page == "register":
            register.render()
        elif auth_page == "forgot":
            forgot_password.render()
        else:
            login.render()
        return

    # Main app: sidebar with SIDEBAR_PAGES only.
    # Toolbar is hidden via .streamlit/config.toml (toolbarMode = "minimal").
    # Only force sidebar and collapse control visible (no width/transform so collapse button works).
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"],
        div[data-testid="stSidebar"],
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
        [data-testid="collapsedControl"] {
            display: block !important;
            visibility: visible !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(theme.get_app_css(), unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<p class="sidebar-app-header">{config.APP_TITLE}</p>'
        '<p class="sidebar-app-subtitle">Skin change tracking</p>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown(
        '<p class="sidebar-nav-title">Navigation</p>', unsafe_allow_html=True
    )

    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "Dashboard"
    current = st.session_state["nav_page"]

    for nav_page in config.SIDEBAR_PAGES:
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
    elif page == "Image History":
        history.render()
    elif page == "Dashboard":
        dashboard.render()
    elif page == "Instructions":
        instructions.render()
    elif page == "About":
        about.render()
    else:
        home.render()


if __name__ == "__main__":
    main()
