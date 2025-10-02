import sqlite3
from pathlib import Path
import threading
import time

DB_PATH = Path('database/mac_cleaner.db')
_LOCK = threading.Lock()

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS clean_runs (id INTEGER PRIMARY KEY, started_at TEXT, duration_sec REAL, space_freed_mb REAL, categories TEXT, mode TEXT)",
    "CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, created_at TEXT, type TEXT, level TEXT, message TEXT)",
    "CREATE TABLE IF NOT EXISTS malware_findings (id INTEGER PRIMARY KEY, scanned_at TEXT, path TEXT, signature TEXT, severity TEXT)"
]

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK, sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        for stmt in SCHEMA:
            cur.execute(stmt)
        conn.commit()


def record_clean_run(started_at, duration_sec, space_freed_mb, categories, mode):
    with _LOCK, sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO clean_runs (started_at, duration_sec, space_freed_mb, categories, mode) VALUES (?,?,?,?,?)",
            (started_at, duration_sec, space_freed_mb, ','.join(categories), mode)
        )
        conn.commit()


def record_alert(alert_type, level, message, created_at):
    with _LOCK, sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO alerts (created_at, type, level, message) VALUES (?,?,?,?)",
            (created_at, alert_type, level, message)
        )
        conn.commit()


def record_malware(path, signature, severity, scanned_at):
    with _LOCK, sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO malware_findings (scanned_at, path, signature, severity) VALUES (?,?,?,?)",
            (scanned_at, path, signature, severity)
        )
        conn.commit()


def stats_summary():
    with _LOCK, sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        summary = {}
        cur.execute("SELECT COUNT(*), COALESCE(SUM(space_freed_mb),0) FROM clean_runs")
        row = cur.fetchone()
        summary['total_runs'] = row[0]
        summary['total_space_freed_mb'] = row[1]
        cur.execute("SELECT COUNT(*) FROM malware_findings")
        summary['malware_detected'] = cur.fetchone()[0]
        return summary
