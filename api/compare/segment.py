"""Segmentation: heuristic mole mask selection with quality flags."""

from __future__ import annotations

from typing import Any, Protocol

import cv2
import numpy as np

import config

MIN_MASK_AREA_PX = getattr(config, "SEGMENT_MIN_MASK_AREA_PX", 100)
MAX_MASK_AREA_RATIO = float(getattr(config, "SEGMENT_MAX_MASK_AREA_RATIO", 0.35))
CENTER_WEIGHT = float(getattr(config, "SEGMENT_CENTER_WEIGHT", 0.8))
SATURATION_WEIGHT = float(getattr(config, "SEGMENT_SATURATION_WEIGHT", 0.6))
DARKNESS_WEIGHT = float(getattr(config, "SEGMENT_DARKNESS_WEIGHT", 0.5))
COIN_PENALTY_WEIGHT = float(getattr(config, "SEGMENT_COIN_PENALTY_WEIGHT", 1.0))


class SegmenterProtocol(Protocol):
    """Protocol for segmenters."""

    def __call__(self, rgb: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
        """Return (mask_uint8_0_255, quality_dict)."""
        ...


def segment_phase1_heuristic(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    """Segment a likely mole region and return quality diagnostics."""
    if rgb is None or not isinstance(rgb, np.ndarray) or rgb.ndim != 3:
        h, w = 256, 256
        return np.zeros((h, w), dtype=np.uint8), {
            "mask_area_px": 0,
            "too_small": True,
            "error": "invalid_input",
        }
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    h, w = gray.shape[:2]
    total_px = float(h * w) if h and w else 1.0
    if num_labels <= 1:
        mask = np.zeros_like(gray, dtype=np.uint8)
        area_px = 0
        quality = {
            "mask_area_px": area_px,
            "too_small": True,
            "candidate_count": 0,
            "suspect_component": True,
            "selected_reason": "no_components",
        }
        return mask, quality

    center_x = (w - 1) / 2.0
    center_y = (h - 1) / 2.0
    max_center_dist = ((center_x ** 2) + (center_y ** 2)) ** 0.5 or 1.0
    selected_idx = None
    selected_score = float("-inf")
    selected_border_touching = False
    selected_coin_like = False
    candidate_count = 0

    for label_idx in range(1, num_labels):
        area = int(stats[label_idx, cv2.CC_STAT_AREA])
        if area < MIN_MASK_AREA_PX:
            continue
        area_ratio = area / total_px
        if area_ratio > MAX_MASK_AREA_RATIO:
            continue

        x = int(stats[label_idx, cv2.CC_STAT_LEFT])
        y = int(stats[label_idx, cv2.CC_STAT_TOP])
        cw = int(stats[label_idx, cv2.CC_STAT_WIDTH])
        ch = int(stats[label_idx, cv2.CC_STAT_HEIGHT])
        border_touching = x <= 0 or y <= 0 or (x + cw) >= (w - 1) or (y + ch) >= (h - 1)

        comp_mask = (labels == label_idx).astype(np.uint8)
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = sum(cv2.arcLength(c, True) for c in contours) if contours else 0.0
        circularity = (4.0 * np.pi * area) / (perimeter * perimeter) if perimeter > 0 else 0.0

        m = cv2.moments(comp_mask)
        if m["m00"] > 0:
            cx = m["m10"] / m["m00"]
            cy = m["m01"] / m["m00"]
        else:
            cx = x + (cw / 2.0)
            cy = y + (ch / 2.0)
        center_dist = ((cx - center_x) ** 2 + (cy - center_y) ** 2) ** 0.5
        center_score = 1.0 - min(1.0, center_dist / max_center_dist)

        comp_pixels = comp_mask > 0
        mean_v = float(np.mean(hsv[:, :, 2][comp_pixels])) if np.any(comp_pixels) else 255.0
        mean_s = float(np.mean(hsv[:, :, 1][comp_pixels])) if np.any(comp_pixels) else 0.0
        darkness_score = max(0.0, (180.0 - mean_v) / 180.0)
        saturation_score = min(1.0, mean_s / 120.0)

        coin_like = circularity > 0.86 and mean_v > 150.0 and mean_s < 45.0
        score = (
            CENTER_WEIGHT * center_score
            + SATURATION_WEIGHT * saturation_score
            + DARKNESS_WEIGHT * darkness_score
            - (0.9 if border_touching else 0.0)
            - (COIN_PENALTY_WEIGHT if coin_like else 0.0)
            + (0.2 if 0.001 <= area_ratio <= 0.06 else 0.0)
        )
        candidate_count += 1
        if score > selected_score:
            selected_score = score
            selected_idx = label_idx
            selected_border_touching = border_touching
            selected_coin_like = coin_like

    if selected_idx is None:
        mask = np.zeros_like(gray, dtype=np.uint8)
        area_px = 0
        quality = {
            "mask_area_px": area_px,
            "too_small": True,
            "candidate_count": 0,
            "suspect_component": True,
            "selected_reason": "no_valid_component",
        }
        return mask, quality

    mask = np.where(labels == selected_idx, 255, 0).astype(np.uint8)
    area_px = int(stats[selected_idx, cv2.CC_STAT_AREA])
    too_small = area_px < MIN_MASK_AREA_PX
    area_ratio = area_px / total_px
    suspect_component = selected_border_touching or selected_coin_like or area_ratio > 0.25
    quality = {
        "mask_area_px": area_px,
        "too_small": too_small,
        "candidate_count": candidate_count,
        "suspect_component": suspect_component,
        "border_touching": selected_border_touching,
        "coin_like": selected_coin_like,
        "area_ratio": area_ratio,
        "score": float(selected_score),
    }
    return mask, quality


def get_segmenter() -> SegmenterProtocol:
    """Return the active segmenter."""
    return segment_phase1_heuristic
