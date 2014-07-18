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
    ModelNews = MVC.loadModel('News')
    data = { 'articles' : ModelNews.getAll() }
    return self.Renderer.build( 'admin/news/index.html', data )
  index.exposed = True

  def article( self, article_id = None ):
    return 'article!'
  article.exposed = True
  
# End File: controllers/ControllerAdminNews.py
