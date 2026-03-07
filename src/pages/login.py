"""Login page. To be implemented."""

import streamlit as st


def render():
    col1, col2 = st.columns([1,1])
    with col1:
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):
            st.success("Login Attempted")

        st.markdown("Forgot Password?")
        st.markdown("Create an account")

