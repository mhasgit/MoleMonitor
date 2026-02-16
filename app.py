"""MoleMonitor entry point. Sets config, nav, and dispatches to page modules."""

import streamlit as st

from src import config
from src.db import database
from src.pages import about, forgot_password, history, home, instructions, login, register
from src.state import session_store


def main() -> None:
    st.set_page_config(page_title=config.APP_TITLE, page_icon=config.PAGE_ICON)
    database.init_db()
    session_store.init_history()

    page = st.sidebar.radio("Navigate", config.NAV_PAGES, key="nav")

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
