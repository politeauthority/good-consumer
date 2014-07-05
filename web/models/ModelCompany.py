#!/usr/bin/python
"""
  Company
  This model controls interactions for a single company
"""

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')
Settings = MVC.loadHelper('Settings')

class ModelCompany( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getById( self, company_id ):
  	print company_id

  """
    getBySlug
    @todo: sanitize the input properly!
  """
  def getBySlug( self, company_slug ):
  	qry = """SELECT * FROM ``.`companies` WHERE `slug` = "%s"; """ % ( self.db_name, company_slug )
  	print company_slug

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`companies` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    companies = Mysql.ex( qry )
    return companies

  """
    Create
    Stores a new company if it does not already exist.
    @params:
      company : {
        'name'    : 'company name',
        'symbol'  : 'CMPY',
        'slug'    : 'company-name',
      }
    @return:
      False or new company_id
  """
  def create( self, company ):
    new_company = {}
    if 'name' not in company or company['name'] == '':
      return False
    qry = """SELECT * FROM `%s`.`companies` WHERE name = "%s";""" % ( self.db_name, company['name'] )
    exists = Mysql.ex( qry )
    if len( exists ) != 0:
      self.update_diff( company, exists[0] )
      return False
    
    new_company['name'] = company['name']
    if 'symbol' not in company:
      new_company['symbol'] = None
    if 'slug' not in company:
      Misc = MVC.loadHelper( 'Misc' )
      new_company['slug'] = Misc.slug( company['name'] )
    if 'wikipedia' not in company:
      new_company['wikipedia'] = ''
    else:
      new_company['wikipedia'] = company['wikipedia']

    Mysql.insert( 'companies', new_company )

    def update_diff( self, company_new, company_rec ):
      print company_new
      print company_rec

# End File: models/ModelCompany.py
