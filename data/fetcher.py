#!/usr/bin/python
"""
	Data Fetcher
	Controls and manages all data collection.
"""

import sys
sys.path.append( '../web/' )
import MVC as MVC

MVC               = MVC.MVC()
ModelCompany      = MVC.loadModel('Company')
ModelCompanies    = MVC.loadModel('Companies')
ModelCompanyTypes = MVC.loadModel('CompanyTypes')
ModelCompanyNews  = MVC.loadModel('CompanyNews')
ModelPerson       = MVC.loadModel('Person')
Wikipedia         = MVC.loadDriver('Wikipedia')
GoogleNews        = MVC.loadDriver('GoogleNews')

Debug             = MVC.loadHelper('Debug')

class Fetcher( object ):

	def __init__( self ):
		self.verbosity = True
		self.run_arguments = {
			'find_new_companies'       : False,
			'update_current_companies' : False,
			'update_current_people'    : False,
			'fetch_company_news'       : True,
		}

	def go( self ):
		if self.run_arguments['find_new_companies']:
			self.find_new_companies( )
		if self.run_arguments['update_current_companies']:
			self.update_current_companies( )
		if self.run_arguments['update_current_people']:
			self.update_current_people( )
		if self.run_arguments['fetch_company_news']:
			self.fetch_company_news()

	def find_new_companies( self ):
		print 'Finding new companies'
		print '  Nothing to do here right now... sorry'
		print ' '

	def update_current_companies( self ):
		if self.verbosity:
			print 'Updating Current Companies'
		update_companies = ModelCompanies.getUpdateSet()
		#update_companies = [ ModelCompany.getBySlug( 'irobot' ) ]
		c = 0
		for company in update_companies:
			if self.verbosity:
				print '  ', company['name']
				print '  ', company['wikipedia']
			c_info = {}
			wiki_info = Wikipedia.get( 'company', company['wikipedia'] )
			the_company = {
				'name' : company['name'],
				'meta' : { }
			}
			if 'people' in wiki_info['infobox']:
				people_ids = ''
				for person in wiki_info['infobox']['people']:
					person_id   = ModelPerson.create( person )
					people_ids += str( person_id ) + ','
				people_ids = people_ids[:-1]
				the_company['meta']['people'] = people_ids
			if 'type' in wiki_info:
				company_type_ids = [ ]
				for company_type in wiki_info['infobox']['type']:
					company_type_ids.append( ModelCompany.create( company_type ) )
				the_company['type'] = company_type_ids
			print the_company
			ModelCompany.create( the_company )

	def update_current_people( self ):
		print 'Updating current people'
		print 'Nothing to do here right now ... sorry'

	def fetch_company_news( self ):
		print 'Fetching Company News'
		update_companies = ModelCompanies.getUpdateSet()

		for company in update_companies:
			print '  Downloading news articles for ', company['name']
			company_news = GoogleNews.get( company['name'] )
			for article in company_news:
				ModelCompanyNews.create( company['company_id'], article )
			ModelCompany.setUpdateTime( company['company_id'] )

if __name__ == "__main__":
	Fetcher().go()

# End File: data/fetcher.py 
