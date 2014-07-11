#!/usr/bin/python
"""
  Get Companies
  Primary to kick off initial database creation and find NEW companies, 
  however this can be used to update base level company content aswell.
"""

import sys
import urllib2
from bs4 import BeautifulSoup
sys.path.append( '../web/' )
import MVC as MVC

MVC = MVC.MVC()

def get_soup( url ):
  try:
    wiki = urllib2.urlopen( url  )
    soup = BeautifulSoup( wiki )
    return soup
  except urllib2.HTTPError:
    print '404 Error Fetching: ', url
    return False  

def find_companies():
  soup = get_soup( 'http://en.wikipedia.org/wiki/List_of_companies_of_the_United_States' )
  if soup:
    content_divs =  soup.find_all( 'div', { 'class' : 'div-col' } )
    for div in content_divs:
      for li in div.find_all('li'):
        company_name = li.text
        wiki_url     = li.find( 'a', { 'href': True } )['href']
        find_company( company_name, wiki_url )

def find_company( company_name, wiki_url ):
  company = {
    'name'      : company_name,
    'wikipedia' : 'http://en.wikipedia.org' + wiki_url
  }
  info = find_company_info( wiki_url )
  if info:
    for key,value in info.iteritems():
      if 'headquarters' in key.lower():
        company['headquarters'] = value
      elif 'founded' in key.lower():
        company['founded'] = value
      elif 'industry' in key.lower():
        company['industry'] = value
    CompanyModel = MVC.loadModel( 'Company' )
    try:
      CompanyModel.create( company )
    except UnicodeEncodeError:
      print 'UnicodeEncodeError, cannot create company'
  # print info
  # for key,value in company.iteritems():
  #   print key + ' ' + value

def find_company_info( wiki_url ):
  url = 'http://en.wikipedia.org' + wiki_url
  print url
  soup = get_soup( url )
  if not soup:
    return False
  company_page = urllib2.urlopen( 'http://en.wikipedia.org' + wiki_url )
  soup = BeautifulSoup( company_page )

  infobox = soup.find( 'table', { 'class' : 'infobox' } )
  if infobox == None:
    return {}
  infobox_rows =  infobox.find_all( 'tr' )

  info = { 'people' : [] }
  for row in infobox_rows:
    table_head = row.find( 'th' )
    if table_head and table_head.text != '':
      table_value = row.find('td')

      # if 'Founder(s)' in table_head.text or 'Key people' in table_head.text:
      #   print table_head
      #   people = table_value.find_all( 'a' )
      #   print people
      #   if people and len( people ) > 0:
      #     for person in people:
      #       print person['href']

      if table_value and table_value.text != '':
        info[ table_head.text ] = table_value.text
  return info

if __name__ == "__main__":
  find_companies()

# End File: data/get_companies_from_wikipedia.py 
