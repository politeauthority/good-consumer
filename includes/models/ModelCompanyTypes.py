#!/usr/bin/python                                                                                                
"""
  Company Types
  This model controls interactions with company types
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')
Debugger = MVC.loadHelper('Debug')

class ModelCompanyTypes( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`company_types`;""" % ( self.db_name )
    c_types = Mysql.ex( qry )
    return c_types

  def getByID( self, company_type_id ):
    qry = """SELECT * FROM 
      `%s`.`company_types` 
      WHERE `company_type_id` = "%s";""" % ( self.db_name, company_type_id )
    c_type = Mysql.ex( qry )
    if len( c_type ) == 0:
      return False
    return c_type[0]

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
        type_id = self.create( name['name'], name['wikipedia'] )
      else:
        type_id = result[0]['company_type_id']
      company_type_ids.append( type_id )
    return company_type_ids
  
  def create( self, name, wikipedia_url, desc = None ):
    qry = """SELECT * FROM `%s`.`company_types` WHERE `wikipedia` = "%s";""" % ( self.db_name, wikipedia_url )
    exists = Mysql.ex( qry )
    if len( exists ) > 0:
      Debugger.write( 'exists', exists[0]['company_type_id'] )
      return exists[0]['company_type_id']
    args = {
      'name'      : name,
      'wikipedia' : wikipedia_url,
      'desc'      : desc,
    }
    Mysql.insert( 'company_types', args );
    qry = """SELECT * FROM `%s`.`company_types` WHERE `wikipedia`="%s";""" % ( self.db_name, wikipedia_url )
    company_type_id = str( Mysql.ex( qry )[0]['company_type_id'] )
    Debugger.write( 'company_type_id', company_type_id )
    return company_type_id

# End File: includes/models/ModelCompanyTypes.py
