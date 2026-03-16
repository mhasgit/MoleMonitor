"""Image load/save and formatting. No Streamlit."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

import config


def format_pair_timestamp(iso_timestamp: str) -> str:
    """Format ISO created_at for display."""
    if not iso_timestamp:
        return "Unknown date"
    try:
        s = iso_timestamp.rstrip("Z").replace("Z", "")
        dt = datetime.fromisoformat(s)
        return dt.strftime("%b %d, %Y, %I:%M %p")
    except (ValueError, TypeError):
        return iso_timestamp if iso_timestamp else "Unknown date"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_image_from_bytes(data: bytes) -> Optional[np.ndarray]:
    """Load image bytes as RGB uint8 numpy array (H, W, 3). Returns None on failure."""
    if not data:
        return None
    try:
        from io import BytesIO
        img = Image.open(BytesIO(data))
        img = img.convert("RGB")
        return np.array(img, dtype=np.uint8)
    except Exception:
        return None


def save_image_to_uploads(img: np.ndarray, suffix: str = "") -> Optional[str]:
    """Save RGB uint8 image to data/uploads/<unique>_<suffix>.jpg. Returns path relative to project root."""
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
    """Load image from path relative to project root. Returns RGB uint8 array or None."""
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
