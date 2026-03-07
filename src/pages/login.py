"""Login page. To be implemented."""

import streamlit as st


def render():
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.markdown('<div class="login-left">', unsafe_allow_html=True)
        st.image("src/images/placeholder.jpg", use_container_width=True)

        st.markdown(
            "<h2 class='hero-title'>MoleMonitor: Tracking your moles.</h2>", unsafe_allow_html=True
        )
        st.markdown("<p class='hero-text'>Track changes to your skin moles over time.</p>", unsafe_allow_html=True
                    )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="login-right">', unsafe_allow_html=True)
        st.markdown("<h3>Log in</h3>", unsafe_allow_html=True)
        email = st.text_input("Email Adress", placeholder="user@example.com")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="********",
        )
        if st.button("Log in"):
            st.success("Login Attempted")
        st.markdown("p class='forgot'>Forgot Password?</p>", unsafe_allow_html=True)
        st.markdown("/div", unsafe_allow_html=True)
        
        
        
        
        """st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Login")
        
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):
            st.success("Login Attempted")

        st.markdown("[Forgot Password?](#)")
        st.markdown("Create an account")

        st.markdown('</div>', unsafe_allow_html=True)
        st.image("src/images/placeholder.jpg", use_container_width=True)"""