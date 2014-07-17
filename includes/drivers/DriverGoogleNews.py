#!/usr/bin/python
"""
  Google News Driver
  Helps fetch and organize content from Google News
"""
import sys
import os
sys.path.append( '../../', )
from MVC import MVC
MVC = MVC()
# End file header

import re
import urllib
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime

TorScrape = MVC.loadDriver('TorScrape')

class DriverGoogleNews( object ):

	def get( self, search_query ):
		"""
			Fetches RSS query from google news, follows article links
			and returns the result out.
			@params: 
				search_query : str()
			@return:
				[ { 
					'headline' : str(),
					'source'   : str(),
					'url'      : str(), 
					'pubDate'  : str() } ]
		"""
		articles   = []
		news_url   = 'https://news.google.com/news/feeds?q=%s&output=rss' % urllib.quote( search_query ).lower()
		scrape     = TorScrape.get_soup( news_url, 'xml' )
		soup       = scrape['soup']
		source_url = self.__get_domain_from_url( scrape['url'] )
		if soup:
			for item in soup.find_all('item'):
				print item.title.text
				full_article = self.get_article_content( item.link.text )
				if not full_article:
					continue
				title_tag = item.title.text
				headline  = title_tag[ : title_tag.rfind(' - ') ].strip()
				source    = title_tag [ title_tag.rfind(' - ') + 2 : ].strip()
				article = {
					'headline' : item.title.text,
					'source'   : {
						'name' : source,
						'url'  : source_url,
					},
					'url'      : scrape['url'],
					'pubDate'  : str( item.pubDate.text ),
					'content'  : full_article
				}
				articles.append( article )
		return articles

	def get_article_content( self, article_url ):
		full_article = TorScrape.get_soup( article_url )['soup']
		if not full_article:
			return False
		counter = 0
		divs_with_paragraphs = []
		all_article_divs     = full_article.find_all('div')
		for div in all_article_divs:
			p_count = len( div.find_all('p') )
			# print 'div %s has %s paragraphs' % ( counter, p_count )
			if p_count > 0:
				divs_with_paragraphs.append( { 'div_num' : counter, 'p_count': p_count } )
			counter = counter + 1
		if len( divs_with_paragraphs ) == 0:
			return False
		most_paragraphs_count = 0
		most_paragraphs_div   = None
		for div in divs_with_paragraphs:
			if div['p_count'] > most_paragraphs_count:
				most_paragraphs_count = div['p_count']
				most_paragraphs_div   = div['div_num']
		export_text = ''
		for paragraph in all_article_divs[ most_paragraphs_div ].find_all('p'):
			p_text = paragraph.text.encode('utf-8')
			if len( p_text ) > 150:
				num_sentances = len( [m.start() for m in re.finditer( '. ', p_text ) ] )
				if num_sentances > 1:
					export_text += p_text
		if len( export_text ) > 100:
			return export_text
		else:
			return False

	def __get_domain_from_url( self, url ):
		"""
			Grabs base domain  from a url string.
		"""
		from urlparse import urlparse
		parsed_uri = urlparse( url )
		domain = '{uri.scheme}://{uri.netloc}/'.format( uri=parsed_uri )
		return domain

# End File: driver/DriverGoogleNews.py
