"""Forgot password: phone step then reset password (mock)."""

import streamlit as st
import streamlit_shadcn_ui as ui

from src.ui import auth_layout


def render() -> None:
    auth_layout.inject_auth_css()

    if "forgot_step" not in st.session_state:
        st.session_state["forgot_step"] = "phone"
    if "forgot_phone_entered" not in st.session_state:
        st.session_state["forgot_phone_entered"] = False

    col_left, col_right = st.columns(2)

    with col_left:
        auth_layout.render_left_panel()

    with col_right:
        st.header("MoleMonitor", anchor=False)
        st.markdown("### Forgot your password?")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state["forgot_step"] == "phone":
            phone = st.text_input(
                "Phone number",
                placeholder="Enter the number used for registration",
                key="forgot_phone",
            )
            st.markdown("")
            if ui.button("Continue", key="forgot_continue", variant="default"):
                if (phone or "").strip():
                    st.session_state["forgot_step"] = "reset"
                    st.session_state["forgot_phone_entered"] = True
                    st.rerun()
                else:
                    st.warning("Please enter your phone number.")
        else:
            st.info("If this number is registered, you can reset your password below.")
            new_password = st.text_input(
                "New password",
                type="password",
                placeholder="********",
                key="forgot_new_pass",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                placeholder="********",
                key="forgot_confirm_pass",
            )
            st.markdown("")
            if ui.button("Reset password", key="forgot_reset_btn", variant="default"):
                if new_password and new_password == confirm_password:
                    st.success("Password reset (mock). You can log in now.")
                    st.session_state["forgot_step"] = "phone"
                    st.session_state["auth_page"] = "login"
                    st.rerun()
                else:
                    st.warning("Passwords must match and not be empty.")
            st.markdown("")
            if ui.button("Back to Log in", key="forgot_back", variant="outline"):
                st.session_state["forgot_step"] = "phone"
                st.session_state["auth_page"] = "login"
                st.rerun()
