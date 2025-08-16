DB_PATH = "../sql/emails.db"
EMAIL_TABLE_NAME = "emails"
FROM_IDS_TABLE_NAME = "company"

AVOID_KEYWORDS = {"indeed", "reed", "totaljobs", "cv-library", "monster", "glassdoor", 
    "linkedin", "adzuna", "jobsite", "gov", "ziprecruiter", "careerbuilder", 
    "simplyhired", "jora", "careerjet", "technojobs", "cwjobs", "workable",
    "itjobboard", "devitjobs", "stackoverflow", "dice", "hired", "greenhouse",
    "workinstartups", "welcometothejungle", "otta", "shecancode", "womenintech",
    "remote", "flexa", "weworkremotely", "remoteok", "workingnomads",
    "nodesk", "eurojobs", "eures"}

JOB_MUST_KEYWORDS = {
    # --- The Application Stage ---
    "application",
    "cv",
    "resume",
    "vacancy",
    "cover letter",
    
    # --- The Interview Process ---
    "interview",
    "interviews",
    
    # --- The Role Itself ---
    "role",
    "position",
    "job",
    "employment",
}

APPLICATION = {
    "application",
    "CV",
    "resume",
    "vacancy",
    "role",
    "candidate",
    "recruiter",
    '"your application"',  
    '"we received your application"',
    '"job opening"',
    '"new role"'
}

INTERVIEW = {
    "interview",
    "screening",
    '"technical test"',
    '"schedule a call"',
    '"schedule an interview"',
}

OFFER = {
    '"job offer"',
    '"offer of employment"',
}

JOB_SITES = {
    # General UK & International Job Boards
    "indeed.com",
    "reed.co.uk",
    "totaljobs.com",
    "cv-library.co.uk",
    "monster.co.uk",
    "monster.com",
    "glassdoor.co.uk",
    "glassdoor.com",
    "linkedin.com",
    "adzuna.co.uk",
    "jobsite.co.uk",
    "gov.uk",  # For 'Find a job' service
    "ziprecruiter.com",
    "careerbuilder.com",
    "simplyhired.com",
    "jora.com",
    "careerjet.com",

    # Tech & IT Focused Job Boards
    "technojobs.co.uk",
    "cwjobs.co.uk",
    "itjobboard.co.uk",
    "it-jobs.co.uk",
    "devitjobs.uk",
    "python.org",
    "stackoverflow.com/jobs",
    "dice.com",
    "hired.com",
    "workinstartups.com",
    "welcometothejungle.com", # Formerly Otta
    "otta.com",

    # Women in Tech Focused
    "shecancode.io",
    "womenintech.co.uk",

    # Remote & Flexible Work Focused
    "remote.co",
    "flexa.careers",
    "weworkremotely.com",
    "remoteok.io",
    "workingnomads.com",
    "nodesk.co",

    # European / Global
    "eurojobs.com",
    "eures.europa.eu"
}