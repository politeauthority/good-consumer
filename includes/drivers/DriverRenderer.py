#!/usr/bin/python                                                   
"""
  Renderer Driver 
  This driver helps build an html page 
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

from jinja2 import Environment, FileSystemLoader

class DriverRenderer( object ):

  def __init__( self ):
    self.parse_html  = True
    self.layout_h    = False
    self.layout_f    = False
    self.layout      = False
    self.layout_args = {}
    self.env = Environment( loader=FileSystemLoader( MVC.web_dir + 'views') )

  def build( self, view, data = None, layout = None ):
    html_source = self.__draw( view, data )
    if layout:
      self.layout = layout
    layout_data = { 'page_yield' : html_source }
    if data:
      if 'layout' in data:
        layout_data['layout'] = data['layout']
      if len( self.layout_args ) > 0:
        if 'layout' in layout_data:
          layout_data['layout'].append( self.layout_args) #this is probably wrong
        else:
          layout_data['layout'] = self.layout_args
    else:
      layout_data['layout'] = ''
    html_source = self.__draw( self.layout, layout_data )
    return html_source

  def make( self, view, data = None, header = None, footer = None ):
    html_source = ''
    if self.layout_h != False:
      if header != False:
        html_source = self.__draw( self.layout_h, header )
    
    html_source = html_source + self.__draw( view, data )

    if self.layout_f != False or header == False:
      if header != False:
        html_source = html_source + self.__draw( self.layout_f, footer )

    html_source = self.__parse_html( html_source )
    return html_source
  
  def __draw( self, view, data = None ):
    view = self.env.get_template( view )
    return view.render( d = data )
  
  def __parse_html( self, source ):
    if self.parse_html:
      if '<_h>' in source or '<_b>' in source:
        from bs4 import BeautifulSoup
        import re
        source = BeautifulSoup( source )
        built_header = ''
        built_body   = ''
        if source._h:
          original_move_content   = str( source._h )
          original_header_content = str( source.head )
          original_body_content   = str( source.body )
          
          header_content = original_move_content.replace('<_h>', '' ).replace('</_h>', '')
          built_header = original_header_content[:-7] + "\n<!-- Auto moved -->\n" + header_content + "\n<!-- / Auto moved --></head>"

          if original_move_content in original_body_content:
            built_body = original_body_content.replace( original_move_content, '' )
          else:
            built_body = original_body_content
        else:
          built_header = str( source.head )
          built_body   = str( source.body )

        if source._b:
          original_move_content = str( source._b )
          move_content          = original_move_content.replace('<_b>', '').replace('</_b>', '')
          built_body = built_body.replace( original_move_content, '' )      
          built_body = "<body>" + move_content + built_body[6:]
          if built_header != '':
            source = built_header + built_body
          else:
            source = str( source.head ) + built_body 
          source = BeautifulSoup( source )
        return source.prettify()
    return source

# End File: driver/DriverRenderer.py
