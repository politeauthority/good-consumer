#!/usr/bin/python                                                                                                
"""
  News Model
  This model controls interactions with news articles
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')

class ModelNews( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self, limit = None ):
    qry = """SELECT * FROM 
      `%s`.`news` 
      ORDER BY `date_updated` DESC """ % ( self.db_name )
    if limit:
      qry = qry + """ LIMIT %s;""" % limit
    else:
      qry = qry + ";"
    news = Mysql.ex( qry )
    return news

  def getByID( self, article_id ):
    qry = """SELECT * FROM
      `%s`.`news` WHERE 
      news_id = `%s` """ % ( self.db_name, article_id )
    article = Mysql.now(qry)
    if len( article ) == 0:
      return False
    return article[0]
  
  def getByCompany( self, company_id ):
    qry = """SELECT * FROM 
      `%s`.`news`
      WHERE `company_id` = "%s"
      ORDER BY `date_updated` DESC """ % ( self.db_name, company_id )
    news = Mysql.ex( qry )
    return news

  def create( self, company_id, article ):
    """
      Make a new news article associated with the company
    """
    qry = """SELECT * FROM 
      `%s`.`news` 
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
      Mysql.insert( 'news', args )

# End File: models/ModelNews.py
