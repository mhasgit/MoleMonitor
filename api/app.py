"""Flask API for MoleMonitor backend."""

import base64
import json
import os
from io import BytesIO

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import config
import database
from compare import run_pipeline
from compare.reporting import snapshot_to_dict
from utils import images
from viz import overlays as viz_overlays


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, origins=os.environ.get("CORS_ORIGINS", "*").split(","))
    database.init_db()

    def _decode_image(field: str):
        f = request.files.get(field)
        if not f:
            return None
        data = f.read()
        return images.load_image_from_bytes(data)

    def _encode_image(arr) -> str | None:
        if arr is None:
            return None
        from PIL import Image
        buf = BytesIO()
        Image.fromarray(arr).save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/api/pairs", methods=["GET"])
    def list_pairs():
        pairs = database.get_pairs()
        out = [
            {
                "id": p["id"],
                "pair_name": p["pair_name"],
                "filename_a": p["filename_a"],
                "filename_b": p["filename_b"],
                "path_a": p["path_a"],
                "path_b": p["path_b"],
                "created_at": p["created_at"],
            }
            for p in pairs
        ]
        return jsonify(out)

    @app.route("/api/pairs", methods=["POST"])
    def create_pair():
        img_a = _decode_image("image_a")
        img_b = _decode_image("image_b")
        if img_a is None or img_b is None:
            return jsonify({"error": "Both image_a and image_b files are required"}), 400
        pair_name = (request.form.get("pair_name") or "").strip() or None
        name_a = request.form.get("filename_a") or "upload"
        name_b = request.form.get("filename_b") or "upload"
        path_a = images.save_image_to_uploads(img_a, "a")
        path_b = images.save_image_to_uploads(img_b, "b")
        if not path_a or not path_b:
            return jsonify({"error": "Failed to save images"}), 500
        rows = database.get_pairs()
        n = len(rows) + 1
        label = pair_name or f"Pair {n}"
        pair_id = database.insert_pair(
            pair_name=label,
            filename_a=name_a,
            filename_b=name_b,
            path_a=path_a,
            path_b=path_b,
        )
        return jsonify({"id": pair_id, "pair_name": label})

    @app.route("/api/pairs/<int:pair_id>", methods=["GET"])
    def get_pair(pair_id):
        p = database.get_pair_by_id(pair_id)
        if not p:
            return jsonify({"error": "Pair not found"}), 404
        return jsonify(dict(p))

    @app.route("/api/pairs/<int:pair_id>", methods=["DELETE"])
    def delete_pair(pair_id):
        p = database.get_pair_by_id(pair_id)
        if not p:
            return jsonify({"error": "Pair not found"}), 404
        database.delete_pair(pair_id)
        return jsonify({"ok": True})

    @app.route("/api/pairs", methods=["DELETE"])
    def clear_pairs():
        database.clear_pairs()
        return jsonify({"ok": True})

    @app.route("/api/compare", methods=["POST"])
    def compare():
        img_a = _decode_image("image_a")
        img_b = _decode_image("image_b")
        if img_a is None or img_b is None:
            return jsonify({"error": "Both image_a and image_b are required"}), 400
        try:
            scale_mm = request.form.get("scale_mm", type=float)
            if scale_mm is not None and scale_mm <= 0:
                scale_mm = None
            use_clahe = request.form.get("use_clahe", "").lower() in ("1", "true", "yes")
            blur_kernel = request.form.get("blur_kernel_size", 0, type=int) or 0
            if blur_kernel and blur_kernel % 2 == 0:
                blur_kernel = max(1, blur_kernel - 1)
        except (TypeError, ValueError):
            scale_mm, use_clahe, blur_kernel = None, False, 0
        try:
            result = run_pipeline(
                img_a,
                img_b,
                scale_mm=scale_mm,
                use_clahe=use_clahe,
                blur_kernel_size=blur_kernel or 0,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Comparison failed: {e}"}), 500
        snap = result.snapshot
        out = snapshot_to_dict(snap)
        # Ensure metrics are JSON-serializable (no numpy)
        def sanitize(obj):
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [sanitize(x) for x in obj]
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj) if isinstance(obj, np.floating) else int(obj)
            return obj
        out["metrics"] = sanitize(out.get("metrics") or {})
        out["mask_a_b64"] = _encode_image(viz_overlays.mask_preview(result.mask_a))
        out["mask_b_b64"] = _encode_image(viz_overlays.mask_preview(result.mask_b))
        out["contour_a_b64"] = _encode_image(viz_overlays.contour_overlay(result.img_a_processed, result.mask_a))
        out["contour_b_b64"] = _encode_image(viz_overlays.contour_overlay(result.img_b_processed, result.mask_b))
        out["change_highlight_b64"] = _encode_image(
            viz_overlays.change_highlight_overlay(result.img_b_processed, result.mask_a, result.mask_b)
        )
        return jsonify(out)

    @app.route("/api/pairs/<int:pair_id>/reports", methods=["GET"])
    def list_reports(pair_id):
        if not database.get_pair_by_id(pair_id):
            return jsonify({"error": "Pair not found"}), 404
        reports = database.get_reports_for_pair(pair_id)
        return jsonify([dict(r) for r in reports])

    @app.route("/api/pairs/<int:pair_id>/reports", methods=["POST"])
    def create_report(pair_id):
        if not database.get_pair_by_id(pair_id):
            return jsonify({"error": "Pair not found"}), 404
        body = request.get_json() or {}
        snap = body.get("snapshot")
        if not snap:
            return jsonify({"error": "snapshot object required"}), 400
        report_id = database.insert_report(
            pair_id=pair_id,
            created_at=snap.get("created_at", ""),
            algo_version=snap.get("algo_version", ""),
            metrics_json=json.dumps(snap.get("metrics") or {}),
            decision_json=json.dumps(snap.get("decision") or {}),
            message_text=snap.get("message_text", ""),
            overlay_path=snap.get("overlay_path"),
            mask_a_path=snap.get("mask_a_path"),
            mask_b_path=snap.get("mask_b_path"),
        )
        return jsonify({"id": report_id})

    # Serve uploaded images (optional); basename-only to avoid path traversal
    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        from pathlib import Path
        root = Path(__file__).resolve().parent
        uploads = root / config.UPLOADS_DIR
        safe_name = os.path.basename(filename)
        return send_from_directory(str(uploads), safe_name)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG", "0") == "1")
