-- MoleMonitor SQLite Schema
-- For use with GraphMyDB and other ER diagram tools

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    pair_name TEXT NOT NULL,
    filename_a TEXT NOT NULL,
    filename_b TEXT NOT NULL,
    path_a TEXT NOT NULL,
    path_b TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE comparison_reports (
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
