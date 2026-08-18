"""
db.py — SQLite storage layer for the Job Tracker.
Handles schema creation, inserts (with de-duplication), and queries.
"""
import sqlite3
from contextlib import contextmanager

DB_PATH = "jobs.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                category TEXT,
                url TEXT,
                published_at TEXT,
                description TEXT,
                status TEXT DEFAULT 'New',   -- New / Interested / Applied / Rejected / Offer
                fetched_at TEXT DEFAULT (datetime('now'))
            )
        """)


def upsert_jobs(jobs: list[dict]) -> int:
    """Insert new jobs, ignore ones already saved (by id). Returns count of new rows added."""
    added = 0
    with get_conn() as conn:
        for job in jobs:
            cur = conn.execute(
                "INSERT OR IGNORE INTO jobs (id, title, company, location, category, url, published_at, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    job["id"], job["title"], job["company"], job["location"],
                    job["category"], job["url"], job["published_at"], job["description"],
                ),
            )
            added += cur.rowcount
    return added


def fetch_jobs(keyword: str = "", status: str = "All", location: str = "All") -> list[sqlite3.Row]:
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    if keyword:
        query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        like = f"%{keyword}%"
        params += [like, like, like]
    if status != "All":
        query += " AND status = ?"
        params.append(status)
    if location != "All":
        query += " AND location = ?"
        params.append(location)
    query += " ORDER BY published_at DESC"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


def get_distinct_locations() -> list[str]:
    """Returns every distinct 'candidate required location' currently saved, for the country/location filter dropdown."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT location FROM jobs WHERE location IS NOT NULL AND location != '' ORDER BY location"
        ).fetchall()
    return [r["location"] for r in rows]


def update_status(job_id: str, new_status: str):
    with get_conn() as conn:
        conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))


def stats() -> dict:
    with get_conn() as conn:
        rows = conn.execute("SELECT status, COUNT(*) as c FROM jobs GROUP BY status").fetchall()
    return {r["status"]: r["c"] for r in rows}
