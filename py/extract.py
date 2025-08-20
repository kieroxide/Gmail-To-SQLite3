from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup
from globals import EMAIL_TABLE, DF_COLS
from utils import chunk_list
from db import addToDB, connect_db
from load import get_email_count
import pandas as pd
import streamlit as st

def extract_email_data_to_sql(service, ids):
    """Iterates over email ids and saves the email's data to the sql database
    in chunks to alleviate wait times"""
    TOTAL_EMAILS = st.session_state.emails_remaining
    CHUNK_SIZE = 100

    df = pd.DataFrame(columns=DF_COLS)

    # UI variables
    st.session_state.progress_ticker = 0
    st.session_state.status_text = st.empty()
    st.session_state.progress_bar = st.progress(0)

    chunked_ids = chunk_list(list(ids), CHUNK_SIZE)
    conn = connect_db()
    # Get a chunk of email data and store in dataframe
    for id_chunk in chunked_ids:
        for id in id_chunk:
            ID = id
            # If a error occurs while requesting from API. Skips the email
            data_arr = extract_data_from_email(service, ID)
            if not data_arr:
                continue
            df.loc[len(df)] = data_arr 

            # Displays progress for the user
            st.session_state.progress_ticker += 1
            st.session_state.progress_bar.progress(st.session_state.progress_ticker/TOTAL_EMAILS)
            st.session_state.status_text.text(
                f"""Processing email {st.session_state.progress_ticker} of {TOTAL_EMAILS} ({round(st.session_state.progress_ticker*100/TOTAL_EMAILS,1)}%)""")

        # Appends data to sql_server
        df.set_index(EMAIL_TABLE["col_names"][0])
        addToDB(df)
        df = df[0:0] # Empties data frame

    conn.close()

def extract_data_from_email(service, ID):
    """Requests the google API for the entire Email from the ID. Traverses the data structure
    and collects, cleans and returns the data into an array"""
    # Extracts all required data to dataframe
    try:
        result = service.users().messages().get(userId="me", id=ID).execute()
    except Exception as e:
        print(f"Error {e}")
        return None
    
    payload = result["payload"]
    SNIPPET = ""
    if "snippet" in result:
        SNIPPET = result["snippet"]

    BODY = get_body(payload)
    FROM, TO, SUBJECT, DATE = get_headers(payload)

    return [ID, FROM, TO, SUBJECT, BODY, SNIPPET, DATE]
    
def clean_html_string(encoded_data):
    """Decodes and cleans an base64 encoded html string"""
    body = ""
    # Google stores the data encoded by base64
    decoded_body = urlsafe_b64decode(encoded_data).decode("utf-8", errors="ignore")
    
    # Use html.parser to get rid of the html syntax
    body_soup = BeautifulSoup(decoded_body, "html.parser")
    body = " ".join(body_soup.get_text().split())

    return body

def get_body(payload):
    """ Takes a payload dictionary and extracts a plaintext string of the email body
        Handles two types of emails. Singular part emails and multipart emails"""
    body = ""
    # Multipart emails have a key "parts" in dictionary
    if "parts" in payload:
        for part in payload["parts"]:
            #Some parts have no plaintext data
            if not "data" in part["body"]:
                continue
            body += clean_html_string(part["body"]["data"])
        return body
    
    else:
        #Some parts have no plaintext data
        if not "data" in payload["body"]:
            return ""
        return clean_html_string(payload["body"]["data"])

def get_headers(payload):
    """Finds and returns headers and 4-part tuple"""
    FROM = TO = SUBJECT = DATE = ""
    headers = payload["headers"]
    for header in headers:
        match header["name"]:
            case "From":
                FROM = header["value"]
            case "To":
                TO = header["value"]
            case "Subject":
                SUBJECT = header["value"]
            case "Date":
                DATE = header["value"]
    return FROM, TO, SUBJECT, DATE