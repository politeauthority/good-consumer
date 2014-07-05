#!/usr/bin/python
"""
  Installer
  This will have to be run as root, as we will be installing all our dependancies here                                """   
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from web.MVC import MVC
MVC = MVC()
# End file header
import subprocess

#install our python dependancies
subprocess.call( "apt-get install python-mysqldb",   shell=True )
subprocess.call( "apt-get install python-cherrypy3", shell=True )
subprocess.call( "apt-get install python-jinja2",   shell=True )
subprocess.call( "apt-get install python-bs4",   shell=True )
Mysql = MVC.loadDriver('Mysql')
Mysql.ex( 'CREATE DATABASE IF NOT EXISTS `%s`;' % MVC.db['name'] )

if( sys.argv[1] and sys.argv[1] == 'cleanup' ):
  dropTable_options         = "DROP TABLE IF EXISTS `%s`.`options`; "         % MVC.db['name']
  dropTable_users           = "DROP TABLE IF EXISTS `%s`.`users`; "           % MVC.db['name']
  dropTable_usermeta        = "DROP TABLE IF EXISTS `%s`.`usermeta`; "        % MVC.db['name']
  dropTable_acl_roles       = "DROP TABLE IF EXISTS `%s`.`acl_roles`; "       % MVC.db['name']
  dropTable_acl_permissions = "DROP TABLE IF EXISTS `%s`.`acl_permissions`; " % MVC.db['name']
  dropTable_acl_role_perms  = "DROP TABLE IF EXISTS `%s`.`acl_role_perms`; "  % MVC.db['name']
  dropTable_acl_user_perms  = "DROP TABLE IF EXISTS `%s`.`acl_user_perms`; "  % MVC.db['name']
  dropTable_acl_user_roles  = "DROP TABLE IF EXISTS `%s`.`acl_user_roles`; "  % MVC.db['name']
  dropTable_companies       = "DROP TABLE IF EXISTS `%s`.`companies`; "       % MVC.db['name']
  dropTable_company_meta    = "DROP TABLE IF EXISTS `%s`.`company_meta`; "    % MVC.db['name']
  dropTable_people          = "DROP TABLE IF EXISTS `%s`.`people`; "          % MVC.db['name']
  dropTable_people_meta     = "DROP TABLE IF EXISTS `%s`.`people_meta`; "     % MVC.db['name']
  Mysql.ex( dropTable_options )
  Mysql.ex( dropTable_users )
  Mysql.ex( dropTable_usermeta )
  Mysql.ex( dropTable_acl_roles )
  Mysql.ex( dropTable_acl_permissions )
  Mysql.ex( dropTable_acl_role_perms )
  Mysql.ex( dropTable_acl_user_perms )
  Mysql.ex( dropTable_acl_user_roles )
  Mysql.ex( dropTable_companies )
  Mysql.ex( dropTable_company_meta )
  Mysql.ex( dropTable_people )
  Mysql.ex( dropTable_people_meta )

# Base Website tables
createTable_options = """
  CREATE TABLE `%s`.`options` (
    `id`              int(10) NOT NULL AUTO_INCREMENT,
    `meta_key`        varchar(255) NOT NULL,
    `meta_value`      varchar(255) NOT NULL,
    `parent`          int(10) DEFAULT 0,
    `pretty_name`     varchar(255) DEFAULT NULL,
    `help_text`       varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
  ); """ % MVC.db['name']

# User tables
createTable_users  = """
  CREATE TABLE `%s`.`users` ( 
    `id`              int(10)       NOT NULL AUTO_INCREMENT,
    `user`            varchar(100) NOT NULL,
    `email`           varchar(250) NOT NULL,
    `pass`            varchar(250) NOT NULL,
    `last_login`      varchar(15) DEFAULT NULL,
    PRIMARY KEY (`id`)
  );""" % MVC.db['name']

createTable_usermeta = """
  CREATE TABLE `%s`.`usermeta` (
    `id`              int(19) NOT NULL AUTO_INCREMENT,
    `user_id`         int(10) NOT NULL,
    `parent`          int(10) NOT NULL,
    `meta_key`        varchar(200) NOT NULL,
    `meta_value`      varchar(200) NOT NULL,
    `pretty_name`     varchar(250) DEFAULT NULL,
    `help_text`       varchar(250) DEFAULT NULL,
    PRIMARY KEY (`id`)
    ); """ % MVC.db['name']

