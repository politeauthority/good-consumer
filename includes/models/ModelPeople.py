#!/usr/bin/python
"""                                                                                                
  Model People
  This model controls interactions for collections of people
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelPeople( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    # qry = """SELECT * FROM `%s`.`people` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    qry = """SELECT * FROM `%s`.`people`;""" % ( self.db_name )    
    people = Mysql.ex( qry )
    return people

  def getUpdateSet( self, limit = 200  ):
    qry = "SELECT * FROM `%s`.`people` ORDER BY date_updated ASC LIMIT %s;" % ( self.db_name, limit )
    return Mysql.ex( qry )

  def getRecentlyUpdated( self, limit = 20 ):
    qry = """SELECT * FROM `%s`.`people` ORDER BY `date_updated` DESC LIMIT %s;""" % ( self.db_name, limit )

# End File: models/ModelCompanies.py