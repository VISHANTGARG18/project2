"""
Thread-safe Database Connection Utility for Lumina Executive Platform.
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "lumina_retail.db")

def get_db_connection():
    """Returns a new SQLite connection with Foreign Keys enabled."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_query(query: str, params=None) -> pd.DataFrame:
    """Executes a SQL query and returns a pandas DataFrame."""
    conn = get_db_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()
