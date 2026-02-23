"""Image History page: list saved pairs, select to view, remove single pair, clear history."""

import streamlit as st

from src.state import session_store
from src.ui import components


def render() -> None:
    st.title("Image History")
    session_store.init_history()
    history = session_store.get_history()

    if not history:
        st.info("No saved pairs yet. Use **Home** to upload and save a pair.")
        return

    selected_idx = st.radio(
        "Select a pair to view",
        range(len(history)),
        format_func=lambda i: f"{history[i]['pair_name']} — {components.format_pair_timestamp(history[i]['timestamp'])}",
        key="history_select",
    )

    if selected_idx is not None and 0 <= selected_idx < len(history):
        entry = history[selected_idx]
        formatted_ts = components.format_pair_timestamp(entry["timestamp"])
        st.caption(f"**{entry['pair_name']}** · {formatted_ts}")
        st.caption(f"Files: {entry['filename_a'] or '—'} / {entry['filename_b'] or '—'}")
        img_a = components.load_image_from_path(entry["path_a"])
        img_b = components.load_image_from_path(entry["path_b"])
        col1, col2 = st.columns(2)
        with col1:
            if img_a is not None:
                st.image(img_a, use_column_width=True, caption="Image A (older)")
            else:
                st.warning("Could not load Image A.")
        with col2:
            if img_b is not None:
                st.image(img_b, use_column_width=True, caption="Image B (newer)")
            else:
                st.warning("Could not load Image B.")

        if st.button("Remove this pair", key="remove_pair_btn"):
            session_store.delete_pair(entry["id"])
            st.success("Pair removed.")
            st.rerun()

    st.divider()
    with st.expander("Clear history"):
        confirm = st.checkbox("I want to clear all saved pairs", key="clear_confirm")
        if st.button("Clear history", disabled=not confirm, key="clear_btn"):
            if confirm:
                session_store.clear_history()
                st.success("Cleared.")
                st.rerun()
