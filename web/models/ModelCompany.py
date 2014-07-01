#!/usr/bin/python                                                                                                
# Company
# This model controls interactions for a single company
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')
Settings = MVC.loadHelper('Settings')

class ModelCompany( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getById( self, company_id ):
  	print company_id

  def getBySlug( self, company_slug ):
  	# @todo: sanitize the input properly!
  	qry = """SELECT * FROM ``.`companies` WHERE `slug` = "%s"; """ % ( self.db_name, company_slug )
  	print company_slug

  def getAll( self ):
    qry = """SELECT * FROM `%s`.`companies` LIMIT %s OFFSET %s;""" % ( self.db_name, '100', '0' )
    companies = Mysql.ex( qry )
    return companies

# End File: models/ModelCompany.py