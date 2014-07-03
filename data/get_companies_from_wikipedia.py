import urllib2
from bs4 import BeautifulSoup

wiki = urllib2.urlopen( 'http://en.wikipedia.org/wiki/List_of_companies_of_the_United_States' )
soup = BeautifulSoup( wiki )

#print(soup.prettify())


print soup.find_all('ul')
