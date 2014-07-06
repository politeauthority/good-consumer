#!/usr/bin/python
"""
  Simple Stats
  Collects simple stats for web display
"""

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')
Settings = MVC.loadHelper('Settings')

class ModelSimpleStats( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def countOfCompanies( self ):
    qry = "SELECT count(*) as c FROM `%s`.`companies`;" % self.db_name
    return Mysql.ex( qry )[0]['c']

# End File: models/ModelSimpleStats.py
