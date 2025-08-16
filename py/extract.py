from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup
from globals import EMAIL_TABLE, DF_COLS
from utils import chunk_list
from db import addToDB, connect_db
import pandas as pd
import time

API_TOTAL = 0

def extract_email_data_to_sql(ids, service):
    """Iterates over email ids and saves the email's data to the sql database
    in chunks to alleviate wait times"""
    global API_TOTAL
    df = pd.DataFrame(columns=DF_COLS)

    CHUNK_SIZE = 100 
    conn = connect_db()
    chunked_ids = chunk_list(list(ids), CHUNK_SIZE)

    # Get a chunk of email data and store in dataframe
    for id_chunk in chunked_ids:
        for id in id_chunk:
            ID = id
            # If a error occurs while requesting from API. Skips the email
            data_arr = extract_data_from_email(service, ID)
            if not data_arr:
                continue
            df.loc[len(df)] = data_arr

        print(f"{API_TOTAL} seconds")
        API_TOTAL = 0
        # Appends data to sql_server
        df.set_index(EMAIL_TABLE["col_names"][0])
        addToDB(df)
        df = df[0:0] # Empties data frame

    conn.close()

def extract_data_from_email(service, ID):
    """Requests the google API for the entire Email from the ID. Traverses the data structure
    and collects, cleans and returns the data into an array"""
    # Extracts all required data to dataframe
    global API_TOTAL
    try:
        API_CALL = time.perf_counter()
        result = service.users().messages().get(userId="me", id=ID).execute()
        API_END = time.perf_counter()
        API_TOTAL += API_END - API_CALL
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