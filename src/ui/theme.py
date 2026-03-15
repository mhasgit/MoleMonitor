"""
Global theme: Slate + Teal palette (Option A).
Centralizes palette, global CSS, and reusable HTML/Streamlit helpers.
Uses streamlit-extras for metric card styling and grid layouts where applicable.
"""

import streamlit as st

try:
    from streamlit_extras.metric_cards import style_metric_cards
    from streamlit_extras.grid import grid
except ImportError:
    style_metric_cards = None
    grid = None

# Palette: Option A — Slate + Teal (clinical, health-friendly)
BACKGROUND = "#0F1419"
CONTENT_BG_1 = "#1A2234"
CONTENT_BG_2 = "#1E293B"
SIDEBAR_BG = "#0C1015"
CARD_BG = "#1A2234"
CARD_ALT = "#1E293B"
ACCENT = "#0D9488"
ACCENT_HOVER = "#14B8A6"
BORDER = "#334155"
# More visible border for history list rows (slate-500)
HISTORY_ROW_BORDER = "#64748B"
TEXT_PRIMARY = "#F1F5F9"
TEXT_MUTED = "#94A3B8"
TEXT_SECONDARY = TEXT_MUTED  # alias

# Accent tint for badges and form card border (teal 0D9488)
ACCENT_RGBA_BORDER = "rgba(13, 148, 136, 0.35)"
ACCENT_RGBA_BG = "rgba(13, 148, 136, 0.2)"
ACCENT_GLOW = "rgba(13, 148, 136, 0.3)"
# Auth left panel overlay gradient (BACKGROUND #0F1419 = 15,20,25)
OVERLAY_GRADIENT = "linear-gradient(180deg, rgba(15,20,25,0.3) 0%, rgba(15,20,25,0.75) 50%, rgba(15,20,25,0.92) 100%)"

# Soft dark shadow for cards; stronger for elevated (neutral, no purple)
CARD_SHADOW = "0 6px 28px rgba(0, 0, 0, 0.35)"
CARD_SHADOW_ELEVATED = "0 8px 32px rgba(0, 0, 0, 0.4)"
CARD_RADIUS = "20px"
CARD_RADIUS_LARGE = "24px"
CARD_PADDING = "1.5rem 1.75rem"
FORM_CARD_PADDING = "2rem 2.5rem"

# Spacing scale (use in CSS and helpers)
SPACE_XS = "0.25rem"
SPACE_SM = "0.5rem"
SPACE_MD = "0.75rem"
SPACE_LG = "1rem"
SPACE_XL = "1.5rem"
PAGE_CONTAINER_TOP = "2rem"
PAGE_CONTAINER_BOTTOM = "2rem"
SECTION_GAP = "1.25rem"


def get_app_css() -> str:
    """Global CSS for main app (main area + sidebar). Inject once when authenticated."""
    return _build_app_css()


def get_auth_base_css() -> str:
    """Base CSS fragment for auth pages: hide header/toolbar, root, and app background. Auth layout injects this then adds layout and form rules."""
    return f"""
    /* Hide Streamlit header, toolbar, decoration */
    header {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    #stApp header {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    [data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    header[data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; z-index: -9999 !important; }}
    div[data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    [data-testid="stToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; position: fixed !important; top: -999px !important; }}
    [data-testid="stAppToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; visibility: hidden !important; height: 0 !important; }}
    #MainMenu {{ display: none !important; visibility: hidden !important; }}
    button[title="View fullscreen"] {{ display: none !important; }}
    button[kind="header"] {{ display: none !important; }}
    div[data-testid="StyledLinkIconContainer"] > a:first-child {{ display: none !important; }}
    h1 > div > a, h2 > div > a, h3 > div > a, h4 > div > a, h5 > div > a, h6 > div > a {{ display: none !important; }}
    [data-testid="stAppViewContainer"] > section {{ background: {BACKGROUND} !important; }}
    """


def inject_global_css() -> None:
    """Inject global theme CSS. Call when you need to render theme CSS (e.g. authenticated app)."""
    st.markdown(get_app_css(), unsafe_allow_html=True)


