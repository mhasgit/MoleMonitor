"""SQLite database: schema, init, and pair CRUD. Images stored on filesystem; DB holds paths."""

import sqlite3
from pathlib import Path
from typing import Any

import config


def _project_root() -> Path:
    """Project root (api folder)."""
    return Path(__file__).resolve().parent


def _db_path() -> Path:
    return _project_root() / config.DB_PATH


def _migrate_users_columns(conn: sqlite3.Connection) -> None:
    """Add full_name and phone to existing users table if missing."""
    cur = conn.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cur.fetchall()}
    if "full_name" not in cols:
        conn.execute("ALTER TABLE users ADD COLUMN full_name TEXT NOT NULL DEFAULT ''")
    if "phone" not in cols:
        conn.execute("ALTER TABLE users ADD COLUMN phone TEXT")


def init_db() -> None:
    """Create data dirs and DB file; create tables if missing."""
    root = _project_root()
    (root / config.DATA_DIR).mkdir(parents=True, exist_ok=True)
    (root / config.UPLOADS_DIR).mkdir(parents=True, exist_ok=True)
    path = _db_path()
    conn = sqlite3.connect(str(path))
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                full_name TEXT NOT NULL DEFAULT '',
                phone TEXT
            );
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                pair_name TEXT NOT NULL,
                filename_a TEXT NOT NULL,
                filename_b TEXT NOT NULL,
                path_a TEXT NOT NULL,
                path_b TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS comparison_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair_id INTEGER NOT NULL REFERENCES pairs(id),
                created_at TEXT NOT NULL,
                algo_version TEXT NOT NULL,
                metrics_json TEXT NOT NULL,
                decision_json TEXT NOT NULL,
                message_text TEXT NOT NULL,
                overlay_path TEXT,
                mask_a_path TEXT,
                mask_b_path TEXT
            );
        """)
        _migrate_users_columns(conn)
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_users_phone_unique
            ON users(phone) WHERE phone IS NOT NULL AND phone != ''
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    """Return a connection to the DB file. Caller is responsible for closing."""
    init_db()
    return sqlite3.connect(str(_db_path()))


def insert_pair(
    pair_name: str,
    filename_a: str,
    filename_b: str,
    path_a: str,
    path_b: str,
    user_id: int | None = None,
) -> int:
    """Insert a pair row; return new id."""
    from datetime import datetime
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        cur = conn.execute(
            """INSERT INTO pairs (user_id, pair_name, filename_a, filename_b, path_a, path_b, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                pair_name,
                filename_a or "",
                filename_b or "",
                path_a,
                path_b,
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_pairs(user_id: int) -> list[dict[str, Any]]:
    """Return pairs for this user only, newest first."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT id, pair_name, filename_a, filename_b, path_a, path_b, created_at
               FROM pairs WHERE user_id = ? ORDER BY id DESC""",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_pair_by_id(pair_id: int, user_id: int | None = None) -> dict[str, Any] | None:
    """Return a single pair by id. If user_id is set, only if owned by that user."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        if user_id is not None:
            row = conn.execute(
                """SELECT id, user_id, pair_name, filename_a, filename_b, path_a, path_b, created_at
                   FROM pairs WHERE id = ? AND user_id = ?""",
                (pair_id, user_id),
            ).fetchone()
        else:
            row = conn.execute(
                """SELECT id, user_id, pair_name, filename_a, filename_b, path_a, path_b, created_at
                   FROM pairs WHERE id = ?""",
                (pair_id,),
            ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def delete_pair(pair_id: int, user_id: int) -> bool:
    """Delete a single pair if it belongs to user_id. Removes reports; does not delete image files."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        row = conn.execute(
            "SELECT id FROM pairs WHERE id = ? AND user_id = ?", (pair_id, user_id)
        ).fetchone()
        if not row:
            return False
        conn.execute("DELETE FROM comparison_reports WHERE pair_id = ?", (pair_id,))
        conn.execute("DELETE FROM pairs WHERE id = ? AND user_id = ?", (pair_id, user_id))
        conn.commit()
        return True
    finally:
        conn.close()


def clear_pairs(user_id: int) -> None:
    """Delete all pairs (and their reports) for this user. Does not delete image files."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.execute(
            """DELETE FROM comparison_reports WHERE pair_id IN
               (SELECT id FROM pairs WHERE user_id = ?)""",
            (user_id,),
        )
        conn.execute("DELETE FROM pairs WHERE user_id = ?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def insert_report(
    pair_id: int,
    created_at: str,
    algo_version: str,
    metrics_json: str,
    decision_json: str,
    message_text: str,
    overlay_path: str | None = None,
    mask_a_path: str | None = None,
    mask_b_path: str | None = None,
) -> int:
    """Insert a comparison report row; return new id."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        cur = conn.execute(
            """INSERT INTO comparison_reports
               (pair_id, created_at, algo_version, metrics_json, decision_json, message_text,
                overlay_path, mask_a_path, mask_b_path)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                pair_id,
                created_at,
                algo_version,
                metrics_json,
                decision_json,
                message_text,
                overlay_path,
                mask_a_path,
                mask_b_path,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_reports_for_pair(pair_id: int) -> list[dict[str, Any]]:
    """Return all reports for a pair, newest first."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT id, pair_id, created_at, algo_version, metrics_json, decision_json, message_text,
                      overlay_path, mask_a_path, mask_b_path
               FROM comparison_reports WHERE pair_id = ? ORDER BY created_at DESC""",
            (pair_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_report_by_id(report_id: int) -> dict[str, Any] | None:
    """Return a single report by id, or None if not found."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """SELECT id, pair_id, created_at, algo_version, metrics_json, decision_json, message_text,
                      overlay_path, mask_a_path, mask_b_path
               FROM comparison_reports WHERE id = ?""",
            (report_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def insert_user(
    full_name: str,
    email: str,
    phone: str,
    password_hash: str,
) -> int:
    """Insert a user; return new id. Email and phone must be unique (phone normalized)."""
    from datetime import datetime

    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        cur = conn.execute(
            """INSERT INTO users (email, password_hash, created_at, full_name, phone)
               VALUES (?, ?, ?, ?, ?)""",
            (
                email.strip().lower(),
                password_hash,
                datetime.utcnow().isoformat() + "Z",
                full_name.strip(),
                phone,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_user_by_email(email: str) -> dict[str, Any] | None:
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, email, password_hash, full_name, phone, created_at FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_phone(phone_normalized: str) -> dict[str, Any] | None:
    if not phone_normalized:
        return None
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, email, password_hash, full_name, phone, created_at FROM users WHERE phone = ?",
            (phone_normalized,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, email, full_name, phone, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_user_password(user_id: int, password_hash: str) -> None:
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
        conn.commit()
    finally:
        conn.close()
