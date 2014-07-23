#!/usr/bin/python
"""
  Simple Stats
  Collects simple stats for web display
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')

class ModelSimpleStats( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def countOfCompanies( self ):
    qry = "SELECT count(*) as c FROM `%s`.`companies`;" % self.db_name
    return Mysql.ex( qry )[0]['c']

  def countOfPeople( self ):
  	qry = "SELECT count(*) as c FROM `%s`.`people`;" % self.db_name
  	return Mysql.ex(qry)[0]['c']

  def countOfArticles( self ):
    qry = "SELECT count(*) as c FROM `%s`.`articles`;" % self.db_name
    return Mysql.ex(qry)[0]['c']

  def countOfArticlesSources( self ):
    qry = "SELECT count(*) as c FROM `%s`.`articles_sources`;" % self.db_name
    return Mysql.ex(qry)[0]['c']

  def runningCompanyStatus( self ):
    qry = """SELECT distinct( `record_status` ), count(*) as `c`
      FROM `%s`.`companies`
      GROUP BY 1
      ORDER BY 1;""" % self.db_name
    return Mysql.ex(qry )

  def runningPeopleStatus( self ):
    qry = """SELECT distinct( `record_status` ), count(*) as `c`
      FROM `%s`.`people`
      GROUP BY 1
      ORDER BY 1;""" % self.db_name
    return Mysql.ex(qry )  

  def runningArticlesStatus( self ):
    qry = """SELECT distinct( `record_status` ), count(*) as `c`
      FROM `%s`.`articles`
      GROUP BY 1
      ORDER BY 1;""" % self.db_name
    return Mysql.ex(qry )        

# End File: includes/models/ModelSimpleStats.py
