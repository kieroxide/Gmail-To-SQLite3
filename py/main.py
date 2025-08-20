import streamlit as st
from ui import init_settings, handle_db_import, authenticate_button, start_import

def main():
    init_settings()
    handle_db_import()
    authenticate_button()
    start_import()

if __name__ == "__main__":
    main()
