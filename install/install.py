#!/usr/bin/python
"""
  Installer
  This will have to be run as root, as we will be installing all our dependancies here
"""   
import sys
import subprocess
sys.path.append( '../web/' )
import MVC as MVC

MVC = MVC.MVC()
# End file header

#install our python dependancies
subprocess.call( "apt-get install python-mysqldb",   shell=True )
subprocess.call( "apt-get install python-cherrypy3", shell=True )
subprocess.call( "apt-get install python-jinja2",    shell=True )
subprocess.call( "apt-get install python-bs4",       shell=True )

Mysql = MVC.loadDriver('Mysql' )
Mysql.ex( 'CREATE DATABASE IF NOT EXISTS `%s`;' % MVC.db['name'] )

if( len( sys.argv ) > 1 and sys.argv[1] == 'cleanup' ):
  dropTable_options          = "DROP TABLE IF EXISTS `%s`.`options`; "         % MVC.db['name']
  dropTable_users            = "DROP TABLE IF EXISTS `%s`.`users`; "           % MVC.db['name']
  dropTable_usermeta         = "DROP TABLE IF EXISTS `%s`.`usermeta`; "        % MVC.db['name']
  dropTable_acl_roles        = "DROP TABLE IF EXISTS `%s`.`acl_roles`; "       % MVC.db['name']
  dropTable_acl_permissions  = "DROP TABLE IF EXISTS `%s`.`acl_permissions`; " % MVC.db['name']
  dropTable_acl_role_perms   = "DROP TABLE IF EXISTS `%s`.`acl_role_perms`; "  % MVC.db['name']
  dropTable_acl_user_perms   = "DROP TABLE IF EXISTS `%s`.`acl_user_perms`; "  % MVC.db['name']
  dropTable_acl_user_roles   = "DROP TABLE IF EXISTS `%s`.`acl_user_roles`; "  % MVC.db['name']
  dropTable_companies        = "DROP TABLE IF EXISTS `%s`.`companies`; "       % MVC.db['name']
  dropTable_company_meta     = "DROP TABLE IF EXISTS `%s`.`company_meta`; "    % MVC.db['name']
  dropTable_company_types    = "DROP TABLE IF EXISTS `%s`.`company_types`; "   % MVC.db['name']
  dropTable_company_industry = "DROP TABLE IF EXISTS `%s`.`company_industry`;" % MVC.db['name']
  dropTable_news             = "DROP TABLE IF EXISTS `%s`.`news`;"             % MVC.db['name']
  dropTable_news_meta        = "DROP TABLE IF EXISTS `%s`.`news_meta`;"        % MVC.db['name']
  dropTable_news_sources     = "DROP TABLE IF EXISTS `%s`.`news_sources`; "    % MVC.db['name']
  dropTable_people           = "DROP TABLE IF EXISTS `%s`.`people`; "          % MVC.db['name']
  dropTable_people_meta      = "DROP TABLE IF EXISTS `%s`.`people_meta`; "     % MVC.db['name']
  dropTable_job_log          = "DROP TABLE IF EXISTS `%s`.`job_log`; "         % MVC.db['name']

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
  Mysql.ex( dropTable_company_types )
  Mysql.ex( dropTable_company_industry )
  Mysql.ex( dropTable_news )
  Mysql.ex( dropTable_news_meta )
  Mysql.ex( dropTable_news_sources )
  Mysql.ex( dropTable_people )
  Mysql.ex( dropTable_people_meta )
  Mysql.ex( dropTable_job_log )

