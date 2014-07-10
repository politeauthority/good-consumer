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
    Get a company by the slugged name
    @params:
      company_slug : str( ) ex: oscar-myer
    return company
  """
  def getBySlug( self, company_slug ):
    qry = """SELECT * FROM `%s`.`companies` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( company_slug ) )
    company = Mysql.ex( qry )
    return company[0]

  """
    getByName
    Get a company by the exact name
    @params : str( ) Oscar Myer
    @return company
  """
  def getByName( self, company_name ):
    qry = """SELECT * FROM `%s`.`companies` WHERE `name` = "%s"; """ % ( self.db_name, Mysql.escape_string( company_name ) )
    company = Mysql.ex( qry )
    return company[0]    

  """
    getRandom
    Gets a random company
    @return company
  """
  def getRandom( self ):
    import random    
    count = Mysql.ex( "SELECT count(*) AS c FROM `%s`.`companies`;" % self.db_name )
    the_id = random.randint( 1, count[0]['c'] )
    company = self.getByID( the_id )
    return company

  """
    getMeta
    @params:
      company_id : int()
      metas : list() meta keys
    @return: 
      dict{ 
        'meta_key': 'meta_value'
      }
  """
  def getMeta( self, company_id, metas = None ):
    qry = """SELECT * FROM `%s`.`company_meta` WHERE `company_id`="%s" """
    if metas:
      if isinstance( metas, str ):
        metas = [ metas ]
      meta  = Mysql.list_to_string( metas )
      qry  += "AND meta_value IN( %s );"
    else:
      qry += ";"
    the_meta = Mysql.ex( qry )
    export_meta = {}
    for meta in the_meta.iteritems():
      export_meta[meta['meta_key']] = export_meta['meta_value']
    return export_meta

  """
    Create
    Stores a new company if it does not already exist.
    @params:
      company : {
        'name'      : 'company name',
        'symbol'    : 'CMPY',
        'slug'      : 'company-name',
        'wikipedia' : 'http://en.wikipedia.org/wiki/Mondel%C4%93z_International',
        'meta'      : {
          'desc'  : 'The company was founded on values.'
        }
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
      self.updateDiff( company, exists[0] )
      company_id = ''
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
      company_id = self.getByName( company['name'] )['company_id']
    if 'meta' in company:
      self.createMeta( company_id, company['meta'] )

  """
    updateDiff
    Updates a company record by a diff of the values
  """
  def updateDiff( self, company_new, company_rec ):
    company_id = company_rec['company_id']
    diff = {}
    if 'symbol' in company_new and company_new['symbol'] != company_rec['symbol']:
      diff['symbol'] = company_new['symbol']
    if 'slug' in company_new and company_new['slug'] != company_rec['slug']:
      diff['slug'] = company_new['slug']
    if 'type' in company_new and company_new['type'] != company_rec['type']:
      diff['type'] = company_new['type']
    if 'industry' in company_new and company_new['industry'] != company_rec['industry']:
      diff['industry'] = company_new['industry']
    if 'headquarters' in company_new and company_new['headquarters'] != company_rec['headquarters']:
      diff['headquarters'] = company_new['headquarters']  
    if 'founded' in company_new and company_new['founded'] != company_rec['founded']:
      diff['founded'] = company_new['founded']
    if 'wikipedia' in company_new and company_new['wikipedia'] != company_rec['wikipedia']:
      diff['wikipedia'] = company_new['wikipedia']
    if len( diff ) > 0:
      diff['date_updated'] = Mysql.now()
      Mysql.update( 'companies', diff, { 'company_id' : company_id } )

  """
    createMeta
    @params:
      company_id : int
      meta       : dict {
        'meta_key' : 'meta_value',
        'meta_key' : 'meta_value',
      }
  """
  def createMeta( self, company_id, metas ):
    company_meta = self.getMeta( company_id )
    update_meta = []
    new_meta    = []
    for meta_key, meta_value in metas.iteritems():
      if meta_key in company_meta:
        if meta_value != company_meta[ meta_key ]:
          update_meta.append( metas[ meta_key ] )
      else:
        new_meta.append( metas[ meta_key ] )
    for meta in new_meta:
      for key, value in meta.iteritems():
        the_insert = {
          'meta_key'     : key,
          'meta_value'   : value,
        }
        Mysql.insert( 'company_meta', the_insert )
    for meta in update_meta:
      for key, value, in meta.iteritems():
        the_update = {
          'meta_value'   : value,
          'date_updated' : Mysql.now()
        }
        the_where = { 'meta_key': key }
        Mysql.update( 'company_meta', the_update, the_where )

# End File: models/ModelCompany.py
