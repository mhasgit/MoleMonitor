"""Registration page: split layout, Name/Email/Password/Phone; mock only."""

import streamlit as st

from src.ui import auth_layout


def render() -> None:
    auth_layout.inject_auth_css()
    col_left, col_right = st.columns(2)

    with col_left:
        auth_layout.render_left_panel()

    with col_right:
        st.header("MoleMonitor", anchor=False)
        st.markdown("### Create account")
        st.markdown("<br>", unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Your name", key="reg_name")
        email = st.text_input(
            "Email address",
            placeholder="user@example.com",
            key="reg_email",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="********",
            key="reg_password",
        )
        phone = st.text_input(
            "Phone number",
            placeholder="Used for password recovery",
            key="reg_phone",
        )
        st.markdown("")
        if st.button("Register", key="reg_btn", type="primary", use_container_width=True):
            if (email or "").strip() and (password or "").strip():
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = (name or email or "").strip()
                st.session_state["nav_page"] = "Dashboard"
                st.rerun()
            else:
                st.warning("Please enter at least email and password.")
        st.markdown("")
        if st.button("Already have an account? Log in", key="reg_login_link"):
            st.session_state["auth_page"] = "login"
            st.rerun()
