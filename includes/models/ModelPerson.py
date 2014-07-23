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
  """
  Person {
      'id'            : 123,
      'name'          : 'Donald Trump'
      'slug'          : 'donald-trump'
      'wikipedia'     : '',
      'display'       : 1
      'record_status' : 0,
      'date_updated'  : '2014-07-15 23:55:12'
    }

    Meta Keys {
      'assoc_company' : 'comma',
      'assoc_people'  : 'comma'
    }

    Record Status Keys {
        0  :  Raw
        1  :  Flagged for Update
        2  :  In Process
        3  :  Finished
    }
    """

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getByID( self, person_id, hide = True, load_level = 'light' ):
    qry = """SELECT * FROM `%s`.`people` WHERE `id` = "%s"; """ % ( self.db_name, person_id )
    person = Mysql.ex( qry )
    if len( person ) == 0:
      return False
    person = self.getLoadLevel( person[0], load_level )
    return person

  def getBySlug( self, person_slug ):
    """
      Get a person by the slugged name
      @params:
        slug : str( ) ex: donald-trump
      return person
    """
    qry = """SELECT * FROM `%s`.`people` WHERE `slug` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_slug ) )
    person = Mysql.ex( qry )
    return person[0]

  def getByName( self, people_name ):
    """
      Get a person by the exact name
      @params : str( ) Donald Trump
      @return person
    """
    qry = """SELECT * FROM `%s`.`people` WHERE `name` = "%s"; """ % ( self.db_name, Mysql.escape_string( person_name ) )
    person = Mysql.ex( qry )
    if len( person ) == 0:
      return False
    return person[0]    

  def getByWiki( self, wikipedia_url ):
    """
      Get a person by the LIKE wiki url
      @params : str( ) /wiki/Donald_Trump
      @return person
    """
    qry  = 'SELECT * FROM `'+self.db_name+'`.`people` WHERE `wikipedia` LIKE "%'+ Mysql.escape_string( wikipedia_url ) + '%";'
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

  def getLoadLevel( self, person, load_level = 'light' ):
    if load_level == 'full':
      person['meta'] = self.getMeta( person['id'] )
      if person['meta']:      
        if 'people' in person['meta']:
          ModelPeople = MVC.loadModel('People')
          people      = []
    return person

  def getMeta( self, people_id, metas = None ):
    """
      @params:
        company_id : int()
        metas : list() meta keys
      @return: 
        dict{ 'meta_key': 'meta_value' }
    """
    MetaStore = MVC.loadHelper('MetaStore')
    return MetaStore.get( entity = 'people', entity_id = people_id  )


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
    qry = """SELECT * FROM `%s`.`people` WHERE `wikipedia` = "%s";""" % ( self.db_name, person['wikipedia'] )
    exists = Mysql.ex( qry )
    if len( exists ) != 0:
      self.updateDiff( person, exists[0] )
      person_id = exists[0]['id']
    else:
      if 'name' in person:
        new_person['name'] = person['name']
      else:
        new_person['name'] = ''
      if 'slug' not in person:
        if 'name' not in person:
          new_person['name'] = ''
        else:
          new_person['slug'] = Misc.slug( person['name'] )
      if 'wikipedia' not in person:
        new_person['wikipedia'] = ''
      else:
        new_person['wikipedia'] = person['wikipedia']
      Mysql.insert( 'people', new_person )
      person_id = self.getByWiki( new_person['wikipedia'] )['id']
    if 'meta' in person:
      self.createMeta( person_id, person['meta'] )
    return person_id

  def updateDiff( self, person_new, person_rec ):
    """
      Updates a person record by a diff of the values
    """
    person_id = person_rec['id']
    diff = {}
    if 'slug' in person_new and person_new['slug'] != person_rec['slug']:
      diff['slug'] = person_new['slug']
    if 'wikipedia' in person_new and person_new['wikipedia'] != person_rec['wikipedia']:
      diff['wikipedia'] = person_new['wikipedia']
    if len( diff ) > 0:
      diff['date_updated'] = Mysql.now()
      Mysql.update( 'people', diff, { 'id' : person_id } )

  def createMeta( self, person_id, metas ):
    """
      @params:
        company_id : int
        meta       : dict {
          'meta_key' : 'meta_value',
          'meta_key' : 'meta_value',
        }
    """
    MetaStore = MVC.loadHelper('MetaStore')
    MetaStore.create( 'people', person_id, metas  )

# End File: includes/models/ModelPerson.py
