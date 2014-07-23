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
import re

TorScrape = MVC.loadDriver('TorScrape')

class DriverWikipedia( object ):

  def __init__( self ):
    self.ignore_people_pages = [ '/wiki/chief_executive_officer', '/wiki/chairmain', '/wiki/president' '/wiki/chairman', 
      '/wiki/ceo', '/wiki/board_of_dcirectors', '/wiki/President', '/wiki/chief_technology_officer', 
      '/wiki/marketing_director', '/wiki/marketing_manager', '/wiki/executive_chairman', '/wiki/president', 
      '/wiki/executive_vice_president', '/wiki/cfo', '/wiki/chairman', '/wiki/chief_operating_officer',
      '/wiki/board_of_directors/wiki/president#non-governmental_presidents', '/wiki/chief_operating_officer', 
      '/wiki/president#non-governmental_presidents', '/wiki/Chief_brand_officer', '/wiki/Chairman#Corporate_governance',
      '/wiki/Senior_vice_president', '/wiki/Vice_President#Vice_presidents_in_business', '/wiki/Treasurer#Corporate_treasurers',
      '/wiki/Creative_director', '/wiki/Chief_financial_officer', '/wiki/Chief_strategy_officer', '/wiki/Entrepreneur',
      '/wiki/Chief_Accounting_Officer', '/wiki/Executive_director', '/wiki/Entrepreneur', '/wiki/Chief_marketing_officer' ]

  def get( self, fetch_type, wiki_url ):
    sourced_info = {}
    soup = self.__get_soup( wiki_url )
    sourced_info['infobox']     = self.__parse_infobox( fetch_type, soup )
    sourced_info['description'] = self.__parse_description( soup )
    if fetch_type == 'people':
      sourced_info['name'] = self.__parse_name( soup )
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
          people = self.__infobox_company_people( row )
          info['people'] = people
        elif 'Key people' in str( row.th ):
          people_wikis = self.__infobox_company_people( row )
          if 'people' not in info and len( people_wikis ) != 0:
            info['people'] = []
          for people in people_wikis:
            info['people'].append( people )
      elif fetch_type == 'person':
        print 'fetching person'
    return info

  def __infobox_company_people( self, row ):
    """
      Finds people with wikipedia pages 
      contained in the company info box row.
      @return: [ {
        'wikipedia': http://en.wikipedia.org/wiki/Donald_Trump
      } ]
    """
    people_wikis = []
    for link in row.td.find_all( 'a' ):
      if link['href'] and link['href'][:6] =='/wiki/':
        if link['href'].lower() not in self.ignore_people_pages:
          people_wikis.append( { 'wikipedia' : 'http://en.wikipedia.org' + link['href'] } )
          print link['href']
    return people_wikis

  def __parse_name( self, soup ):
    if row.find( 'h1', { 'id': 'firstHeading' } ):
      print row.find( 'h1', { 'id': 'firstHeading' } ).text
      return row.find( 'h1', { 'id': 'firstHeading' } ).text
    else:
      return False

  def __parse_description( self, soup ):
    paragraphs = soup.find_all('p')
    if len( paragraphs ) != 0:
      return paragraphs[0].text
    else:
      return False

  def __strip_wiki( self, string_ ):
    print string_

# End File: includes/driver/DriverWikipedia.py
