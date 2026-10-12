import sqlite3
from datetime import datetime, timezone
from app.core.config import get_settings

settings = get_settings()

def init_db():
    settings.audit_db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.audit_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            question TEXT,
            source_used TEXT,
            trace TEXT
        )
    """)
    conn.commit()
    conn.close()

def write_audit(question: str, source_used: str, trace: list):
    conn = sqlite3.connect(settings.audit_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_logs (created_at, question, source_used, trace) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), question, source_used, str(trace))
    )
    conn.commit()
    conn.close()