#!/usr/bin/python
"""
  Admin Settings Controller
  This Controller handles Admin - Company interactions
"""
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdminCompanies( object ):

  def __init__( self ):
      self.Renderer          = MVC.loadDriver('Renderer')
      self.Renderer.layout_h = 'admin/layout/header.html'
      self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self ):
    Settings = MVC.loadHelper('Settings')
    data = { 'options' : Settings.get_options() }
    return self.Renderer.make( 'admin/settings/index.html', data )
  index.exposed = True

  def update( self, **kwargs ):
    Settings = MVC.loadHelper( 'Settings')
    if kwargs['meta_id'] == '':
      Settings.create(  kwargs['meta_key'], kwargs['meta_value'] )
    else:
      Settings.update( kwargs['meta_key'], kwargs['meta_value'] )
    raise cherrypy.HTTPRedirect( '/admin/settings' )
  update.exposed = True

  def delete( self, meta_id ):
    Settings = MVC.loadHelper( 'Settings')
    Settings.delete( meta_id )
    raise cherrypy.HTTPRedirect( '/admin/settings' )
  delete.exposed = True
  
# End File: controllers/ControllerAdminCompanies.py
