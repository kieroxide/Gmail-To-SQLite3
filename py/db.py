import sqlite3
import os
import pandas as pd
from datetime import datetime
from globals import DB_PATH, TABLE_NAME

def load_db():
    df = pd.DataFrame(columns=["id", "from", "to", "subject", "body", "snippet", "date"])
    if not os.path.exists(DB_PATH):
        return df
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Need to check if table exists
    if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails';").fetchone():
        return df
    
    # Selects only the required columns in case of auto-increment index
    df = pd.read_sql_query(
        f"SELECT id, `from`, `to`, subject, body, snippet, date FROM {TABLE_NAME}",
        conn
    )
    conn.close()
    return df

def get_date_range():
    """Returns the oldest and newest date"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MIN(date) AS oldest_date,
               MAX(date) AS newest_date
        FROM emails;
    """)
    oldest_date, newest_date = cursor.fetchone()
    # Convert to datetime objects 
    oldest_date = datetime.strptime(oldest_date, "%d %b %Y %H:%M:%S %z")
    newest_date = datetime.strptime(newest_date, "%a, %d %b %Y %H:%M:%S %z")

    # Convert to Gmail API date format (YYYY/MM/DD)
    oldest_gmail = oldest_date.strftime("%Y/%m/%d")
    newest_gmail = newest_date.strftime("%Y/%m/%d")

    conn.close()
    return oldest_gmail, newest_gmail
