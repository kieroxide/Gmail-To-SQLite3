from globals import APPLICATION, INTERVIEW, OFFER, JOB_SITES

def get_msg_ids(service):
    """Builds and returns array of all email ids outside date range of db at a batch of max 500 each time
       page token allows to request the next batch"""

    ids = []
    page_token = None
    # Started with 10 days to speed dup the loading process
    query = build_query() + " newer_than:10d"
    while(True):
        try:
            results = service.users().messages().list(userId="me", maxResults=500, pageToken=page_token, q=query).execute()
            id_batch = results.get("messages", [])
            page_token = results.get("nextPageToken")
            ids.extend(id_batch)
            if not page_token:
                break

        except Exception as e:
            print(f"Error {e}")
    print(len(ids))
    return ids


def build_query():
    query = ""
    keywords_2Darr = [APPLICATION, INTERVIEW, OFFER, JOB_SITES]
    for keywords in keywords_2Darr:
        for keyword in keywords:
            query += " " + keyword + " OR"
    # Removes the trailing OR
    query = query[:-3] 
    return query