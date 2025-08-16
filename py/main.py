from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
#from py.archive.analysis import assign_to_company
from db import group_db, load_table
from globals import FROM_IDS_TABLE_NAME
import pandas as pd

def main():
    #group_db()
    #df = load_table(table=FROM_IDS_TABLE_NAME, columns="email_ids")
    service = authenticate_gmail()
    print("Authentication Complete")
    ids = get_msg_ids(service)
    print("IDs get complete")
    extract_email_data_to_sql(ids, service)
    print("Save to db complete")
    df = load_table()
    print("loading db complete")
    df.to_csv("data.csv", mode="a")

if __name__ == '__main__':
    main()