def _build_app_css() -> str:
    """Build the full app CSS string using current palette."""
    return f"""
    <style>
    /* Normalize zoom/scale after Streamlit update */
    #root, [data-testid="stAppViewContainer"] {{ font-size: 16px; }}
    .main .block-container {{ font-size: 1rem; }}
    /* Hide Streamlit header, toolbar, decoration - multiple selectors for different versions */
    header {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    #stApp header {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    [data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    header[data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; z-index: -9999 !important; }}
    div[data-testid="stHeader"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    [data-testid="stToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }}
    div[data-testid="stToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; position: fixed !important; top: -999px !important; }}
    [data-testid="stAppToolbar"] {{ display: none !important; visibility: hidden !important; height: 0 !important; }}
    div[data-testid="stDecoration"] {{ display: none !important; visibility: hidden !important; height: 0 !important; }}
    #MainMenu {{ display: none !important; visibility: hidden !important; }}
    button[title="View fullscreen"] {{ display: none !important; }}
    button[kind="header"] {{ display: none !important; }}
    /* Hide anchor/link icon next to headings (e.g. next to "MoleMo") */
    div[data-testid="StyledLinkIconContainer"] > a:first-child {{ display: none !important; }}
    h1 > div > a, h2 > div > a, h3 > div > a, h4 > div > a, h5 > div > a, h6 > div > a {{ display: none !important; }}
    /* Main app background and content width - fixed max-width so sidebar stays visible */
    [data-testid="stAppViewContainer"] > section {{ background: {BACKGROUND} !important; }}
    .main .block-container {{ padding-top: {PAGE_CONTAINER_TOP}; padding-bottom: {PAGE_CONTAINER_BOTTOM}; max-width: 1100px; }}
    .main {{ max-width: 100%; }}
    /* Sidebar: visible when main app runs; do not force width/transform so collapse toggle works */
    section[data-testid="stSidebar"],
    div[data-testid="stSidebar"],
    [data-testid="stAppViewContainer"] ~ section[data-testid="stSidebar"],
    [data-testid="stAppViewContainer"] + section[data-testid="stSidebar"] {{
        display: block !important;
        visibility: visible !important;
        background: {SIDEBAR_BG} !important;
        border-right: 1px solid {BORDER};
        overflow: visible !important;
        position: relative !important;
    }}
    /* Sidebar collapse/expand control: on the right edge of the sidebar, not inset */
    [data-testid="collapsedControl"],
    div[data-testid="collapsedControl"],
    button[data-testid="collapsedControl"] {{
        z-index: 9999 !important;
        position: absolute !important;
        right: 0 !important;
        top: 0.5rem !important;
        min-width: 2.5rem !important;
        overflow: visible !important;
        visibility: visible !important;
        display: block !important;
        margin: 0 !important;
    }}
    section[data-testid="stSidebar"] .sidebar-app-header,
    div[data-testid="stSidebar"] .sidebar-app-header {{
        color: {TEXT_PRIMARY};
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
    }}
    section[data-testid="stSidebar"] .sidebar-app-subtitle,
    div[data-testid="stSidebar"] .sidebar-app-subtitle {{
        color: {TEXT_MUTED};
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        margin-bottom: 1.25rem;
        display: block;
    }}
    section[data-testid="stSidebar"] .sidebar-nav-title,
    div[data-testid="stSidebar"] .sidebar-nav-title {{
        color: {TEXT_MUTED};
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        padding-left: 0.25rem;
    }}
    section[data-testid="stSidebar"] .stMarkdown,
    div[data-testid="stSidebar"] .stMarkdown {{ color: {TEXT_PRIMARY}; }}
    section[data-testid="stSidebar"] .stButton > button,
    div[data-testid="stSidebar"] .stButton > button {{
        color: {TEXT_PRIMARY} !important;
        background: transparent !important;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.35rem;
        font-weight: 500;
        justify-content: flex-start;
        width: 100%;
        transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover,
    div[data-testid="stSidebar"] .stButton > button:hover {{
        background: {CARD_BG} !important;
        border-color: {BORDER};
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    div[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: {ACCENT} !important;
        border-color: {ACCENT};
        color: white !important;
        box-shadow: 0 2px 12px {ACCENT_GLOW};
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    div[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
        background: {ACCENT_HOVER} !important;
        border-color: {ACCENT_HOVER};
        box-shadow: 0 4px 16px {ACCENT_GLOW};
    }}
    section[data-testid="stSidebar"] [data-testid="stButton"] > button[data-testid="baseButton-primary"],
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"],
    div[data-testid="stSidebar"] [data-testid="stButton"] > button[data-testid="baseButton-primary"],
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {{
        background: {ACCENT} !important;
        border-color: {ACCENT};
        color: white !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover,
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover,
    div[data-testid="stSidebar"] [data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover,
    div[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {{
        background: {ACCENT_HOVER} !important;
        border-color: {ACCENT_HOVER};
    }}
    /* Main content text and typography hierarchy */
    .main h1, .main h2, .main h3, .main .stMarkdown {{ color: {TEXT_PRIMARY} !important; }}
    .main h1 {{ font-size: 1.85rem !important; font-weight: 700 !important; letter-spacing: -0.02em; margin-bottom: 0.5rem; }}
    .main h2 {{ font-size: 1.3rem !important; font-weight: 600 !important; margin-top: 1.25rem; margin-bottom: 0.5rem; }}
    .main h3 {{ font-size: 1.1rem !important; font-weight: 600 !important; }}
    .main p, .main .stCaption {{ color: {TEXT_MUTED} !important; line-height: 1.55; }}
    .main p {{ font-size: 0.95rem; }}
    .main .stCaption {{ font-size: 0.85rem; color: {TEXT_MUTED} !important; }}
    .main hr {{ border-color: {BORDER} !important; }}
    /* Global card styling: depth, shape, spacing. Use .mm-card, .mm-stat-card, .mm-card-empty, .mm-card-cta */
    .main .mm-card, .main .mm-stat-card {{
        border-radius: {CARD_RADIUS};
        border: 1px solid {BORDER};
        box-shadow: {CARD_SHADOW};
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
        margin-top: {SECTION_GAP} !important;
        margin-bottom: {SECTION_GAP} !important;
    }}
    .main .mm-card:hover, .main .mm-stat-card:hover {{
        box-shadow: {CARD_SHADOW_ELEVATED};
        border-color: {BORDER};
    }}
    .main .mm-card-empty {{
        border: 1px dashed {BORDER};
        border-radius: {CARD_RADIUS};
        background: {CARD_ALT};
    }}
    .main .mm-card-cta {{
        text-align: center;
    }}
    .main .mm-card {{
        background: {CARD_BG};
        padding: {CARD_PADDING};
        min-height: 100px;
    }}
    .main .mm-card.mm-card-alt {{
        background: {CARD_ALT};
    }}
    .main .mm-stat-card {{
        background: {CARD_BG};
        padding: 1.25rem 1.5rem;
        min-height: 130px;
    }}
    .main .mm-card.mm-card-accent-left {{
        border-left: 4px solid {ACCENT};
    }}
    /* Uniform-height cards (e.g. instructions tip row) */
    .main .mm-card-uniform {{
        min-height: 200px;
        display: flex !important;
        flex-direction: column !important;
    }}
    .main .mm-card-uniform .mm-card-body {{
        flex: 1;
        display: flex;
        flex-direction: column;
    }}
    /* Metrics */
    [data-testid="stMetric"] label {{ color: {TEXT_MUTED} !important; }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {TEXT_PRIMARY} !important; }}
    [data-testid="stMetric"] div[data-testid="stMetricDelta"] {{ color: {TEXT_MUTED} !important; }}
    .main [data-testid="stMetric"] {{ min-height: 130px; display: flex; flex-direction: column; justify-content: flex-start; margin-top: {SECTION_GAP} !important; margin-bottom: {SECTION_GAP} !important; }}
    /* Expander, inputs, file uploader */
    .main .streamlit-expanderHeader {{ color: {TEXT_PRIMARY} !important; }}
    .main .stTextInput label, .main .stFileUploader label {{ color: {TEXT_PRIMARY} !important; }}
    .main .stSelectbox label {{ color: {TEXT_PRIMARY} !important; }}
    /* Alerts */
    .main [data-testid="stAlert"] {{ background: {CARD_BG} !important; border: 1px solid {BORDER}; border-radius: 10px; }}
    /* Buttons in main: primary = accent, rounded, clearly clickable */
    .main .stButton > button {{
        background: {CARD_BG} !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .main .stButton > button:hover {{
        background: {CARD_ALT} !important;
        border-color: {ACCENT};
    }}
    .main .stButton > button:focus {{
        box-shadow: 0 0 0 2px {ACCENT};
    }}
    .main .stButton > button[kind="primary"] {{
        background: {ACCENT} !important;
        border-color: {ACCENT};
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
    }}
    .main .stButton > button[kind="primary"]:hover {{
        background: {ACCENT_HOVER} !important;
        border-color: {ACCENT_HOVER};
        box-shadow: 0 4px 14px {ACCENT_GLOW};
    }}
    /* Primary button fallback for Streamlit versions that use data-testid instead of kind */
    .main [data-testid="stButton"] > button[data-testid="baseButton-primary"],
    .main button[data-testid="baseButton-primary"] {{
        background: {ACCENT} !important;
        border-color: {ACCENT} !important;
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
    }}
    .main [data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover,
    .main button[data-testid="baseButton-primary"]:hover {{
        background: {ACCENT_HOVER} !important;
        border-color: {ACCENT_HOVER} !important;
        box-shadow: 0 4px 14px {ACCENT_GLOW};
    }}
    /* Images: rounded corners (thumbnails and previews) */
    .main .stImage img {{ border-radius: 8px; overflow: hidden; }}
    .main [data-testid="stImage"] img {{ border-radius: 8px !important; }}
    /* History list: form-based rows – visible border on each form container */
    .main [data-testid="stForm"] {{
        border: 2px solid {HISTORY_ROW_BORDER} !important;
        border-left: 4px solid {ACCENT} !important;
        background: {CARD_BG} !important;
        border-radius: {CARD_RADIUS};
        padding: 1.5rem !important;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
        box-shadow: {CARD_SHADOW};
    }}
    .main [data-testid="stForm"] .stButton > button {{
        white-space: nowrap !important;
    }}
    /* Legacy history row selectors (kept for non-form fallback) */
    /* History list: one horizontal card per row (mm-row-card marker + next block)
       Target next sibling with * so border applies even if Streamlit wraps in an extra div. */
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"],
    .main .mm-row-card + [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"],
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
    .main [data-testid="stVerticalBlock"] > [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stHorizontalBlock"],
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + * {{
        background: {CARD_BG} !important;
        border: 2px solid {HISTORY_ROW_BORDER} !important;
        border-left: 4px solid {ACCENT} !important;
        border-radius: {CARD_RADIUS};
        box-shadow: {CARD_SHADOW};
        padding: 1.25rem 1.5rem;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
        min-height: 100px;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    /* When the next sibling is a wrapper div, style the inner horizontal block so it has the card look */
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] {{
        background: {CARD_BG} !important;
        border: 2px solid {HISTORY_ROW_BORDER} !important;
        border-left: 4px solid {ACCENT} !important;
        border-radius: {CARD_RADIUS};
        box-shadow: {CARD_SHADOW};
        padding: 1.25rem 1.5rem;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
        min-height: 100px;
    }}
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 0;
    }}
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stHorizontalBlock"]:hover,
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"]:hover,
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"]:hover,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:hover,
    .main [data-testid="stVerticalBlock"] > [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stHorizontalBlock"]:hover,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + *:hover {{
        box-shadow: {CARD_SHADOW_ELEVATED};
        border-left-color: {ACCENT_HOVER} !important;
    }}
    /* History row: prevent "View Report" button text from wrapping */
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stHorizontalBlock"] .stButton > button,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] .stButton > button,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + * .stButton > button {{
        white-space: nowrap !important;
    }}
    /* History row: vertical center for button column (with wrapper fallback) */
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child,
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] [data-testid="column"]:last-child {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    /* History row: constrain thumbnail size (with wrapper fallback) */
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child img,
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child img,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child img {{
        width: 64px !important;
        height: 48px !important;
        max-width: 64px !important;
        max-height: 48px !important;
        object-fit: cover !important;
        display: block !important;
    }}
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"],
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"],
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"] {{
        width: 64px !important;
        height: 48px !important;
        overflow: hidden !important;
    }}
    .main .stMarkdown:has(.mm-row-card) + [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"] img,
    .main .stMarkdown:has(.mm-row-card) + div [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"] img,
    .main [data-testid="stMarkdown"]:has(.mm-row-card) + [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child [data-testid="stImage"] img {{
        width: 64px !important;
        height: 48px !important;
        max-width: 64px !important;
        max-height: 48px !important;
        object-fit: cover !important;
    }}
    /* Report modal (st.dialog) content: section spacing, bold headings, emphasized final result */
    [data-testid="stDialog"] {{
        background: {BACKGROUND} !important;
        border-radius: {CARD_RADIUS};
        border: 1px solid {BORDER};
        box-shadow: {CARD_SHADOW_ELEVATED};
    }}
    [data-testid="stDialog"] .stMarkdown:first-of-type p,
    [data-testid="stDialog"] .stMarkdown h1,
    [data-testid="stDialog"] .stMarkdown h2 {{
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: {TEXT_PRIMARY} !important;
        margin-bottom: 0.75rem !important;
    }}
    [data-testid="stDialog"] .stMarkdown {{ margin-bottom: 1.25rem; }}
    [data-testid="stDialog"] .stMarkdown p {{ margin-bottom: 0.5rem; }}
    [data-testid="stDialog"] .stButton > button {{ border-radius: 12px; font-weight: 600; padding: 0.5rem 1.25rem; }}
    /* Expander: theme-consistent */
    .main .streamlit-expanderHeader {{ border-radius: 8px; }}
    .main [data-testid="stExpander"] {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }}
    /* Home page: upload and preview blocks as cards; upload zone hover */
    .main .stMarkdown:has(.mm-home-upload-sentinel) + [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-home-preview-sentinel) + [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-home-upload-sentinel) + div [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-home-preview-sentinel) + div [data-testid="stHorizontalBlock"] {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: {CARD_RADIUS};
        box-shadow: {CARD_SHADOW};
        padding: 1.25rem 1.5rem;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .main .stMarkdown:has(.mm-home-upload-sentinel) + [data-testid="stHorizontalBlock"]:hover,
    .main .stMarkdown:has(.mm-home-upload-sentinel) + div [data-testid="stHorizontalBlock"]:hover {{
        border-color: {BORDER};
        box-shadow: {CARD_SHADOW_ELEVATED};
    }}
    /* Home: select from uploads card */
    .main .stMarkdown:has(.mm-home-select-sentinel) + [data-testid="stHorizontalBlock"],
    .main .stMarkdown:has(.mm-home-select-sentinel) + div [data-testid="stHorizontalBlock"] {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: {CARD_RADIUS};
        box-shadow: {CARD_SHADOW};
        padding: 1.25rem 1.5rem;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
    }}
    /* Home: action card (label + save) */
    .main .stMarkdown:has(.mm-home-action-sentinel) + [data-testid="stVerticalBlock"],
    .main .stMarkdown:has(.mm-home-action-sentinel) + div [data-testid="stVerticalBlock"] {{
        background: {CARD_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: {CARD_RADIUS};
        box-shadow: {CARD_SHADOW};
        padding: 1.25rem 1.5rem;
        margin-top: {SECTION_GAP};
        margin-bottom: {SECTION_GAP};
    }}
    </style>
    """


