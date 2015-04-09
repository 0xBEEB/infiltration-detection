settings = {
        "username": "infiltration_bot",
        "password": "Wouldn't you like to know",
        "suspicious_subs": [
            "anarchism",
            "anarcho_capitalism",
            "anarchy101",
            "antipozi",
            "beatingcripples",
            "beatingniggers",
            "beatingwomen2",
            "beatingtrannies",
            "coontown",
            "conservative",
            "european",
            "fatlogic",
            "fatpeoplehate",
            "greatapes",
            "hbd",
            "killingwomen",
            "kotakuinaction",
            "libertarian",
            "mensrights",
            "metanarchism",
            "monarchism",
            "nationalsocialism",
            "nazi",
            "new_right",
            "polistan",
            "rapingwomen",
            "sjsucks",
            "sjwhate",
            "srssucks",
            "strugglefucking",
            "theredpill",
            "trans_fags",
            "tumblerinaction",
            "whiterights",
            ],
        }

try:
    from local_config import local_settings
    settings.update(local_settings)
except ImportError as e:
    pass
