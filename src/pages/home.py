"""Home page: upload Image A (older) and Image B (newer), preview, save to history. Can also pick from History."""

import streamlit as st

from src import config
from src.state import session_store
from src.ui import components


def render() -> None:
    st.title("MoleMonitor (MVP)")

    # Session state for "pick from History" (pair_id, "a"|"b") or None
    if "home_from_history_a" not in st.session_state:
        st.session_state["home_from_history_a"] = None
    if "home_from_history_b" not in st.session_state:
        st.session_state["home_from_history_b"] = None

    history = session_store.get_history()

    col_a, col_b = st.columns(2)
    with col_a:
        file_a = st.file_uploader(
            "Image A (older)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_a",
        )
        if file_a is not None:
            st.session_state["home_from_history_a"] = None
    with col_b:
        file_b = st.file_uploader(
            "Image B (newer)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_b",
        )
        if file_b is not None:
            st.session_state["home_from_history_b"] = None

    # Resolve img_a: from file or from history
    img_a = None
    name_a = ""
    if file_a is not None:
        img_a = components.load_image_safe(file_a)
        name_a = file_a.name or ""
        if img_a is None:
            st.error("Could not load Image A.")
    elif st.session_state["home_from_history_a"] is not None:
        pair_id, slot = st.session_state["home_from_history_a"]
        entry = next((e for e in history if e["id"] == pair_id), None)
        if entry:
            path = entry["path_a"] if slot == "a" else entry["path_b"]
            img_a = components.load_image_from_path(path)
            name_a = entry["filename_a"] if slot == "a" else entry["filename_b"]
            if img_a is None:
                st.error("Could not load Image A from history.")
        else:
            st.session_state["home_from_history_a"] = None

    # Resolve img_b: from file or from history
    img_b = None
    name_b = ""
    if file_b is not None:
        img_b = components.load_image_safe(file_b)
        name_b = file_b.name or ""
        if img_b is None:
            st.error("Could not load Image B.")
    elif st.session_state["home_from_history_b"] is not None:
        pair_id, slot = st.session_state["home_from_history_b"]
        entry = next((e for e in history if e["id"] == pair_id), None)
        if entry:
            path = entry["path_a"] if slot == "a" else entry["path_b"]
            img_b = components.load_image_from_path(path)
            name_b = entry["filename_a"] if slot == "a" else entry["filename_b"]
            if img_b is None:
                st.error("Could not load Image B from history.")
        else:
            st.session_state["home_from_history_b"] = None

    st.subheader("Preview")
    prev_a, prev_b = st.columns(2)
    with prev_a:
        if img_a is not None:
            st.image(img_a, use_column_width=True, caption="Image A (older)")
        else:
            st.info("Upload Image A or pick from History to see preview.")
    with prev_b:
        if img_b is not None:
            st.image(img_b, use_column_width=True, caption="Image B (newer)")
        else:
            st.info("Upload Image B or pick from History to see preview.")

    # Or pick from History
    if history:
        with st.expander("Or pick from History"):
            options = [
                f"{e['pair_name']} — {components.format_pair_timestamp(e['timestamp'])}"
                for e in history
            ]
            selected_idx = st.selectbox(
                "Select a saved pair",
                range(len(options)),
                format_func=lambda i: options[i],
                key="home_pick_pair_select",
            )
            if selected_idx is not None and 0 <= selected_idx < len(history):
                pair_id = history[selected_idx]["id"]
                pick_col_a, pick_col_b = st.columns(2)
                with pick_col_a:
                    st.caption("Use as Image A (older)")
                    if st.button("Use left (older)", key="pick_left_a"):
                        st.session_state["home_from_history_a"] = (pair_id, "a")
                        st.rerun()
                    if st.button("Use right (newer)", key="pick_right_a"):
                        st.session_state["home_from_history_a"] = (pair_id, "b")
                        st.rerun()
                with pick_col_b:
                    st.caption("Use as Image B (newer)")
                    if st.button("Use left (older)", key="pick_left_b"):
                        st.session_state["home_from_history_b"] = (pair_id, "a")
                        st.rerun()
                    if st.button("Use right (newer)", key="pick_right_b"):
                        st.session_state["home_from_history_b"] = (pair_id, "b")
                        st.rerun()

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
            try:
                session_store.append_pair(
                    label=custom_label or "",
                    name_a=name_a or "from_history",
                    name_b=name_b or "from_history",
                    img_a=img_a,
                    img_b=img_b,
                )
                st.success("Saved.")
                st.rerun()
            except RuntimeError as e:
                st.error(str(e))

    st.caption(f"Saved pairs: **{len(history)}**")