def page_header(title: str, subtitle: str | None = None, eyebrow: str | None = None) -> None:
    """Render a page title with optional eyebrow and subtitle. Uses Streamlit elements."""
    if eyebrow:
        st.markdown(
            f'<p style="color: {TEXT_MUTED}; font-size: 0.7rem; font-weight: 600; '
            'text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.35rem;">'
            f"{eyebrow}</p>",
            unsafe_allow_html=True,
        )
    st.title(title)
    if subtitle:
        st.caption(subtitle)
        st.markdown("<br>", unsafe_allow_html=True)


def section_label(text: str) -> None:
    """Render a small uppercase muted label above a section. Alias for section_subtitle."""
    section_subtitle(text)


def section_subtitle(text: str) -> None:
    """Render a small uppercase muted label above a section."""
    st.markdown(
        f'<p style="color: {TEXT_MUTED}; font-size: 0.75rem; font-weight: 600; '
        'text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">'
        f"{text}</p>",
        unsafe_allow_html=True,
    )


def card_html(
    title: str,
    content_html: str,
    icon: str = "",
    variant: str = "default",
    uniform_height: bool = False,
    accent_left: bool = False,
) -> str:
    """Return HTML for a card. variant: 'default' (CARD_BG) or 'alt' (CARD_ALT). uniform_height: use min-height and flex for equal-height layout. accent_left: teal left border like dashboard metric cards. Styling from global .mm-card CSS."""
    icon_part = f'<span style="font-size:1.25rem; margin-right:0.4rem;">{icon}</span>' if icon else ""
    extra_class = " mm-card-uniform" if uniform_height else ""
    alt_class = " mm-card-alt" if variant == "alt" else ""
    accent_class = " mm-card-accent-left" if accent_left else ""
    return f"""
    <div style="margin-top: {SECTION_GAP}; margin-bottom: {SECTION_GAP}; width: 100%;">
    <div class="mm-card{extra_class}{alt_class}{accent_class}" style="height: 100%; width: 100%;">
        <div style="color: {TEXT_MUTED}; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem;">
            {icon_part}{title}
        </div>
        <div class="mm-card-body" style="color: {TEXT_PRIMARY}; line-height: 1.55;">
            {content_html}
        </div>
    </div>
    </div>
    """


