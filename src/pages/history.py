"""Image History page: list of comparison pairs as horizontal record cards; View report opens in a modal dialog only."""

import streamlit as st

from src.state import session_store
from src.ui import components
from src.ui import theme

THUMBNAIL_WIDTH = 64
THUMBNAIL_HEIGHT = 48


def _mock_report(pair_id: int) -> dict:
    """Return mock report for a pair (thresholds to be provided later)."""
    return {
        "size": "+2 mm" if pair_id % 3 == 0 else "No significant change",
        "shape": "Slight asymmetry noted" if pair_id % 4 == 0 else "No significant change",
        "color": "Slight darkening" if pair_id % 5 == 0 else "No significant change",
        "result": "Within normal range" if pair_id % 2 == 0 else "Review recommended",
    }


def _report_content_html(pair_id: int, pair_name: str, timestamp: str) -> str:
    """Build report content as HTML for the modal: title, date, sections, highlighted final result."""
    report = _mock_report(pair_id)
    date_str = components.format_pair_timestamp(timestamp)
    title = pair_name or f"Pair {pair_id}"
    parts = [
        f'<div style="margin-bottom: 1.25rem;">'
        f'<p style="margin:0 0 0.25rem 0; font-size:1.25rem; font-weight: 700; color: {theme.TEXT_PRIMARY};">{title}</p>'
        f"</div>",
        theme.report_section_html("Comparison date", date_str),
        theme.report_section_html("Mole size changes", report["size"]),
        theme.report_section_html("Mole shape changes", report["shape"]),
        theme.report_section_html("Color changes", report["color"]),
        theme.report_final_result_html(report["result"]),
    ]
    return "".join(parts)


def _show_report_dialog(pair_id: int, pair_name: str, timestamp: str) -> None:
    """Render report inside the modal using native Streamlit elements so the dialog always displays correctly (no raw HTML)."""
    report = _mock_report(pair_id)
    date_str = components.format_pair_timestamp(timestamp)
    title = pair_name or f"Pair {pair_id}"

    st.markdown(f"**{title}**")
    st.caption("Comparison date")
    st.markdown(date_str)

    st.caption("Mole size changes")
    st.markdown(report["size"])

    st.caption("Mole shape changes")
    st.markdown(report["shape"])

    st.caption("Color changes")
    st.markdown(report["color"])

    st.markdown("---")
    st.caption("Final result")
    st.markdown(f"**{report['result']}**")

    if st.button("Close", key="report_close"):
        if "history_report_pair_id" in st.session_state:
            del st.session_state["history_report_pair_id"]
        st.rerun()


def _thumbnail_placeholder(label: str) -> str:
    """HTML for a small placeholder when image cannot be loaded."""
    return f"""
    <div style="
        width: {THUMBNAIL_WIDTH}px; height: {THUMBNAIL_HEIGHT}px;
        background: {theme.CARD_ALT};
        border: 1px dashed {theme.BORDER};
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {theme.TEXT_MUTED};
        font-size: 0.7rem;
        text-align: center;
        padding: 4px;
    ">{label}</div>
    """


def render() -> None:
    theme.page_header("Image History", subtitle=None, eyebrow=None)
    session_store.init_history()
    history = session_store.get_history()

    has_dialog = getattr(st, "dialog", None) is not None

    # Open report: modal when Streamlit 1.36+, otherwise show report in-page
    if "history_report_pair_id" in st.session_state and history:
        pair_id = st.session_state["history_report_pair_id"]
        entry = next((e for e in history if e["id"] == pair_id), None)
        if entry:
            if has_dialog:
                show_dialog = st.dialog("Comparison Report", width="large")(_show_report_dialog)
                show_dialog(entry["id"], entry["pair_name"], entry["timestamp"])
            else:
                st.info(
                    "Report dialog requires **Streamlit 1.36+**. "
                    "Run: `pip install -U \"streamlit>=1.36\"` then restart the app to view reports in a modal."
                )
                st.markdown("<br>", unsafe_allow_html=True)
                report_html = _report_content_html(entry["id"], entry["pair_name"], entry["timestamp"])
                st.markdown(
                    f'<div class="mm-card mm-card-alt">{report_html}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Close report", key="report_close_fallback"):
                    del st.session_state["history_report_pair_id"]
                    st.rerun()

    # Empty state
    if not history:
        empty_html = theme.card_html(
            "No comparison history yet",
            "Upload two images on the <strong>Home</strong> page to create your first report.",
            variant="alt",
        )
        st.markdown(empty_html, unsafe_allow_html=True)
        return

    # List of comparison pairs as horizontal cards; one form per row so we can style the form container with a border
    for entry in history:
        formatted_ts = components.format_pair_timestamp(entry["timestamp"])
        img_a = components.load_image_from_path(entry["path_a"])
        img_b = components.load_image_from_path(entry["path_b"])
        pair_name = entry["pair_name"] or f"Pair {entry['id']}"

        with st.form(key=f"history_row_{entry['id']}"):
            col_left, col_right = st.columns([4, 1])
            with col_left:
                col_thumbs, col_meta = st.columns([1, 6])
                with col_thumbs:
                    data_a = components.image_to_data_url(img_a) if img_a is not None else ""
                    data_b = components.image_to_data_url(img_b) if img_b is not None else ""
                    thumb_a_html = (
                        f'<img src="{data_a}" style="width:{THUMBNAIL_WIDTH}px;height:{THUMBNAIL_HEIGHT}px;object-fit:cover;border-radius:8px;" alt="A" />'
                        if data_a
                        else _thumbnail_placeholder("A")
                    )
                    thumb_b_html = (
                        f'<img src="{data_b}" style="width:{THUMBNAIL_WIDTH}px;height:{THUMBNAIL_HEIGHT}px;object-fit:cover;border-radius:8px;" alt="B" />'
                        if data_b
                        else _thumbnail_placeholder("B")
                    )
                    thumbs_row = f'<div style="display:flex; gap:8px; align-items:center;">{thumb_a_html} {thumb_b_html}</div>'
                    st.markdown(thumbs_row, unsafe_allow_html=True)
                with col_meta:
                    meta_html = f"""
                    <p style="margin:0 0 0.2rem 0; font-size:1.25rem; font-weight: 700; color: {theme.TEXT_PRIMARY}; line-height: 1.3;">{pair_name}</p>
                    <p style="margin:0; font-size: 0.9rem; font-weight: 600; color: {theme.TEXT_MUTED};">{formatted_ts}</p>
                    """
                    st.markdown(meta_html, unsafe_allow_html=True)
            with col_right:
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    view_clicked = st.form_submit_button("View Report")
                with btn_col2:
                    delete_clicked = st.form_submit_button("Delete")
            if view_clicked:
                st.session_state["history_report_pair_id"] = entry["id"]
                st.rerun()
            if delete_clicked:
                session_store.delete_pair(entry["id"])
                if st.session_state.get("history_report_pair_id") == entry["id"]:
                    del st.session_state["history_report_pair_id"]
                st.rerun()
