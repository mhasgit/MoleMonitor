"""SQLite database: schema, init, and pair CRUD. Images stored on filesystem; DB holds paths."""

import sqlite3
from pathlib import Path
from typing import Any

from src import config


def _project_root() -> Path:
    """Project root (folder containing app.py)."""
    return Path(__file__).resolve().parent.parent.parent


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
    """Return all pairs, newest first. Keys: id, pair_name, filename_a, filename_b, path_a, path_b, created_at."""
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


def clear_pairs() -> None:
    """Delete all pairs from DB. Does not delete image files."""
    init_db()
    conn = sqlite3.connect(str(_db_path()))
    try:
        conn.execute("DELETE FROM pairs")
        conn.commit()
    finally:
        conn.close()
