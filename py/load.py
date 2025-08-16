from globals import EMAIL_TABLE
from db import load_table

def get_msg_ids(service):
    """Builds and returns set of all email ids outside date range of db at a batch of max 500 each time
       page token allows to request the next batch"""

    ids = set()
    page_token = None
    # Started with 10 days to speed up the loading process
    query = "newer_than:1d"
    while(True):
        try:
            results = service.users().messages().list(userId="me", maxResults=500, pageToken=page_token, q=query).execute()
            # Google returns IDs and unneeded "thread IDs"
            full_batch = results.get("messages", [])
            id_batch = {item["id"] for item in full_batch}

            page_token = results.get("nextPageToken")
            ids.update(id_batch)
            if not page_token:
                break

        except Exception as e:
            print(f"Error {e}")
        
    culled_ids = cull_ids(ids)
    return culled_ids

def cull_ids(ids):
    df = load_table(EMAIL_TABLE)
    db_ids = set(df.index)
    # Removes emails already stored in db
    ids = ids - db_ids
    return ids 

#def build_query():
#    query = ""
#    keywords_2Darr = [APPLICATION, INTERVIEW, OFFER, JOB_SITES]
#    for keywords in keywords_2Darr:
#        for keyword in keywords:
#            query += " " + keyword + " OR"
#    # Removes the trailing OR
#    query = query[:-3] 
#    return query