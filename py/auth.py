from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os

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
    if os.path.exists('../token.pkl'):
        with open('../token.pkl', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # If credentials have expired and a refresh token exists, we can get a new
        # access token without bothering the user.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Otherwise, run the full, one-time consent flow for the user.
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('../token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error {e}")
        return None