def feature_card(
    title: str,
    content_html: str,
    icon: str = "",
    variant: str = "default",
) -> str:
    """Return HTML for a feature card. variant: 'default' (CARD_BG) or 'elevated' (CARD_ALT, stronger shadow)."""
    if variant == "elevated":
        return card_html(title, content_html, icon=icon, variant="alt")
    return card_html(title, content_html, icon=icon, variant=variant)


def stat_card_html(
    label: str,
    value: str | int,
    sublabel: str | None = None,
    icon: str = "",
) -> str:
    """Return HTML for a stat/metric card: value prominent, label and sublabel muted. Styling from global .mm-stat-card CSS."""
    icon_part = f'<span style="font-size:1.25rem; margin-right:0.4rem;">{icon}</span>' if icon else ""
    sublabel_html = f'<p style="margin:0.25rem 0 0 0; font-size:0.8rem; color: {TEXT_MUTED};">{sublabel}</p>' if sublabel else ""
    return f"""
    <div style="margin-top: {SECTION_GAP}; margin-bottom: {SECTION_GAP};">
    <div class="mm-stat-card">
        <div style="color: {TEXT_MUTED}; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;">
            {icon_part}{label}
        </div>
        <p style="margin:0.5rem 0 0 0; font-size:1.85rem; font-weight: 700; color: {TEXT_PRIMARY};">{value}</p>
        {sublabel_html}
    </div>
    </div>
    """


