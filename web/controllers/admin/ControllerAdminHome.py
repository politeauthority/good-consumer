#!/usr/bin/python
"""
  Admin Home Controller
  Handles all /admin URL requests.
  File : web/controllers/admin/ControllerAdminHome.py
"""
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
  people    = MVC.loadController( 'admin/AdminPeople' )
  articles  = MVC.loadController( 'admin/AdminArticles' )
  search    = MVC.loadController( 'admin/AdminSearch' )

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
    SimpleStats      = MVC.loadModel('SimpleStats')
    ModelCompanies   = MVC.loadModel('Companies')
    ModelPeople      = MVC.loadModel('People')
    ModelArticles    = MVC.loadModel('Articles')
    data = {
      'jobs' : ModelJobLog.get(),
      'recently_updated_companies' : ModelCompanies.getRecentlyUpdated( limit=8 ),
      'recently_updated_people'    : ModelPeople.getRecentlyUpdated( limit=8 ),
      'recently_added_articles'    : ModelArticles.getAll( 8 ),
      'stats'          : {
        'company_count'     : SimpleStats.countOfCompanies(),
        'people_count'      : SimpleStats.countOfPeople(),
        'article_count'     : SimpleStats.countOfArticles(),
        'sources_count'     : SimpleStats.countOfArticlesSources(),
        'company_status'    : SimpleStats.runningCompanyStatus(),
        'people_status'     : SimpleStats.runningPeopleStatus(),
        'articles_status'   : SimpleStats.runningArticlesStatus(),

      }
    }
    return self.Renderer.build('admin/dashboard.html', data )    
  dashboard.exposed = True

  def edit_ajax( self, edit_type, **kwargs ):
    if edit_type == 'company':
      ModelCompany = MVC.loadModel('Company')
      print ' '
      print ' '
      print ' '
      print kwargs
      company = {
        'id'    : '',
        'name'  : kwargs['name'],
        'slug'  : kwargs['slug']
      }
      if ModelCompany.create( company ):
        return 'success'
      else:
        return 'failure'
  edit_ajax.exposed = True     

# End File: web/controllers/admin/ControllerAdminHome.py
