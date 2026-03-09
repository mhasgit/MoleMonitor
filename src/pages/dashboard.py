"""Dashboard page: welcome, stats cards, and report dates."""

from datetime import datetime

import streamlit as st

from src.state import session_store
from src.ui import components
from src.ui import theme


def _timestamp_to_date_str(iso_timestamp: str) -> str:
    """Return date string (e.g. Mar 8, 2025) for display."""
    if not iso_timestamp:
        return "Unknown date"
    try:
        s = iso_timestamp.rstrip("Z").replace("Z", "")
        dt = datetime.fromisoformat(s)
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return iso_timestamp or "Unknown date"


def render() -> None:
    user_name = st.session_state.get("user_name", "User")
    theme.page_header(f"Welcome, {user_name}", subtitle=None, eyebrow=None)

    session_store.init_history()
    history = session_store.get_history()
    report_count = len(history)
    total_images = sum(2 for _ in history)
    dates_with_reports = []
    most_recent_name = None
    most_recent_ts = None
    for e in history:
        dates_with_reports.append(e["timestamp"])
        if most_recent_ts is None or (e["timestamp"] or "") > (most_recent_ts or ""):
            most_recent_ts = e["timestamp"]
            most_recent_name = e["pair_name"] or "Pair (Image A / Image B)"

    report_dates = sorted(
        set(_timestamp_to_date_str(ts) for ts in dates_with_reports if ts)
    )
    mock_changes = min(report_count * 2, 7) if report_count else 0

    welcome_content = (
        "<p style='margin:0; font-size:1rem; line-height:1.55;'>"
        "Track your skin health over time. Upload mole photos, compare them, "
        "and keep an eye on changes with simple reports."
        "</p>"
    )
    welcome_card_html = theme.feature_card(
        "Welcome to MoleMonitor",
        welcome_content,
        icon="",
        variant="elevated",
    )

    # Row 1: welcome card full width. Row 2: three equal metric cards (st.metric styled via theme).
    my_grid = theme.make_grid(1, 3, gap="medium", vertical_align="top")
    if my_grid is not None:
        my_grid.markdown(welcome_card_html, unsafe_allow_html=True)
        my_grid.metric(label="Reports generated", value=report_count)
        my_grid.metric(label="Overall changes", value=mock_changes)
        my_grid.metric(label="Total images uploaded", value=total_images)
        theme.apply_metric_cards_style()
    else:
        # Fallback: welcome card first, then three metric columns
        st.markdown(welcome_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Reports generated", value=report_count)
        with m2:
            st.metric(label="Overall changes", value=mock_changes)
        with m3:
            st.metric(label="Total images uploaded", value=total_images)
        theme.apply_metric_cards_style()

    st.markdown("<br>", unsafe_allow_html=True)
    # Report dates: full-width card matching metric cards (same background, 1px border, teal left accent, padding)
    border_color = theme.BORDER
    accent = theme.ACCENT
    card_bg = theme.CARD_BG
    radius = theme.CARD_RADIUS
    gap = theme.SECTION_GAP
    muted = theme.TEXT_MUTED
    primary = theme.TEXT_PRIMARY
    stat_padding = "1.25rem 1.5rem"
    min_height = "130px"
    if report_dates:
        dates_list = "".join(
            f'<li style="margin-bottom:0.35rem; color: {primary};">{d}</li>'
            for d in report_dates
        )
        dates_content = f"<ul style='margin:0; padding-left:1.25rem;'>{dates_list}</ul>"
    else:
        dates_content = (
            f"<p style='margin:0; font-size:0.9rem; color: {primary};'>"
            "No reports yet. Upload and compare images on the Home page."
            "</p>"
        )
    report_card_html = f"""
    <div style="margin-top: {gap}; margin-bottom: {gap}; width: 100%;">
        <div style="
            width: 100%;
            background: {card_bg};
            border: 1px solid {border_color};
            border-left: 4px solid {accent};
            border-radius: {radius};
            padding: {stat_padding};
            box-shadow: {theme.CARD_SHADOW};
            min-height: {min_height};
        ">
            <div style="color: {muted}; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem;">
                Report dates
            </div>
            <div style="color: {primary}; line-height: 1.55;">
                {dates_content}
            </div>
        </div>
    </div>
    """
    st.markdown(report_card_html, unsafe_allow_html=True)
