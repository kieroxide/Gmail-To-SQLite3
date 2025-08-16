DB_PATH = "../sql/emails.db"

DF_COLS = ["email_id", "sender", "recipient", "subject", "body", "snippet", "timestamp"]

EMAIL_TABLE = {
    "name": "emails",
    "columns": [
        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        ("email_id", "TEXT"),
        ("sender_id", "INTEGER"),
        ("recipient_id", "INTEGER"),
        ("snippet", "TEXT"),
        ("subject", "TEXT"),
        ("body", "TEXT"),
        ("timestamp", "TEXT"),
        ("FOREIGN KEY(sender_id)", "REFERENCES senders(id)"),
        ("FOREIGN KEY(recipient_id)", "REFERENCES recipients(id)")
    ]
}

SENDER_TABLE = {
    "name" : "senders",
    "columns" : [
        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), 
        ("sender", "TEXT UNIQUE")
    ]
}

RECIPIENT_TABLE = {
    "name" : "recipients",
    "columns" : [
        ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), 
        ("recipient", "TEXT UNIQUE")
    ]
}
