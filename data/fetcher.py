#!/usr/bin/python
"""
	Data Fetcher
	Controls and manages all data collection.
"""

import sys
import urllib2
from bs4 import BeautifulSoup
sys.path.append( '../web/' )
import MVC as MVC

MVC               = MVC.MVC()
ModelCompany      = MVC.loadModel('Company')
ModelCompanies    = MVC.loadModel('Companies')
ModelCompanyTypes = MVC.loadModel('CompanyTypes')
ModelPerson       = MVC.loadModel('Person')

Debug             = MVC.loadHelper('Debug')

class Fetcher( object ):

	def __init__( self ):
		self.verbosity = True
		self.run_arguments = {
			'find_new_companies'       : False,
			'update_current_companies' : True,
		}

	def go( self ):
		if self.run_arguments['find_new_companies']:
			self.find_new_companies( )
		if self.run_arguments['update_current_companies']:
			self.update_current_companies( )

	def find_new_companies( self ):
		print 'Nothing to do here right now... sorry'

	def update_current_companies( self ):
		if self.verbosity:
			print 'Updating Current Companies'
		update_companies = ModelCompanies.getUpdateSet()
		c = 0
		for company in update_companies:
			if self.verbosity:
				print '  ', company['name']
				print company['wikipedia']
			c_info = {}
			soup = self.__get_soup( company['wikipedia'] )
			if soup:
				infobox = soup.find( 'table', { 'class' : 'infobox' } )
				if infobox == None:
					continue
				infobox_content = self.__parse_infobox( infobox )
				print infobox_content
                                c = c + 1
                                if c == 10:
                                        sys.exit()

	def __get_soup( self, url ):
		try:
			wiki = urllib2.urlopen( url  )
			soup = BeautifulSoup( wiki )
			return soup
		except urllib2.HTTPError:
			print '404 Error Fetching: ', url
			return False

	def __parse_infobox( self, soup ):
                info = { }
		infobox_rows =  soup.find_all( 'tr' )
		for row in infobox_rows:
			if row.find_all('a', { 'title': 'Types of business entity' } ):
				o_types = row.find( 'td' ).find_all( 'a' )
				c_types = []
				for o in o_types:
					the_type = {
						'name'      : o.text,
						'wikipedia' : 'http://en.wikipedia.org' + o['href']
					}
					c_types.append( the_type )
				type_ids = ModelCompanyTypes.getIDsByName( c_types, create_if_not_exists = True )
                                info['type'] = type_ids
                        elif 'Founder' in str( row.th ):
                                print row.td
                                info['people'] = []
                                for person in row.td.findAll( 'a' ):
                                        p = {
                                                'name'      : person.text,
                                                'wikipedia' : 'http://en.wikipedia.org' + person['href']
                                        }
                                        info['people'].append( p )
                                        #person_id = ModelPerson.create( p )
                                        #print person_id
                                        #info['people'].append( person_id )
                        elif 'Key People' in str( row.th ):
                                if 'people' not in info:
                                        info['people'] = []
                                print row.td
                        #else:
                                #print ''
                                #print str( row.th )
                                #print ''
                                #print row.td
                        people = [ ]
                        if 'people' in info:
                                print info['people']
                                #Debug.write( 'check', info['people'] )
                                for person in info['people']:
                                        person_id = ModelPerson.create( person )
                                        people.append( person_id )
                                info['people'] = people

                        print ' '
                return info


if __name__ == "__main__":
	Fetcher().go()

# End File: data/fetcher.py 
