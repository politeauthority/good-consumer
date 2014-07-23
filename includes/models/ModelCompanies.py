#!/usr/bin/python
"""                                                                                                
  Model Companies
  This model controls interactions for collections of companies
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql  = MVC.loadDriver('Mysql')
Debugger = MVC.loadHelper('Debug')

class ModelCompanies( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self, hide = True ):
    qry = """SELECT * FROM `%s`.`companies`""" % ( self.db_name )
    if hide:
      qry += """ WHERE `display`="1";"""
    else:
      qry += ";"
    companies = Mysql.ex( qry )
    return companies

  def getUpdateSet( self, limit = 10, hide = True ):
    """
    Gets a set of company ids 
    """
    limit = 5
    # Check the raw status
    qry = """SELECT * FROM 
      `%s`.`companies` 
      WHERE `record_status` = 0 """ % self.db_name
    if hide:
      qry += """ AND `display` = 1 """
    qry += """ORDER BY `date_updated` ASC LIMIT %s;""" % limit
    update_companies = Mysql.ex( qry )
    final_set = []
    for c in update_companies:
      final_set.append( final_set )
    # Check the flagged status
    if len( final_set ) < limit:
      the_diff = limit - len( final_set )
      qry = """SELECT * FROM
        `%s`.companies
        WHERE `record_status` = 1 """ % self.db_name
      qry += """ORDER BY `date_updated` ASC LIMIT %s;""" % the_diff 
      update_companies_added = Mysql.ex( qry ) 
      for c in update_companies_added:
        final_set.append(c)
    company_ids = []
    for c in final_set:
      company_ids.append( c['id'] )
    qry2 = """UPDATE `%s`.`companies`
      SET `record_status` = 2
      WHERE `id` IN ( %s );""" % ( self.db_name, Mysql.list_to_string( company_ids ) )
    Debugger.write( 'qry', qry2)
    Mysql.ex(qry2)
    return update_companies

  def getRecentlyUpdated( self, limit = 20, hide = True ):
    qry = """SELECT * FROM 
      `%s`.`companies` 
      ORDER BY `date_updated` 
      DESC LIMIT %s;""" % ( self.db_name, limit )
    return Mysql.ex( qry )

# End File: includes/models/ModelCompanies.py