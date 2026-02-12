"""Shared UI helpers and safe image loading."""

from typing import Optional

import numpy as np
from PIL import Image


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
