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
    comparison = compare_metrics(m_a, m_b, scale_mm=scale_mm)
    metrics = {
        "image_a": m_a,
        "image_b": m_b,
        "area_change_percent": comparison["area_change_percent"],
        "diam_change_px": comparison["diam_change_px"],
        "diam_change_mm": comparison.get("diam_change_mm"),
        "irregularity_delta": comparison["irregularity_delta"],
        "color_deltaE": comparison["color_deltaE"],
        "scale_available": comparison["scale_available"],
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
