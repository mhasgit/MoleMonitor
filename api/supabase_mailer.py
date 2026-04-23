"""Helpers for syncing users and sending recovery emails via Supabase Auth REST API."""

from __future__ import annotations

import json
import logging
import secrets
from urllib import request
from urllib.error import HTTPError, URLError

import config

logger = logging.getLogger(__name__)


def _is_configured() -> bool:
    return bool(config.SUPABASE_URL and config.SUPABASE_SERVICE_ROLE_KEY)


def _request_json(path: str, payload: dict, *, allow_statuses: tuple[int, ...] = ()) -> dict:
    url = f"{config.SUPABASE_URL.rstrip('/')}{path}"
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=url,
        method="POST",
        data=body,
        headers={
            "apikey": config.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {config.SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8") if resp else ""
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        status = exc.code
        raw = exc.read().decode("utf-8", errors="ignore")
        if status in allow_statuses:
            try:
                return json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return {}
        raise RuntimeError(f"Supabase request failed ({status}): {raw}") from exc
    except URLError as exc:
        raise RuntimeError(f"Supabase request failed: {exc.reason}") from exc


def _signup_via_public_api(email: str, password: str) -> None:
    """Create a Supabase Auth user using the same public key as /recover (no service role)."""
    try:
        _request_json("/auth/v1/signup", {"email": email, "password": password})
        logger.info("Supabase Auth user created via signup for %s", email)
    except RuntimeError as exc:
        text = str(exc).lower()
        # Duplicate / already registered — safe to ignore.
        if any(
            s in text
            for s in (
                "user_already",
                "already registered",
                "already exists",
                "email address is already",
                "user already",
            )
        ):
            logger.info("Supabase signup skipped (user already exists) for %s", email)
            return
        raise


def ensure_auth_user(email: str, password: str | None = None) -> None:
    """Ensure a matching Supabase Auth user exists for recovery emails."""
    if not _is_configured():
        return
    chosen_password = password or secrets.token_urlsafe(24) + "!"
    try:
        _request_json(
            "/auth/v1/admin/users",
            {
                "email": email,
                "password": chosen_password,
                "email_confirm": True,
            },
            allow_statuses=(422,),
        )
        return
    except RuntimeError as exc:
        # If key is anon/publishable, admin endpoint is unauthorized — use public signup.
        if "(401)" not in str(exc) and "(403)" not in str(exc):
            raise
    try:
        _signup_via_public_api(email, chosen_password)
    except RuntimeError as signup_exc:
        logger.warning(
            "Supabase public signup failed for %s (recover may not send if no Auth user): %s",
            email,
            signup_exc,
        )


def send_password_reset_email(email: str, redirect_to: str) -> None:
    """Ask Supabase Auth to send a password recovery email."""
    if not _is_configured():
        parts: list[str] = []
        if not config.SUPABASE_URL.strip():
            parts.append("SUPABASE_URL (or VITE_SUPABASE_URL in client/.env)")
        if not config.SUPABASE_SERVICE_ROLE_KEY:
            parts.append("SUPABASE_SERVICE_ROLE_KEY (set in api/.env — never use the anon key here)")
        raise RuntimeError(
            "Supabase reset email is not configured. Missing: "
            + ", ".join(parts)
            + ". Restart the API after editing env files."
        )
    _request_json("/auth/v1/recover", {"email": email, "redirect_to": redirect_to})
    logger.info("Supabase /recover requested for %s (check inbox and spam)", email)
