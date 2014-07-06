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

  def getByID( self, company_id ):
    if isinstance( company_id, int ):
      qry = """SELECT * FROM `%s`.`companies` WHERE `company_id` = %s; """ % ( self.db_name, company_id )
      company = Mysql.ex( qry )[0]
      return company

  """
    getBySlug
  """
  def getBySlug( self, company_slug ):
    qry = """SELECT * FROM `%s`.`companies` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( company_slug ) )
    company = Mysql.ex( qry )
    return company[0]

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`companies` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    companies = Mysql.ex( qry )
    return companies

  def getRandom( self ):
    import random    
    count = Mysql.ex( "SELECT count(*) AS c FROM `%s`.`companies`;" % self.db_name )
    the_id = random.randint( 1, count[0]['c'] )
    company = self.getByID( the_id )
    return company


  """
    Create
    Stores a new company if it does not already exist.
    @params:
      company : {
        'name'      : 'company name',
        'symbol'    : 'CMPY',
        'slug'      : 'company-name',
        'wikipedia' : 'http://en.wikipedia.org/wiki/Mondel%C4%93z_International'
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
    else:
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

  """
    update_diff
    Updates a company record by a diff of the values
  """
  def update_diff( self, company_new, company_rec ):
    company_id = company_rec['company_id']
    diff = {}
    if 'symbol' in company_new['symbol'] and company_new['symbol'] != company_rec['symbol']:
      diff['symbol'] = company_new['symbol']
    if 'slug' in company_new['slug'] and company_new['slug'] != company_rec['slug']:
      diff['slug'] = company_new['slug']
    if 'type' in company_new['type'] and company_new['type'] != company_rec['type']:
      diff['type'] = company_new['type']
    if 'industry' in company_new['industry'] and company_new['industry'] != company_rec['industry']:
      diff['industry'] = company_new['industry']
    if 'headquarters' in company_new['headquarters'] and company_new['headquarters'] != company_rec['headquarters']:
      diff['headquarters'] = company_new['headquarters']  
    if 'founded' in company_new['founded'] and company_new['founded'] != company_rec['founded']:
      diff['founded'] = company_new['founded']
    if 'wikipedia' in company_new['wikipedia'] and company_new['wikipedia'] != company_rec['wikipedia']:
      diff['wikipedia'] = company_new['wikipedia']  
    Mysql.update( 'company', diff, { 'company_id' : company_id } )

# End File: models/ModelCompany.py
