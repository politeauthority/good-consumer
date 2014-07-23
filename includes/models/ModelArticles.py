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
  """
    Article {
      'id'            : 123,
      'url'           : 'http://www.nytimes.com/2014/07/22/world/europe/ukrainian-military-and-rebel-fighters-clash-in-donetsk.html',
      'headline'      : 'Ukrainian Military and Rebel Fighters Clash in Donetsk'
      'publish_date'  : '2014-07-15 23:55:12',
      'content'       :'Heres the article and shit.',
      'source_id'     : 23,
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
    self.meta_key_type = {
      'assoc_company' : 'comma',
      'assoc_people'  : 'comma',
    }
    self.reocrd_status_keys = {
      0  :  'Raw',
      1  :  'Flagged for Update',
      2  :  'In Process',
      3  :  'Finished',
    }

  def getAll( self, limit = 50 ):
    """
      @params: 
        limit int()
      @return: [ Article{}, Article{} ]
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

  def getByID( self, article_id, hide = True, load_level = 'light' ):
    """
      Get an article at the requested load level by id.
      @return: article { }
    """
    qry = """SELECT * FROM
      `%s`.`articles` WHERE 
      `id` = "%s" """ % ( self.db_name, article_id )
    article = Mysql.ex( qry )
    if len( article ) == 0:
      return False
    article = self.getLoadLevel( article[0], hide, load_level )
    return article
  
  def getByCompany( self, company_id, load_level = 'light' ):
    """
      Gets a collection of articles by company_id
      @return [ Article{ }, Article{ } ]
    """
    qry ="""SELECT * FROM `%s`.`articles_meta` 
      WHERE `meta_key` = "assoc_company" 
      AND `meta_value` IN( "%s" ); """ % ( self.db_name, Mysql.escape_string( company_id ) )
    articles_meta = Mysql.ex( qry )
    if len( articles_meta ) == 0:
      return False
    articles = []
    for article_m in articles_meta:
      articles.append( self.getByID( article_m['id'], load_level = load_level ) )
    return articles

  def getBySource( self, source_id, load_level = 'light' ):
    """
      Get a collection of articles by the source_id
      @return [ Article{ }, Article{ } ]
    """
    qry = """SELECT * FROM `%s`.`articles` WHERE `source_id` = "%s"; """ ( self.db_name, source_id)
    articles_l = Mysql.ex( qry )
    if len( articles ) == 0:
      return False
    loaded_articles = []
    for article in articles:
      loaded_articles.append( self.getLoadLevel( article[0], hide, load_level ) )
    return loaded_articles

  def getUpdateSet( self, limit = 10, hide = True ):
    qry = """SELECT `id` FROM `%s`.`articles` WHERE `record_status` = 0 """ % self.db_name
    if hide:
      qry += """ AND `display` = 1 """
    qry += """ORDER BY `date_updated` ASC LIMIT %s;""" % limit
    update_companies = Mysql.ex( qry )
    # @todo: come up with a way of looking harder for work to do here
    if len( update_companies ) == 0:
      return []
    articles_ids = []
    for c in update_companies:
      articles_ids.append( c['id'] )
    qry2 = """UPDATE `%s`.`articles`
      SET `record_status` = 2
      WHERE `id` IN ( %s );""" % ( self.db_name, Mysql.list_to_string( articles_ids ) )
    Mysql.ex( qry2 )
    return update_companies

  def getMeta( self, article_id, metas = None ):
    """
      @params:
        article_id : int()
        metas : list() meta keys
      @return: 
        dict{ 'meta_key': 'meta_value' }
    """
    MetaStore = MVC.loadHelper('MetaStore')
    return MetaStore.get( entity='articles', entity_id=article_id  )

  def getLoadLevel( self, article, hide = True, load_level = 'light' ):
    if load_level == 'full':
      ModelArticlesSources = MVC.loadModel('ArticlesSources')
      article['source'] = ModelArticlesSources.getByID( article['source_id'] )
      article['meta'] = self.getMeta( article['id'] )
      if article['meta']:
        if 'assoc_company' in article['meta']:
          ModelCompany = MVC.loadModel('Company')
          article['meta']['companies'] = []
          for c_id in article['meta']['assoc_company']['value']:
            article['meta']['companies'].append( ModelCompany.getByID( c_id, hide ) )
    return article

  def create( self, article ):
    """
      Make an article associated by meta
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
        meta       : [ {
          "meta_key"   : 'test_meta',
          "meta_value" : '13,254',
          "meta_type"  : 'comma'
        }, ]
    """
    MetaStore = MVC.loadHelper('MetaStore')
    MetaStore.create( 'articles', article_id, metas  )

  def update( self, article ):
    print 'time to update'

# End File: includes/models/ModeArticles.py
