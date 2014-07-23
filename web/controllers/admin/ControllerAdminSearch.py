#!/usr/bin/python
"""
  Admin Search Controller
  This Controller handles Admin - Search interactions
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdminSearch( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout   = 'admin/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    }

  def index( self ):
    ModelCompanies = MVC.loadModel('Companies')
    data = { 'companies' : ModelCompanies.getAll() }
    return self.Renderer.build( 'admin/search/index.html', data )
  index.exposed = True
  
# End File: web/controllers/ControllerAdminSearch.py
