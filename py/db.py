import sqlite3
import os
import pandas as pd
from datetime import datetime
from globals import DB_PATH, EMAIL_TABLE_NAME, FROM_IDS_TABLE_NAME

def group_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create a new table with sender + all email IDs for that sender
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {FROM_IDS_TABLE_NAME} AS
        SELECT "from", GROUP_CONCAT("id") AS email_ids
        FROM {EMAIL_TABLE_NAME}
        GROUP BY "from"
    """)
    cur.execute(f'PRAGMA table_info({FROM_IDS_TABLE_NAME})')
    print(cur.fetchall())
    conn.commit()
    conn.close()

def db_exists():
    """Returns whether the db file and table exists"""
    if not os.path.exists(DB_PATH):
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Need to check if table exists
    if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails';").fetchone():
        return False
    conn.close()
    return True

def load_table(table = EMAIL_TABLE_NAME, columns='"id", "from", "to", "subject", "body", "snippet", "date"'):
    """Loads the inputted columns from db to a pd dataframe. If it doesn't exists, returns empty df with correct columns"""
    if not db_exists():
        return pd.DataFrame(columns=columns)
    
    conn = sqlite3.connect(DB_PATH)
    # Selects only the required columns in case of auto-increment index
    df = pd.read_sql_query(
        f"SELECT {columns} FROM {table}", # from and to are reserved words in sql 
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
