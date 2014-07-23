#!/usr/bin/python
"""
  MetaStore Helper
"""

import sys
import os
sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import json
from datetime import datetime

Mysql    = MVC.loadDriver('Mysql')
Debugger = MVC.loadHelper('Debug')

class HelperMetaStore( object ):

  def __init__( self, entity = None ):
    self.db_name    = MVC.db['name']
    self.entity     = entity
    self.meta_types = [ 'string', 'int', 'date', 'json', 'comma' ]
    self.entities   = [ 'companies', 'people', 'articles' ] 

  def get( self, entity_id, entity = None, metas = None ):
    """
      @params:
        entity_id : 12
        entity    : 'companies'
        metas     : [ 'meta_key', 'meta_key' ]
      @return: [ {
        'meta_key' : {
          'meta_value' : 'something',
          'meta_type'  : 'string',
          'meta_id'    : 1234,
          'id'         : 42
        },
      } ]
    """
    if self.entity not in self.entities and entity not in self.entities:
      print 'INCORRECT ENTITY USAGE: ', entity
      sys.exit()
    if entity == None:
      entity = self.entity
    qry_args = {
      'db_name'   : self.db_name,
      'entity'    : entity,
      'entity_id' : entity_id,
    }
    qry = """SELECT * FROM 
      `%(db_name)s`.`%(entity)s_meta` 
      WHERE `id` = "%(entity_id)s" """ % qry_args
    if metas:
      if isinstance( metas, str ):
        metas = [ metas ]
      meta  = Mysql.list_to_string( metas )
      qry  += "AND meta_key IN( %s );" % meta
    else:
      qry += ";" 
    meta_records = Mysql.ex( qry )
    if len( meta_records ) == 0:
      return False
    meta_return = {}
    for record in meta_records:
      meta_return[ record['meta_key'] ] = {
        'meta_id'      : record['meta_id'],
        'date_updated' : record['date_updated'],
        'type'         : record['meta_type'],
        'value'        : self.__decode_value( record['meta_type'], record['meta_value'] )
      }
    return meta_return

  def create( self, entity, entity_id, metas ):
    """
    Create of update a meta entry.
    @params:
      entity    : 'companies',
      entity_id : 103
      metas     : [ {
        'meta_key'   : 'assoc_company',
        'meta_value' : '123,532',
        'meta_type'  : 'comma',
        'action'     : 'append'
      } ]
    """
    self.entity = entity
    entity_meta = self.get( entity_id )
    update_meta = []
    new_meta    = []
    if metas and len( metas ) > 0:
      m_count = 0
      for the_meta in metas:
        if entity_meta and the_meta['meta_key'] in entity_meta:
          update_meta.append( metas[ m_count ] )
        else:
          new_meta.append( metas[ m_count ] )
        m_count = m_count + 1

    for n_meta in new_meta:
      if 'meta_type' not in n_meta:
        parsed     = self.__parse_value( n_meta['meta_value'] )
        meta_type  = parsed['type']
        meta_value = parsed['value']
      else:
        if n_meta['meta_type'] in self.meta_types:
          meta_type  = n_meta['meta_type']
        else:
          meta_type   = 'string'
        meta_value = self.__encode_value( meta_type, n_meta['meta_value'] )
      values = {
        'id'         : entity_id,
        'meta_key'   : n_meta['meta_key'],
        'meta_value' : meta_value,
        'meta_type'  : meta_type,
      }
      Mysql.insert( "%s_meta" % entity, values )

    for u_meta in update_meta:
      meta_value = u_meta['meta_value']
      try:
        meta_type = entity_meta[ u_meta['meta_key'] ]['meta_type']
      except KeyError:
        Debugger.write( 'KeyERROR line 123 entity_meta, u_meta[meta_key]', ( entity_meta,  u_meta['meta_key'] ) )
        sys.exit()
      if 'action' in u_meta:
        if u_meta['action'] == 'append':
          if u_meta['meta_type'] == 'comma':
            meta_value = entity_meta[ u_meta['meta_key'] ]['value']
            meta_value.append( u_meta['meta_value'] )
      values = {
        'meta_value' : self.__encode_value( meta_type,meta_value )
      }
      where = {
        'id'       : entity_id,
        'meta_key' : u_meta['meta_key']
      }
      Mysql.update( "%s_meta" % entity, values, where )

  def __parse_value( self, meta_value ):
    parsed = {}
    if isinstance( meta_value, str ):
      parsed['value'] = meta_value
      parsed['type']  = 'string'
    return parsed

  def __encode_value( self, e_type, value ):
    """
      Encodes a value on its way to the datbase.
    """
    if e_type == 'string':
      return value
    elif e_type == 'date':
      if value == 'now':
        return Mysql.now()
      try:
        return datetime.strptime( value, '%Y-%m-%d %H:%M:%S' )
      except:
        return value
    elif e_type == 'comma':
      return str( value )
    elif e_type == 'json':
      return json.dumps( value, ensure_ascii=False )

  def __decode_value( self, e_type, value ):
    """
      Decodes a value from the database out to the application
      based on the type of data which is stored.
    """
    if e_type == 'string':
      return str( value )
    elif e_type == 'date':
      try:
        return datetime.strptime( value, '%Y-%m-%d %H:%M:%S' )
      except:
        return value
    elif e_type == 'comma' and value:
      if ',' in value:
        return value.split( ',' )
      else:
        return [ value ]
    elif e_type == 'json':
      return json.loads( value )

# End File: includes/helpers/HelperMetaStore.py
