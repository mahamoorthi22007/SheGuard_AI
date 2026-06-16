# app/database.py
import sqlite3
import json
from datetime import datetime

DB_FILE = "location_tracking_history.db"

def init_db():
    """Creates the persistent history tables if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spatial_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            threat_score INTEGER NOT NULL,
            assessment_meta TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_breadcrumb(user_id: str, lat: float, lon: float, score: int, meta: dict):
    """Inserts a fresh live location record into permanent disk storage."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO spatial_history (user_id, timestamp, latitude, longitude, threat_score, assessment_meta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, datetime.utcnow().isoformat(), lat, lon, score, json.dumps(meta)))
    conn.commit()
    conn.close()

def fetch_user_history(user_id: str):
    """Retrieves all historical tracking records for a specific device user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, latitude, longitude, threat_score, assessment_meta 
        FROM spatial_history WHERE user_id = ? ORDER BY timestamp DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "timestamp": r[0],
            "latitude": r[1],
            "longitude": r[2],
            "threat_score": r[3],
            "assessment": json.loads(r[4])
        } for r in rows
    ]