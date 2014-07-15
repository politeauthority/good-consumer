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

  companies = MVC.loadController( 'admin/AdminCompanies' )
  news      = MVC.loadController( 'admin/AdminNews' )

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout   = 'admin/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    }    

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
    ModelJobLog      = MVC.loadModel('JobLog')
    SimpleStats = MVC.loadModel( 'SimpleStats' )
    ModelCompanies   = MVC.loadModel('Companies')
    ModelCompanyNews = MVC.loadModel('CompanyNews')
    data = {
      'jobs' : ModelJobLog.get(),
      'recently_updated_companies' : ModelCompanies.getRecentlyUpdated( limit=8 ),
      'recently_added_news'        : ModelCompanyNews.getAll( 8 ),
      'stats'          : {
        'company_count' : SimpleStats.countOfCompanies(),
        'people_count'  : SimpleStats.countOfPeople(),
        'article_count' : SimpleStats.countOfNews()
      }
    }
    return self.Renderer.build('admin/dashboard.html', data )    
  dashboard.exposed = True

# End File: controllers/admin/ControllerAdminHome.py
