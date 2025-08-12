import sqlite3
import pandas as pd

def load_db():
    conn = sqlite3.connect("emails.db")
    df = pd.read_sql_query("SELECT * FROM Emails", conn)
    conn.close()
    return df