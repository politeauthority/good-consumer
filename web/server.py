#!/usr/bin/python
"""
	Web Server executible file
""" 
import sys
import os
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

if __name__ == '__main__':  
	Root = MVC.loadController( 'Home', callable = True )
	cherrypy.quickstart( Root(),  config = MVC.cherrypy_config )

# End File: web/server.py
