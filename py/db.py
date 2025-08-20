import sqlite3
import pandas as pd
import streamlit as st
from globals import EMAIL_TABLE, SENDER_TABLE, RECIPIENT_TABLE

def connect_db():
    """Ensures foreign_keys is always allowed by default"""
    conn = sqlite3.connect("../sql/" + st.session_state.db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def addToDB(df):
    """Adds a dataframe batch to the sql database. Handles foreign key assignment"""
    df = assign_foreign_keys(df)
    conn = connect_db()
    df.to_sql(EMAIL_TABLE["name"], conn, if_exists="append", index=False)
    conn.close()

def assign_foreign_keys(df):
    """Assigns the foreign keys to the dataframe and renames the columns"""
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
    # Using ? syntax to prevent SQL injection
    cur.execute(f"""SELECT {TABLE_ID} 
                    FROM {TABLE_NAME} 
                    WHERE {TABLE_ITEMS} = ?""", (ITEM,))
    
    row = cur.fetchone()

    if row:
        conn.close()
        key = row[0]
        return key
    else:
        cur.execute(f"INSERT INTO {TABLE_NAME} ({TABLE_ITEMS}) VALUES (?)", (ITEM,))
        conn.commit()
        conn.close()
        key = cur.lastrowid
        return key

def init_tables():
    """Initalises the sql tables to enforce database structure"""
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
    
    # Inits the 3 tables to represent the email data
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(EMAIL_TABLE)}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(SENDER_TABLE)}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {column_def(RECIPIENT_TABLE)}")

    conn.commit()
    conn.close()

def load_table(TABLE = EMAIL_TABLE):
    """Loads the inputted columns from db to a pd dataframe"""
    
    cols = ", ".join(TABLE["col_names"])
    conn = connect_db()
    # Selects only the required columns in case of auto-increment index
    df = pd.read_sql_query(
        f"SELECT {cols} FROM {TABLE["name"]}", # from and to are reserved words in sql 
        conn
    )
    df = df.set_index(TABLE["col_names"][0])
    conn.close()
    return df

def current_email_count():
    """Returns the current amount of emails in the db"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {EMAIL_TABLE["name"]};")
    row_count = cursor.fetchone()[0]
    return row_count

