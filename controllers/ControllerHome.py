#!/usr/bin/python                                                                                                      
# Admin Controller                                                                                                     
# This model controls interactions with the indoor and outdoor weather actions which need to occur                     
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
import cherrypy

class ControllerHome( object ):

  admin = MVC.loadController('admin/AdminHome')

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    #self.Renderer.layout_h = 'admin/layout/header.html'
    #self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self ):
    return self.Renderer.make('index.html')
  index.exposed = True

  def error_page_404( status, message, traceback, version ):
    Renderer = MVC.loadDriver('Renderer')
    return Renderer.make( 'errors/404.html', header = False )
  cherrypy.config.update({'error_page.404': error_page_404})

# End File: controllers/ControllerHome.py
