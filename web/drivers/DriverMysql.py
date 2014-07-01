#!/usr/bin/python
#!/usr/bin/python                                                                                                
# Mysql DB Driver
# This driver simplifies some of the MySQL interactions

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import MySQLdb as mdb

class DriverMysql( object ):

  def __init__( self ):
    self.host     = MVC.db['host']
    self.dbname   = MVC.db['name']
    self.user     = MVC.db['user']
    self.password = MVC.db['pass']

  def ex(self, query):
    conn = mdb.connect( self.host, self.user, self.password)
    cur = conn.cursor()
    cur.execute( query )
    conn.commit()
    return cur.fetchall()

  def insert(self, table, items ):
    columns = []
    values  = []
    for column, value in items.items():
      columns.append(column)
      values.append( str(value) )
    column_sql = ''
    for column in columns:
      column_sql = column_sql + "`%s`," % column
    column_sql = column_sql.rstrip( column_sql[-1:] )
    value_sql = ''
    for value in values:
      value_sql = value_sql + '"%s",' % self.escape_string( value )
    value_sql = value_sql.rstrip( value_sql[-1:] )

    sql = """INSERT INTO `%s`.`%s` (%s) VALUES(%s);""" % ( self.dbname, table, column_sql, value_sql )
    self.ex( sql )

  def update( self, table, items, where, limit = 1 ):
    set_sql = ''
    for column, value in items.items():
      set_sql = set_sql + '`%s`="%s", ' % ( column, value )
    set_sql = set_sql.rstrip( set_sql[-2:] )
    where_sql = ''
    for column, value in where.items():
      where_sql = where_sql + '`%s`="%s" AND ' % ( column, value )
    where_sql = where_sql.rstrip( where_sql[-4:] )

    sql = """UPDATE `%s`.`%s` SET %s WHERE %s LIMIT %s;""" % ( self.dbname, table, set_sql, where_sql, limit )
    self.ex( sql )

  def escape_string( self, string ):
    return mdb.escape_string( string )

  def alt_con( self, host, dbname, dbuser, dbpass ):
    self.host     = host
    self.dbname   = dbname
    self.user     = dbuser
    self.password = dbpass

# End File: driver/DriverMysql
