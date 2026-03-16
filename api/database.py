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
                created_at TEXT NOT NULL
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


def get_pairs() -> list[dict[str, Any]]:
    """Return all pairs, newest first."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, pair_name, filename_a, filename_b, path_a, path_b, created_at FROM pairs ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_pair_by_id(pair_id: int) -> dict[str, Any] | None:
    """Return a single pair by id, or None if not found."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, pair_name, filename_a, filename_b, path_a, path_b, created_at FROM pairs WHERE id = ?",
            (pair_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def delete_pair(pair_id: int) -> None:
    """Delete a single pair by id. Does not delete image files."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.execute("DELETE FROM pairs WHERE id = ?", (pair_id,))
        conn.commit()
    finally:
        conn.close()


def clear_pairs() -> None:
    """Delete all pairs from DB. Does not delete image files."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.execute("DELETE FROM pairs")
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