createTable_acl_roles       = """
  CREATE TABLE `%s`.`acl_roles` ( 
    `id`            int(10) unsigned NOT NULL AUTO_INCREMENT,
    `role_name`     varchar(20) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `role_name` (`role_name`)
  ); """ % MVC.db['name']

createTable_acl_permissions = """
  CREATE TABLE `%s`.`acl_permissions` (
    `id`         int(10) unsigned NOT NULL AUTO_INCREMENT,
    `perm_key`   varchar(30) NOT NULL,
    `perm_name`  varchar(30) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `perm_key` (`perm_key`)
  ); """ % MVC.db['name']

createTable_acl_role_perms  = """
CREATE TABLE `%s`.`acl_role_perms` (
  `id`        int(10) unsigned NOT NULL AUTO_INCREMENT,
  `role_id`   int(10) NOT NULL,
  `perm_id`   int(10) NOT NULL,
  `value`     tinyint(1) NOT NULL DEFAULT '0',
  `added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_id` (`role_id`,`perm_id`)
); """ % MVC.db['name']

createTable_acl_user_perms  = """
CREATE TABLE `%s`.`acl_user_perms` ( 
  `id`         int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id`    int(10) NOT NULL,
  `perm_id`    int(10) NOT NULL,
  `value`      tinyint(1) NOT NULL DEFAULT '0',
  `added`      datetime NOT NULL,
  PRIMARY KEY (`ID`), 
  UNIQUE KEY `user_id` (`user_id`,`perm_id`)
 ); """ % MVC.db['name']

createTable_acl_user_roles  = """
  CREATE TABLE `%s`.`acl_user_roles` (
    `user_id`   int(10) NOT NULL,
    `role_id`   int(10) NOT NULL,
    `added`     datetime NOT NULL,
    UNIQUE KEY `user_id` (`user_id`,`role_id`)
  ); """ % MVC.db['name']

# Create Good Consumer tables
createTable_companies = """
  CREATE TABLE `%s`.`companies` (
    `company_id`   int(10) NOT NULL AUTO_INCREMENT,
    `name`         varchar(255) DEFAULT NULL,
    `symbol`       varchar(10) DEFAULT NULL,
    `slug`         varchar(255) DEFAULT NULL,
    `type`         varchar(255) DEFAULT NULL,
    `industry`     varchar(255) DEFAULT NULL,
    `headquarters` varchar(255) DEFAULT NULL,
    `founded`      TIMESTAMP DEFAULT 0,
    `wikipedia`    varchar(255) DEFAULT NULL,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`company_id`)
  )""" % MVC.db['name']

createTable_company_meta = """
  CREATE TABLE `%s`.`company_meta` (
    `meta_id`     int(10) NOT NULL AUTO_INCREMENT,
    `parent`      int(10) NOT NULL,
    `meta_key`    varchar(255) NOT NULL,
    `meta_value`  varchar(255) NOT NULL,
    `pretty_name` varchar(255) DEFAULT NULL,
    `help_text`   varchar(255) DEFAULT NULL,
    PRIMARY KEY (`meta_id`)
  ); """ % MVC.db['name']

createTable_people = """ 
  CREATE TABLE `%s`.`people` (
    `person_id`    int(10) NOT NULL AUTO_INCREMENT,
    `name`         varchar(255) DEFAULT NULL,
    `wikipedia`    varchar(255) DEFAULT NULL,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`person_id`)    
  ); """ % MVC.db['name']

createTable_people_meta = """
  CREATE TABLE `%s`.`people_meta` (
    `meta_id`     int(10) NOT NULL AUTO_INCREMENT,
    `parent`      int(10) NOT NULL,
    `meta_key`    varchar(255) NOT NULL,
    `meta_value`  varchar(255) NOT NULL,
    `pretty_name` varchar(255) DEFAULT NULL,
    `help_text` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`meta_id`)
); """ % MVC.db['name']

Mysql.ex( createTable_options )
Mysql.ex( createTable_users )
Mysql.ex( createTable_usermeta )
Mysql.ex( createTable_acl_roles )
Mysql.ex( createTable_acl_permissions )
Mysql.ex( createTable_acl_role_perms)
Mysql.ex( createTable_acl_user_perms )
Mysql.ex( createTable_acl_user_roles )
Mysql.ex( createTable_companies )
Mysql.ex( createTable_company_meta )
Mysql.ex( createTable_people )
Mysql.ex( createTable_people_meta )

User = MVC.loadModel( 'User' )
ACL  = MVC.loadHelper( 'ACL' )

# User.create( 'admin', '', 'password' )

# End File install/install.py
