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
from bs4 import BeautifulSoup

class DriverGoogleNews( object ):

	def get( self, search_query ):
		articles = []
		print search_query
		news_url = 'https://news.google.com/news/feeds?q=%s&output=rss' % urllib.quote( search_query ).lower()
		soup     = self.__get_soup( news_url, 'xml' )

		for item in soup.find_all('item'):
			print news_url
			print item.title.text
			full_article = self.get_article_content( item.link.text )
			if not full_article:
				continue
			# print item
			# print item.link.text
			# print item.pubDate.text
			# print item.description.text
			article = {
				'headline' : item.title.text,
				'url'      : item.link.text,
				'pubDate'  : item.pubDate.text,
				'content'     : full_article,				
			}
			articles.append( article )
			break
		return articles

	def get_article_content( self, article_url ):
		full_article = self.__get_soup( article_url )
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

	def __get_soup( self, url, type_of_soup = None ):
		try:
			wiki = urllib2.urlopen( url  )
			if type_of_soup == 'xml':
				soup = BeautifulSoup( wiki, 'xml' )
			else:
				soup = BeautifulSoup( wiki )
			return soup
		except urllib2.HTTPError:
			print '404 Error Fetching: ', url
			return False

# End File: driver/DriverGoogleNews.py
