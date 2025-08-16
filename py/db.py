import sqlite3
import os
import pandas as pd
from datetime import datetime
from globals import DB_PATH, EMAIL_TABLE, SENDER_TABLE, RECIPIENT_TABLE

def connect_db():
    """Ensures foreign_keys is always allowed by default"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def addToDB(df):
    df = assign_foreign_keys(df)
    conn = connect_db()
    df.to_sql(EMAIL_TABLE["name"], conn, if_exists="append", index=False)
    conn.close()

def assign_foreign_keys(df):
    for _, email in df.iterrows():
        foreign_key = get_unique_identifier(email["sender"], SENDER_TABLE)
        email["sender"] = foreign_key
        foreign_key = get_unique_identifier(email["recipient"], RECIPIENT_TABLE)
        email["recipient"] = foreign_key
    df = df.rename(columns={"sender": "sender_id", "recipient": "recipient_id"})
    return df

def get_unique_identifier(ITEM, TABLE):
    """Returns the foreign key to the TABLE for the ITEM, if it is not 
    in the db, adds the ITEM and returns the newly created foreign key"""
    TABLE_NAME = TABLE["name"]
    TABLE_ID = TABLE["col_names"][0]
    TABLE_ITEMS = TABLE["col_names"][1]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(f"""SELECT {TABLE_ID} 
                    FROM {TABLE_NAME} 
                    WHERE {TABLE_ITEMS} = ?""", (ITEM,))
    
    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]
    else:
        cur.execute(f"INSERT INTO {TABLE_NAME} ({TABLE_ITEMS}) VALUES (?)", (ITEM,))
        conn.commit()
        conn.close()
        return cur.lastrowid

def init_tables():

    def column_def(TABLE_DEF):
        """Generates the SQL string query for a table to correctly initialize it"""
        i = 0
        table_def = f"{TABLE_DEF["name"]} ("
        for COL_NAME, DEF in TABLE_DEF["columns"]:
            if(i > 0):
                table_def += ", "
            table_def += f"{COL_NAME} {DEF}"
            i += 1
        return table_def + ")" 
      
    conn = connect_db()
    cur = conn.cursor()
    
    # Create a new table with sender + all email IDs for that sender
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(EMAIL_TABLE)}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(SENDER_TABLE)}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(RECIPIENT_TABLE)}")

    conn.commit()
    conn.close()

#def group_db():
#    conn = connect_db()
#    cur = conn.cursor()
#
#    # Create a new table with sender + all email IDs for that sender
#    cur.execute(f"""
#        CREATE TABLE IF NOT EXISTS {FROM_IDS_TABLE_NAME} AS
#        SELECT "from", GROUP_CONCAT("id") AS email_ids
#        FROM {EMAIL_TABLE_NAME}
#        GROUP BY "from"
#    """)
#
#    cur.execute(f'PRAGMA table_info({FROM_IDS_TABLE_NAME})')
#    print(cur.fetchall())
#    conn.commit()
#    conn.close()

def db_exists():
    """Returns whether the db file and table exists"""
    if not os.path.exists(DB_PATH):
        return False
    
    conn = connect_db()
    cursor = conn.cursor()

    # Need to check if table exists
    if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails';").fetchone():
        return False
    conn.close()
    return True

def load_table(table = EMAIL_TABLE["name"], columns=EMAIL_TABLE["columns"]):
    """Loads the inputted columns from db to a pd dataframe. If it doesn't exists, returns empty df with correct columns"""
    if not db_exists():
        return pd.DataFrame(columns=columns)
    
    conn = connect_db()
    # Selects only the required columns in case of auto-increment index
    df = pd.read_sql_query(
        f"SELECT {columns} FROM {table}", # from and to are reserved words in sql 
        conn
    )
    conn.close()
    return df

def get_date_range():
    """Returns the oldest and newest date"""

    conn = connect_db()
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
