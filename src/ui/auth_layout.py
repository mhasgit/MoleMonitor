"""Shared auth layout: split-panel CSS using app theme (theme constants only)."""

import base64
import io
from pathlib import Path

import streamlit as st
from PIL import Image

from src.ui import theme

# Login left-panel image: put login.png in the project's assets folder
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGIN_IMAGE_PATH = _PROJECT_ROOT / "assets" / "login.png"


def inject_auth_css() -> None:
    """Inject CSS for full-viewport split layout using theme palette. Uses theme.get_auth_base_css() then adds layout and form-only rules."""
    base = theme.get_auth_base_css()
    st.markdown(
        f"""
        <style>
        {base}
        /* Ensure entire auth view uses app background (no Streamlit default light theme) */
        [data-testid="stAppViewContainer"] {{ background: {theme.BACKGROUND} !important; }}
        [data-testid="stAppViewContainer"] section {{ background: {theme.BACKGROUND} !important; }}
        [data-testid="stAppViewContainer"] .main {{ background: {theme.BACKGROUND} !important; color: {theme.TEXT_PRIMARY} !important; }}
        /* Force Streamlit theme variables to app accent so primary buttons use teal not red */
        [data-testid="stAppViewContainer"] {{
            --primary-color: {theme.ACCENT} !important;
            --primary-color-hover: {theme.ACCENT_HOVER} !important;
        }}
        /* Remove top gap: no padding/margin above main content */
        [data-testid="stAppViewContainer"] {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stAppViewContainer"] > section {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stAppViewContainer"] section > div {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stAppViewContainer"] section > div:first-child {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stAppViewContainer"] .main > div {{ padding-top: 0 !important; margin-top: 0 !important; }}
        #stApp .block-container {{ padding-top: 0 !important; margin-top: 0 !important; }}
        .block-container {{ max-width: 100%; padding: 0 !important; padding-top: 0 !important; }}
        .main .block-container {{ padding-top: 0 !important; }}
        .main {{ padding-top: 0 !important; }}
        [data-testid="stVerticalBlock"] {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stHorizontalBlock"] {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stHorizontalBlock"] {{ margin-top: -2rem !important; }}
        div[class*="blockContainer"] {{ padding-top: 0 !important; }}
        #root .block-container {{ padding-top: 0 !important; }}
        [data-testid="column"]:nth-child(1) > div {{ padding-top: 0 !important; margin-top: 0 !important; }}
        div.st-emotion-cache-1gxm18h {{ padding-top: 0 !important; margin-top: 0 !important; }}
        div[class*="e1f1d6gn2"] {{ padding-top: 0 !important; margin-top: 0 !important; }}
        div[class*="1gxm18h"] {{ padding-top: 0 !important; margin-top: 0 !important; }}
        [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {{ width: 100%; }}
        [data-testid="column"] {{ min-height: 100vh; padding: 1.5rem 2rem !important; }}
        [data-testid="column"]:nth-child(1) {{ background: {theme.BACKGROUND}; padding: 0 !important; min-height: 100vh !important; }}
        [data-testid="column"]:nth-child(2) {{ background: {theme.BACKGROUND}; }}
        [data-testid="column"]:nth-child(2) {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 2rem !important;
        }}
        /* Right panel: use app card/surface color so login matches main app */
        [data-testid="column"]:nth-child(2) {{
            background: {theme.CARD_BG} !important;
            border-left: 1px solid {theme.ACCENT_RGBA_BORDER};
            border-radius: 0 {theme.CARD_RADIUS} {theme.CARD_RADIUS} 0;
            box-shadow: -8px 0 32px rgba(0, 0, 0, 0.25), 0 25px 50px -12px rgba(0, 0, 0, 0.4), 0 0 0 1px {theme.ACCENT_RGBA_BORDER} !important;
            padding: {theme.FORM_CARD_PADDING} !important;
        }}
        /* Center the form content within the right column */
        [data-testid="column"]:nth-child(2) > div {{
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            width: 100% !important;
        }}
        /* Force main content area on auth to use app background (no default Streamlit white) */
        [data-testid="column"]:nth-child(2) .main {{
            background: transparent !important;
        }}
        /* Form container: transparent so card shows through; narrow width for short inputs; centered */
        [data-testid="column"]:nth-child(2) .block-container {{
            max-width: 260px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            background: transparent !important;
        }}
        [data-testid="column"]:nth-child(2) .stTextInput {{
            max-width: 260px !important;
            width: 100% !important;
        }}
        [data-testid="column"]:nth-child(2) .stTextInput > div {{
            max-width: 260px !important;
        }}
        [data-testid="column"]:nth-child(2) .stTextInput input {{
            background: {theme.CARD_ALT} !important;
            color: {theme.TEXT_PRIMARY} !important;
            border-radius: 8px;
            border: 1px solid {theme.BORDER};
            max-width: 100% !important;
        }}
        [data-testid="column"]:nth-child(2) .stTextInput input::placeholder {{ color: {theme.TEXT_MUTED}; }}
        [data-testid="column"]:nth-child(2) .stTextInput input:focus {{
            border-color: {theme.ACCENT};
            box-shadow: 0 0 0 2px {theme.ACCENT};
            outline: none;
        }}
        [data-testid="column"]:nth-child(2) .stTextInput label {{ color: {theme.TEXT_PRIMARY} !important; }}
        [data-testid="column"]:nth-child(2) .stTextInput {{ margin-bottom: {theme.SPACE_LG} !important; }}
        [data-testid="column"]:nth-child(2) .stButton {{
            max-width: 260px !important;
        }}
        [data-testid="column"]:nth-child(2) .stButton > button {{
            background: {theme.CARD_BG} !important;
            color: {theme.TEXT_PRIMARY} !important;
            border: 1px solid {theme.BORDER};
            border-radius: 10px;
            width: 100%;
            font-weight: 600;
            margin-top: {theme.SPACE_SM};
            padding: 0.5rem 1rem;
            transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        [data-testid="column"]:nth-child(2) .stButton > button:hover {{
            background: {theme.CARD_ALT} !important;
            border-color: {theme.ACCENT};
        }}
        [data-testid="column"]:nth-child(2) .stButton > button:focus {{
            box-shadow: 0 0 0 2px {theme.ACCENT};
            outline: none;
        }}
        [data-testid="column"]:nth-child(2) .stButton > button[kind="primary"] {{
            background: {theme.ACCENT} !important;
            border-color: {theme.ACCENT} !important;
            color: white !important;
            border-radius: 12px;
            padding: 0.6rem 1rem;
        }}
        [data-testid="column"]:nth-child(2) .stButton > button[kind="primary"]:hover {{
            background: {theme.ACCENT_HOVER} !important;
            border-color: {theme.ACCENT_HOVER} !important;
        }}
        [data-testid="column"]:nth-child(2) .stButton > button[kind="primary"]:focus {{
            box-shadow: 0 0 0 2px {theme.ACCENT};
            outline: none;
        }}
        /* Primary button: Streamlit often uses data-testid instead of kind="primary" */
        [data-testid="column"]:nth-child(2) [data-testid="stButton"] > button[data-testid="baseButton-primary"],
        [data-testid="column"]:nth-child(2) button[data-testid="baseButton-primary"] {{
            background: {theme.ACCENT} !important;
            border-color: {theme.ACCENT} !important;
            color: white !important;
            border-radius: 12px;
            padding: 0.6rem 1rem;
        }}
        /* Global fallback: any primary button on auth screen (in case column order differs) */
        [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"] {{
            background: {theme.ACCENT} !important;
            border-color: {theme.ACCENT} !important;
            color: white !important;
        }}
        [data-testid="stAppViewContainer"] button[data-testid="baseButton-primary"]:hover {{
            background: {theme.ACCENT_HOVER} !important;
            border-color: {theme.ACCENT_HOVER} !important;
        }}
        [data-testid="column"]:nth-child(2) [data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover,
        [data-testid="column"]:nth-child(2) button[data-testid="baseButton-primary"]:hover {{
            background: {theme.ACCENT_HOVER} !important;
            border-color: {theme.ACCENT_HOVER} !important;
        }}
        [data-testid="column"]:nth-child(2) [data-testid="stButton"] > button[data-testid="baseButton-primary"]:focus,
        [data-testid="column"]:nth-child(2) button[data-testid="baseButton-primary"]:focus {{
            box-shadow: 0 0 0 2px {theme.ACCENT};
            outline: none;
        }}
        [data-testid="column"]:nth-child(2) .stCaption {{ color: {theme.TEXT_MUTED} !important; }}
        [data-testid="column"]:nth-child(2) h1, [data-testid="column"]:nth-child(2) h2, [data-testid="column"]:nth-child(2) h3, [data-testid="column"]:nth-child(2) .stMarkdown {{ color: {theme.TEXT_PRIMARY} !important; }}
        [data-testid="column"]:nth-child(2) p {{ color: {theme.TEXT_MUTED} !important; }}
        [data-testid="column"]:nth-child(2) [data-testid="stAlert"] {{
            background: {theme.CARD_ALT} !important;
            border: 1px solid {theme.BORDER} !important;
            border-radius: 10px;
            color: {theme.TEXT_PRIMARY} !important;
        }}
        .auth-eyebrow {{ color: {theme.TEXT_MUTED} !important; font-size: 0.7rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; margin-bottom: 0.25rem !important; }}
        .auth-helper {{ color: {theme.TEXT_MUTED} !important; font-size: 0.875rem !important; margin-bottom: 1rem !important; line-height: 1.5 !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_left_panel() -> None:
    """Render left panel: full-height image with overlay (gradient, headline, supporting text, feature badges)."""
    if LOGIN_IMAGE_PATH.is_file():
        try:
            img = Image.open(LOGIN_IMAGE_PATH)
            img = img.convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=90)
            b64 = base64.b64encode(buf.getvalue()).decode()
            overlay_html = (
                '<div style="position:absolute; inset:0; '
                f'background: {theme.OVERLAY_GRADIENT}; '
                'display: flex; flex-direction: column; justify-content: flex-end; padding: 2.5rem 2rem; box-sizing: border-box;">'
                f'<p style="margin:0 0 0.5rem 0; font-size: 1.75rem; font-weight: 700; color: {theme.TEXT_PRIMARY}; letter-spacing: -0.02em; line-height: 1.25;">Track mole changes over time</p>'
                f'<p style="margin:0 0 1.25rem 0; font-size: 0.95rem; color: {theme.TEXT_MUTED}; line-height: 1.5;">Upload pairs of photos, compare them, and keep a simple history in one place.</p>'
                '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem 0.75rem;">'
                f'{theme.badge_html("Photo comparison")}'
                f'{theme.badge_html("Simple reports")}'
                f'{theme.badge_html("Your data stays private")}'
                "</div>"
                "</div>"
            )
            html = (
                '<div style="position:relative; width:100%; height:100vh; min-height:100vh; overflow:hidden;">'
                f'<img src="data:image/jpeg;base64,{b64}" '
                'style="width:100%; height:100%; min-height:100vh; object-fit:cover; display:block;" alt="Login" />'
                f"{overlay_html}"
                "</div>"
            )
            st.markdown(html, unsafe_allow_html=True)
        except Exception:
            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    height: 100vh;
                    min-height: 100vh;
                    background: {theme.CARD_BG};
                    border-right: 1px solid {theme.BORDER};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 3.5rem;
                ">🩺</div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"""
            <div style="
                width: 100%;
                height: 100vh;
                min-height: 100vh; 
                background: {theme.CARD_BG};
                border-right: 1px solid {theme.BORDER};
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3.5rem;
            ">🩺</div>
            """,
            unsafe_allow_html=True,
        )

