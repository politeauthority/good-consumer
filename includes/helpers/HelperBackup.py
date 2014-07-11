#!/usr/bin/python
"""
	Backup Helper
	Class for database, logfiles, and remote export of those files if needed
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

from os import path
import subprocess

class HelperBackup( object ):

	def __init__( self ):
		self.db_host    = MVC.db['host']
		self.db_name    = MVC.db['name']
		self.db_user    = MVC.db['user']
		self.db_pass    = MVC.db['pass']
		self.backup_dir = MVC.app_dir + 'export/'

	def database( self, phile, tables = None, zzip = True ):
		if path.isdir( self.backup_dir ) == False:
			os.mkdir( self.backup_dir )
		args = {
			'host'   : self.db_host, 
			'dbname' : self.db_name, 
			'user'   : self.db_user, 
			'pass'   : self.db_pass,
			'file'   : self.backup_dir + phile + '.sql'
		}
		if tables:
			table_str = ''
			for table in tables:
				table_str += table + ' '
			table_str = table_str[:-1]
			args['tables'] = table_str
			command = "mysqldump -h%(host)s -u%(user)s -p%(pass)s %(dbname)s %(tables)s > %(file)s" % args
		else:
			command = "mysqldump -h%(host)s -u%(user)s -p%(pass)s %(dbname)s > %(file)s" % args
		print command
		sys.exit()
		subprocess.call( command, shell=True )
		self.__zip( args['file'] )

	def __zip( self, phile ):
		print phile
		subprocess.call( 'zip ' + phile )


# End File: helpers/HelperBackup.py
