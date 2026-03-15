"""Dashboard page: welcome, stats cards, and report dates."""

from datetime import datetime

import streamlit as st

from src.state import session_store
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
    st.markdown(welcome_card_html, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Reports generated", value=report_count)
    with m2:
        st.metric(label="Overall changes", value=mock_changes)
    with m3:
        st.metric(label="Total images uploaded", value=total_images)
    theme.apply_metric_cards_style()

    st.markdown("<br>", unsafe_allow_html=True)

    if report_dates:
        dates_list = "".join(
            f'<li style="margin-bottom:0.35rem;">{d}</li>' for d in report_dates
        )
        dates_content = f"<ul style='margin:0; padding-left:1.25rem;'>{dates_list}</ul>"
    else:
        dates_content = (
            "<p style='margin:0; font-size:0.9rem;'>"
            "No reports yet. Upload and compare images on the Home page."
            "</p>"
        )
    report_card_html = theme.card_html(
        "Report dates",
        dates_content,
        accent_left=True,
    )
    st.markdown(report_card_html, unsafe_allow_html=True)
