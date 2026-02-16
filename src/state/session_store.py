"""Image pair history: persisted in SQLite; images on filesystem. init_history ensures DB exists."""

from typing import Any

from src.db import database
from src.ui import components


def init_history() -> None:
    """Ensure DB and data dirs exist."""
    database.init_db()


def get_history() -> list[dict[str, Any]]:
    """Return pairs from DB, newest first. Each dict has pair_name, timestamp, filename_a, filename_b, path_a, path_b (load images via load_image_from_path)."""
    init_history()
    rows = database.get_pairs()
    return [
        {
            "pair_name": r["pair_name"],
            "timestamp": r["created_at"],
            "filename_a": r["filename_a"] or "",
            "filename_b": r["filename_b"] or "",
            "path_a": r["path_a"],
            "path_b": r["path_b"],
        }
        for r in rows
    ]


def append_pair(
    label: str,
    name_a: str,
    name_b: str,
    img_a: Any,
    img_b: Any,
) -> None:
    """Save both images to data/uploads/, then insert a row in SQLite. Uses 'Pair N' if label empty."""
    init_history()
    path_a = components.save_image_to_uploads(img_a, "a")
    path_b = components.save_image_to_uploads(img_b, "b")
    if not path_a or not path_b:
        raise RuntimeError("Failed to save one or both images to disk.")
    rows = database.get_pairs()
    n = len(rows) + 1
    pair_name = (label or "").strip() or f"Pair {n}"
    database.insert_pair(
        pair_name=pair_name,
        filename_a=name_a or "",
        filename_b=name_b or "",
        path_a=path_a,
        path_b=path_b,
    )


def clear_history() -> None:
    """Delete all pairs from DB. Image files in data/uploads/ are left on disk."""
    database.clear_pairs()
