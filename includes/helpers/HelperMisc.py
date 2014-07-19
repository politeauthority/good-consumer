#!/usr/bin/python
"""
  Misc Helper
  Pretty much the junk drawer of an application.
  Many of these functions could probably be put somewhere else.
"""

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

  def gmt_to_mtn( self, gmt_date ):
    subtract_offset_in_hours = 6
    from datetime import date, timedelta
    d = gmt_date - timedelta( hours = subtract_offset_in_hours )
    return d


# End File: helpers/HelperMisc.py