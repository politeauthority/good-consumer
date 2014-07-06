#!/usr/bin/python                                                                                                
# User Companies
# This model controls interactions for collections of companies
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')
Settings = MVC.loadHelper('Settings')

class ModelCompanies( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`companies` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    companies = Mysql.ex( qry )
    return companies

  def getUpdateSet( self ):
    qry = "SELECT * FROM `%s`.`companies` ORDER BY date_updated ASC LIMIT 200;" % MVC.db['name']    
    return Mysql.ex( qry )
    
# End File: models/ModelCompanies.py