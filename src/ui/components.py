"""Shared UI helpers and safe image loading."""

import uuid
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

from src import config


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_image_safe(uploaded_file) -> Optional[np.ndarray]:
    """
    Load an uploaded file as RGB uint8 numpy array (H, W, 3).
    Returns None on failure; caller should show st.error and not crash.
    """
    if uploaded_file is None:
        return None
    try:
        img = Image.open(uploaded_file)
        img = img.convert("RGB")
        arr = np.array(img, dtype=np.uint8)
        return arr
    except Exception:
        return None


def save_image_to_uploads(img: np.ndarray, suffix: str = "") -> Optional[str]:
    """
    Save RGB uint8 image to data/uploads/<unique>_<suffix>.jpg.
    Returns path relative to project root (e.g. data/uploads/abc123_a.jpg), or None on failure.
    """
    try:
        root = _project_root()
        uploads = root / config.UPLOADS_DIR
        uploads.mkdir(parents=True, exist_ok=True)
        name = f"{uuid.uuid4().hex}_{suffix}.jpg" if suffix else f"{uuid.uuid4().hex}.jpg"
        path = uploads / name
        pil = Image.fromarray(img)
        pil.save(str(path), "JPEG")
        return path.relative_to(root).as_posix()
    except Exception:
        return None


def load_image_from_path(relative_path: str) -> Optional[np.ndarray]:
    """
    Load image from path relative to project root. Returns RGB uint8 array or None on failure.
    """
    if not relative_path:
        return None
    try:
        root = _project_root()
        full = root / relative_path
        if not full.is_file():
            return None
        img = Image.open(full)
        img = img.convert("RGB")
        return np.array(img, dtype=np.uint8)
    except Exception:
        return None
