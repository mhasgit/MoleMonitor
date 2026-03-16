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
    if decision.confidence == Confidence.LOW:
        parts.append("Results are uncertain due to image quality or missing scale.")
        parts.append("We recommend retaking photos with consistent lighting and, if possible, a reference object for scale.")
        parts.append("")
    else:
        if decision.action == Action.NONE:
            parts.append("No significant change detected by this tool.")
        elif decision.action == Action.MONITOR:
            parts.append(decision.summary_reason)
        else:
            parts.append(decision.summary_reason)
        parts.append("")
        parts.append("In simple terms:")
        triggered = set(decision.triggered_rules or [])
        size_triggered = "area_change_percent" in triggered or "diameter_increase_mm" in triggered
        if size_triggered:
            if scale_available and metrics.get("diam_change_mm") is not None:
                d_mm = metrics["diam_change_mm"]
                if d_mm > 0:
                    parts.append("• Size: the newer image shows a slightly larger area than the older one.")
                else:
                    parts.append("• Size: the newer image shows a slightly smaller area than the older one.")
            else:
                area_ch = metrics.get("area_change_percent") or 0
                if area_ch > 0:
                    parts.append("• Size: the newer image shows a larger area than the older one. (Scale not available for exact measurements.)")
                else:
                    parts.append("• Size: the newer image shows a smaller area than the older one. (Scale not available for exact measurements.)")
        else:
            parts.append("• Size: about the same.")
        if "color_deltaE" in triggered:
            delta_e = metrics.get("color_deltaE") or 0
            if delta_e >= 6:
                parts.append("• Color: a noticeable color difference between the two images.")
            else:
                parts.append("• Color: a slight color difference between the two images.")
        else:
            parts.append("• Color: no notable change.")
        if "irregularity_delta" in triggered:
            parts.append("• Shape: the outline appears somewhat different between the two images.")
        else:
            parts.append("• Shape: similar in both images.")
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
