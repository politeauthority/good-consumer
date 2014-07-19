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

import inspect
import pprint
from datetime import date, datetime, time, timedelta

class HelperDebug( object ):

  def __init__( self ):
    self.log_dir  = MVC.app_dir + 'logs/'
    self.debug_on = MVC.server['debug']

  def write( self, title, message = None, log_file = None):

    
    if self.debug_on:
      if os.path.isdir( self.log_dir ) == False:
        os.mkdir( self.log_dir )

      if log_file == None:
        log_file = 'debug.log'
      else:
        log_file = log_file + '.log'
      
      pp = pprint.PrettyPrinter( indent=4 )
      write_message = str( message ) + "\n"
      f = open( self.log_dir + log_file,'a')
      f.write('[%s] %s: %s' % (  datetime.now(), title, write_message ) )
      print ' '
      print ' '
      print ' ****** START DEBUG MESSAGE ******'
      # print 'File:   ', inspect.stack()[6]
      # print 'Method: ', inspect.stack()[8]
      # print 'Line:   ', inspect.stack()[7]
      print title
      print pp.pprint( message )
      print ' '
      print ' '
      print ' ****** END DEBUG MESSAGE ******'
      print ' '
        
# End File: includes/helpers/HelperDebug.py
