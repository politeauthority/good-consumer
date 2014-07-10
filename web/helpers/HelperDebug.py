#!/usr/bin/python
"""
  Debug Helper
"""

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

from os import path

class HelperDebug( object ):

  def __init__( self ):
    self.log_dir  = MVC.app_dir + 'logs/'
    self.debug_on = MVC.server['debug']

  def write( self, title, message = None, log_file = None):
    from datetime import date, datetime, time, timedelta
    
    if self.debug_on:
      if path.isdir( self.log_dir ) == False:
        os.mkdir( self.log_dir )

      if log_file == None:
        log_file = 'debug.log'
      else:
        log_file = log_file + '.log'
      message = message + "\n"
      f = open( self.log_dir + log_file,'a')
      f.write('[%s] %s: %s' % (  datetime.now(), title, message ) )
      print ' '
      print ' '
      print ' ****** START DEBUG MESSAGE ******'
      print title
      print message
      print ' '
      print ' '
      print ' ****** START DEBUG MESSAGE ******'
      print ' '
        
# End File: helpers/HelperDebug.py
