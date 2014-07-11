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

class ModelPerson( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getByID( self, person_id ):
    if isinstance( person_id, int ):
      qry = """SELECT * FROM `%s`.`people` WHERE `person_id` = %s; """ % ( self.db_name, person_id )
      person = Mysql.ex( qry )[0]
      return person

  """
    getBySlug
    Get a company by the slugged name
    @params:
      company_slug : str( ) ex: oscar-myer
    return company
  """
  def getBySlug( self, person_slug ):
    qry = """SELECT * FROM `%s`.`person` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_slug ) )
    person = Mysql.ex( qry )
    return company[0]

  def getByName( self, person_name ):
    """
      getByName
      Get a company by the exact name
      @params : str( ) Oscar Myer
      @return company
    """
    qry = """SELECT * FROM `%s`.`people` WHERE `name` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_name ) )
    person = Mysql.ex( qry )
    return person[0]    

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

  def create( self, person ):
    """
      Stores a new person if it does not already exist.
      @params:
        person : {
          'name'      : 'Donald Trump',
          'slug'      : 'donald-trump',
          'wikipedia' : 'http://en.wikipedia.org/wiki/Mondel%C4%93z_International',
          'meta'      : {
            'desc'  : 'The company was founded on values.'
         }
        }
      @return:
        False or new company_id
    """
    Misc = MVC.loadHelper( 'Misc' )
    new_person = {}
    if 'name' not in person or person['name'] == '':
      return False
    qry = """SELECT * FROM `%s`.`people` WHERE name = "%s";""" % ( self.db_name, person['name'] )
    exists = Mysql.ex( qry )
    if len( exists ) != 0:
      self.updateDiff( person, exists[0] )
      person_id = exists[0]['person_id']
    else:
      new_person['name'] = person['name']
      if 'slug' not in person:
        new_person['slug'] = Misc.slug( person['name'] )
      if 'wikipedia' not in person:
        new_person['wikipedia'] = ''
      else:
        new_person['wikipedia'] = person['wikipedia']
      Mysql.insert( 'people', new_person )
      person_id = self.getByName( new_person['name'] )['person_id']
    if 'meta' in person:
      self.createMeta( person_id, person['meta'] )

  """
    updateDiff
    Updates a company record by a diff of the values
  """
  def updateDiff( self, person_new, person_rec ):
    person_id = person_rec['person_id']
    diff = {}
    if 'slug' in person_new and person_new['slug'] != person_rec['slug']:
      diff['slug'] = person_new['slug']
    if 'wikipedia' in person_new and person_new['wikipedia'] != person_rec['wikipedia']:
      diff['wikipedia'] = person_new['wikipedia']
    if len( diff ) > 0:
      diff['date_updated'] = Mysql.now()
      Mysql.update( 'people', diff, { 'person_id' : person_id } )

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
