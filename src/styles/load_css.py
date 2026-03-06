import streamlit as st
from pathlib import Path

def load_css():
    css_path = Path(__file__).parent / "globalstyle.css"

    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"CSS file not found: {css_path}")


"""import streamlit as st
from pathlib import Path

def load_css():
    css_path = Path("src/styles/globalstyle.css")

    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style", unsafe_allow_html= True)"""