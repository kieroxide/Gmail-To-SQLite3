from db import get_date_range

def get_msg_ids(service):
    """Builds and returns array of all email ids outside date range of db at a batch of max 500 each time
       page token allows to request the next batch"""
    
    def query_list(service, query, page_token):
        results = service.users().messages().list(userId="me", maxResults=500, pageToken=page_token, q=query).execute()
        id_batch = results.get("messages", [])
        page_token = results.get("nextPageToken")
        return id_batch, page_token
    
    old_date, new_date = get_date_range()
    ids = []
    # Google does not allow before and after to be used as an OR query
    # So they have been separated
    # For older emails not in db
    page_token = None
    while(True):
        try:
            id_batch, page_token = query_list(service, f"before:{old_date}", page_token)
            ids.extend(id_batch)
            if not page_token:
                break

        except Exception as e:
            print(f"Error {e}")

    # For newer emails not in the db
    page_token = None
    while(True):
        try:
            id_batch, page_token = query_list(service, f"after:{new_date}", page_token)
            ids.extend(id_batch)
            if not page_token:
                break

        except Exception as e:
            print(f"Error {e}")
            
    return sort_ids(service, ids)

def fetch_metadata(msg_id, service):
    try:
        msg = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="metadata"
        ).execute()
        return msg
    except Exception as e:
        print(f"Failed to fetch metadata for {msg_id}: {e}")
        return None

def sort_ids(service, ids):
    metadata_list = []
    for id in ids:
        metadata = fetch_metadata(id["id"], service)
        if metadata:
            metadata_list.append(metadata)
    
    metadata_list.sort(key=lambda m: int(m["internalDate"]), reverse=True)

    sorted_ids = [m["id"] for m in metadata_list]
    return sorted_ids