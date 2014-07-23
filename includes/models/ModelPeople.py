#!/usr/bin/python
"""                                                                                                
  Model People
  This model controls interactions for collections of people
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelPeople( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    # qry = """SELECT * FROM `%s`.`people` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    qry = """SELECT * FROM `%s`.`people`;""" % ( self.db_name )    
    people = Mysql.ex( qry )
    return people

  def getUpdateSet( self, limit = 200, hide = True, load_level ='light' ):
    qry = """SELECT * FROM `%s`.`people` WHERE `record_status` = 0 """ % self.db_name
    if hide:
      qry += """ AND `display` = 1 """
    qry += """ORDER BY `date_updated` ASC LIMIT %s;""" % limit
    update_people = Mysql.ex( qry )
    # @todo: come up with a way of looking harder for work to do here
    if len( update_people ) == 0:
      return []
    people_ids = []
    for p in update_people:
      people_ids.append( p['id'] )
    qry2 = """UPDATE `%s`.`people`
      SET `record_status` = 1
      WHERE `id` IN ( %s );""" % ( self.db_name, Mysql.list_to_string( people_ids ) )
    Mysql.ex(qry2)
    return update_people

  def getRecentlyUpdated( self, limit = 20 ):
    qry = """SELECT * FROM `%s`.`people` ORDER BY `date_updated` DESC LIMIT %s;""" % ( self.db_name, limit )
    return Mysql.ex( qry )

# End File: includes/models/ModelCompanies.py