def report_section_html(title: str, content: str) -> str:
    """Return HTML for a report section with bold heading and spacing."""
    return f"""
    <div style="margin-bottom: 1.25rem;">
        <div style="color: {TEXT_MUTED}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.35rem;">{title}</div>
        <div style="color: {TEXT_PRIMARY}; font-size: 0.95rem; line-height: 1.5;">{content}</div>
    </div>
    """


def report_final_result_html(result_text: str) -> str:
    """Return HTML for the highlighted Final result section in the report modal."""
    return f"""
    <div style="
        margin-top: 1.25rem;
        padding: 1.25rem 1.5rem;
        background: {CARD_ALT};
        border: 2px solid {ACCENT};
        border-radius: 12px;
        box-shadow: 0 4px 16px {ACCENT_GLOW};
    ">
        <div style="color: {TEXT_MUTED}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">Final result</div>
        <div style="color: {ACCENT}; font-size: 1.15rem; font-weight: 700;">{result_text}</div>
    </div>
    """


def empty_placeholder_html(message: str) -> str:
    """Return HTML for an empty-state placeholder (e.g. no history, no image). Uses .mm-card.mm-card-empty for consistent look."""
    return f"""
    <div class="mm-card mm-card-empty" style="
        padding: 2rem;
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 0.95rem;
        line-height: 1.5;
    ">{message}</div>
    """


