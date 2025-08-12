from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup

def clean_html_string(encoded_data):
    """Decodes and cleans an base64 encoded html string"""
    body = ""
    # Google stores the data encoded by base64
    decoded_body = urlsafe_b64decode(encoded_data).decode("utf-8", errors="ignore")
    
    # Use html.parser to get rid of the html syntax
    body_soup = BeautifulSoup(decoded_body, "html.parser")
    body = "".join(body_soup.get_text().split())

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
        if not payload["body"]["data"]:
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