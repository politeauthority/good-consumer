#!/usr/bin/python                                                                                                
"""
  Articles Model
  This model controls interactions with articles
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

Mysql    = MVC.loadDriver('Mysql')
Debugger = MVC.loadHelper('Debug')

class ModelArticles( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getAll( self, limit = 50 ):
    """
      @params: 
        limit int()
      @return: 
        [ { 
            'article_id' : 4 ,
            'headline'   : 'Some Headline',
          } 
        ]
    """    
    qry = """SELECT * FROM 
      `%s`.`articles` 
      ORDER BY `date_updated` DESC """ % ( self.db_name )
    if limit:
      qry = qry + """ LIMIT %s;""" % limit
    else:
      qry = qry + ";"
    articles = Mysql.ex( qry )
    return articles

  def getByID( self, article_id, load_level = 'light' ):
    qry = """SELECT * FROM
      `%s`.`articles` WHERE 
      `id` = "%s" """ % ( self.db_name, article_id )
    article = Mysql.ex( qry )
    if len( article ) == 0:
      return False
    article = self.getLoadLevel( article[0], load_level )
    return article
  
  def getByCompany( self, company_id ):
    qry = """SELECT * FROM 
      `%s`.`articles`
      WHERE `company_id` = "%s"
      ORDER BY `date_updated` DESC """ % ( self.db_name, company_id )
    articles = Mysql.ex( qry )
    return articles

  def getMeta( self, article_id, metas = None ):
    """
      @params:
        article_id : int()
        metas : list() meta keys
      @return: 
        dict{ 'meta_key': 'meta_value' }
    """
    qry = """SELECT * FROM `%s`.`articles_meta` WHERE `id`="%s" """ % ( self.db_name, article_id )
    if metas:
      if isinstance( metas, str ):
        metas = [ metas ]
      meta  = Mysql.list_to_string( metas )
      qry  += "AND meta_key IN( %s );" % meta
    else:
      qry += ";"
    the_meta = Mysql.ex( qry )
    export_meta = {}
    for meta in the_meta:
      export_meta[ meta['meta_key'] ] = meta['meta_value']
    return export_meta

  def getLoadLevel( self, article, load_level = 'light' ):
    if load_level == 'full':
      article['meta'] = self.getMeta( article['id'] )
    return article

  def create( self, article ):
    """
      Make a articles associated by meta
    """
    qry = """SELECT * FROM 
      `%s`.`articles` 
      WHERE `url` = "%s"; """ % ( 
        self.db_name, 
        article['url'] 
    )
    exists = Mysql.ex(qry)
    if len( exists ) == 0:
      args = {
        'url'          : article['url'],
        'headline'     : article['headline'],
        'publish_date' : article['pubDate'],
        'content'      : article['content'],
        'source_id'    : article['source_id']
      }
      Mysql.insert( 'articles', args )
      qry2 = """SELECT `id` FROM `%s`.`articles` 
      WHERE `url`="%s";""" % ( self.db_name, args['url'] )
      article_id = Mysql.ex( qry2 )[0]['id']
    else:
      article_id = exists[0]['id']
    if 'meta' in article:
      self.createMeta( article_id, article['meta'] )
    return article_id

  def createMeta( self, article_id, metas ):
    """
      @params:
        article_id : int
        meta       : dict {
          'meta_key' : 'meta_value',
          'meta_key' : 'meta_value',
        }
    """
    # Debugger.write( metas )
    MetaStore = MVC.loadHelper('MetaStore')
    MetaStore.create( 'articles', article_id, metas  )


# End File: includes/models/ModeArticles.py
