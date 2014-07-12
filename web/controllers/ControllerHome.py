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
    self.Renderer             = MVC.loadDriver('Renderer')
    self.Renderer.layout      = 'frontend/layout.html'
    self.Renderer.layout_args = {
      'ga_tracker' : '',
      'cdn'        : MVC.server['cdn'],
      'production' : MVC.server['production']
    } 

  def index( self ):
    """
      Main home page.
    """
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

  def companies( self ):
    """
      List of all companies.
    """
    Compaines = MVC.loadModel( 'Companies' )
    data = {
      'companies' : Compaines.getAll()
    }
    return self.Renderer.build( 'frontend/companies.html', data )
  companies.exposed = True

  def info( self, slug_name ):
    """
      General Information page for a single company
    """    
    CompanyModel = MVC.loadModel( 'Company' )
    Company = CompanyModel.getBySlug( slug_name, 'full' )
    if Company:
      data = { 'company' : Company }
      return self.Renderer.build( 'frontend/info.html', data )
    else:
      data = { 'searched_for' : slug_name }
      return self.Renderer.build( 'errors/company_not_found.html', data )
  info.exposed = True

  def people( self ):
    """
      Roster page of people
    """
    PeopleModel = MVC.loadModel('People')
    data = { 'people' : PeopleModel.getAll() }
    return self.Renderer.build( 'frontend/people.html' )

  def about( self ):
    """
      Static page for about information
    """
    return self.Renderer.build( 'frontend/about.html' )
  about.exposed = True
  
  def donate( self ):
    """
      Static page for about information
    """    
    return self.Renderer.build( 'frontend/donate.html' )
  donate.exposed = True
  
  def contact( self ):
    """
      Static page for about information
    """    
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
