#!/usr/bin/python                                                                                                
# AdminUser Controller
# This Controller handles Admin - User based interactions
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdminUser( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout_h = 'admin/layout/header.html'
    self.Renderer.layout_f = 'admin/layout/footer.html'

  @cherrypy.expose
  def index( self  ):
    User = MVC.loadModel('User')
    data = {
      'users' : User.getAll()
    }
    return self.Renderer.make( 'admin/user/index.html', data = data )

  @cherrypy.expose
  def info( self, user_id = False ):
    UserModel = MVC.loadModel( 'User' )
    ACL       = MVC.loadHelper( 'ACL' )
    data = {}
    if user_id != False:
      data['user']  = UserModel.getById( user_id )
      data['roles'] = ACL.getAllRoles()
      return self.Renderer.make( 'admin/user/info.html', data )
    else:
      return 'error'

  @cherrypy.expose
  def edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.update( kwargs['user_id'], kwargs['user_name'], kwargs['email'] )
      raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )

  @cherrypy.expose
  def password_edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      if kwargs['password_1'] == kwargs['password_2']:
        User.updatePass( kwargs['user_id'], kwargs['password_1'] )
    raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )

  @cherrypy.expose
  def perms_edit( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      try:
        role_ids = kwargs['acl_roles[]']        
      except:
        role_ids = []
      try:
        perm_ids = kwargs['acl_perms[]']
      except:
        perm_ids = []
      ACL.updateUserAccess( kwargs['user_id'], role_ids, perm_ids )
    raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  perms_edit.exposed = True

  @cherrypy.expose
  def meta_create( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      help_text = ''
      parent    = ''
      User.addMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], kwargs['pretty_name'], help_text, parent )
      raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )

  @cherrypy.expose
  def meta_edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.updateUserMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], meta_id = kwargs['meta_id'] )
      raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )

  # @todo: add connection to model, add url var to view
  @cherrypy.expose
  def meta_delete( self, user_id, metaID_or_key = False ):
    if metaID_or_key:
      UserModel = MVC.loadModel( 'User' )
      if metaID_or_key.isdigit():
        meta_id = metaID_or_key
      else:
        meta_key = metaID_or_key
        # @todo: build a way to delete by meta_key
    raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )      

  # should be absolved into self.users as a modal window
  @cherrypy.expose  
  def create( self ):
    return self.Renderer.make( 'admin/user/create.html' )

  @cherrypy.expose  
  def add( self, **kwargs ):
    if kwargs:
      if kwargs['password_1'] == kwargs['password_2']:
        User = MVC.loadModel('User')
        new_user = User.create( kwargs['user_name'], kwargs['email'], kwargs['password_1'] )
      raise cherrypy.HTTPRedirect('/admin/user/') 

  @cherrypy.expose
  def delete( self, user_id = None ):
    if user_id:
      User = MVC.loadModel('User')
      User.delete( user_id )
      raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % user_id )

  ### ACL Maintenence Feaures ###

  @cherrypy.expose
  def acl( self ):
    ACL = MVC.loadHelper('ACL')
    roles = ACL.getAllRoles()
    data = { 'roles': roles }
    return self.Renderer.make( 'admin/user/acl.html', data )
  
  # Updates a Rolels
  @cherrypy.expose  
  def acl_role_update( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      if kwargs['role_id'] == '':
        ACL.createRole( kwargs['role_name'] )
    raise cherrypy.HTTPRedirect( '/admin/user_acl/' )

  # Updates a Permission
  @cherrypy.expose  
  def acl_perm_update( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      if kwargs['perm_id'] == '':
        Misc = MVC.loadHelper( 'Misc' )
        perm_id = ACL.createPerm( Misc.slug( kwargs['perm_name'] ), kwargs['perm_name'] )[0]
        if kwargs['role_id'] != '':
          ACL.createRolePerm( kwargs['role_id'], perm_id )
      raise cherrypy.HTTPRedirect( '/admin/user_acl/' )

# End File: controllers/admin/ControllerAdminUser.py