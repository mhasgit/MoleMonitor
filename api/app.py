"""Flask API for MoleMonitor backend."""

import base64
import json
import os
import sqlite3
from io import BytesIO
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

import auth_tokens
import auth_validation
import config
import database
import supabase_mailer
from compare import run_pipeline
from compare.reporting import snapshot_to_dict
from utils import images
from viz import overlays as viz_overlays


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, origins=os.environ.get("CORS_ORIGINS", "*").split(","))
    database.init_db()

    def _get_auth_user_id() -> int | None:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth[7:].strip()
        if not token:
            return None
        return auth_tokens.decode_token(token, auth_tokens.TOKEN_TYPE_ACCESS)

    def _pair_public_dict(p: dict) -> dict:
        return {
            "id": p["id"],
            "pair_name": p["pair_name"],
            "filename_a": p["filename_a"],
            "filename_b": p["filename_b"],
            "path_a": p["path_a"],
            "path_b": p["path_b"],
            "created_at": p["created_at"],
        }

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

    def _build_reset_redirect_url(reset_token: str) -> str:
        base = config.PASSWORD_RESET_REDIRECT_URL
        parts = urlsplit(base)
        q = dict(parse_qsl(parts.query, keep_blank_values=True))
        q["reset_token"] = reset_token
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q), parts.fragment))

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/api/auth/register", methods=["POST"])
    def auth_register():
        data = request.get_json() or {}
        full_name = (data.get("full_name") or "").strip()
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""
        if not full_name:
            return jsonify({"error": "Full name is required"}), 400
        if not auth_validation.is_valid_email(email):
            return jsonify({"error": "Invalid email address"}), 400
        if not auth_validation.is_valid_password(password):
            return jsonify(
                {"error": "Password must be more than 6 characters and include a special character"}
            ), 400
        if database.get_user_by_email(email):
            return jsonify({"error": "An account with this email already exists"}), 409
        pw_hash = generate_password_hash(password)
        try:
            user_id = database.insert_user(full_name, email, pw_hash, pw_hash)
        except sqlite3.IntegrityError:
            return jsonify({"error": "Could not create account"}), 409
        # Keep Supabase Auth in sync so recovery emails can be sent later.
        try:
            supabase_mailer.ensure_auth_user(email, password)
        except RuntimeError as exc:
            app.logger.warning("Supabase auth user sync failed for %s: %s", email, exc)
        return (
            jsonify({"ok": True, "message": "Account created."}),
            201,
        )

    @app.route("/api/auth/login", methods=["POST"])
    def auth_login():
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        user = database.get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid email or password"}), 401
        row = database.get_user_by_id(user["id"])
        token = auth_tokens.encode_access_token(user["id"])
        return jsonify(
            {
                "token": token,
                "user": {
                    "id": row["id"],
                    "email": row["email"],
                    "full_name": row["full_name"],
                },
            }
        )

    @app.route("/api/auth/me", methods=["GET"])
    def auth_me():
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        user = database.get_user_by_id(uid)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        return jsonify(
            {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
            }
        )

    @app.route("/api/auth/forgot/verify-email", methods=["POST"])
    def auth_forgot_verify_email():
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        if not auth_validation.is_valid_email(email):
            return jsonify({"error": "Enter a valid email address"}), 400
        user = database.get_user_by_email(email)
        if user:
            reset_token = auth_tokens.encode_reset_token(user["id"])
            redirect_url = _build_reset_redirect_url(reset_token)
            try:
                # Backfill Supabase Auth users for accounts created before sync was added.
                supabase_mailer.ensure_auth_user(email)
                supabase_mailer.send_password_reset_email(email, redirect_url)
            except RuntimeError as exc:
                msg = str(exc).lower()
                if "429" in str(exc) or "over_email_send_rate_limit" in msg:
                    app.logger.warning("Password reset rate limited for %s", email)
                    return jsonify(
                        {
                            "error": (
                                "Too many reset emails were sent from this project. "
                                "Wait several minutes (or up to an hour on free tiers), then try again."
                            )
                        }
                    ), 429
                app.logger.exception("Password reset email send failed for %s: %s", email, exc)
                return jsonify({"error": "Could not send reset email. Please try again."}), 500
        # Use neutral messaging to avoid account enumeration.
        return jsonify({"ok": True, "message": "If an account exists for this email, a reset link has been sent."})

    @app.route("/api/auth/forgot/reset", methods=["POST"])
    def auth_forgot_reset():
        data = request.get_json() or {}
        reset_token = (data.get("reset_token") or "").strip()
        new_password = data.get("new_password") or ""
        if not reset_token:
            return jsonify({"error": "Reset token is required"}), 400
        uid = auth_tokens.decode_token(reset_token, auth_tokens.TOKEN_TYPE_RESET)
        if uid is None:
            return jsonify({"error": "Invalid or expired reset link"}), 400
        if not auth_validation.is_valid_password(new_password):
            return jsonify(
                {"error": "Password must be more than 6 characters and include a special character"}
            ), 400
        database.update_user_password(uid, generate_password_hash(new_password))
        return jsonify({"ok": True})

    @app.route("/api/pairs", methods=["GET"])
    def list_pairs():
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        pairs = database.get_pairs(uid)
        out = [_pair_public_dict(p) for p in pairs]
        return jsonify(out)

    @app.route("/api/pairs", methods=["POST"])
    def create_pair():
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
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
        rows = database.get_pairs(uid)
        n = len(rows) + 1
        label = pair_name or f"Pair {n}"
        pair_id = database.insert_pair(
            pair_name=label,
            filename_a=name_a,
            filename_b=name_b,
            path_a=path_a,
            path_b=path_b,
            user_id=uid,
        )
        return jsonify({"id": pair_id, "pair_name": label})

    @app.route("/api/pairs/<int:pair_id>", methods=["GET"])
    def get_pair(pair_id):
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        p = database.get_pair_by_id(pair_id, user_id=uid)
        if not p:
            return jsonify({"error": "Pair not found"}), 404
        return jsonify(_pair_public_dict(p))

    @app.route("/api/pairs/<int:pair_id>", methods=["DELETE"])
    def delete_pair(pair_id):
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        if not database.delete_pair(pair_id, uid):
            return jsonify({"error": "Pair not found"}), 404
        return jsonify({"ok": True})

    @app.route("/api/pairs", methods=["DELETE"])
    def clear_pairs():
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        database.clear_pairs(uid)
        return jsonify({"ok": True})

    @app.route("/api/compare", methods=["POST"])
    def compare():
        if _get_auth_user_id() is None:
            return jsonify({"error": "Unauthorized"}), 401
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
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        if not database.get_pair_by_id(pair_id, user_id=uid):
            return jsonify({"error": "Pair not found"}), 404
        reports = database.get_reports_for_pair(pair_id)
        return jsonify([dict(r) for r in reports])

    @app.route("/api/pairs/<int:pair_id>/reports", methods=["POST"])
    def create_report(pair_id):
        uid = _get_auth_user_id()
        if uid is None:
            return jsonify({"error": "Unauthorized"}), 401
        if not database.get_pair_by_id(pair_id, user_id=uid):
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
    port = int(os.environ.get("PORT", 5000))
    _debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    # use_reloader reloads routes when you edit app.py (set FLASK_DEBUG=1 for local dev)
    app.run(host="0.0.0.0", port=port, debug=_debug, use_reloader=_debug)
