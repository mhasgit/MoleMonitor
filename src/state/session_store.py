"""In-app image pair history using Streamlit session_state. No database."""

from datetime import datetime
from typing import Any

import streamlit as st


HISTORY_KEY = "image_history"


def init_history() -> None:
    """Ensure session_state has the history list."""
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []


def get_history() -> list[dict[str, Any]]:
    """Return history list, newest first. Call init_history() before first use."""
    init_history()
    raw = st.session_state[HISTORY_KEY]
    return list(reversed(raw))


def append_pair(
    label: str,
    name_a: str,
    name_b: str,
    img_a: Any,
    img_b: Any,
) -> None:
    """Append one pair. Uses 'Pair N' if label is empty."""
    init_history()
    history = st.session_state[HISTORY_KEY]
    n = len(history) + 1
    pair_name = (label or "").strip() or f"Pair {n}"
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pair_name": pair_name,
        "filename_a": name_a or "",
        "filename_b": name_b or "",
        "image_a": img_a,
        "image_b": img_b,
    }
    history.append(record)


def clear_history() -> None:
    """Clear all saved pairs."""
    st.session_state[HISTORY_KEY] = []
