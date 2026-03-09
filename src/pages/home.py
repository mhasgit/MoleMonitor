"""Home page: upload Image A (older) and Image B (newer), preview, save to history. Can also select from already uploaded images."""

import streamlit as st

from src import config
from src.state import session_store
from src.ui import components
from src.ui import theme


def _get_uploaded_images_list():
    """Return list of (path, display_label) for all images in history, deduped by path."""
    history = session_store.get_history()
    seen = set()
    out = []
    for e in history:
        for path, name in [(e["path_a"], e["filename_a"]), (e["path_b"], e["filename_b"])]:
            if path and path not in seen:
                seen.add(path)
                label = name or path.split("/")[-1] if path else "Unknown"
                out.append((path, label))
    return out


def render() -> None:
    theme.page_header("Upload & Compare", subtitle=None, eyebrow=None)

    if "home_selected_path_a" not in st.session_state:
        st.session_state["home_selected_path_a"] = None
    if "home_selected_path_b" not in st.session_state:
        st.session_state["home_selected_path_b"] = None

    history = session_store.get_history()
    uploaded_list = _get_uploaded_images_list()

    theme.section_label("Upload")
    st.markdown('<div class="mm-home-upload-sentinel"></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        file_a = st.file_uploader(
            "Image A (older)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_a",
        )
        if file_a is not None:
            st.session_state["home_selected_path_a"] = None
    with col_b:
        file_b = st.file_uploader(
            "Image B (newer)",
            type=list(config.ALLOWED_EXTENSIONS),
            key="upload_b",
        )
        if file_b is not None:
            st.session_state["home_selected_path_b"] = None

    if uploaded_list:
        st.markdown('<div class="mm-home-select-sentinel"></div>', unsafe_allow_html=True)
        sel_col_a, sel_col_b = st.columns(2)
        options_paths = [""] + [p for p, _ in uploaded_list]
        options_labels = ["— Select image —"] + [label for _, label in uploaded_list]
        with sel_col_a:
            sel_a = st.selectbox(
                "Image A (older) from uploads",
                range(len(options_paths)),
                format_func=lambda i: options_labels[i],
                key="home_select_upload_a",
            )
        with sel_col_b:
            sel_b = st.selectbox(
                "Image B (newer) from uploads",
                range(len(options_paths)),
                format_func=lambda i: options_labels[i],
                key="home_select_upload_b",
            )
        if sel_a is not None and sel_a > 0:
            st.session_state["home_selected_path_a"] = options_paths[sel_a]
        else:
            st.session_state["home_selected_path_a"] = None
        if sel_b is not None and sel_b > 0:
            st.session_state["home_selected_path_b"] = options_paths[sel_b]
        else:
            st.session_state["home_selected_path_b"] = None

    img_a = None
    name_a = ""
    if file_a is not None:
        img_a = components.load_image_safe(file_a)
        name_a = file_a.name or ""
        if img_a is None:
            st.error("Could not load Image A.")
    elif st.session_state.get("home_selected_path_a"):
        path = st.session_state["home_selected_path_a"]
        img_a = components.load_image_from_path(path)
        name_a = path.split("/")[-1] if path else ""
        if img_a is None:
            st.error("Could not load Image A from uploads.")

    img_b = None
    name_b = ""
    if file_b is not None:
        img_b = components.load_image_safe(file_b)
        name_b = file_b.name or ""
        if img_b is None:
            st.error("Could not load Image B.")
    elif st.session_state.get("home_selected_path_b"):
        path = st.session_state["home_selected_path_b"]
        img_b = components.load_image_from_path(path)
        name_b = path.split("/")[-1] if path else ""
        if img_b is None:
            st.error("Could not load Image B from uploads.")

    st.markdown('<div class="mm-home-preview-sentinel"></div>', unsafe_allow_html=True)
    prev_a, prev_b = st.columns(2)
    with prev_a:
        if img_a is not None:
            st.image(img_a, width=400, caption="Image A (older)")
        else:
            placeholder = theme.empty_placeholder_html("Upload Image A or select from uploads to see preview.")
            st.markdown(placeholder, unsafe_allow_html=True)
    with prev_b:
        if img_b is not None:
            st.image(img_b, width=400, caption="Image B (newer)")
        else:
            placeholder = theme.empty_placeholder_html("Upload Image B or select from uploads to see preview.")
            st.markdown(placeholder, unsafe_allow_html=True)

    st.markdown('<div class="mm-home-action-sentinel"></div>', unsafe_allow_html=True)
    custom_label = st.text_input(
        "Pair label (optional)",
        value="",
        placeholder="Leave empty for auto (Pair 1, Pair 2, …)",
        key="home_label",
    )
    st.caption("Give this comparison a name, or leave blank to auto-generate.")
    both_ok = img_a is not None and img_b is not None
    if st.button("Save pair to history", disabled=not both_ok, key="save_pair", type="primary" if both_ok else "secondary", use_container_width=True):
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="color: {theme.TEXT_MUTED}; font-size: 0.85rem; margin: 0;">Saved pairs: <strong style="color: {theme.TEXT_PRIMARY};">{len(history)}</strong></p>',
        unsafe_allow_html=True,
    )
