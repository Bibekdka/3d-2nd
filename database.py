import sqlite3
import pandas as pd
import os

DB_PATH = "brain.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def check_connection():
    try:
        conn = get_conn()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        print("DB ERROR:", e)
        return False

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            source TEXT,
            details TEXT,
            amount REAL,
            summary TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_entry(type_, source, details, amount, summary, tags):
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO history (type, source, details, amount, summary, tags) VALUES (?, ?, ?, ?, ?, ?)",
            (type_, source, details, amount, summary, tags)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def load_history():
    try:
        conn = get_conn()
        df = pd.read_sql("SELECT * FROM history ORDER BY created_at DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def get_db_stats():
    """Returns basic stats about the history."""
    try:
        df = load_history()
        if df.empty: return {"total": 0, "success_rate": 0, "top_tags": []}
        return {"total": len(df)}
    except:
        return {"total": 0}
