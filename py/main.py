from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
from db import load_db
import pandas as pd

def main():
    service = authenticate_gmail()
    print("Authentication Complete")
    ids = get_msg_ids(service)
    print("IDs get complete")
    extract_email_data_to_sql(ids, service)
    print("Save to db complete")
    df = load_db()
    print("loading db complete")
    df.to_csv("data.csv", mode="a")

if __name__ == '__main__':
    main()
