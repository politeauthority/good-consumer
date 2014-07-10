#!/usr/bin/python                                                                                                
# Company Types
# This model controls interactions with company types
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelCompanyTypes( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`company_types`;""" % ( self.db_name )
    c_types = Mysql.ex( qry )
    return c_types

  def create( self, name, wiki, desc = None ):
    qry = """SELECT * FROM `%s`.`company_types` WHERE `name`"""
    args = {
      'name' : name,
      'wiki' : wiki,
      'desc' : desc,
    }
    Mysql.insert( 'company_types', args );
    
# End File: models/ModelCompanyTypes.py
