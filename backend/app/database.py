import sqlite3
import os
from datetime import datetime
from backend.app.config import settings

DB_PATH = os.path.join(settings.BASE_DIR, "healthbridge.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS triage_sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT,
            symptoms_text TEXT,
            predicted_condition TEXT,
            urgency_level TEXT,
            red_flag_triggered INTEGER,
            feedback_outcome TEXT,
            consent_given INTEGER
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS privacy_log (
            session_id TEXT PRIMARY KEY,
            timestamp TEXT,
            action TEXT,
            details TEXT
        )
        """)
        conn.commit()

def log_triage_session(session_id: str, symptoms_text: str, predicted_condition: str, urgency_level: str, red_flag_triggered: bool, consent_given: bool):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO triage_sessions 
        (session_id, created_at, symptoms_text, predicted_condition, urgency_level, red_flag_triggered, consent_given)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(session_id), str(datetime.now().isoformat()), str(symptoms_text), str(predicted_condition), str(urgency_level), 1 if red_flag_triggered else 0, 1 if consent_given else 0))
        conn.commit()

def delete_session_record(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM triage_sessions WHERE session_id = ?", (str(session_id),))
        cursor.execute("""
        INSERT OR REPLACE INTO privacy_log (session_id, timestamp, action, details)
        VALUES (?, ?, ?, ?)
        """, (str(session_id), str(datetime.now().isoformat()), "ERASURE_EXECUTE", "Session data permanently deleted under DPDP Act 2023"))
        conn.commit()

# Initialize database
init_db()
