from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
from db import load_table, init_tables
from globals import SENDER_TABLE, RECIPIENT_TABLE

def main():
    init_tables()
    service = authenticate_gmail()
    print("Authentication Complete")
    ids = get_msg_ids(service)
    print("IDs get complete")
    extract_email_data_to_sql(ids, service)
    print("Save to db complete")
    df = load_table()
    df.to_csv("csv/emails.csv", mode="a")
    df = load_table(SENDER_TABLE)
    df.to_csv("csv/senders.csv", mode="a")
    df = load_table(RECIPIENT_TABLE)
    df.to_csv("csv/recipients.csv", mode="a")

if __name__ == '__main__':
    main()
