"""Orchestrator: preprocess -> segment -> measure -> compare -> decision -> reporting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

import config
from compare.decision import decide
from compare.measure import compare_metrics, measure_single
from compare.preprocess import preprocess_pair
from compare.reporting import ReportSnapshot, build_snapshot
from compare.scale import calibrate_px_per_mm
from compare.segment import get_segmenter


@dataclass
class PipelineResult:
    """Result of run_pipeline: snapshot + masks/processed images for viz."""
    snapshot: ReportSnapshot
    mask_a: np.ndarray
    mask_b: np.ndarray
    img_a_processed: np.ndarray
    img_b_processed: np.ndarray


def run_pipeline(
    img_a: np.ndarray,
    img_b: np.ndarray,
    scale_mm: float | None = None,
    *,
    use_clahe: bool = False,
    blur_kernel_size: int = 0,
) -> PipelineResult:
    """
    Run full comparison pipeline. Returns PipelineResult.
    Raises ValueError on invalid inputs.
    """
    if img_a is None or img_b is None:
        raise ValueError("Both images are required")
    segmenter = get_segmenter()
    algo_version = getattr(config, "COMPARE_ALGO_VERSION", "phase1_heuristic_v1")
    a, b, quality_a, quality_b = preprocess_pair(
        img_a, img_b, use_clahe=use_clahe, blur_kernel_size=blur_kernel_size
    )
    mask_a, seg_quality_a = segmenter(a)
    mask_b, seg_quality_b = segmenter(b)
    m_a = measure_single(a, mask_a)
    m_b = measure_single(b, mask_b)
    try:
        auto_px_per_mm_a, scale_diag_a = calibrate_px_per_mm(a)
    except Exception as exc:
        auto_px_per_mm_a, scale_diag_a = None, {"coin_detected": False, "reason": f"scale_error:{exc}"}
    try:
        auto_px_per_mm_b, scale_diag_b = calibrate_px_per_mm(b)
    except Exception as exc:
        auto_px_per_mm_b, scale_diag_b = None, {"coin_detected": False, "reason": f"scale_error:{exc}"}
    manual_px_per_mm = scale_mm if scale_mm is not None and scale_mm > 0 else None
    detected_scales = [x for x in (auto_px_per_mm_a, auto_px_per_mm_b) if x is not None]
    if detected_scales:
        px_per_mm = float(np.median(np.array(detected_scales)))
        scale_source = "coin_detected"
    else:
        px_per_mm = manual_px_per_mm
        scale_source = "manual" if manual_px_per_mm else "none"
    comparison = compare_metrics(m_a, m_b, px_per_mm=px_per_mm)
    metrics = {
        "image_a": m_a,
        "image_b": m_b,
        "area_change_percent": comparison["area_change_percent"],
        "diam_change_px": comparison["diam_change_px"],
        "diam_change_mm": comparison.get("diam_change_mm"),
        "irregularity_delta": comparison["irregularity_delta"],
        "color_deltaE": comparison["color_deltaE"],
        "scale_available": comparison["scale_available"],
        "px_per_mm": comparison.get("px_per_mm"),
        "scale_source": scale_source,
        "scale_diagnostics": {
            "image_a": scale_diag_a,
            "image_b": scale_diag_b,
            "manual_px_per_mm": manual_px_per_mm,
        },
    }
    decision = decide(
        metrics,
        quality_a,
        quality_b,
        seg_quality_a,
        seg_quality_b,
    )
    snapshot = build_snapshot(decision, metrics, algo_version=algo_version)
    return PipelineResult(
        snapshot=snapshot,
        mask_a=mask_a,
        mask_b=mask_b,
        img_a_processed=a,
        img_b_processed=b,
    )
