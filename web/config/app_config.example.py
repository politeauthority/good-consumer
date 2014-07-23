"""
    Primary config file, before install this is the only file you must modify.
"""

settings = {
    'server' : {
        'cdn'            : True,
        'template_cache' : False,
        'production'     : False,
        'debug'          : True
    },
    'database': {
        'host'       : "localhost",
        'user'       : "user",
        'pass'       : "pass",
        'name'       : "good_consumer",
    }
}

# Endfile: web/config/app_config.py
