import en_core_web_trf
import pandas as pd
from db import load_db
from collections import Counter
from globals import AVOID_KEYWORDS, JOB_MUST_KEYWORDS
import string

def assign_to_company():
    """Tries to find a company name in the email and if not it discards the email"""
    email_df = load_db()
    DATA_COLUMNS = ["from","subject","body","snippet"]
    for id, email in email_df.iterrows():
        # Easier to collect data into one string then analyse
        target_data = ""
        for col in DATA_COLUMNS:
            target_data += email[col]

        # Easier to perform analysis without punctation
        clean_data = target_data.translate(str.maketrans('', '', string.punctuation))
        if(not must_have_keywords_check(clean_data)):
            continue
        COMPANY_NAME = estimate_company_name(clean_data)
        print(COMPANY_NAME)

def must_have_keywords_check(str):
    """Returns if the str contains a must-have keyword"""
    for keyword in JOB_MUST_KEYWORDS:
        if keyword in str:
            return True
    return False
            

def estimate_company_name(data):
    # Uses NER to assign ORG label to sub strings
    # Extremely fast NER model
    nlp = en_core_web_trf.load()
    doc = nlp(data)
    ents = [ent for ent in doc.ents if ent.label_ == "ORG"]
    ents_no_keywords = keyword_check(ents)
    company_name_est = get_most_common_word(ents_no_keywords)
    return company_name_est

def get_most_common_word(ents):
    """Returns the most common word in the text of all entity"""
    all_words = []
    for ent in ents:
        word_arr = ent.text.split()
        all_words.extend(word_arr)
    most_common_word, _ = Counter(all_words).most_common(1)[0]
    return most_common_word

def keyword_check(ents):
    """Removes any entities with keywords to avoid returns the clean array of entities"""
    new_ents = []
    for ent in ents:
        for KEYWORD in AVOID_KEYWORDS:
            if KEYWORD in ent.text.lower():
                break
        else:
            new_ents.append(ent)
    return new_ents
    