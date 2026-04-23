"""Preprocessing: size matching, optional CLAHE/blur, quality checks."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np

import config

MAX_PROCESSING_SIDE = int(getattr(config, "COMPARE_MAX_PROCESSING_SIDE", 1200))


def _validate_rgb(img: np.ndarray) -> None:
    if img is None or not isinstance(img, np.ndarray):
        raise ValueError("Image must be a numpy array")
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Image must be RGB (H, W, 3)")
    if img.dtype != np.uint8:
        raise ValueError("Image must be uint8")


def match_sizes(
    img_a: np.ndarray, img_b: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Resize to common width (min of the two), then center-crop to common height (min)."""
    _validate_rgb(img_a)
    _validate_rgb(img_b)
    h_a, w_a = img_a.shape[:2]
    h_b, w_b = img_b.shape[:2]
    w_common = min(w_a, w_b)
    h_common = min(h_a, h_b)
    scale_a = w_common / w_a
    scale_b = w_common / w_b
    a_resized = cv2.resize(img_a, (w_common, int(h_a * scale_a)), interpolation=cv2.INTER_LINEAR)
    b_resized = cv2.resize(img_b, (w_common, int(h_b * scale_b)), interpolation=cv2.INTER_LINEAR)

    def center_crop(img: np.ndarray, target_h: int) -> np.ndarray:
        h, w = img.shape[:2]
        if h <= target_h:
            return img
        start = (h - target_h) // 2
        return img[start : start + target_h, :].copy()

    h_final = min(a_resized.shape[0], b_resized.shape[0], h_common)
    a_crop = center_crop(a_resized, h_final)
    b_crop = center_crop(b_resized, h_final)
    return a_crop, b_crop


def downscale_if_needed(img: np.ndarray, max_side: int = MAX_PROCESSING_SIDE) -> np.ndarray:
    """Downscale large images to bounded size for predictable runtime."""
    _validate_rgb(img)
    h, w = img.shape[:2]
    longest = max(h, w)
    if max_side <= 0 or longest <= max_side:
        return img.copy()
    scale = max_side / float(longest)
    target_w = max(1, int(round(w * scale)))
    target_h = max(1, int(round(h * scale)))
    return cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)


def apply_clahe_lab(img_rgb: np.ndarray) -> np.ndarray:
    """Apply CLAHE on L channel in LAB space; return RGB."""
    _validate_rgb(img_rgb)
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l_ch, a_ch, b_ch = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_eq = clahe.apply(l_ch)
    lab_eq = cv2.merge([l_eq, a_ch, b_ch])
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)


def apply_gaussian_blur(img: np.ndarray, kernel_size: int) -> np.ndarray:
    """Apply Gaussian blur. kernel_size 0 or 1 = no blur; must be odd."""
    _validate_rgb(img)
    if kernel_size is None or kernel_size < 2:
        return img.copy()
    k = int(kernel_size)
    if k % 2 == 0:
        k += 1
    return cv2.GaussianBlur(img, (k, k), 0)


def quality_checks(img_rgb: np.ndarray) -> dict[str, Any]:
    """Run blur and exposure checks."""
    _validate_rgb(img_rgb)
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l_ch = lab[:, :, 0]
    mean_l = float(np.mean(l_ch))
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    low_sharpness = laplacian_var < getattr(config, "BLUR_DETECTION_LAPLACIAN_THRESHOLD", 100.0)
    exposure_low = getattr(config, "EXPOSURE_LOW_L", 30.0)
    exposure_high = getattr(config, "EXPOSURE_HIGH_L", 220.0)
    exposure_warning = mean_l < exposure_low or mean_l > exposure_high
    return {
        "low_sharpness": low_sharpness,
        "exposure_warning": exposure_warning,
        "mean_L": mean_l,
        "laplacian_variance": laplacian_var,
    }


def preprocess_pair(
    img_a: np.ndarray,
    img_b: np.ndarray,
    *,
    use_clahe: bool = False,
    blur_kernel_size: int = 0,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any], dict[str, Any]]:
    """Match sizes, optionally CLAHE/blur, then quality checks. Returns (img_a, img_b, quality_a, quality_b)."""
    _validate_rgb(img_a)
    _validate_rgb(img_b)
    a, b = match_sizes(img_a, img_b)
    a = downscale_if_needed(a)
    b = downscale_if_needed(b)
    if use_clahe:
        a = apply_clahe_lab(a)
        b = apply_clahe_lab(b)
    if blur_kernel_size and blur_kernel_size >= 2:
        a = apply_gaussian_blur(a, blur_kernel_size)
        b = apply_gaussian_blur(b, blur_kernel_size)
    quality_a = quality_checks(a)
    quality_b = quality_checks(b)
    return a, b, quality_a, quality_b
