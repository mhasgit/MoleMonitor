"""Scale calibration utilities (coin-based pixels-per-mm estimation)."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np

import config

MAX_COIN_DETECT_SIDE = int(getattr(config, "COIN_DETECT_MAX_SIDE", 1024))
MAX_CONTOURS_EVAL = int(getattr(config, "COIN_DETECT_MAX_CONTOURS", 60))


def _resize_for_coin_detection(rgb: np.ndarray) -> tuple[np.ndarray, float]:
    """Downscale large images to keep coin detection bounded and fast."""
    h, w = rgb.shape[:2]
    longest = max(h, w)
    if longest <= MAX_COIN_DETECT_SIDE:
        return rgb, 1.0
    scale = MAX_COIN_DETECT_SIDE / float(longest)
    target_w = max(1, int(round(w * scale)))
    target_h = max(1, int(round(h * scale)))
    resized = cv2.resize(rgb, (target_w, target_h), interpolation=cv2.INTER_AREA)
    return resized, scale


def _mean_hsv_in_contour(hsv: np.ndarray, contour: np.ndarray) -> tuple[float, float]:
    """Compute mean saturation/value in contour region using ROI mask."""
    x, y, w, h = cv2.boundingRect(contour)
    roi_hsv = hsv[y : y + h, x : x + w]
    if roi_hsv.size == 0:
        return 255.0, 0.0
    roi_mask = np.zeros((h, w), dtype=np.uint8)
    contour_local = contour.copy()
    contour_local[:, 0, 0] -= x
    contour_local[:, 0, 1] -= y
    cv2.drawContours(roi_mask, [contour_local], -1, 255, thickness=-1)
    pixels = roi_mask > 0
    if not np.any(pixels):
        return 255.0, 0.0
    mean_s = float(np.mean(roi_hsv[:, :, 1][pixels]))
    mean_v = float(np.mean(roi_hsv[:, :, 2][pixels]))
    return mean_s, mean_v


def _detect_coin_diameter_px(rgb: np.ndarray) -> tuple[float | None, dict[str, Any]]:
    """Detect likely coin and return diameter in pixels with diagnostics."""
    if rgb is None or not isinstance(rgb, np.ndarray) or rgb.ndim != 3:
        return None, {"coin_detected": False, "reason": "invalid_input"}
    rgb_small, resize_scale = _resize_for_coin_detection(rgb)
    gray = cv2.cvtColor(rgb_small, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 1.5)
    h, w = gray.shape[:2]
    min_r = max(8, int(min(h, w) * 0.03))
    max_r = max(min_r + 4, int(min(h, w) * 0.24))

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=max(16, int(min(h, w) * 0.1)),
        param1=120,
        param2=20,
        minRadius=min_r,
        maxRadius=max_r,
    )
    if circles is None:
        edges = cv2.Canny(blurred, 60, 160)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:MAX_CONTOURS_EVAL]
        hsv_fallback = cv2.cvtColor(rgb_small, cv2.COLOR_RGB2HSV)
        best_d = None
        best_score = float("-inf")
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area <= 20:
                continue
            perimeter = cv2.arcLength(cnt, True)
            if perimeter <= 0:
                continue
            circularity = (4.0 * np.pi * area) / (perimeter * perimeter)
            if circularity < 0.65:
                continue
            (cx, cy), radius = cv2.minEnclosingCircle(cnt)
            if radius < min_r or radius > max_r:
                continue
            mean_s, mean_v = _mean_hsv_in_contour(hsv_fallback, cnt)
            score = circularity + (mean_v / 255.0) - (mean_s / 255.0)
            if score > best_score:
                best_score = score
                best_d = 2.0 * float(radius)
        if best_d is None:
            # Final fallback: bright, low-saturation blobs approximating a coin.
            sat = hsv_fallback[:, :, 1]
            val = hsv_fallback[:, :, 2]
            metallic_mask = np.logical_and(sat < 55, val > 150).astype(np.uint8) * 255
            metallic_mask = cv2.morphologyEx(
                metallic_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            contours2, _ = cv2.findContours(metallic_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours2 = sorted(contours2, key=cv2.contourArea, reverse=True)[:MAX_CONTOURS_EVAL]
            best_d2 = None
            best_score2 = float("-inf")
            for cnt in contours2:
                area = cv2.contourArea(cnt)
                if area <= 20:
                    continue
                perimeter = cv2.arcLength(cnt, True)
                if perimeter <= 0:
                    continue
                circularity = (4.0 * np.pi * area) / (perimeter * perimeter)
                if circularity < 0.55:
                    continue
                (_, _), radius = cv2.minEnclosingCircle(cnt)
                if radius < min_r or radius > max_r:
                    continue
                score = circularity + min(1.0, area / (np.pi * radius * radius + 1e-6))
                if score > best_score2:
                    best_score2 = score
                    best_d2 = 2.0 * float(radius)
            if best_d2 is None:
                return None, {"coin_detected": False, "reason": "no_circle"}
            best_d2 = best_d2 / resize_scale
            return best_d2, {
                "coin_detected": True,
                "reason": "metallic_blob_fallback",
                "coin_diameter_px": float(best_d2),
                "metallic_score": float(best_score2),
                "resized_for_detection": resize_scale != 1.0,
            }
        best_d = best_d / resize_scale
        return best_d, {
            "coin_detected": True,
            "reason": "contour_fallback",
            "coin_diameter_px": float(best_d),
            "metallic_score": float(best_score),
            "resized_for_detection": resize_scale != 1.0,
        }

    hsv = cv2.cvtColor(rgb_small, cv2.COLOR_RGB2HSV)
    best_score = float("-inf")
    best_d = None
    best_meta: dict[str, Any] = {}
    for c in circles[0]:
        cx, cy, r = float(c[0]), float(c[1]), float(c[2])
        if r <= 0:
            continue
        x0 = max(0, int(cx - r))
        y0 = max(0, int(cy - r))
        x1 = min(w, int(cx + r + 1))
        y1 = min(h, int(cy + r + 1))
        if x1 <= x0 or y1 <= y0:
            continue
        roi_hsv = hsv[y0:y1, x0:x1]
        yy, xx = np.ogrid[y0:y1, x0:x1]
        circle_mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
        if not np.any(circle_mask):
            continue
        mean_s = float(np.mean(roi_hsv[:, :, 1][circle_mask]))
        mean_v = float(np.mean(roi_hsv[:, :, 2][circle_mask]))
        center_dist = ((cx - (w / 2.0)) ** 2 + (cy - (h / 2.0)) ** 2) ** 0.5
        center_penalty = center_dist / ((w ** 2 + h ** 2) ** 0.5 + 1e-6)
        metallic_score = (mean_v / 255.0) - (mean_s / 255.0) - center_penalty
        if metallic_score > best_score:
            best_score = metallic_score
            best_d = 2.0 * r
            best_meta = {"mean_s": mean_s, "mean_v": mean_v, "metallic_score": metallic_score}

    if best_d is None:
        return None, {"coin_detected": False, "reason": "no_valid_circle"}
    best_d = best_d / resize_scale
    return best_d, {
        "coin_detected": True,
        "reason": "hough_circle",
        "coin_diameter_px": float(best_d),
        "resized_for_detection": resize_scale != 1.0,
        **best_meta,
    }


def calibrate_px_per_mm(
    rgb: np.ndarray,
    *,
    coin_diameter_mm: float | None = None,
) -> tuple[float | None, dict[str, Any]]:
    """
    Estimate px_per_mm using a detected coin.

    Returns (px_per_mm, diagnostics).
    """
    coin_mm = coin_diameter_mm or float(getattr(config, "COIN_5P_DIAMETER_MM", 18.0))
    if coin_mm <= 0:
        return None, {"coin_detected": False, "reason": "invalid_coin_mm"}
    diameter_px, diag = _detect_coin_diameter_px(rgb)
    if diameter_px is None or diameter_px <= 0:
        return None, diag
    px_per_mm = float(diameter_px) / coin_mm
    quality = "high" if px_per_mm >= 2.0 else "medium"
    out = dict(diag)
    out["coin_diameter_mm"] = coin_mm
    out["px_per_mm"] = px_per_mm
    out["scale_quality"] = quality
    return px_per_mm, out
