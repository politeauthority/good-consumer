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

class ControllerAdminHome( object ):

  user     = MVC.loadController( 'admin/AdminUser' )
  settings = MVC.loadController( 'admin/AdminSettings' )

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout_h = 'admin/layout/header.html'
    self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self, **kwargs ):
    return self.Renderer.make( 'admin/login.html', header = False )
  index.exposed = True

  # @todo: make this work!
  def auth( self, **kwargs ):
    if kwargs:
      UserModel = MVC.loadModel('User')
      user      = UserModel.auth( kwargs['user_name'], kwargs['password'] )
      if user:
        return 'youre in'
      else:
        return 'youre out'
    else:
      print ''
    return ''
  auth.exposed = True

  def dashboard( self ):
    return self.Renderer.make('admin/dashboard.html')    
  dashboard.exposed = True

# End File: controllers/admin/ControllerAdminHome.py
