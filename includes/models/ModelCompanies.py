#!/usr/bin/python
"""                                                                                                
  Model Companies
  This model controls interactions for collections of companies
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelCompanies( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    # qry = """SELECT * FROM `%s`.`companies` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    qry = """SELECT * FROM `%s`.`companies`;""" % ( self.db_name )    
    companies = Mysql.ex( qry )
    return companies

  def getUpdateSet( self, limit = 200  ):
    qry = "SELECT * FROM `%s`.`companies` ORDER BY date_updated ASC LIMIT %s;" % ( self.db_name, limit )
    return Mysql.ex( qry )

  def getRecentlyUpdated( self, limit = 20 ):
    qry = """SELECT * FROM `%s`.`companies` ORDER BY `date_updated` DESC LIMIT %s;""" % ( self.db_name, limit )

# End File: models/ModelCompanies.py