#!/usr/bin/python
"""
	Data Fetcher
	Controls and manages all data collection.
"""
import sys
sys.path.append( '../web/' )
import MVC as MVC
import getopt

MVC                   = MVC.MVC()
JobLog                = MVC.loadModel('JobLog')
ModelCompany          = MVC.loadModel('Company')
ModelCompanies        = MVC.loadModel('Companies')
ModelCompanyTypes     = MVC.loadModel('CompanyTypes')
ModelArticles         = MVC.loadModel('Articles')
ModelArticlesSources  = MVC.loadModel('ArticlesSources')
ModelPeople           = MVC.loadModel('People')
ModelPerson           = MVC.loadModel('Person')
Wikipedia             = MVC.loadDriver('Wikipedia')
GoogleNews            = MVC.loadDriver('GoogleNews')
TorScrape             = MVC.loadDriver('TorScrape')
Debugger              = MVC.loadHelper('Debug')

class Fetcher( object ):

	def __init__( self ):
		self.verbosity = True
		self.run_arguments = {
			'find_new_companies'        : False,
			'update_companies'          : False,
			'update_people'             : False,
			'fetch_company_articles'    : False,
			'evaluate_company_articles' : False,
			'update_source_counts'      : False,
		}
		TorScrape.test_tor()

	def go( self ):
		"""
			Controls the running of all jobs
		"""
		if len( self.run_arguments ) == 0:
			print '  -- Fetcher Options -- '
			print ' '
			print ' --find_new_companies'
			print ' --update_companies'
			print ' --update_people'
			print ' --fetch_company_articles'
			print ' --evaluate_company_articles'
			print ' --update_source_counts'
		if self.run_arguments['find_new_companies']:
			self.find_new_companies( )
		if self.run_arguments['update_companies']:
			self.update_companies( )
		if self.run_arguments['update_people']:
			self.update_people( )
		if self.run_arguments['fetch_company_articles']:
	 		self.fetch_company_articles()
		if self.run_arguments['evaluate_company_articles']:
			self.evaluate_company_articles()
		if self.run_arguments['update_source_counts']:
			self.update_source_counts()			

	def find_new_companies( self ):
		import subprocess
		print 'Finding new companies'
		job_id = JobLog.start( 'find_new_companies' )			
		subprocess.call( 'python ' + MVC.app_dir + 'data/get_companies_from_wikipedia.py', shell=True)
		JobLog.stop( job_id )

	def update_companies( self, count = 30 ):
		if self.verbosity:
			print 'Updating Current Companies'
		job_id = JobLog.start( 'update_companies' )			
		update_companies  = ModelCompanies.getUpdateSet( count, hide = False )
		# update_companies = [ ModelCompany.getBySlug( 'best-buy' ) ]id
		companies_updated = 0
		people_found      = 0
		c = 0
		for company in update_companies:
			if self.verbosity:
				print '  ', company['name']
				print '  ', company['wikipedia']
			wiki_info = Wikipedia.get( 'company', company['wikipedia'] )
			the_company_update = {
				'id'            : company['id'],
				'name'          : company['name'],
				'record_status' : 3,
				'meta'          : []
			}
			if 'people' in wiki_info['infobox']:
				print 'we found some fucking people'
				print wiki_info['infobox']['people']
				people_ids = ''
				for person in wiki_info['infobox']['people']:
					meta_assoc = {
					'meta_key'   : 'assoc_company',
					'meta_value' : company['id'],
					'meta_type'  : 'comma',
					'action'     : 'append'
					}
					person['meta'] = [ meta_assoc ]
					person_id   = ModelPerson.create( person )
					people_ids += str( person_id ) + ','
					people_found = people_found + 1
				people_ids = people_ids[:-1]
				meta_p = {
					'meta_key'   : 'assoc_people',
					'meta_value' : people_ids,
					'meta_type'  : 'comma'
				}
				the_company_update['meta'].append( meta_p )				
				meta_j = {
					'meta_key'   : 'job_update_companies',
					'meta_value' : 'now',
					'meta_type'  : 'date',
				}
				the_company_update['meta'].append( meta_j )
			
			if 'description' in wiki_info:
				meta_desc = {
					'meta_key'   : 'description',
					'meta_value' : wiki_info['description'],
					'meta_type'  : 'string'
				}
				the_company_update['meta'].append( meta_desc )
			# Disabling type for now
			# if 'type' in wiki_info['infobox']:
			# 	company_type_ids = [ ]
			# 	for company_type in wiki_info['infobox']['type']:
			# 		company_type_ids.append( ModelCompanyTypes.create( company_type['name'], company_type['wikipedia'] ) )
			# 	the_company_update['type'] = company_type_ids
			ModelCompany.create( the_company_update )
			companies_updated = companies_updated + 1
		JobLog.stop( job_id, 'Updated %s companies and found %s people' % ( companies_updated, people_found ) )

	def update_people( self, count = 300 ):
		if self.verbosity:
			print 'Updating current people'
		# job_id = JobLog.start( 'update_people' )						
		people =  ModelPeople.getUpdateSet( count, hide = False )
		people_updated = 0
		for person in people:
			if self.verbosity:
				if person['name']:
					print '  Downloading: ', person['name']
				else:
					print '  Downloading: ', person['wikipedia']
			wiki_info = Wikipedia.get( 'person', person['wikipedia'] )
			if 'meta' not in person:
				person['meta'] = []			
			meta_desc = {
				'meta_key'   : 'description',
				'meta_value' : wiki_info['description'],
				'meta_type'  : 'string'
			}
			person['meta'].append( meta_desc )
			meta_j = {
					'meta_key'   : 'job_update_people',
					'meta_value' : 'now',
					'meta_type'  : 'date',
			}
			person['meta'].append( meta_j )			
			ModelPerson.create( person )
			people_updated = people_updated + 1
			# Debugger.write( 'person', person )

		# JobLog.stop( job_id, 'Updated x people')

	def fetch_company_articles( self, count = 5 ):
		print 'Fetching Company Articles'
		job_id = JobLog.start( 'fetch_company_articles' )
		update_companies = ModelCompanies.getUpdateSet( count, hide = False )
		companies_count  = 0
		articles_count   = 0
		if len( update_companies ) == 0:
			if self.verbosity:
				print 'No companies found for articles fetch'
			return
		for company in update_companies:
			print '  Downloading news articles for ', company['name']
			company_news = GoogleNews.get( company['name'] )
			for article in company_news:
				news_source_id = ModelArticlesSources.create( article['source'] )
				a_meta = {
					'meta_key'   : 'assoc_company',
					'meta_value' : company['id'],
					'meta_type'  : 'comma',
				}
				article.update( { 'source_id' : news_source_id } )
				article.update( { 'meta': [ a_meta ] } )
				ModelArticles.create( article )
				articles_count = articles_count + 1
			the_company_update = {
				'id'            : company['id'],
				'record_status' : 3,
				'meta'          : [],
			}
			job_meta = {
				'meta_key'   : 'job_fetch_company_articles',
				'meta_value' : 'now',
				'meta_type'  : 'date',
			}
			the_company_update['meta'].append( job_meta )
			ModelCompany.create( the_company_update )
			companies_count = companies_count + 1
		JobLog.stop( job_id, "Ran %s companies and read %s articles" % ( companies_count, articles_count ) )

	def evaluate_company_articles( self ):
		subprocess.call( 'python ' + MVC.app_dir + 'data/job_nltk_test.py', shell=True )

	def update_source_counts( self ):
		if self.verbosity:
			print 'Updating News Sources counts'
		job_id = JobLog.start( 'update_source_counts' )
		ModelArticlesSources.updateCounts()
		JobLog.stop( job_id )		

