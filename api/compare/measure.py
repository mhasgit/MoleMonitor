"""Measurement: per-image metrics and comparison metrics."""

from __future__ import annotations

import math
from typing import Any

import cv2
import numpy as np


def _validate_mask(mask: np.ndarray, img: np.ndarray) -> None:
    if mask is None or mask.ndim != 2 or img is None or img.shape[:2] != mask.shape[:2]:
        raise ValueError("Mask must be 2D and match image shape")


def measure_single(rgb: np.ndarray, mask: np.ndarray) -> dict[str, Any]:
    """Compute per-image metrics: area_px, diam_px, perimeter, bbox, aspect_ratio, irregularity, LAB means."""
    _validate_mask(mask, rgb)
    area_px = int(np.sum(mask > 0))
    if area_px == 0:
        return {
            "area_px": 0,
            "diam_px": 0.0,
            "perimeter": 0.0,
            "bbox_w": 0,
            "bbox_h": 0,
            "aspect_ratio": 0.0,
            "irregularity": 0.0,
            "mean_L": 0.0,
            "mean_A": 0.0,
            "mean_B": 0.0,
            "invalid_mask": True,
        }
    diam_px = 2.0 * math.sqrt(area_px / math.pi)
    contours, _ = cv2.findContours(
        (mask > 0).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    perimeter = 0.0
    for c in contours:
        perimeter += cv2.arcLength(c, True)
    x, y, bbox_w, bbox_h = cv2.boundingRect(
        np.vstack(contours) if contours else np.array([[0, 0], [0, 0]])
    )
    if bbox_h > 0:
        aspect_ratio = bbox_w / bbox_h
    else:
        aspect_ratio = 0.0
    irregularity = (perimeter ** 2) / area_px if area_px else 0.0
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    mask_bool = mask > 0
    mean_l = float(np.mean(lab[:, :, 0][mask_bool]))
    mean_a = float(np.mean(lab[:, :, 1][mask_bool]))
    mean_b = float(np.mean(lab[:, :, 2][mask_bool]))
    return {
        "area_px": area_px,
        "diam_px": diam_px,
        "perimeter": perimeter,
        "bbox_w": int(bbox_w),
        "bbox_h": int(bbox_h),
        "aspect_ratio": aspect_ratio,
        "irregularity": irregularity,
        "mean_L": mean_l,
        "mean_A": mean_a,
        "mean_B": mean_b,
        "invalid_mask": False,
    }


def compare_metrics(
    m_a: dict[str, Any],
    m_b: dict[str, Any],
    px_per_mm: float | None = None,
) -> dict[str, Any]:
    """Compute comparison metrics: area_change_percent, diam_change_px, diam_change_mm, etc."""
    area_a = m_a.get("area_px") or 0
    area_b = m_b.get("area_px") or 0
    if area_a > 0:
        area_change_percent = 100.0 * (area_b - area_a) / area_a
    else:
        area_change_percent = 0.0 if area_b == 0 else 100.0
    diam_a = m_a.get("diam_px") or 0.0
    diam_b = m_b.get("diam_px") or 0.0
    diam_change_px = diam_b - diam_a
    diam_change_mm: float | None = None
    area_change_mm2: float | None = None
    if px_per_mm is not None and px_per_mm > 0 and diam_a > 0:
        diam_a_mm = diam_a / px_per_mm
        diam_b_mm = diam_b / px_per_mm
        diam_change_mm = diam_b_mm - diam_a_mm
        area_change_mm2 = ((area_b - area_a) / (px_per_mm ** 2)) if area_a > 0 or area_b > 0 else 0.0
    irr_a = m_a.get("irregularity") or 0.0
    irr_b = m_b.get("irregularity") or 0.0
    irregularity_delta = irr_b - irr_a
    l_a, a_a, b_a = m_a.get("mean_L", 0), m_a.get("mean_A", 0), m_a.get("mean_B", 0)
    l_b, a_b, b_b = m_b.get("mean_L", 0), m_b.get("mean_A", 0), m_b.get("mean_B", 0)
    color_deltaE = math.sqrt((l_b - l_a) ** 2 + (a_b - a_a) ** 2 + (b_b - b_a) ** 2)
    out = {
        "area_change_percent": area_change_percent,
        "diam_change_px": diam_change_px,
        "irregularity_delta": irregularity_delta,
        "color_deltaE": color_deltaE,
        "scale_available": px_per_mm is not None and px_per_mm > 0,
        "px_per_mm": px_per_mm if px_per_mm is not None and px_per_mm > 0 else None,
    }
    if diam_change_mm is not None:
        out["diam_change_mm"] = diam_change_mm
    else:
        out["diam_change_mm"] = None
    if area_change_mm2 is not None:
        out["area_change_mm2"] = area_change_mm2
    else:
        out["area_change_mm2"] = None
    return out
