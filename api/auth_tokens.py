"""JWT access and password-reset tokens."""

from __future__ import annotations

import time

import jwt

import config

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_RESET = "reset"


def encode_access_token(user_id: int) -> str:
    now = int(time.time())
    # PyJWT 2.x requires "sub" to be a string (RFC 7519 string subject).
    return jwt.encode(
        {
            "sub": str(user_id),
            "typ": TOKEN_TYPE_ACCESS,
            "exp": now + config.JWT_ACCESS_EXPIRATION_SECONDS,
        },
        config.JWT_SECRET,
        algorithm="HS256",
    )


def encode_reset_token(user_id: int) -> str:
    now = int(time.time())
    return jwt.encode(
        {
            "sub": str(user_id),
            "typ": TOKEN_TYPE_RESET,
            "exp": now + config.JWT_RESET_EXPIRATION_SECONDS,
        },
        config.JWT_SECRET,
        algorithm="HS256",
    )


def decode_token(token: str, expected_type: str) -> int | None:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        if payload.get("typ") != expected_type:
            return None
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (jwt.PyJWTError, TypeError, ValueError):
        return None
