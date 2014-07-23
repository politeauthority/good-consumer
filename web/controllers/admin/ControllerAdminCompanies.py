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
Debugger = MVC.loadHelper('Debug')

class ControllerAdminCompanies( object ):

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
    data = { 'companies' : ModelCompanies.getAll( hide = False ) }
    return self.Renderer.build( 'admin/companies/index.html', data )
  index.exposed = True

  def info( self, company_id = None ):
    if company_id:
      ModelCompany     = MVC.loadModel('Company')
      # ModelCompanyNews = MVC.loadModel('CompanyNews')
      company = ModelCompany.getByID( company_id, 'full', hide = False )     
      if not company:
        raise cherrypy.HTTPRedirect( '/admin/error/?e="cantfindcompany"' )
      ModelArticles = MVC.loadModel('Articles')
      data = { 
        'company' : company,
        'articles' : ModelArticles.getByCompany( company_id )
      }
      return self.Renderer.build( 'admin/companies/info.html', data )
    else:
      raise cherrypy.HTTPRedirect( '/admin/error/?e="cantfindcompany"' )      
  info.exposed = True

  def types( self ):
    ModelCompanyTypes = MVC.loadModel('CompanyTypes')
    data = {
      'types' : ModelCompanyTypes.getAll()
    }
    return self.Renderer.build( 'admin/companies/types.html', data )
  types.exposed = True

  def delete( self, meta_id ):
    Settings = MVC.loadHelper( 'Settings')
    Settings.delete( meta_id )
    raise cherrypy.HTTPRedirect( '/admin/settings' )
  delete.exposed = True
  
# End File: web/controllers/ControllerAdminCompanies.py
