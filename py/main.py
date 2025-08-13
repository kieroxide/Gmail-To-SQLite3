from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
from db import load_db
import pandas as pd

def main():
    service = authenticate_gmail()
    ids = get_msg_ids(service)
    extract_email_data_to_sql(ids, service)
    df = load_db()
    df.to_csv("data.csv", mode="w")

if __name__ == '__main__':
    main()
