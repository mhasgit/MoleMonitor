"""Rule-based decision engine: thresholds, Decision, confidence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import config


class Action(Enum):
    NONE = "NONE"
    MONITOR = "MONITOR"
    RECOMMEND_REVIEW = "RECOMMEND_REVIEW"


class Confidence(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class Decision:
    action: Action
    confidence: Confidence
    triggered_rules: list[str]
    summary_reason: str


def _compute_confidence(
    quality_a: dict[str, Any],
    quality_b: dict[str, Any],
    seg_quality_a: dict[str, Any],
    seg_quality_b: dict[str, Any],
    scale_available: bool,
) -> Confidence:
    issues = 0
    if quality_a.get("low_sharpness") or quality_b.get("low_sharpness"):
        issues += 1
    if quality_a.get("exposure_warning") or quality_b.get("exposure_warning"):
        issues += 1
    if seg_quality_a.get("too_small") or seg_quality_b.get("too_small"):
        issues += 1
    if not scale_available:
        issues += 1
    if issues >= 2:
        return Confidence.LOW
    if issues == 1:
        return Confidence.MEDIUM
    return Confidence.HIGH


def decide(
    metrics: dict[str, Any],
    quality_a: dict[str, Any],
    quality_b: dict[str, Any],
    seg_quality_a: dict[str, Any],
    seg_quality_b: dict[str, Any],
) -> Decision:
    """Rule-based decision. Confidence from quality + mask + scale."""
    scale_available = metrics.get("scale_available", False)
    confidence = _compute_confidence(
        quality_a, quality_b, seg_quality_a, seg_quality_b, scale_available
    )
    diam_mm_thresh = getattr(config, "DIAMETER_INCREASE_MM_THRESHOLD", 1.0)
    area_thresh = getattr(config, "AREA_CHANGE_PERCENT_THRESHOLD", 20.0)
    color_thresh = getattr(config, "COLOR_DELTAE_THRESHOLD", 6.0)
    irr_thresh = getattr(config, "IRREGULARITY_DELTA_THRESHOLD", 2.0)
    triggered: list[str] = []
    action = Action.NONE
    if confidence == Confidence.LOW:
        return Decision(
            action=Action.NONE,
            confidence=confidence,
            triggered_rules=[],
            summary_reason="Results are uncertain due to image quality or missing scale. Consider retaking photos with consistent lighting and a reference scale.",
        )
    diam_change_mm = metrics.get("diam_change_mm")
    if diam_change_mm is not None and scale_available and diam_change_mm >= diam_mm_thresh:
        triggered.append("diameter_increase_mm")
        action = Action.RECOMMEND_REVIEW
    area_change = metrics.get("area_change_percent") or 0
    if abs(area_change) >= area_thresh:
        triggered.append("area_change_percent")
        if abs(area_change) >= area_thresh * 1.5:
            action = Action.RECOMMEND_REVIEW
        elif action == Action.NONE:
            action = Action.MONITOR
    color_delta = metrics.get("color_deltaE") or 0
    if color_delta >= color_thresh and action != Action.RECOMMEND_REVIEW:
        triggered.append("color_deltaE")
        if action == Action.NONE:
            action = Action.MONITOR
        if color_delta >= color_thresh * 1.2:
            action = Action.RECOMMEND_REVIEW
    irr_delta = abs(metrics.get("irregularity_delta") or 0)
    if irr_delta >= irr_thresh and action != Action.RECOMMEND_REVIEW:
        triggered.append("irregularity_delta")
        if action == Action.NONE:
            action = Action.MONITOR
    if action == Action.NONE and not triggered:
        summary_reason = "No significant change detected by this tool."
    elif action == Action.RECOMMEND_REVIEW:
        summary_reason = "One or more changes suggest professional review: " + ", ".join(triggered)
    elif action == Action.MONITOR:
        summary_reason = "Some changes detected; consider monitoring: " + ", ".join(triggered)
    else:
        summary_reason = "No significant change detected by this tool."
    return Decision(
        action=action,
        confidence=confidence,
        triggered_rules=triggered,
        summary_reason=summary_reason,
    )


def decision_to_dict(d: Decision) -> dict[str, Any]:
    return {
        "action": d.action.value,
        "confidence": d.confidence.value,
        "triggered_rules": d.triggered_rules,
        "summary_reason": d.summary_reason,
    }


def dict_to_decision(data: dict[str, Any]) -> Decision:
    return Decision(
        action=Action(data.get("action", "NONE")),
        confidence=Confidence(data.get("confidence", "MEDIUM")),
        triggered_rules=list(data.get("triggered_rules") or []),
        summary_reason=str(data.get("summary_reason", "")),
    )
