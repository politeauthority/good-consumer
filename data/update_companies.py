#!/usr/bin/python
"""
  Update Companies

"""

import sys
import urllib2
from bs4 import BeautifulSoup
import re
sys.path.append( '../web/' )
import MVC as MVC

MVC = MVC.MVC()

CompaniesModel = MVC.loadModel( 'Companies' )

def start():
  companies = CompaniesModel.getUpdateSet()
  for company in companies:
    print company['wikipedia']
    soup = get_soup( company['wikipedia'] )
    description = get_description( soup )
    sys.exit()

def get_description( soup ):
  p_tags = soup.find('div', { 'id' : 'mw-content-text' } ).findAll('p')  

  for tag in p_tags:
    print clean_wiki_text( tag )
    sys.exit()

def clean_wiki_text( wiki_string ):
  print wiki_string
  print ' '
  remove_starts = []
  remove_ends   = []
  if '<sup ' in wiki_string:
    print str( wiki_string ).find( '<sup' )

  TAG_RE = re.compile(r'<[^>]+>')

def get_soup( url ):
  try:
    wiki = urllib2.urlopen( url  )
    soup = BeautifulSoup( wiki )
    return soup
  except urllib2.HTTPError:
    print '404 Error Fetching: ', url
    return False  


start()

# End File: data/update_companies.py 
