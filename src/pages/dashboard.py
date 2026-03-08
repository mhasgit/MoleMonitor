import streamlit as st
from src.styles.load_css import load_css
load_css()

from src import config
from src.state import session_store
from src.ui import components

def render() -> None:
    st.title("Dashboard")
    st.write("Welcome to the MoleMonitor Dashboard")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.markdown('p class="card-title">Total Images</p', unsafe_allow_html=True)
        st.markdown('p class="card-value">24</p>', unsafe_allow_html=True)
        st.markdown('</div', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('p class="card-title">Moles Tracked</p', unsafe_allow_html=True)
        st.markdown('p class="card-value">12</p>', unsafe_allow_html=True)
        st.markdown('</div', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('p class="card-title">Mole Changes</p', unsafe_allow_html=True)
        st.markdown('p class="card-value">1</p>', unsafe_allow_html=True)
        st.markdown('</div', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload New Image")
    uploaded_img = st.file_uploader("Upload a skin image")
    if uploaded_img:
        st.success("Image successfuly uploaded")
    
    st.markdown('</div>', unsafe_allow_html=True)

    """with col1:
        st.metric("Mole Checks: ", "")
    with col2:
        st.metric("Changes Detected: ", "")
    with col3:
        st.metric("Latest Upload: ", "")"""

