#!/usr/bin/python                                                                                                
"""
  News Sources
  This model controls interactions with company news articles
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')

class ModelNewsSources( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self, limit = None ):
    qry = """SELECT * FROM 
      `%s`.`news_sources` 
      ORDER BY `date_updated` DESC """ % ( self.db_name )
    if limit:
      qry = qry + """ LIMIT %s;""" % limit
    else:
      qry = qry + ";"
    news = Mysql.ex( qry )
    return news

  def getByID( self, article_id ):
    qry = """SELECT * FROM
      `%s`.`news_sources` WHERE 
      company_news_id = `%s` """ % ( self.db_name, article_id )
    article = Mysql.now(qry)
    if len( article ) == 0:
      return False
    return article[0]
  
  def create( self, source ):
    """
      Make a new news source
      @params:
        source : dict{ 'name': '', 'url': '' }
      @return:
        news_source_id : int()
    """
    qry = """SELECT * FROM 
      `%s`.`news_sources` 
      WHERE `url` = "%s"; """ % ( 
        self.db_name, 
        source['url'] 
    )
    exists = Mysql.ex(qry)
    if len( exists ) == 0:
      args = {
        'name'    : source['name'],
        'url'     : source['url'],
      }
      Mysql.insert( 'news_sources', args )
      qry = """SELECT * FROM 
        `%s`.`news_sources` 
        WHERE `url` = "%s";""" % (
        self.db_name,
        source['url']
      )
      exists = Mysql.ex(qry)
    return exists[0]['source_id']

# End File: models/ModelCompanyNews.py
