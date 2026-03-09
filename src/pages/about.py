"""About page: app description and disclaimer."""

import streamlit as st

from src.ui import theme


def render() -> None:
    theme.page_header("About MoleMonitor", subtitle=None, eyebrow=None)

    card1 = theme.card_html(
        "What MoleMonitor does",
        "<p style='margin:0; line-height:1.6;'>"
        "MoleMonitor is an MVP app for tracking skin mole images over time. "
        "You can upload pairs of photos, compare them, and keep a simple history of your records. "
        "It is designed to help you monitor changes in a single place."
        "</p>",
        variant="default",
    )
    card2 = theme.card_html(
        "Why consistent images matter",
        "<p style='margin:0; line-height:1.6;'>"
        "Taking photos in similar lighting, from the same angle, and at a similar distance "
        "makes it easier to spot real changes over time. Small differences in how you take the photo "
        "can look like changes when they are not. Consistency improves the usefulness of your history."
        "</p>",
        variant="alt",
    )
    card3 = theme.card_html(
        "Important disclaimer",
        "<p style='margin:0; line-height:1.6;'>"
        "MoleMonitor does not provide medical diagnosis. "
        "It only helps you store and compare images. "
        "If you have any concern about a mole or your skin health, please consult a healthcare professional."
        "</p>",
        variant="alt",
    )

    _, center, _ = st.columns([1, 8, 1])
    with center:
        my_grid = theme.make_grid(1, 1, 1, gap="medium", vertical_align="top")
        if my_grid is not None:
            my_grid.markdown(card1, unsafe_allow_html=True)
            my_grid.markdown(card2, unsafe_allow_html=True)
            my_grid.markdown(card3, unsafe_allow_html=True)
        else:
            st.markdown(card1, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(card2, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(card3, unsafe_allow_html=True)
