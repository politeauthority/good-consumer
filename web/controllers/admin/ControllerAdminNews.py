#!/usr/bin/python
"""
  Admin News Controller
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

class ControllerAdminNews( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout   = 'admin/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    }

  def index( self ):
    ModelNews        = MVC.loadModel('News')
    ModelNewsSources = MVC.loadModel('NewsSources')
    data = { 
      'articles' : ModelNews.getAll(),
      'sources'  : ModelNewsSources.getAll()
    }
    return self.Renderer.build( 'admin/news/index.html', data )
  index.exposed = True

  def article( self, article_id = None ):
    ModelNews = MVC.loadModel('News')    
    data = {
      'article' : ModelNews.getByID( article_id, load_level = 'full' )
    }
    return self.Renderer.build( 'admin/news/article.html', data )
  article.exposed = True

  def source( self, source_id = None ):
    ModelNews = MVC.loadModel('News')
    data = {
      'articles' : ModelNews.getBySource( source_id )
    }
    return self.Renderer.build( 'admin/news/source.html', data )    
  source.exposed = True  

# End File: web/controllers/ControllerAdminNews.py
