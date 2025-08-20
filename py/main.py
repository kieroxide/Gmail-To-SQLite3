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

def init_settings():
    if "db_name" not in st.session_state:
        st.session_state.db_name = "emails.db"
    if "download_name" not in st.session_state:
        st.session_state.download_name = st.session_state.db_name
    if "service" not in st.session_state:
        st.session_state.service = None

    st.title("📧 Gmail → SQLite3 Importer")
    st.write("Import your Gmail messages into a local SQLite database.")
    if st.session_state.service:
        st.success("✅ Gmail Connected Successfully")
    else:
        st.warning("⚠️ Not Connected")

def handle_db_import():
    st.subheader("Database Setup")
    import_choice = st.checkbox("Import an existing SQLite DB?")
    if import_choice:
        uploaded_file = st.file_uploader("📂 Choose a DB file", type=["db", "sqlite"])
        if uploaded_file:
            # Ensure folder exists
            os.makedirs("../sql", exist_ok=True)
            
            # Save file to disk
            st.session_state.db_name = uploaded_file.name
            db_path = "../sql/" + st.session_state.db_name
            with open(db_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Database `{st.session_state.db_name}` imported successfully!")

    # Let user rename for download
    st.session_state.download_name = st.text_input(
        "Database name for download", st.session_state.db_name
    )

def authenticate_button():
    if not st.session_state.service:
        if st.button("Connect Gmail"):
            st.session_state.service = authenticate_gmail()
            st.session_state.ids = get_msg_ids(st.session_state.service)
            if "emails_remaining" not in st.session_state:
                st.session_state.emails_remaining = get_email_count(st.session_state.service)
                st.session_state.emails_remaining -= current_email_count()
            st.rerun()

def start_import():
    init_tables()
    if st.session_state.service:
        if st.button("Start Import"):
            db_path = "../sql/" + st.session_state.db_name
            extract_email_data_to_sql(st.session_state.service, st.session_state.ids)
            st.success(f"✅ Import finished! Database saved as `{st.session_state.download_name}`")

            # Download button
            with open(db_path, "rb") as f:
                st.download_button(
                    label="📥 Download SQLite DB",
                    data=f,
                    file_name=st.session_state.download_name,
                    mime="application/x-sqlite3"
                )

if __name__ == "__main__":
    main()
