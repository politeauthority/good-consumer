#!/usr/bin/python
"""                                                                                                    
  Home Controller                                                                                                     
  Primary web controller
"""
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
    self.Renderer.layout   = 'frontend/layout.html'

  """
    Index
    Main home page.
  """
  def index( self ):
    Company = MVC.loadModel( 'Company' )
    SimpleStats = MVC.loadModel( 'SimpleStats' )
    data = { 
      'random_company' : Company.getRandom(),
      'stats'          : {
        'company_count' : SimpleStats.countOfCompanies(),
        'people_count'  : SimpleStats.countOfPeople()
      }
    }
    return self.Renderer.build( 'frontend/index.html', data )
  index.exposed = True

  """
    Companies
    List of all companies.
  """
  def companies( self ):
    Compaines = MVC.loadModel( 'Companies' )
    data = {
      'companies' : Compaines.getAll()
    }
    return self.Renderer.build( 'frontend/companies.html', data )
  companies.exposed = True

  """
    Info
    General Information page for a single company
  """
  def info( self, slug_name ):
    CompanyModel = MVC.loadModel( 'Company' )
    Company = CompanyModel.getBySlug( slug_name )
    if Company:
      data = { 'company' : Company }
      return self.Renderer.build( 'frontend/info.html', data )
    else:
      data = { 'searched_for' : slug_name }
      return self.Renderer.build( 'errors/company_not_found.html', data )
  info.exposed = True

  """
    About
    Static page for about information
  """
  def about( self ):
    return self.Renderer.build( 'frontend/about.html' )
  about.exposed = True
  
  """
    Donate
    Static page for about information
  """
  def donate( self ):
    return self.Renderer.build( 'frontend/donate.html' )
  donate.exposed = True
  
  """
    Contact
    Static page for about information
  """
  def contact( self ):
    return self.Renderer.build( 'frontend/contact.html' )
  contact.exposed = True

  """
    Error Page 404
  """
  # def error_page_404( status, message, traceback, version ):
  #   Renderer = MVC.loadDriver('Renderer')
  #   return Renderer.make( 'errors/404.html', header = False )
  # cherrypy.config.update({'error_page.404': error_page_404})

# End File: controllers/ControllerHome.py
