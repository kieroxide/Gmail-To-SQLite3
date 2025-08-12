from auth import authenticate_gmail
from load import get_msg_ids
from utils import chunk_list
from extract import get_body, get_headers
from db import load_db
import pandas as pd
import sqlite3

def main():
    CHUNK_SIZE = 500
    load_db()
    service = authenticate_gmail()
    ids = get_msg_ids(service)
    print("ID's fetched and sorted")
    df = pd.DataFrame(columns=["id", "from", "to", "subject", "body", "snippet", "date"])
    conn = sqlite3.connect('emails.db')

    chunked_ids = chunk_list(ids, CHUNK_SIZE)
    # Get a chunk of email data and store in dataframe
    chunks_completed = 0
    for id_chunk in chunked_ids:
        for id in id_chunk:
            # Extracts all required data to dataframe
            ID = id["id"]

            result = service.users().messages().get(userId="me", id=ID).execute()
            payload = result["payload"]

            SNIPPET = ""
            if "snippet" in payload:
                SNIPPET = payload["snippet"]

            BODY = get_body(payload)
            FROM, TO, SUBJECT, DATE = get_headers(payload)

            df.loc[len(df)] = [ID, FROM, TO, SUBJECT, BODY, SNIPPET, DATE]
        # Appends data to sql_server
        df.to_sql("Emails", conn, if_exists="append")
        df = df[0:0]
        chunks_completed += 1
        print(chunks_completed)
    conn.close()


if __name__ == '__main__':
    main()
