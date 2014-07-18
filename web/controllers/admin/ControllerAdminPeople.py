#!/usr/bin/python
"""
  Admin People Controller
  This Controller handles Admin - People interactions
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdminPeople( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout   = 'admin/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    }

  def index( self ):
    ModelPeople = MVC.loadModel('People')
    data = { 'people' : ModelPeople.getAll() }
    return self.Renderer.build( 'admin/people/index.html', data )
  index.exposed = True

  def info( self, person_id = None ):
    ModelPerson = MVC.loadModel('Person')
    return ModelPerson.getByID( person_id )
  info.exposed = True
  
# End File: controllers/ControllerAdminPeople.py
