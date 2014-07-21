#!/usr/bin/python
"""
  Admin Articles Controller
  This Controller handles Admin - News interactions
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

Debugger = MVC.loadHelper('Debug')

class ControllerAdminArticles( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout   = 'admin/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    }

  def index( self ):
    ModelArticles        = MVC.loadModel('Articles')
    ModelArticlesSources = MVC.loadModel('ArticlesSources')
    data = { 
      'articles' : ModelArticles.getAll(),
      'sources'  : ModelArticlesSources.getAll()
    }
    return self.Renderer.build( 'admin/articles/index.html', data )
  index.exposed = True

  def article( self, article_id = None ):
    ModelArticles = MVC.loadModel('News')    
    data = {
      'article' : ModelArticles.getByID( article_id, load_level = 'full' )
    }
    return self.Renderer.build( 'admin/articles/article.html', data )
  article.exposed = True

  def source( self, source_id = None ):
    ModelArticles = MVC.loadModel('Articles')
    data = {
      'articles' : ModelArticles.getBySource( source_id )
    }
    return self.Renderer.build( 'admin/articles/source.html', data )    
  source.exposed = True  

# End File: web/controllers/ControllerAdminNews.py
