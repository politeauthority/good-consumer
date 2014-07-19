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
      `%s`.`news` 
      ORDER BY `date_updated` DESC """ % ( self.db_name )
    if limit:
      qry = qry + """ LIMIT %s;""" % limit
    else:
      qry = qry + ";"
    news = Mysql.ex( qry )

    return news

  def getByID( self, article_id, load_level = 'light' ):
    qry = """SELECT * FROM
      `%s`.`news` WHERE 
      `article_id` = "%s" """ % ( self.db_name, article_id )
    article = Mysql.ex( qry )
    if len( article ) == 0:
      return False
    article = self.getLoadLevel( article[0], load_level )
    return article
  
  def getByCompany( self, company_id ):
    qry = """SELECT * FROM 
      `%s`.`news`
      WHERE `company_id` = "%s"
      ORDER BY `date_updated` DESC """ % ( self.db_name, company_id )
    news = Mysql.ex( qry )
    return news

  def getMeta( self, article_id, metas = None ):
    """
      @params:
        article_id : int()
        metas : list() meta keys
      @return: 
        dict{ 'meta_key': 'meta_value' }
    """
    qry = """SELECT * FROM `%s`.`news_meta` WHERE `article_id`="%s" """ % ( self.db_name, article_id )
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
      article['meta'] = self.getMeta( article['article_id'] )
    return article

  def create( self, article ):
    """
      Make a new news article associated by meta
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
        'url'          : article['url'],
        'headline'     : article['headline'],
        'publish_date' : article['pubDate'],
        'content'      : article['content'],
        'source_id'    : article['source_id']
      }
      Mysql.insert( 'news', args )
      qry2 = """SELECT `article_id` FROM `%s`.`news` 
      WHERE `url`="%s";""" % ( self.db_name, args['url'] )
      article_id = Mysql.ex( qry2 )[0]['article_id']
    else:
      article_id = exists[0]['article_id']
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
    article_meta = self.getMeta( article_id )
    update_meta = []
    new_meta    = []
    for meta_key, meta_value in metas.iteritems():
      if meta_key in article_meta:
        if meta_value != article_meta[ meta_key ]:
          meta_value = self.__prepare_meta_value( meta_value )
          update_meta.append( { meta_key : meta_value } )
      else:
        new_meta.append( {  meta_key : meta_value } )
    # Write new meta
    for meta in new_meta:
      for key, value in meta.iteritems():
        the_insert = {
          'article_id'   : article_id,
          'meta_key'     : key,
          'meta_value'   : value,
        }
        Mysql.insert( 'news_meta', the_insert )
    # Updated existing meta
    for meta in update_meta: 
      for key, value, in meta.iteritems():
        the_update = {
          'meta_value'   : value,
          'date_updated' : Mysql.now()
        }
        the_where = { 
          'meta_key'   : key, 
          'article_id' : article_id
        }
        Mysql.update( 'news_meta', the_update, the_where )

# End File: includes/models/ModelNews.py
