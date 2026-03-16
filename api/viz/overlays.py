"""Mask previews, contour overlay, change highlight (XOR) overlay."""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np


def _validate_gray(mask: np.ndarray) -> bool:
    return (
        mask is not None
        and isinstance(mask, np.ndarray)
        and mask.ndim == 2
        and mask.dtype in (np.uint8, np.bool_)
    )


def _validate_rgb(img: np.ndarray) -> bool:
    return (
        img is not None
        and isinstance(img, np.ndarray)
        and img.ndim == 3
        and img.shape[2] == 3
        and img.dtype == np.uint8
    )


def mask_preview(mask: np.ndarray) -> Optional[np.ndarray]:
    """Convert binary mask to RGB for display. Returns (H, W, 3) uint8 or None."""
    if not _validate_gray(mask):
        return None
    try:
        if mask.dtype == np.bool_:
            m = (mask.astype(np.uint8) * 255)
        else:
            m = np.where(mask > 0, 255, 0).astype(np.uint8)
        return np.repeat(m[:, :, np.newaxis], 3, axis=2)
    except Exception:
        return None


def contour_overlay(img_rgb: np.ndarray, mask: np.ndarray, color: tuple[int, int, int] = (0, 255, 0), thickness: int = 2) -> Optional[np.ndarray]:
    """Draw mask contour on image. color in RGB."""
    if not _validate_rgb(img_rgb) or not _validate_gray(mask):
        return None
    if img_rgb.shape[:2] != mask.shape[:2]:
        return None
    try:
        out = img_rgb.copy()
        binary = (mask > 0).astype(np.uint8)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, color, thickness)
        return out
    except Exception:
        return None


def change_highlight_overlay(img_b_rgb: np.ndarray, mask_a: np.ndarray, mask_b: np.ndarray, alpha: float = 0.4, highlight_color: tuple[int, int, int] = (255, 200, 0)) -> Optional[np.ndarray]:
    """XOR of mask_a and mask_b; overlay semi-transparent highlight on image B."""
    if not _validate_rgb(img_b_rgb) or not _validate_gray(mask_a) or not _validate_gray(mask_b):
        return None
    h, w = img_b_rgb.shape[:2]
    if mask_a.shape != (h, w) or mask_b.shape != (h, w):
        return None
    try:
        m_a = (mask_a > 0).astype(np.uint8)
        m_b = (mask_b > 0).astype(np.uint8)
        xor_region = np.logical_xor(m_a, m_b).astype(np.uint8)
        if np.sum(xor_region) == 0:
            return img_b_rgb.copy()
        out = img_b_rgb.copy().astype(np.float32)
        overlay = np.zeros_like(out)
        overlay[:, :, 0] = highlight_color[0]
        overlay[:, :, 1] = highlight_color[1]
        overlay[:, :, 2] = highlight_color[2]
        blend = out * (1 - alpha * xor_region[:, :, np.newaxis]) + overlay * (alpha * xor_region[:, :, np.newaxis])
        return np.clip(blend, 0, 255).astype(np.uint8)
    except Exception:
        return None
