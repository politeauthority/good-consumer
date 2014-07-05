import sys
import urllib2
from bs4 import BeautifulSoup
sys.path.append( '../web/' )
import MVC as MVC

MVC = MVC.MVC()

def find_companies():
  wiki = urllib2.urlopen( 'http://en.wikipedia.org/wiki/List_of_companies_of_the_United_States' )
  soup = BeautifulSoup( wiki )
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
  
  for key,value in info.iteritems():
    if 'headquarters' in key.lower():
      company['headquarters'] = value
    elif 'founded' in key.lower():
      company['founded'] = value
    elif 'industry' in key.lower():
      company['industry'] = value

  CompanyModel = MVC.loadModel( 'Company' )

  CompanyModel.create( company )
  # print info
  # for key,value in company.iteritems():
  #   print key + ' ' + value

def find_company_info( wiki_url ):
  url = 'http://en.wikipedia.org/' + wiki_url
  # print url
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

find_companies()

# End File: data/get_companies_from_wikipedia.py 