def empty_state(message: str) -> str:
    """Return HTML for an empty-state placeholder. Alias for empty_placeholder_html."""
    return empty_placeholder_html(message)


def instruction_tip_card_html(title: str, content_html: str, icon: str = "", variant: str = "default") -> str:
    """Return HTML for an instruction tip card with a large, bold, bordered and padded heading. All cards use the same min-height for a uniform row."""
    icon_part = f'<span style="font-size:1.2rem; margin-right:0.5rem;">{icon}</span>' if icon else ""
    bg = CARD_ALT if variant == "alt" else CARD_BG
    min_h = "310px"  # fixed height so all instruction cards are exactly the same length
    return f"""
    <div style="margin-top: {SECTION_GAP}; margin-bottom: {SECTION_GAP}; width: 100%; height: 100%;">
    <div class="mm-card mm-card-uniform" style="
        height: {min_h}; min-height: {min_h}; width: 100%;
        background: {bg};
        border: 2px solid {HISTORY_ROW_BORDER};
        border-radius: {CARD_RADIUS};
        padding: {CARD_PADDING};
        display: flex; flex-direction: column;
    ">
        <div style="
            color: {TEXT_PRIMARY};
            font-size: 1.15rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.75rem;
            border: 2px solid {BORDER};
            border-radius: 10px;
            padding: 0.75rem 1rem;
            background: {CARD_BG};
            flex-shrink: 0;
        ">
            {icon_part}{title}
        </div>
        <div class="mm-card-body" style="color: {TEXT_PRIMARY}; font-size: 1.05rem; line-height: 1.6; flex: 1; display: flex; flex-direction: column;">
            {content_html}
        </div>
    </div>
    </div>
    """


