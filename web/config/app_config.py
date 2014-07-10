"""
    Primary config file, before install this is the only file you must modify.
"""

settings = {
    'server' : {
        'cdn'            : True,
        'template_cache' : True,
        'production'     : False,
    },
    'database': {
        'host'       : "localhost",
        'user'       : "user",
        'pass'       : "pass",
        'name'       : "good_consumer",
    }
}

# Endfile: config/app_config.py