# Base Website tables
createTable_options = """
  CREATE TABLE `%s`.`options` (
    `id`              INT(10) NOT NULL AUTO_INCREMENT,
    `meta_key`        VARCHAR(255) NOT NULL,
    `meta_value`      VARCHAR(255) NOT NULL,
    `parent`          INT(10) DEFAULT 0,
    `pretty_name`     VARCHAR(255) DEFAULT NULL,
    `help_text`       VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

# User tables
createTable_users  = """
  CREATE TABLE `%s`.`users` ( 
    `id`              INT(10)       NOT NULL AUTO_INCREMENT,
    `user`            VARCHAR(100) NOT NULL,
    `email`           VARCHAR(250) NOT NULL,
    `pass`            VARCHAR(250) NOT NULL,
    `last_login`      VARCHAR(15) DEFAULT NULL,
    PRIMARY KEY (`id`)
  )
  DEFAULT CHARSET = utf8;""" % MVC.db['name']

createTable_usermeta = """
  CREATE TABLE `%s`.`usermeta` (
    `id`              INT(10) NOT NULL AUTO_INCREMENT,
    `user_id`         INT(10) NOT NULL,
    `parent`          INT(10) NOT NULL,
    `meta_key`        VARCHAR(200) NOT NULL,
    `meta_value`      VARCHAR(200) NOT NULL,
    `pretty_name`     VARCHAR(250) DEFAULT NULL,
    `help_text`       VARCHAR(250) DEFAULT NULL,
    PRIMARY KEY (`id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_acl_roles       = """
  CREATE TABLE `%s`.`acl_roles` ( 
    `id`            INT(10) unsigned NOT NULL AUTO_INCREMENT,
    `role_name`     VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `role_name` (`role_name`)        
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_acl_permissions = """
  CREATE TABLE `%s`.`acl_permissions` (
    `id`         INT(10) unsigned NOT NULL AUTO_INCREMENT,
    `perm_key`   VARCHAR(30) NOT NULL,
    `perm_name`  VARCHAR(30) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `perm_key` (`perm_key`)        
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_acl_role_perms  = """
  CREATE TABLE `%s`.`acl_role_perms` (
    `id`        INT(10) unsigned NOT NULL AUTO_INCREMENT,
    `role_id`   INT(10) NOT NULL,
    `perm_id`   INT(10) NOT NULL,
    `value`     TINYINT(1) NOT NULL DEFAULT '0',
    `added`     DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `role_id` (`role_id`,`perm_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_acl_user_perms  = """
  CREATE TABLE `%s`.`acl_user_perms` ( 
    `id`         INT(10) unsigned NOT NULL AUTO_INCREMENT,
    `user_id`    INT(10) NOT NULL,
    `perm_id`    INT(10) NOT NULL,
    `value`      tinyint(1) NOT NULL DEFAULT '0',
    `added`      DATETIME NOT NULL,
    PRIMARY KEY (`ID`), 
    UNIQUE KEY `user_id` (`user_id`,`perm_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_acl_user_roles  = """
  CREATE TABLE `%s`.`acl_user_roles` (
    `user_id`   INT(10) NOT NULL,
    `role_id`   INT(10) NOT NULL,
    `added`     DATETIME NOT NULL,
    UNIQUE KEY `user_id` (`user_id`,`role_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

# Create Good Consumer tables
createTable_companies = """
  CREATE TABLE `%s`.`companies` (
    `company_id`     INT(10) NOT NULL AUTO_INCREMENT,
    `name`           VARCHAR(255) DEFAULT NULL,
    `slug`           VARCHAR(255) DEFAULT NULL,
    `type`           VARCHAR(255) DEFAULT NULL,
    `industry`       VARCHAR(255) DEFAULT NULL,
    `headquarters`   VARCHAR(255) DEFAULT NULL,
    `founded`        TIMESTAMP DEFAULT 0,
    `wikipedia`      VARCHAR(255) DEFAULT NULL,
    `display`        INT(1) DEFAULT 0,
    `record_status`  INT(10) DEFAULT 0,    
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`company_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_company_meta = """
  CREATE TABLE `%s`.`company_meta` (
    `meta_id`      INT(10) NOT NULL AUTO_INCREMENT,
    `company_id`   INT(10) NOT NULL,
    `meta_key`     VARCHAR(255) NOT NULL,
    `meta_value`   TEXT DEFAULT NULL,
    `pretty_name`  VARCHAR(255) DEFAULT NULL,
    `help_text`    VARCHAR(255) DEFAULT NULL,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`meta_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_company_types = """
  CREATE TABLE `%s`.`company_types` (
    `company_type_id`   INT(10) NOT NULL AUTO_INCREMENT,
    `name`              VARCHAR(255) NOT NULL,
    `desc`              VARCHAR(255) NULL,
    `wikipedia`         VARCHAR(255) NULL,
    PRIMARY KEY(`company_type_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_company_industry = """
  CREATE TABLE `%s`.`company_industry` (
    `company_industry_id` INT(10) NOT NULL AUTO_INCREMENT,
    `name`                VARCHAR(255)   NOT NULL,
    `desc`                VARCHAR(255)   NULL,
    `wikipedia`           VARCHAR(255)   NULL,
    PRIMARY KEY(`company_industry_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_news = """
  CREATE TABLE `%s`.`news` (
    `article_id`      INT(10) NOT NULL AUTO_INCREMENT,
    `url`             TEXT NOT NULL,    
    `headline`        VARCHAR(255) NULL,
    `publish_date`    TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    `source_id`       INT(10) DEFAULT NULL,
    `content`         TEXT DEFAULT NULL,
    `record_status`   INT(10) DEFAULT 0,
    `date_updated`    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`article_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_news_meta = """
  CREATE TABLE `%s`.`news_meta` (
    `meta_id`      INT(10) NOT NULL AUTO_INCREMENT,
    `article_id`   INT(10) NOT NULL,
    `meta_key`     VARCHAR(255) NOT NULL,
    `meta_value`   TEXT DEFAULT NULL,
    `pretty_name`  VARCHAR(255) DEFAULT NULL,
    `help_text`    VARCHAR(255) DEFAULT NULL,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`meta_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_news_sources = """
  CREATE TABLE `%s`.`news_sources` (
    `source_id`       INT(10) NOT NULL AUTO_INCREMENT,
    `name`            VARCHAR(255) DEFAULT NULL,
    `url`             TEXT DEFAULT NULL,
    `date_updated`    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    
    PRIMARY KEY(`source_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_people = """ 
  CREATE TABLE `%s`.`people` (
    `person_id`       INT(10) NOT NULL AUTO_INCREMENT,
    `name`            VARCHAR(255) DEFAULT NULL,
    `slug`            VARCHAR(255) DEFAULT NULL,
    `wikipedia`       VARCHAR(255) DEFAULT NULL,
    `display`         INT(1) DEFAULT 1,
    `record_status`   INT(10) DEFAULT 0,
    `date_updated`    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`person_id`)
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_people_meta = """
  CREATE TABLE `%s`.`people_meta` (
    `meta_id`      INT(10) NOT NULL AUTO_INCREMENT,
    `person_id`    INT(10) NOT NULL,
    `meta_key`     VARCHAR(255) NOT NULL,
    `meta_value`   VARCHAR(255) NOT NULL,
    `pretty_name`  VARCHAR(255) DEFAULT NULL,
    `help_text`    VARCHAR(255) DEFAULT NULL,
    `date_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`meta_id`) 
  )
  DEFAULT CHARSET = utf8; """ % MVC.db['name']

createTable_job_log = """
  CREATE TABLE `good_consumer`.`job_log` (
    `id`         INT(10) NOT NULL AUTO_INCREMENT,
    `job`        VARCHAR(255) NOT NULL,
    `start`      TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    `end`        TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    `message`    TEXT DEFAULT NULL,
    PRIMARY KEY (`id`)
  )
  DEFAULT CHARSET = utf8;
"""

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
Mysql.ex( createTable_company_types )
Mysql.ex( createTable_company_industry )
Mysql.ex( createTable_news )
Mysql.ex( createTable_news_meta )
Mysql.ex( createTable_news_sources)
Mysql.ex( createTable_people )
Mysql.ex( createTable_people_meta )
Mysql.ex( createTable_job_log )

# FIRST USER CREATION 
# User = MVC.loadModel( 'User' )
# ACL  = MVC.loadHelper( 'ACL' )
# User.create( 'admin', '', 'password' )

# End File install/install.py
