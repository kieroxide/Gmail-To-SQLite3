def chunk_list(lst, chunk_size):
    """Splits list into list of chunk_size lists"""
    if(len(lst) == 0) : return []
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]