#!/usr/bin/python
"""
	NLTK 
	Controls and manages all data collection.
"""

import sys
sys.path.append( '../web/' )
import MVC as MVC

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

Debugger              = MVC.loadHelper('Debug')

import nltk

def nltk_test( ):
	# articles = ModelArticles.getUpdateSet( 1, hide = False )
	articles   = [ ModelArticles.getByID( 5124, hide = False ) ]
	for article in articles:
		parse_article( article['id'] )

def parse_article( article_id ):
	article = ModelArticles.getByID( article_id, hide = False, load_level = 'full' )
	
	print article['headline']
	tokens = nltk.word_tokenize( article['content'] )
	print 'TAGGED'
	tagged = nltk.pos_tag(tokens)
	print 'ENTITIES'
	entities = nltk.chunk.ne_chunk( tagged )

	print tagged
	print entities
if __name__ == "__main__":
	nltk_test()

# End File: data/nltk_test.py 
