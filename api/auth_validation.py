"""Shared validation for registration, login, and password reset."""

import re

# Aligned with client/src/utils/validation.ts
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
SPECIAL_CHAR_PATTERN = re.compile(r'[!@#$%^&*(),.?":{}|<>\[\]\\/_\-+=]')


def normalize_phone(phone: str) -> str:
    """Digits only for storage and matching."""
    return re.sub(r"\D", "", (phone or "").strip())


def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_PATTERN.match(email.strip()))


def is_valid_password(password: str) -> bool:
    """More than 6 characters and at least one special character."""
    if not password or len(password) <= 6:
        return False
    return bool(SPECIAL_CHAR_PATTERN.search(password))
