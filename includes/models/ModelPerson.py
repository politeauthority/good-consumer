#!/usr/bin/python
"""
  Person
  This model controls interactions for a single person
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

  def getBySlug( self, person_slug ):
    """
      getBySlug
      Get a person by the slugged name
      @params:
        slug : str( ) ex: donald-trump
      return person
    """
    qry = """SELECT * FROM `%s`.`person` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_slug ) )
    person = Mysql.ex( qry )
    return person[0]

  def getByName( self, person_name ):
    """
      getByName
      Get a person by the exact name
      @params : str( ) Oscar Myer
      @return person
    """
    qry = """SELECT * FROM `%s`.`people` WHERE `name` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_name ) )
    person = Mysql.ex( qry )
    return person[0]    

  def getRandom( self ):
    """
      getRandom
      Gets a random person
      @return person
    """
    import random    
    count = Mysql.ex( "SELECT count(*) AS c FROM `%s`.`people`;" % self.db_name )
    the_id = random.randint( 1, count[0]['c'] )
    people = self.getByID( the_id )
    return people

  def getMeta( self, person_id, metas = None ):
    """
      @params:
        person_id : int()
        metas : list() meta keys
      @return: 
        dict{ 
          'meta_key': 'meta_value'
        }
    """
    qry = """SELECT * FROM `%s`.`people_meta` WHERE `people_id`="%s";"""
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
          'wikipedia' : 'http://en.wikipedia.org/wiki/Donald_Trump',
          'meta'      : {
            'desc'  : 'The person was founded on values.'
         }
        }
      @return:
        False or new person_id
    """
    Misc = MVC.loadHelper( 'Misc' )
    new_person = {}
    if 'wikipedia' not in person or person['wikipedia'] == '':
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
    return person_id

  def updateDiff( self, person_new, person_rec ):
    """
      Updates a person record by a diff of the values
    """
    person_id = person_rec['person_id']
    diff = {}
    if 'slug' in person_new and person_new['slug'] != person_rec['slug']:
      diff['slug'] = person_new['slug']
    if 'wikipedia' in person_new and person_new['wikipedia'] != person_rec['wikipedia']:
      diff['wikipedia'] = person_new['wikipedia']
    if len( diff ) > 0:
      diff['date_updated'] = Mysql.now()
      Mysql.update( 'people', diff, { 'person_id' : person_id } )

  def createMeta( self, person_id, metas ):
    """
      @params:
        person_id : int
        meta       : dict {
          'meta_key' : 'meta_value',
          'meta_key' : 'meta_value',
        }
    """
    person_meta = self.getMeta( person_id )
    update_meta = []
    new_meta    = []
    for meta_key, meta_value in metas.iteritems():
      if meta_key in person_meta:
        if meta_value != person_meta[ meta_key ]:
          update_meta.append( metas[ meta_key ] )
      else:
        new_meta.append( metas[ meta_key ] )
    for meta in new_meta:
      for key, value in meta.iteritems():
        the_insert = {
          'meta_key'     : key,
          'meta_value'   : value,
        }
        Mysql.insert( 'people_meta', the_insert )
    for meta in update_meta:
      for key, value, in meta.iteritems():
        the_update = {
          'meta_value'   : value,
          'date_updated' : Mysql.now()
        }
        the_where = { 'meta_key': key }
        Mysql.update( 'people_meta', the_update, the_where )

# End File: models/ModelPerson.py
