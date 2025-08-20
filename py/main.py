import streamlit as st
from auth import authenticate_gmail
from load import get_msg_ids, get_email_count
from extract import extract_email_data_to_sql
from db import init_tables, current_email_count
import os

def main():
    init_settings()
    handle_db_import()
    authenticate_button()
    start_import()

if __name__ == "__main__":
    main()
