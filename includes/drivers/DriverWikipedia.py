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
        elif 'Key people' in str( row.th ):
          people_wikis = []
          for link in row.td.find_all( 'a' ):
            if link['href'] and link['href'][:6] =='/wiki/':
              job_titles = [ '/wiki/chief_executive_officer', '/wiki/chairmain', '/wiki/president' '/wiki/chairman', 
                '/wiki/ceo', '/wiki/board_of_dcirectors', '/wiki/President', '/wiki/chief_technology_officer', 
                '/wiki/marketing_director', '/wiki/marketing_manager', '/wiki/executive_chairman', '/wiki/president', 
                '/wiki/executive_vice_president', '/wiki/cfo', '/wiki/chairman', '/wiki/chief_operating_officer',
                '/wiki/Board_of_Directors/wiki/President#Non-governmental_presidents', '/wiki/chief_operating_officer', 
                '/wiki/president#non-governmental_presidents' ]
              if link['href'].lower() not in job_titles:
                people_wikis.append( { 'wikipedia' : 'http://en.wikipedia.org' + link['href'] } )
                print link['href']
          if 'people' not in info and len( people_wikis ) != 0:
            info['people'] = []
          for people in people_wikis:
            info['people'].append( people )
      elif fetch_type == 'person':
        info = {}
    return info

# End File: driver/DriverWikipedia.py
