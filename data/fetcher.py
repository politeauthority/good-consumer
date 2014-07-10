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

MVC            = MVC.MVC()
ModelCompanies = MVC.loadModel('Companies')
ModelCompany   = MVC.loadModel('Company')



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
				c_info = {}
				print company['wikipedia']
				soup = self.__get_soup( company['wikipedia'] )
				if soup:
					infobox = soup.find( 'table', { 'class' : 'infobox' } )
					if infobox == None:
						continue
						infobox_content = self.__parse_infobox( infobox )
			if c == 5:
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
		infobox_rows =  infobox.find_all( 'tr' )
		for row in infobox_rows:
			if row.find_all('a', { 'title': 'Types of business entity' } ):
				o_types = row.find( 'td' ).find_all( 'a' )
				c_types = []
				print row
				print o_types
				for o in o_types:
					print o
					c_types.append( o_types.text )
					print c_types
					sys.exit()
					c = c + 1


if __name__ == "__main__":
	Fetcher().go()

# End File: data/fetcher.py 
