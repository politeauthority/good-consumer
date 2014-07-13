#!/usr/bin/python                                                   
"""
  Tor Scrape Driver 
  This driver downloads content through a tor proxy and makes it ready for scrapping.
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import urllib2

class DriverTorScrape( object ):

  def __init__( self ):
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    self.opener = urllib2.build_opener(proxy_support)
    self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]

  def get_soup( self, url, type_of_soup = None ):
    try:
      source = self.opener.open( url ).read()
      if type_of_soup == 'xml':
        soup = BeautifulSoup( source, 'xml' )
      else:
        soup = BeautifulSoup( source )
      return soup
    except urllib2.HTTPError:
      print '404 Error Fetching: ', url
      return False

  def test_tor( self ):
    count = 0
    while count > 5:
      count = count + 1
# End File: driver/DriverTorScrape.py
