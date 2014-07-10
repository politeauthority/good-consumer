#!/usr/bin/python
"""
  Mysql DB Driver
  This driver simplifies some of the MySQL interactions
"""

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import MySQLdb as mdb

class DriverMysql( object ):

  def __init__( self, connect = True ):
    self.host     = MVC.db['host']
    self.dbname   = MVC.db['name']
    self.user     = MVC.db['user']
    self.password = MVC.db['pass']
    if connect:
      self.conn = mdb.connect( self.host, self.user, self.password, charset = 'utf8' )
      self.cur  = False

  """
    ex
    Executes commands, creates a dictionary cursor
    @params:
      query : str() query to be executed
      args  : str(), list() or dict{} for paramaterized queries
  """
  def ex( self, query, args = None ):
    self.cur = mdb.cursors.DictCursor( self.conn )
    self.cur.execute( query, args )
    self.conn.commit()
    return self.cur.fetchall()
  
  """
    insert
    Simple insert statement
    @params:
      table : str()
      items : dict{
        'table_cell' : 'value',
      }
  """
  def insert( self, table, items ):
    columns = []
    values  = []
    for column, value in items.items():
      if value:
        columns.append(column)
        values.append( str( value.encode('utf8') ) )
    column_sql = ''
    for column in columns:
      column_sql = column_sql + "`%s`," % column
    column_sql = column_sql.rstrip( column_sql[-1:] )
    value_sql = ''
    for value in values:
      if isinstance( value, int ):
        value_sql += '%s,' % value
      else:
        value_sql += '"%s",' % self.escape_string( value )
    value_sql = value_sql.rstrip( value_sql[-1:] )
    sql = """INSERT INTO `%s`.`%s` (%s) VALUES(%s);""" % ( self.dbname, table, column_sql, value_sql )
    self.ex( sql )

  def update( self, table, items, where, limit = None ):
    set_sql = ''
    for column, value in items.items():
      set_sql = set_sql + '`%s`="%s", ' % ( column, value )
    set_sql = set_sql.rstrip( set_sql[-2:] )
    where_sql = ''
    for column, value in where.items():
      where_sql = where_sql + '`%s`="%s" AND ' % ( column, value )
    where_sql = where_sql.rstrip( where_sql[-4:] )
    limit_sql = ''
    if limit:
      limit_sql = ' LIMIT = "%s"' % limit
    sql = """UPDATE `%s`.`%s` SET %s WHERE %s %s;""" % ( self.dbname, table, set_sql, where_sql, limit_sql )
    self.ex( sql )

  def escape_string( self, string_ ):    
    if not isinstance( string_, unicode ):
      string_ = unicode( string_, errors='ignore')
    return mdb.escape_string( string_ )

  def list_to_string( self, the_list ):
    string = ''
    for thing in the_list:
      string += '"' + thing + '",'
    string = string[ : len(string) - 1 ]
    return string

  """
    now
    Gives out a basic MySQL timestamp
    @return str() ex: 2014-07-02 23:31:23
  """
  def now( self, format = None ):
    import time
    if format:
      return time.strftime( format )      
    else:
      return time.strftime('%Y-%m-%d %H:%M:%S')

  def alt_con( self, host, dbname, dbuser, dbpass ):
    self.host     = host
    self.dbname   = dbname
    self.user     = dbuser
    self.password = dbpass
  
  def __close( self ):
    self.conn.close()    

# End File: driver/DriverMysql
