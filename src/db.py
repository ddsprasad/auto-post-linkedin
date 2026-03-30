"""
SQLite-based post history tracker.
Tracks what has been posted to avoid duplicates and maintain series continuity.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "posts.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                posted_at   TEXT NOT NULL,
                topic_key   TEXT NOT NULL,
                post_type   TEXT NOT NULL,
                subtopic    TEXT NOT NULL,
                content     TEXT NOT NULL,
                linkedin_id TEXT,
                status      TEXT NOT NULL DEFAULT 'published'
            )
        """)
        conn.commit()


def record_post(
    topic_key: str,
    post_type: str,
    subtopic: str,
    content: str,
    linkedin_id: str | None = None,
    status: str = "published",
) -> int:
    """Insert a post record and return its ID."""
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO posts (posted_at, topic_key, post_type, subtopic, content, linkedin_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (datetime.utcnow().isoformat(), topic_key, post_type, subtopic, content, linkedin_id, status),
        )
        conn.commit()
        return cursor.lastrowid


def get_post_count(topic_key: str | None = None) -> int:
    """Return number of posts recorded. If topic_key given, count only that topic."""
    with _connect() as conn:
        if topic_key:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM posts WHERE topic_key = ?",
                (topic_key,),
            ).fetchone()
        else:
            row = conn.execute("SELECT COUNT(*) as cnt FROM posts").fetchone()
        return row["cnt"]


def get_recent_subtopics(topic_key: str, limit: int = 5) -> list[str]:
    """Return the most recently used subtopics for a given topic."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT subtopic FROM posts
            WHERE topic_key = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (topic_key, limit),
        ).fetchall()
        return [r["subtopic"] for r in rows]


def get_last_post() -> dict | None:
    """Return the most recent post record as a dict."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM posts ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


def was_posted_today(topic_key: str | None = None) -> bool:
    """Return True if a post was already made today (UTC) for the given topic (or any topic)."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    with _connect() as conn:
        if topic_key:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM posts WHERE posted_at LIKE ? AND topic_key = ? AND status = 'published'",
                (f"{today}%", topic_key),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM posts WHERE posted_at LIKE ? AND status = 'published'",
                (f"{today}%",),
            ).fetchone()
        return row["cnt"] > 0
