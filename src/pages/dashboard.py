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
        st.metric("Mole Checks: ", "")
    with col2:
        st.metric("Changes Detected: ", "")
    with col3:
        st.metric("Latest Upload: ", "")