def disclaimer_card_html(title: str, body_html: str) -> str:
    """Return HTML for a disclaimer card (accent border, prominent title). Uses theme card classes with internal padding."""
    return f"""
    <div class="mm-card mm-card-alt" style="border: 2px solid {ACCENT}; border-radius: 10px; padding: {CARD_PADDING};">
        <p style="margin:0 0 0.5rem 0; font-weight: 700; font-size: 1.1rem; color: {TEXT_PRIMARY};">{title}</p>
        <div style="font-size: 0.95rem; color: {TEXT_MUTED}; line-height: 1.55;">{body_html}</div>
    </div>
    """


def cta_card_html(message: str) -> str:
    """Return HTML for a CTA card (centered message, e.g. above a button). Uses theme card classes."""
    return f"""
    <div class="mm-card mm-card-cta">
        <p style="margin:0 0 1rem 0; font-size: 0.95rem; color: {TEXT_MUTED}; line-height: 1.5;">{message}</p>
    </div>
    """


def badge_html(text: str) -> str:
    """Return HTML for a pill/badge using accent tint. Use in auth panel or elsewhere."""
    return f'<span style="background: {ACCENT_RGBA_BG}; color: {TEXT_PRIMARY}; font-size: 0.75rem; font-weight: 600; padding: 0.35rem 0.65rem; border-radius: 8px;">{text}</span>'


def apply_metric_cards_style() -> None:
    """Apply theme-matched styling to st.metric() cards using streamlit-extras. No-op if extras not installed."""
    if style_metric_cards is None:
        return
    style_metric_cards(
        background_color=CARD_BG,
        border_size_px=1,
        border_color=BORDER,
        border_radius_px=20,
        border_left_color=ACCENT,
        box_shadow=True,
    )


def make_grid(*spec, gap: str = "medium", vertical_align: str = "top"):
    """Return a streamlit-extras grid container with theme-friendly gap. Falls back to None if extras not installed."""
    if grid is None:
        return None
    return grid(*spec, gap=gap, vertical_align=vertical_align)
