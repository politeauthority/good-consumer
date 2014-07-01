#!/usr/bin/python                                                   
# Prowl Driver 
# This is a simple driver for sending Prowl messages to iOS devices
# Requirements: prowlpy ( https://github.com/jacobb/prowlpy )

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import prowlpy

class DriverProwl( object ):

  def send( self, apikey, subject, message, priority ):
    app_name = MVC.app_name
    prowl    = prowlpy.Prowl( apikey )
    try:
      prowl.add( app_name, subject, message, 1, None, "http://www.prowlapp.com/")
      print 'Success'
    except Exception, msg:
      print msg

# End File: driver/DriverProwl.py
