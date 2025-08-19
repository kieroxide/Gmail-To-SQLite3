import streamlit as st
from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
from db import load_table, init_tables
from globals import SENDER_TABLE, RECIPIENT_TABLE

def main():
    st.title("📧 Gmail → SQLite3 Importer")
    st.write("Import your Gmail messages into a local SQLite database.")
    init_tables()
    service = authenticate_gmail()
    ids = get_msg_ids(service)
    if st.button("Start Import"):
        extract_email_data_to_sql(ids, service)


if __name__ == '__main__':
    main()
