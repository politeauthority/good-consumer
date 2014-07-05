#!/usr/bin/python
# Backup Helper
# @description
# Class for database, logfiles, and remote export of those files if needed
#

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

from os import path
import subprocess

class HelperMisc( object ):

  # Allows, ('.', '-', '_' )
  def slug( self, butterfly ):
    chars_to_remove = [ '!', '@', '#', '$', '%', '^','*',
      '(', ')', '+', '=', '?', ',', ';', '"', "'", "`",
      '[', ']', '(', ')', '.']
    chars_to_translate = { '&' : 'and' }
    slug = butterfly.lower()
    slug = slug.replace( ' ', '-' )
    for char in chars_to_remove:
      slug = slug.replace( char, '' )
    for key, trans in chars_to_translate.iteritems():
      slug = slug.replace( key, trans )
    return slug

# End File: helpers/HelperMisc.py