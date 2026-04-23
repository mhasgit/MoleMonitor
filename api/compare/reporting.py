"""Template-based reporting and ReportSnapshot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from compare.decision import Action, Confidence, Decision, decision_to_dict


DISCLAIMER = "This tool does not provide medical diagnosis. If you are concerned, seek professional advice."


@dataclass
class ReportSnapshot:
    created_at: str
    algo_version: str
    metrics: dict[str, Any]
    decision: dict[str, Any]
    message_text: str
    overlay_path: str | None = None
    mask_a_path: str | None = None
    mask_b_path: str | None = None


def build_message(decision: Decision, metrics: dict[str, Any]) -> str:
    """Build user-facing message from decision and metrics."""
    parts = []
    scale_available = metrics.get("scale_available", False)
    seg_a = (metrics.get("image_a") or {}).get("invalid_mask", False)
    seg_b = (metrics.get("image_b") or {}).get("invalid_mask", False)
    if decision.confidence == Confidence.LOW:
        parts.append("Results are uncertain due to image or segmentation quality.")
        if seg_a or seg_b:
            parts.append("At least one image had weak mole segmentation; retake with sharper focus and tighter framing.")
        else:
            parts.append("We recommend retaking photos with consistent lighting and, if possible, a visible 5p coin.")
        parts.append("")
    else:
        if decision.action == Action.NONE:
            parts.append("No significant change detected by this tool.")
        elif decision.action == Action.MONITOR:
            parts.append(decision.summary_reason)
        else:
            parts.append(decision.summary_reason)
    diam_change_mm = metrics.get("diam_change_mm")
    if isinstance(diam_change_mm, (int, float)):
        parts.append(f"Measured diameter change: {diam_change_mm:+.2f} mm")
    elif not scale_available:
        parts.append("Measured diameter change: unavailable (scale not detected)")
    parts.append("")
    parts.append(DISCLAIMER)
    return "\n".join(parts)


def build_snapshot(
    decision: Decision,
    metrics: dict[str, Any],
    algo_version: str,
    overlay_path: str | None = None,
    mask_a_path: str | None = None,
    mask_b_path: str | None = None,
) -> ReportSnapshot:
    """Build ReportSnapshot with generated message_text."""
    created_at = datetime.now(timezone.utc).isoformat()
    decision_dict = decision_to_dict(decision)
    message_text = build_message(decision, metrics)
    return ReportSnapshot(
        created_at=created_at,
        algo_version=algo_version,
        metrics=metrics,
        decision=decision_dict,
        message_text=message_text,
        overlay_path=overlay_path,
        mask_a_path=mask_a_path,
        mask_b_path=mask_b_path,
    )


def snapshot_to_dict(s: ReportSnapshot) -> dict[str, Any]:
    return {
        "created_at": s.created_at,
        "algo_version": s.algo_version,
        "metrics": s.metrics,
        "decision": s.decision,
        "message_text": s.message_text,
        "overlay_path": s.overlay_path,
        "mask_a_path": s.mask_a_path,
        "mask_b_path": s.mask_b_path,
    }


def dict_to_snapshot(d: dict[str, Any]) -> ReportSnapshot:
    return ReportSnapshot(
        created_at=d["created_at"],
        algo_version=d["algo_version"],
        metrics=d.get("metrics") or {},
        decision=d.get("decision") or {},
        message_text=d["message_text"],
        overlay_path=d.get("overlay_path"),
        mask_a_path=d.get("mask_a_path"),
        mask_b_path=d.get("mask_b_path"),
    )
