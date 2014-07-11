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

  def getIDsByName( self, type_names, create_if_not_exists = False ):
    """
      @params: 
        names : list[]
        create_if_not_exists : bool makes non-existant company types
    """
    company_type_ids = []
    for name in type_names:
      qry = """SELECT * FROM `%s`.`company_types` WHERE `name` = "%s";  """ % ( self.db_name, name['name'] )
      result = Mysql.ex( qry )
      if len( result ) == 0:
        type_id = self.create( name['name'], name['wiki'] )
      else:
        type_id = result[0]['company_type_id']
      company_type_ids.append( type_id )
    return company_type_ids
  
  def create( self, name, wiki, desc = None ):
    qry = """SELECT * FROM `%s`.`company_types` WHERE `name`"""
    args = {
      'name' : name,
      'wiki' : wiki,
      'desc' : desc,
    }
    Mysql.insert( 'company_types', args );
    qry = """SELECT * FROM `%s`.`company_types` WHERE `name`="%s";""" % ( self.db_name, name )
    id = Mysql.ex( qry )[0]['company_type_id']
    return id
# End File: models/ModelCompanyTypes.py
