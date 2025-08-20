import streamlit as st
from auth import authenticate_gmail
from load import get_msg_ids
from extract import extract_email_data_to_sql
from db import load_table, init_tables

def main():
    init_settings()
    import_current_db()
    authenticate_button()
    start_import()

def init_settings():
    if "db_name" not in st.session_state:
        st.session_state.db_name = "emails.db"

    st.title("📧 Gmail → SQLite3 Importer")
    st.write("Import your Gmail messages into a local SQLite database.")
    # placeholder for connection status to keep its position
    status_placeholder = st.empty()

    # Dynamic updating of connection status
    if "service" in st.session_state:
        status_placeholder.success("✅ Gmail Connected Successfully")
    else:
        status_placeholder.warning("⚠️ Not Connected")

def import_current_db():
    uploaded_file = st.file_uploader("📂 Import existing SQLite DB", type=["db", "sqlite"])
    if uploaded_file is not None:
        db_path = "../sql/" + st.session_state.db_name

        # Save uploaded file to that location (overwrite or rename)
        with open(db_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Database imported successfully!")
        return db_path
    
    return None

def authenticate_button():
    # Only show the button if service is not yet connected
    if "service" not in st.session_state:
        if st.button("Connect Gmail"):
            st.session_state.service = authenticate_gmail()
            st.session_state.ids = get_msg_ids(st.session_state.service)
            if "emails_remaining" not in st.session_state:
                st.session_state.emails_remaining = get_email_count(st.session_state.service)
                st.session_state.emails_remaining -= current_email_count()
            st.rerun()

def start_import():
    init_tables()
    if "service" in st.session_state:
        st.session_state.db_name = st.text_input("Database name", "emails.db")
        
        if st.button("Start Import"):
            extract_email_data_to_sql(st.session_state.service, st.session_state.ids)
            st.success(f"✅ Import finished! Database saved as `{st.session_state.db_name}`")

            # Displays download button
            with open("../sql/" + st.session_state.db_name, "rb") as f:
                st.download_button(
                    label="📥 Download SQLite DB",
                    data=f,
                    file_name=st.session_state.db_name,
                    mime="application/x-sqlite3"
                )

if __name__ == '__main__':
    main()
