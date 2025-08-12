import sqlite3
import pandas as pd
from datetime import datetime

def load_db():
    conn = sqlite3.connect("emails.db")
    df = pd.read_sql_query("SELECT * FROM Emails", conn)
    conn.close()
    return df

def get_date_range():
    """Returns the oldest and newest date"""

    conn = sqlite3.connect("emails.db")
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
