settings = {
        "delay": 15,
        "limit": 1000,
        "username": "infiltration_bot",
        "password": "Wouldn't you like to know",
        "subreddit": "Anarchism",
        "wiki_page_name": "suspicious_subs",
        }

try:
    from local_config import local_settings
    settings.update(local_settings)
except ImportError as e:
    pass
