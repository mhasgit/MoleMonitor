"""Segmentation: Phase 1 heuristic + interface for Phase 2 swap."""

from __future__ import annotations

from typing import Any, Protocol

import cv2
import numpy as np

import config

MIN_MASK_AREA_PX = getattr(config, "SEGMENT_MIN_MASK_AREA_PX", 100)


class SegmenterProtocol(Protocol):
    """Protocol for segmenters."""

    def __call__(self, rgb: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
        """Return (mask_uint8_0_255, quality_dict)."""
        ...


def segment_phase1_heuristic(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    """Phase 1 heuristic: grayscale -> blur -> Otsu -> morph -> largest CC."""
    if rgb is None or not isinstance(rgb, np.ndarray) or rgb.ndim != 3:
        h, w = 256, 256
        return np.zeros((h, w), dtype=np.uint8), {
            "mask_area_px": 0,
            "too_small": True,
            "error": "invalid_input",
        }
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    if num_labels <= 1:
        mask = np.zeros_like(gray, dtype=np.uint8)
        area_px = 0
    else:
        areas = stats[1:, cv2.CC_STAT_AREA]
        largest_idx = 1 + int(np.argmax(areas))
        mask = np.where(labels == largest_idx, 255, 0).astype(np.uint8)
        area_px = int(stats[largest_idx, cv2.CC_STAT_AREA])
    too_small = area_px < MIN_MASK_AREA_PX
    quality = {"mask_area_px": area_px, "too_small": too_small}
    return mask, quality


def get_segmenter() -> SegmenterProtocol:
    """Return the active segmenter."""
    return segment_phase1_heuristic
