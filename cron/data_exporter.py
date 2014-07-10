#!/usr/bin/python
"""
  Data Exporter
  Creates two exports, one for site backup, one for public sharing
"""

import os
import sys
import urllib2
from bs4 import BeautifulSoup
sys.path.append( '../web/' )
import MVC as MVC
MVC = MVC.MVC()
Backup = MVC.loadHelper( 'Backup' )


print MVC.app_dir
print 'Backing Up Database'
# Backup.database( phile='public', tables=['companies', 'company_meta', 'people', 'people_meta'] )

# Backup.database( phile='backup')