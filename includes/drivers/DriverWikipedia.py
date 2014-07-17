#!/usr/bin/python
"""
  Wikipedia Driver
  Helps fetch and organize content from Wikipedia
"""

import sys
import os
sys.path.append( '../../', )
from MVC import MVC
MVC = MVC()
# End file header

import urllib2
from bs4 import BeautifulSoup

TorScrape = MVC.loadDriver('TorScrape')

class DriverWikipedia( object ):

  def get( self, fetch_type, wiki_url ):
    sourced_info = {}
    soup = self.__get_soup( wiki_url )
    infobox = self.__parse_infobox( fetch_type, soup )
    sourced_info['infobox'] = infobox
    return sourced_info

  def __get_soup( self, wiki_url ):
    try:
      wiki = urllib2.urlopen( wiki_url  )
      soup = BeautifulSoup( wiki )
      return soup
    except urllib2.HTTPError:
      print '404 Error Fetching: ', wiki_url
      return False

  def __parse_infobox( self, fetch_type, soup ):
    info = { }
    infobox = soup.find( 'table', { 'class' : 'infobox' } )
    if infobox == None:
      return info   
    infobox_rows =  infobox.find_all( 'tr' )
    for row in infobox_rows:
      if fetch_type == 'company':
        if row.find_all('a', { 'title': 'Types of business entity' } ):
          o_types = row.find( 'td' ).find_all( 'a' )
          c_types = []
          for o in o_types:
            the_type = {
              'name'      : o.text,
              'wikipedia' : 'http://en.wikipedia.org' + o['href']
            }
            c_types.append( the_type )
          # type_ids = ModelCompanyTypes.getIDsByName( c_types, create_if_not_exists = True )
          info['type'] = c_types
        elif 'Founder' in str( row.th ):
          info['people'] = []
          for person in row.td.findAll( 'a' ):
            p = {
              'name'      : person.text,
              'wikipedia' : 'http://en.wikipedia.org' + person['href']
            }
            info['people'].append( p )
        elif 'Key People' in str( row.th ):
          if 'people' not in info:
            info['people'] = []
      elif fetch_type == 'person':
        info = {}
    return info

# End File: driver/DriverWikipedia.py
