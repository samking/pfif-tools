#!/usr/bin/env python
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for the PFIF Validator"""

import re
from datetime import datetime
import urllib

# XML Parsing Utilities

def extract_tag(etree_tag):
  """An etree tag comes in the form: {namespace}tag.  This returns the tag"""
  match = re.match(r'(?:\{.+\})?(.+)', etree_tag)
  if not match:
    return ""
  return match.group(1)

# String Functions
def to_unicode(obj, encoding='utf-8'):
  """Converts a string to unicode if necessary.  From:
  http://farmdev.com/talks/unicode/"""
  if isinstance(obj, basestring) and not isinstance(obj, unicode):
    obj = unicode(obj, encoding)
  return obj

# Dependency Injection for Time -- from PersonFinder
_utcnow_for_test = None # pylint: disable=c0103

def set_utcnow_for_test(now):
  """Set current time for debug purposes."""
  global _utcnow_for_test # pylint: disable=w0603
  _utcnow_for_test = now

def get_utcnow():
  """Return current time in utc, or debug value if set."""
  return _utcnow_for_test or datetime.utcnow()

# Dependency injection for files
_file_for_test = None # pylint: disable=c0103

def set_file_for_test(file_for_test):
  """Set current file or url for debugging purposes."""
  global _file_for_test # pylint: disable=w0603
  _file_for_test = file_for_test

def open_file(filename, mode='r'):
  """Opens the file or returns a debug value if set."""
  return _file_for_test or open(filename, mode)

def open_url(url):
  """Opens the url or returns a debug value if set."""
  return _file_for_test or urllib.urlopen(url)
