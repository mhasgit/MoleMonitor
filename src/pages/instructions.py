"""Instructions page: photo guidelines, tip cards, safety disclaimer, CTA to upload."""

import streamlit as st
import streamlit_shadcn_ui as ui

from src.ui import theme


def render() -> None:
    theme.page_header("Take a Clear Mole Photo", subtitle=None, eyebrow=None)

    intro_card_html = theme.feature_card(
        "Photo guidelines",
        "<p style='margin:0; font-size:1rem; line-height:1.55;'>"
        "Follow these tips to help the system compare your mole images accurately.</p>",
        icon="",
        variant="elevated",
    )
    st.markdown(intro_card_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tips = [
        ("Good Lighting", "💡", "Use natural or bright indoor light. Do not use flash."),
        (
            "Keep It Sharp",
            "📷",
            "Hold your phone steady and tap the screen to focus on the mole.",
        ),
        (
            "Straight Angle",
            "📐",
            "Take the photo directly above the mole. Avoid angled photos.",
        ),
        (
            "Clear Skin",
            "✨",
            "Make sure the mole is fully visible. Move hair away and avoid creams or makeup.",
        ),
        (
            "Reference Coin (Optional)",
            "🪙",
            "Place a small coin (e.g. a 5p coin) near the mole to help measure size changes.",
        ),
    ]

    tip_cards_html = [
        theme.instruction_tip_card_html(
            title,
            f"<p style='margin:0; font-size:1.05rem; line-height:1.6;'>{body}</p>",
            icon=icon,
            variant="default" if i % 2 == 0 else "alt",
        )
        for i, (title, icon, body) in enumerate(tips)
    ]
    my_grid = theme.make_grid(5, gap="medium", vertical_align="top")
    if my_grid is not None:
        for html in tip_cards_html:
            my_grid.markdown(html, unsafe_allow_html=True)
    else:
        cols = st.columns(len(tips))
        for col, html in zip(cols, tip_cards_html):
            with col:
                st.markdown(html, unsafe_allow_html=True)

    disclaimer_body = (
        "MoleMonitor detects visible changes in a mole over time. It does <strong>not</strong> provide medical diagnosis. "
        "If you are concerned about a mole, please consult a healthcare professional."
    )
    st.markdown(theme.disclaimer_card_html("Disclaimer", disclaimer_body), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(theme.cta_card_html("Ready to add your first comparison?"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if ui.button("Continue to Upload Photo", key="instructions_cta", variant="default"):
        st.session_state["nav_page"] = "Home"
        st.rerun()
