#!/usr/bin/python                                                                                                
# User Model
# This model controls interactions with the user tables, aside from the ACL
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
Mysql    = MVC.loadDriver('Mysql')
Settings = MVC.loadHelper('Settings')

class ModelUser( object ):

  def __init__( self ):
    self.db_name = MVC.db['name']

  def getByName( self, user_name ):
    sql = """SELECT * FROM `%s`.`users` WHERE `user` = "%s" LIMIT 1;""" % ( MVC.db['name'], user_name )
    user = Mysql.ex( sql )
    return user

  def getById( self, user_id ):
    sql = """SELECT * FROM `%s`.`users` WHERE `id` = "%s" LIMIT 1;""" % ( MVC.db['name'], user_id )
    user = Mysql.ex( sql )
    try:
      the_user = {
        'id'         : user[0][0],
        'user'       : user[0][1],
        'email'      : user[0][2],
        'last_login' : user[0][4],
        'meta'       : self.getUserMeta( user[0][0] ),
        'perms'      : self.__get_perms( user[0][0] )
      }
    except:
      raise NameError( 'Bad User ID' )
    return the_user

  def getAll( self ):
    sql = """SELECT * FROM `%s`.`users`;""" % self.db_name
    users = Mysql.ex( sql )
    return users

  def auth( self, user_name, password ):
    sql = """SELECT * FROM `%s`.`users` WHERE `user` = "%s" AND `pass` = MD5( "%s" ) LIMIT 1;""" % ( self.db_name, user_name, password )
    auth = Mysql.ex( sql )
    if auth:
      return self.getById( auth[0][0] )
    else:
      return False
  
  def create( self, user_name, email, password ):
    data = {
      'user'  : user_name,
      'email' : email,
      'pass'  : password,
    }
    # @todo: check user name space
    # @todo: hash passwords dummy
    Mysql.insert( 'users', data )
    return self.getByName( user_name )

  def update( self, user_id, user_name, email ):
    data = {
      'user' : user_name,
      'email': email
    }
    where = { 'id' : user_id }
    Mysql.update( 'users', data, where )

  def updatePass( self, user_id, password ):
    import hashlib
    m = hashlib.md5()
    m.update( password )
    data  = { 'pass' : m.hexdigest() }
    where = { 'id'   : user_id }
    Mysql.update( 'users', data, where )

  def delete( self, user_id ):
    sql_user = """DELETE FROM `%s`.`users` WHERE `id` = "%s";""" % ( self.db_name, user_id )
    sql_user_meta = """DELETE FROM `%s`.`usermeta` WHERE `user_id` = "%s";""" % ( self.db_name, user_id )
    sql_user_roles = """DELETE FROM `%s`.`acl_user_roles` WHERE `user_id` = "%s";""" % ( self.db_name, user_id )
    sql_user_perms = """DELETE FROM `%s`.`acl_user_perms` WHERE `user_id` = "%s";""" % ( self.db_name, user_id )
    Mysql.ex( sql_user )
    Mysql.ex( sql_user_meta )    
    Mysql.ex( sql_user_roles )
    Mysql.ex( sql_user_perms )
    return True

  def getUsersWithMeta( self, meta_key ):
    sql = """SELECT * FROM `%s`.`usermeta` WHERE `meta_key` = "%s";""" % ( self.db_name, meta_key  )
    meta_records = Mysql.ex( sql )
    users = []
    for meta in meta_records:
      users.append( self.getById( meta[1] ) )
    return users

  def getUserMeta( self, user_id ):
    sql = """SELECT * FROM `%s`.`usermeta` WHERE `user_id` = "%s";""" % ( MVC.db['name'], user_id )
    user_meta = Mysql.ex( sql )
    meta_dict = {}
    for meta in user_meta:
      meta_dict[ meta[3] ]= { 'id': meta[0], 'value': meta[4] }
    return meta_dict

  def addMeta( self, user_id, meta_key, meta_value, pretty_name, help_text, parent  ):
    data = {
      'user_id'     : user_id,
      'meta_key'    : meta_key,
      'meta_value'  : meta_value,
      'pretty_name' : pretty_name,
      'help_text'   : help_text,
      'parent'      : parent,
    }
    Mysql.insert( 'usermeta', data )

  def updateUserMeta( self, user_id, meta_key, meta_value, meta_id = None ):
    if meta_id:
      data = {
        'meta_key'  : meta_key,
        'meta_value': meta_value
      }
      where = { 'id' : meta_id }
    else:
      data = { 'meta_value' : meta_value }
      where = {
        'user_id'  : user_id,
        'meta_key' : meta_key
      }
    Mysql.update( 'usermeta', data, where )

  def deleteMeta( self, meta_id ):
    sql = """DELETE FROM `%s`.`usermeta` WHERE `id` = "%s"; """ % ( self.db_name, meta_id )
    Mysql.ex( sql )

  def __get_perms( self, user_id ):
    ACL = MVC.loadHelper( 'ACL', user_id )
    return ACL

# End File: models/ModelUser.py