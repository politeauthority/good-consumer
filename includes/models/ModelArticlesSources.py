#!/usr/bin/python                                                                                                
"""
  Articles Sources
  This model controls interactions with company articles
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')

class ModelArticlesSources( object ):
  """
    AritcleSource {
      'id'            : 50,
      'name'          : 'New York Times',
      'url'           : 'http://www.nytimes.com/'
      'article_count' : 20,
      'date_updated'  : '2014-07-15 23:55:12'
    }
  """

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self, limit = None ):
    """
      @return: [ ArticleSource{}, ArticleSource{} ]
    """
    qry = """SELECT * FROM 
      `%s`.`articles_sources` 
      ORDER BY `article_count` DESC """ % ( self.db_name )
    if limit:
      qry = qry + """ LIMIT %s;""" % limit
    else:
      qry = qry + ";"
    articles = Mysql.ex( qry )
    return articles

  def getByID( self, article_id ):
    qry = """SELECT * FROM
      `%s`.`articles_sources` 
      WHERE `id` = "%s"; """ % ( self.db_name, article_id )
    source = Mysql.ex(qry)
    if len( source ) == 0:
      return False
    return source[0]
  
  def create( self, source ):
    """
      Make a new articles source
      @params:
        source : dict{ 'name': '', 'url': '' }
      @return:
        id : int()
    """
    qry = """SELECT * FROM 
      `%s`.`articles_sources` 
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
      Mysql.insert( 'articles_sources', args )
      qry = """SELECT * FROM 
        `%s`.`articles_sources` 
        WHERE `url` = "%s";""" % (
        self.db_name,
        source['url']
      )
      exists = Mysql.ex(qry)
    return exists[0]['id']

  def updateCounts( self ):
    """
      Sets the proper article count by each unique source.
    """
    qry = """ SELECT distinct(`source_id`), count(*) as c 
      FROM `%s`.`articles` GROUP BY 1 ORDER BY 2;""" % self.db_name
    sources = Mysql.ex( qry )
    for source in sources:
      the_args  = { 'article_count' : source['c'] }
      the_where = { 'id' : source['source_id'] }
      Mysql.update( 'articles_sources', the_args, the_where )
    return True

# End File: includes/models/ModelArticles.py
