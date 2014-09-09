#Web Server Config File

import os
import string
import cherrypy

current_path =os.path.dirname(os.path.realpath(__file__))
app_path = current_path[:-7]

settings = { 
    'global': {
        'server.socket_port'          : 9777,
        'server.socket_host'          : "192.168.7.72",
        'server.socket_file'          : "",
        'server.socket_queue_size'    : 5,
        'server.protocol_version'     : "HTTP/1.0",
        'server.log_to_screen'        : True,
        'server.log_file'             : "log/server.log",
        'server.reverse_dns'          : False,
        'server.thread_pool'          : 40,
        'server.environment'          : "development",
    },
    '/': {
        #'favicon_ico'                 : 'favicon.ico',
        'tools.sessions.on'           : True,
        'tools.sessions.storage_type' : "file",
        'tools.sessions.storage_path' : app_path + "web/tmp/sessions",
        'tools.sessions.timeout'      : 60,
        'tools.staticdir.root'        : app_path + "web/public_html",
        'tools.staticdir.debug'       : True,
    },
    '/css': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir': "css"
    },
    '/js': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir': "js"
    },
    '/libs': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir': "libs"
    },
    '/font-awesome': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir': "font-awesome"
    }    
}

# End file: config/webserver_config.py
