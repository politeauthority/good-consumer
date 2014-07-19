#!/usr/bin/python
"""
  Company Model
  This model controls interactions for a single company
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')
Debugger = MVC.loadHelper('Debug')

class ModelCompany( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']
    self.meta_key_type = {
      'people'   : 'entity_people',
      'job_news' : 'date_time'
    }

  def getByID( self, company_id, load_level = 'light', hide = True ):
    """
      Gets a company by ID
      @params:
        company_id : int( ) ex: 5
      return company      
    """
    qry = """SELECT * FROM `%s`.`companies` WHERE `company_id` = "%s" """ % ( self.db_name, company_id )
    if hide:
      qry += " AND `display` = 1;"
    else:
      qry += ";"
    company = Mysql.ex( qry )
    if len( company ) == 0:
      return False
    company = self.getLoadLevel( company[0], load_level )
    return company

  def getBySlug( self, company_slug, load_level = 'light' ):
    """
      Get a company by the slugged name
      @params:
        company_slug : str( ) ex: oscar-myer
      return company
    """
    qry = """SELECT * FROM `%s`.`companies` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( company_slug ) )
    company = Mysql.ex( qry )
    if len( company ) == 0:
      return False
    company = self.getLoadLevel( company[0], load_level )
    return company

  def getByName( self, company_name, load_level = 'light' ):
    """
      Get a company by the exact name
      @params : str( ) Oscar Myer
      @return company
    """
    qry = """SELECT * FROM `%s`.`companies` WHERE `name` = "%s"; """ % ( self.db_name, Mysql.escape_string( company_name ) )
    company = Mysql.ex( qry )
    return company[0]    

  def getRandom( self ):
    """
      Gets a random company
      @return company
    """
    import random    
    count = Mysql.ex( "SELECT count(*) AS c FROM `%s`.`companies`;" % self.db_name )
    if count == 0:
      return False
    the_id = random.randint( 1, count[0]['c'] )
    company = self.getByID( the_id )
    return company

  def getMeta( self, company_id, metas = None ):
    """
      @params:
        company_id : int()
        metas : list() meta keys
      @return: 
        dict{ 'meta_key': 'meta_value' }
    """
    qry = """SELECT * FROM `%s`.`company_meta` WHERE `company_id`="%s" """ % ( self.db_name, company_id )
    if metas:
      if isinstance( metas, str ):
        metas = [ metas ]
      meta  = Mysql.list_to_string( metas )
      qry  += "AND meta_key IN( %s );" % meta
    else:
      qry += ";"
    the_meta = Mysql.ex( qry )
    export_meta = {}
    for meta in the_meta:
      export_meta[ meta['meta_key'] ] = meta['meta_value']
    return export_meta

  def getLoadLevel( self, company, load_level = 'light' ):
    if load_level == 'full':
      company['meta'] = self.getMeta( company['company_id'] )
      if 'people' in company['meta']:
        ModelPeople = MVC.loadModel('People')
        people      = []
        if ',' in company['meta']['people']:
          for person_id in company['meta']['people'].split(','):
            people.append( ModelPeople.getByID( person_id ) )
        else:
          people.append( ModelPeople.getByID( company['meta']['people'] ) )
        company['meta']['people'] = people
      ModelCompanyTypes = MVC.loadModel('CompanyTypes')
      company['type']   = ModelCompanyTypes.getByID( company['type'] )
    return company

  def create( self, company ):
    """
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
    new_company = {}
    if 'company_id' in company:
      company_rec = self.getByID( company['company_id'], hide = False )
      self.updateDiff( company, company_rec )
    if 'name' not in company or company['name'] == '':
      return False
    qry = """SELECT * FROM `%s`.`companies` WHERE name = "%s";""" % ( self.db_name, company['name'] )
    exists = Mysql.ex( qry )
    if len( exists ) != 0:
      company_id = self.updateDiff( company, exists[0] )
    else:
      new_company['name'] = company['name']
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
    return company_id

  def updateDiff( self, company_new, company_rec ):
    """
      Updates a company record by a diff of the values
      @params:
        company_new : dict{ }
        company_rec : dict{ }
    """
    company_id = company_rec['company_id']
    diff = {}
    company_fields = [
      'name', 
      'slug', 
      'type', 
      'industry', 
      'headquarters', 
      'founded',
      'wikipedia',
      'record_status']
    for field in company_fields:
      if field in company_new and company_new[ field ] != company_rec[ field ]:
        diff[ field ] = company_new[ field ]   
    diff['date_updated'] = Mysql.now()
    Mysql.update( 'companies', diff, { 'company_id' : company_id } )
    # Debugger.write( 'Company: %s' % company_id, diff )
    return company_id

  def createMeta( self, company_id, metas ):
    """
      @params:
        company_id : int
        meta       : dict {
          'meta_key' : 'meta_value',
          'meta_key' : 'meta_value',
        }
    """
    company_meta = self.getMeta( company_id )
    update_meta = []
    new_meta    = []
    for meta_key, meta_value in metas.iteritems():
      if meta_key in company_meta:
        if meta_value != company_meta[ meta_key ]:
          meta_value = self.__prepare_meta_value( meta_value )
          update_meta.append( { meta_key : meta_value } )
      else:
        new_meta.append( {  meta_key : meta_value } )
    # Write new meta
    for meta in new_meta:
      for key, value in meta.iteritems():
        the_insert = {
          'company_id'   : company_id,
          'meta_key'     : key,
          'meta_value'   : value,
        }
        Mysql.insert( 'company_meta', the_insert )
    # Updated existing meta
    for meta in update_meta: 
      for key, value, in meta.iteritems():
        the_update = {
          'meta_value'   : value,
          'date_updated' : Mysql.now()
        }
        the_where = { 
          'meta_key'   : key, 
          'company_id' : company_id
        }
        Mysql.update( 'company_meta', the_update, the_where )

  def setUpdateTime( self, company_id ):
    the_update = { 'date_updated' : Mysql.now() }
    the_where  = { 'company_id' : company_id }
    Mysql.update( 'companies', the_update, the_where )

  def setMeta( self, company_id, meta_key, meta_value ):
    """
      Creates a single meta addition or update.
      @params:
        company_id : int()
        meta_key   : str()
        meta_value : int(), str(), list[], dict{}
    """
    self.createMeta( company_id, { meta_key: meta_value } )

  def __prepare_meta_value( self, meta_value ):
    """
      Creates the proper store for meta values
      @params:
        meta_value : str(), int(), list[], dict{}
      @return: SQL ready json object or str()
    """
    import json
    if isinstance( meta_value, list ):
      meta_value = json.loads( meta_value )
      print 'its a list'
    elif isinstance( meta_value, dict ):
      meta_value = json.loads( meta_value )
    print meta_value
    return meta_value

# End File: includes/models/ModelCompany.py
