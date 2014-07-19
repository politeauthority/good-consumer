#!/usr/bin/python
"""
	Data Fetcher
	Controls and manages all data collection.
"""

import sys
sys.path.append( '../web/' )
import MVC as MVC

MVC               = MVC.MVC()
JobLog            = MVC.loadModel('JobLog')
ModelCompany      = MVC.loadModel('Company')
ModelCompanies    = MVC.loadModel('Companies')
ModelCompanyTypes = MVC.loadModel('CompanyTypes')
ModelNews         = MVC.loadModel('News')
ModelNewsSources  = MVC.loadModel('NewsSources')
ModelPerson       = MVC.loadModel('Person')
Wikipedia         = MVC.loadDriver('Wikipedia')
GoogleNews        = MVC.loadDriver('GoogleNews')

Debugger          = MVC.loadHelper('Debug')

class Fetcher( object ):

	def __init__( self ):
		self.verbosity = True
		self.run_arguments = {
			'find_new_companies'       : False,
			'update_current_companies' : False,
			'update_current_people'    : False,
			'fetch_company_news'       : True,
			'evaluate_comapny_news'    : False,
		}

	def go( self ):
		"""
			Controls the running of all jobs
		"""
		if self.run_arguments['find_new_companies']:
			self.find_new_companies( )
		if self.run_arguments['update_current_companies']:
			self.update_current_companies( )
		if self.run_arguments['update_current_people']:
			self.update_current_people( )
		if self.run_arguments['fetch_company_news']:
			self.fetch_company_news()
		if self.run_arguments['evaluate_comapny_news']:
			self.evaluate_comapny_news()

	def find_new_companies( self ):
		import subprocess
		print 'Finding new companies'
		job_id = JobLog.start( 'find_new_companies' )			
		subprocess.call( 'python ' + MVC.app_dir + 'data/get_companies_from_wikipedia.py', shell=True)
		JobLog.stop( job_id )

	def update_current_companies( self ):
		if self.verbosity:
			print 'Updating Current Companies'
		job_id = JobLog.start( 'update_current_companies' )			
		update_companies = ModelCompanies.getUpdateSet( 300, hide = False )
		# update_companies = [ ModelCompany.getBySlug( 'best-buy' ) ]
		companies_updated = 0
		people_found      = 0
		c = 0
		for company in update_companies:
			if self.verbosity:
				print '  ', company['name']
				print '  ', company['wikipedia']
			wiki_info = Wikipedia.get( 'company', company['wikipedia'] )
			the_company_update = {
				'company_id'    : company['company_id'],
				'name'          : company['name'],
				'record_status' : 2,
				'meta'          : { }
			}
			if 'people' in wiki_info['infobox']:
				people_ids = ''
				for person in wiki_info['infobox']['people']:
					person_id   = ModelPerson.create( person )
					people_ids += str( person_id ) + ','
					people_found = people_found + 1
				people_ids = people_ids[:-1]
				the_company_update['meta']['people'] = people_ids

			# Disabling type for now
			# if 'type' in wiki_info['infobox']:
			# 	company_type_ids = [ ]
			# 	for company_type in wiki_info['infobox']['type']:
			# 		company_type_ids.append( ModelCompanyTypes.create( company_type['name'], company_type['wikipedia'] ) )
			# 	the_company_update['type'] = company_type_ids
			
			# Debugger.write( 'the_company_update', the_company_update )
			ModelCompany.create( the_company_update )
			companies_updated = companies_updated + 1
			# Debugger.write( 'Company by id', ModelCompany.getByID( the_company_update['company_id'], 'full' ) )
		JobLog.stop( job_id, 'Updated %s companies and found %s people' % ( companies_updated, people_found ) )

	def update_current_people( self ):
		print 'Updating current people'
		print 'Nothing to do here right now ... sorry'

	def fetch_company_news( self ):
		print 'Fetching Company News'
		job_id = JobLog.start( 'fetch_company_news' )
		update_companies = ModelCompanies.getUpdateSet( 250, hide = False )
		companies_count  = 0
		articles_count   = 0
		if len( update_companies ) == 0:
			if self.verbosity:
				print 'No companies found for news fetch'
			return
		for company in update_companies:
			print '  Downloading news articles for ', company['name']
			company_news = GoogleNews.get( company['name'] )

			for article in company_news:
				news_source_id = ModelNewsSources.create( article['source'] )
				a_meta = {
					'company_asso' : company['company_id']
				}
				article.update( { 'news_source_id' : news_source_id } )
				article.update( { 'meta': a_meta } )

				Debugger.write( 'article', article )
				ModelNews.create( article )
				articles_count = articles_count + 1



			the_company_update = {
				'company_id'    : company['company_id'],
				'record_status' : 2,
				'meta'       : {
					'job_news' : 'ran'
				}
			}
			ModelCompany.create( the_company_update )
			companies_count = companies_count + 1
		JobLog.stop( job_id, "Ran %s companies and read %s articles" % ( companies_count, articles_count ) )

	def evaluate_comapny_news( self ):
		print 'stuff'

if __name__ == "__main__":
	Fetcher().go()

# End File: data/fetcher.py 
