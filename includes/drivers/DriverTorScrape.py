#!/usr/bin/python                                                   
"""
  Tor Scrape Driver 
  This driver downloads content through a tor proxy
  and turns it into soup, ready for scrapping.
"""
import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import urllib2
from bs4 import BeautifulSoup

class DriverTorScrape( object ):

  def __init__( self ):
    self.use_tor      = True
    self.auto_test    = False
    if self.use_tor:
      proxy_support     = urllib2.ProxyHandler({"http" : "localhost:8118"})
      self.torOpener    = urllib2.build_opener( proxy_support )
      self.torOpener.addheaders = [('User-agent', 'Mozilla/5.0')]
    else:
      self.auto_test = False      
      self.torOpener = urllib2.build_opener()
    if self.auto_test:
      self.test_tor()

  def get_soup( self, url, type_of_soup = None ):
    try:
      source = self.torOpener.open( url ).read()
      if type_of_soup == 'xml':
        soup = BeautifulSoup( source, 'xml' )
      else:
        soup = BeautifulSoup( source )
      return soup
    except urllib2.HTTPError:
      print '404 Error Fetching: ', url
      return False

  def test_tor( self ):
    """
      Checks to make sure we're getting a
      IP different from the current connection.
      If not exit out so we dont make everyone
      on your network have to submit google captchas.
      @todo:
        Should grab the local IP address, from a chain of sites.
    """
    url        = 'http://www.whatsmyip.org/'

    # source     = urllib2.urlopen( url )
    # soup       = BeautifulSoup( source )
    # current_ip = soup.find('h1').find('span').text

    # try:
    #   source = urllib2.urlopen( url )
    #   soup = BeautifulSoup( source )
    #   current_ip = soup.find('h1').find('span').text
    # except:
    #   print 'Error opening URL.'

    try:    
      source = self.torOpener.open( url ).read()
    except urllib2.URLError as error:
      print 'Error Connecting to Tor proxy: ', error
      sys.exit()

    outgoing_ips = []
    count = 0
    while count < 5:
      soup = BeautifulSoup( source )
      outgoing_ips.append( soup.find('h1').find('span').text )
      count = count + 1

    for ip in outgoing_ips:
      print ip
      # print 'Tor does not seem to be working properly.'
      # if ip == current_ip:

      #   sys.exit()

# End File: driver/DriverTorScrape.py