def usage():
	print 'Good Consumer Fetcher'

def __opt_search( key_search, opts, default = None ):
	"""
		Search through the options return the arg if available or True if its set
	"""	
	if not isinstance( key_search, list ):
		key_search = [ key_search ]
	for opt, arg in opts:
		if opt in key_search:
			if not arg:
				return True
			return arg
	if default:
		return default
	return False

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hg:v", 
			["help",
			"find_new_companies",
			"update_companies",
			"update_people",
			"fetch_company_articles",
			"evaluate_company_articles", 
			"update_source_counts" ] )
	except getopt.GetoptError, e:
		print 'Error: Problem parsing arguments'
		print e
		usage()
		sys.exit()

	Fetcher = Fetcher()

	find_new_companies = __opt_search( '--find_new_companies', opts )
	if find_new_companies:
		Fetcher.run_arguments['find_new_companies'] = True
	else:
		Fetcher.run_arguments['find_new_companies'] = False

	update_companies = __opt_search( '--update_companies', opts )
	if update_companies:
		Fetcher.run_arguments['update_companies'] = True
	else:
		Fetcher.run_arguments['update_companies'] = False

	update_people = __opt_search( '--update_people', opts )
	if find_new_companies:
		Fetcher.run_arguments['update_people'] = True
	else:
		Fetcher.run_arguments['update_people'] = False				

	fetch_company_articles = __opt_search( '--fetch_company_articles', opts )
	if fetch_company_articles:
		Fetcher.run_arguments['fetch_company_articles'] = True
	else:
		Fetcher.run_arguments['fetch_company_articles'] = False

	evaluate_company_articles = __opt_search( '--evaluate_company_articles', opts )
	if evaluate_company_articles:
		Fetcher.run_arguments['evaluate_company_articles'] = True
	else:
		Fetcher.run_arguments['evaluate_company_articles'] = False

	update_source_counts = __opt_search( '--update_source_counts', opts )
	if update_source_counts:
		Fetcher.run_arguments['update_source_counts'] = True
	else:
		Fetcher.run_arguments['update_source_counts'] = False											
	
	Fetcher.go()

# End File: data/fetcher.py 
