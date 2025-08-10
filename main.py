from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
import base64
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticates with the Google Gmail API using OAuth 2.0.

    Handles token storage, retrieval, and refresh. If no valid token is found,
    it initiates the OAuth consent flow.

    Returns:
        googleapiclient.discovery.Resource: An authorized Gmail API service object.
    """
    creds = None
    # The file token.pkl stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # If credentials have expired and a refresh token exists, we can get a new
        # access token without bothering the user.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Otherwise, run the full, one-time consent flow for the user.
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_msg_ids(service):
    results = service.users().messages().list(userId="me", maxResults = 500).execute()
    msg_id = results.get("messages", [])
    return msg_id

def main():
    service = authenticate_gmail()
    msg_ids = get_msg_ids(service)    
    msg = service.users().messages().get(userId="me", id=msg_ids[1]["id"], format="full").execute()
    raw_body_html = base64.urlsafe_b64decode(msg["payload"]["body"]["data"])
    body_soup = BeautifulSoup(raw_body_html, "html.parser")
    print(body_soup.getText())

if __name__ == '__main__':
    main()
