#!/usr/bin/python                                                                                                
"""
  Company News
  This model controls interactions with company news articles
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelCompanyNews( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self ):
    qry = """SELECT * FROM 
      `%s`.`company_news`;""" % ( self.db_name )
    c_types = Mysql.ex( qry )
    return c_types
  
  def create( self, company_id, article ):
    """
      Make a new news article associated with the company
    """
    qry = """SELECT * FROM 
      `%s`.`company_news` 
      WHERE `url` = "%s"; """ % ( 
        self.db_name, 
        article['url'] 
    )
    exists = Mysql.ex(qry)
    if len( exists ) == 0:
      args = {
        'company_id'   : company_id,
        'url'          : article['url'],
        'headline'     : article['headline'],
        'publish_date' : article['pubDate'],
        'content'      : article['content'],
      }
      Mysql.insert( 'company_news', args )

# End File: models/ModelCompanyNews.py
