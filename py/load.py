def get_msg_ids(service):
    """Builds and returns array of all email ids of the user at a batch of max 500 each time
       page token allows to request the next batch"""
    page_token = None
    ids = []
    while(True):
        try:
            results = service.users().messages().list(userId="me", maxResults=500, pageToken=page_token).execute()
            id_batch = results.get("messages", [])
            ids.extend(id_batch)
            page_token = results.get("nextPageToken")
            if not page_token:
                break

        except Exception as e:
            print(f"Error {e}")
    return ids