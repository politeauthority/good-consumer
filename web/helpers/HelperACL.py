#!/usr/bin/python                                                                                                  
# ACL Helper
# @description
#   Access Control List manager 
# @requirements ( drivers/DriverMySql )

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import types
Mysql = MVC.loadDriver('Mysql')

# TODO: combine this with the getPermNameFromID
# TODO: combine this with the getPermNameFromID 

# TODO: combine userSpecific Perms
# TODO  add more features to help in UI for editing all of this
class HelperACL( object ):

  def __init__( self, user_id = False ):
    self.database   = MVC.db['name'] 
    self.perms      = []
    self.user_id    = user_id
    self.user_roles = self.getUserRoles()
    self.buildACL()

  def hasPerm( self, perm_key ):
    for perm in self.perms:
      if perm['perm_key'] == perm_key:
        if perm['value'] == True:
          return True
        else:
          return False
    return False

  def buildACL( self ):
    if self.user_id:
      if len( self.user_roles ) > 0:
        self.perms = self.getRolePerms( self.user_roles )
    return self.perms

  def getAllRoles( self ):
    roles = Mysql.ex( "SELECT * FROM `%s`.`acl_roles`;" % self.database )
    roles_dicts = []
    for role in roles:
      roles_dicts.append( { 
        'role_id' : role[0],
        'name'    : role[1],
        'perms'   : self.getRolePerms( role[0] )
      } )
    return roles_dicts
  
  def getUserRoles( self ):
    roles = []
    if self.user_id:
      sql = """SELECT * FROM `%s`.`acl_user_roles` WHERE `user_id` = '%s' ORDER BY `added` ASC;""" % ( self.database, self.user_id )
      results = Mysql.ex( sql )
      for role in results:
        roles.append( role[1] )
    return roles

  # Get the PERMISSIONS assigned to a ROLE
  # @param : role ( list or string )
  def getRolePerms( self, roles ):
    sql = """SELECT * FROM `%s`.`acl_role_perms` WHERE `role_id` """ % self.database
    if isinstance( roles, types.ListType ):
      role_ids = ''
      for role in roles:
        role_ids += str( role ) + ','
      role_ids = role_ids[:-1]
      sql += 'IN ( %s ) ORDER BY `id` ASC;' % role_ids
    else:
      if roles != '':
        sql += 'IN ( %s ) ORDER BY `id` ASC;' % roles 
      else:
        return []

    rolePerms = Mysql.ex( sql )

    perms = []
    for rolePerm in rolePerms:
      pK = self.getPermKeyByID( rolePerm[2] )
      if pK == '':
        continue
      if rolePerm[3] == 1:
        hP = True
      else:
        hP = False
      perm_dict = { 
        'perm_key'   : pK,
        'inheritted' : False,
        'value'      : hP,
        'name'       : self.getPermNameFromID( rolePerm[2] ),
        'id'         : rolePerm[0]
      }
      perms.append( perm_dict )
    return perms

  def getUserPerms( self, user_id ):
    sql = """SELECT * FROM `%s`.`acl_user_perms` WHERE `user_id` = %s ORDER BY `added` ASC;""" % ( self.database, user_id )
    userPerms = Mysql.ex( sql )

    perms = []
    for userPerm in userPerms:
      pK = self.getPermKeyByID( userPerm[2] )
      if pK == '':
        continue      
      if userPerm[3] == 1:
        hP = True
      else:
        hP = False
      perm_dict = { 
        'perm_key'   : pK,
        'inheritted' : False,
        'value'      : hP,
        'name'       : self.getPermNameFromID( rolePerm[2] ),
        'id'         : rolePerm[0]
      }
      perms.append( perm_dict )
    return perms

  # TODO: combine this with the getPermNameFromID 
  def getPermKeyByID( self, perm_id ):
    sql = """SELECT `perm_key` FROM `%s`.`acl_permissions` WHERE `id` = %s;""" % ( self.database, perm_id )
    permKeyID = Mysql.ex( sql )
    return permKeyID[0][0]

  def getPermByKey( self, key ):
    sql = """SELECT * FROM `%s`.`acl_permissions` WHERE `perm_key` = "%s";""" % ( self.database, key )
    permKeyID = Mysql.ex( sql )
    return permKeyID[0]

  # TODO: combine this with the getPermKeyByID 
  def getPermNameFromID( self, perm_id ):
    sql = """SELECT `perm_name` FROM `%s`.`acl_permissions` WHERE `id` = %s;""" % ( self.database, perm_id )
    permKeyID = Mysql.ex( sql )
    return permKeyID[0][0]    

  def createRole( self, role_name ):
    sql = """INSERT INTO `%s`.`acl_roles` ( role_name ) VALUES ( "%s" );""" % ( self.database, role_name )
    Mysql.ex( sql )

  def createPerm( self, perm_key, perm_name ):
    sql_check = """SELECT * FROM `%s`.`acl_permissions` WHERE `perm_key` = "%s";""" % ( self.database, perm_key )
    perm_exists = Mysql.ex( sql_check )
    if len( perm_exists ) == 0:
      sql = """INSERT INTO `%s`.`acl_permissions` ( perm_key, perm_name ) VALUES ( "%s", "%s" );""" % ( self.database, perm_key, perm_name )
      Mysql.ex( sql )
    return self.getPermByKey( perm_key )

  # This method creates a permission ( if it doesnt exist ) and a relationship to a role
  def createRolePerm( self, role_id, perm_id ):
    from datetime import datetime
    sql_check = """SELECT * FROM `%s`.`acl_role_perms` WHERE `role_id` = "%s" AND `perm_id` = "%s";""" % ( self.database, role_id, perm_id )
    role_perm_exists = Mysql.ex( sql_check )
    if len( role_perm_exists ) == 0:
      insert_sql = """INSERT INTO `%s`.`acl_role_perms` ( `role_id`, `perm_id`, `value`, `added` ) VALUES( "%s", "%s", "1", "%s");""" % ( self.database, role_id, perm_id, datetime.now() )
      Mysql.ex( insert_sql )
    else:
      update_sql = """UPDATE `%s`.`acl_role_perms` SET `value` = 1 WHERE `id` = %s; """ % ( self.database, role_perm_exists[0][0] )
      Mysql.ex( update_sql )

  ###### ADMIN MAINTAINENCE SECTION ######

  def updateUserAccess( self, user_id, role_ids, perm_ids ):
    from datetime import datetime
    # Handle User Roles, first remove current
    delete_sql = """DELETE FROM `%s`.`acl_user_roles` WHERE `user_id` = "%s";""" % ( self.database, user_id )
    Mysql.ex( delete_sql )
    for role_id in role_ids:
      data = {
        'user_id' : user_id,
        'role_id' : role_id,
        'added'   : datetime.now()      
      }
      Mysql.insert( 'acl_user_roles', data )
    new_role_perms = self.getRolePerms( role_ids )

    # Handle User Permissions, remove current, then remove perms associated with a users role, they are unnescisarry
    delete_sql = """DELETE FROM `%s`.`acl_user_perms` WHERE `user_id` = "%s";""" % ( self.database, user_id )
    Mysql.ex( delete_sql )    
    for perm_id in perm_ids:
      skip_perm_set = False
      for new_perm in new_role_perms:       
        if int( new_perm['id'] ) == int( perm_id ):
          skip_perm_set = True
      if skip_perm_set == False:
        data = {
          'user_id' : user_id,
          'perm_id' : perm_id,
          'added'   : datetime.now()
        }
        Mysql.insert( 'acl_user_perms', data )

# End File: helpers/HelperACL.py

# Debug section, this can be deleted out soon
if __name__ == "__main__":
  ACL = HelperACL( 2 )
  for perm in ACL.perms:
    print 'ID: %s     Key: %s      Value: %s ' % ( perm['id'], perm['perm_key'], perm['value'] )
  print ''
  print ACL.user_roles
  print ''
  print ''

  print 'access-admin: ' + str( ACL.hasPerm('access-admin') )