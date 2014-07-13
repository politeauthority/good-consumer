#!/usr/bin/python
"""
  Job Log Model
  Runs interactions for job logging
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')

class ModelJobLog( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def start( self, job_name ):
    args = {
      'job'   : job_name,
      'start' : Mysql.now()
    }
    Mysql.insert( 'job_log', args )
    qry = """SELECT `id` FROM `%s`.`job_log` ORDER BY `id` DESC;""" % self.db_name
    last_id = Mysql.ex( qry )[0]['id']
    return last_id

  def stop( self, job_id, message = None ):
    the_update = { 
      'end'     : Mysql.now(),
      'message' : message
    }
    the_where  = { 'id' : job_id }
    Mysql.update( 'job_log', the_update, the_where )
 
# End File: models/ModelJobLog.py
