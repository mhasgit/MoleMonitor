"""Login page: split layout, mock login (any credentials let user in)."""

import streamlit as st
import streamlit_shadcn_ui as ui

from src.ui import auth_layout


def render() -> None:
    auth_layout.inject_auth_css()
    # Half image, half form (50/50). Form content stays narrow via auth_layout CSS.
    col_left, col_right = st.columns(2)

    with col_left:
        auth_layout.render_left_panel()

    with col_right:
        st.header("MoleMonitor", anchor=False)
        st.markdown("### Log in")
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input(
            "Email address",
            placeholder="user@example.com",
            key="login_email",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="********",
            key="login_password",
        )
        st.markdown("")
        if ui.button("Log in", key="login_btn", variant="default"):
            if (email or "").strip() and (password or "").strip():
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = (email or "").strip()
                st.session_state["nav_page"] = "Dashboard"
                st.rerun()
            else:
                st.warning("Please enter email and password.")
        st.markdown("")
        if ui.button("Forgot your password?", key="login_forgot_link", variant="outline"):
            st.session_state["auth_page"] = "forgot"
            st.rerun()
        st.markdown("")
        if ui.button("Don't have an account? Register", key="login_register_link", variant="outline"):
            st.session_state["auth_page"] = "register"
            st.rerun()
