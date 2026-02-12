"""Home page: upload Image A (older) and Image B (newer), preview, save to history."""

import streamlit as st

from src import config
from src.state import session_store
from src.ui import components


def render() -> None:
    st.title("MoleMonitor (MVP)")

    col_a, col_b = st.columns(2)
    with col_a:
        file_a = st.file_uploader(
            "Image A (older)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_a",
        )
    with col_b:
        file_b = st.file_uploader(
            "Image B (newer)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_b",
        )

    img_a = None
    img_b = None
    if file_a:
        img_a = components.load_image_safe(file_a)
        if img_a is None:
            st.error("Could not load Image A.")
    if file_b:
        img_b = components.load_image_safe(file_b)
        if img_b is None:
            st.error("Could not load Image B.")

    st.subheader("Preview")
    prev_a, prev_b = st.columns(2)
    with prev_a:
        if img_a is not None:
            st.image(img_a, use_container_width=True, caption="Image A (older)")
        else:
            st.info("Upload Image A to see preview.")
    with prev_b:
        if img_b is not None:
            st.image(img_b, use_container_width=True, caption="Image B (newer)")
        else:
            st.info("Upload Image B to see preview.")

    with st.expander("Label (optional)"):
        custom_label = st.text_input(
            "Pair label",
            value="",
            placeholder="Leave empty for auto (Pair 1, Pair 2, …)",
            key="home_label",
        )

    both_ok = img_a is not None and img_b is not None
    if st.button("Save pair to history", disabled=not both_ok, key="save_pair"):
        if both_ok:
            session_store.append_pair(
                label=custom_label or "",
                name_a=file_a.name if file_a else "",
                name_b=file_b.name if file_b else "",
                img_a=img_a,
                img_b=img_b,
            )
            st.success("Saved.")
            st.rerun()

    history = session_store.get_history()
    st.caption(f"Saved pairs: **{len(history)}**")
