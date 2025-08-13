DB_PATH = "../sql/emails.db"
TABLE_NAME = "emails"

APPLICATION = [
    "application",
    "CV",
    "resume",
    "vacancy",
    "position",
    "opportunity",
    "role",
    "candidate",
    "recruiter",
    '"your application"',  
    '"we received your application"',
    '"job opening"',
    '"new role"'
]

INTERVIEW = [
    "interview",
    "assessment",
    "test",
    "screen",
    "screening",
    '"phone screen"',
    '"technical test"',
    '"coding challenge"',
    '"schedule a call"',
    '"schedule an interview"',
    '"next steps"',
]

OFFER = [
    "offer",
    '"job offer"',
    '"offer of employment"',
    "contract",
    "onboarding",
    '"pleased to offer"'
]

JOB_SITES = [
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
]