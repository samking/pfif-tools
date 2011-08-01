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
import lxml.etree as ET

# XML Parsing Utilities

def extract_tag(etree_tag):
  """An etree tag comes in the form: {namespace}tag.  This returns the tag"""
  match = re.match(r'(?:\{.+\})?(.+)', etree_tag)
  if not match:
    return ""
  return match.group(1)

# Dependency Injection for Time -- from PersonFinder
_utcnow_for_test = None # pylint: disable=c0103

def set_utcnow_for_test(now):
  """Set current time for debug purposes."""
  global _utcnow_for_test # pylint: disable=w0603
  _utcnow_for_test = now

def get_utcnow():
  """Return current time in utc, or debug value if set."""
  return _utcnow_for_test or datetime.utcnow()

# Doesn't inherit from ET.ElementTree to avoid messing with the
# ET.ElementTree.parse factory method
class PfifXmlTree():
  """An XML tree with PFIF-XML-specific helper functions."""

  def __init__(self, xml_file):
    parser = ET.XMLParser(remove_comments=True)
    self.tree = ET.parse(xml_file, parser=parser)
    self.namespace = None


  def initialize_pfif_version(self):
    root = self.tree.getroot()
    tag = root.tag
    # xml.etree.Element.tag is formatted like: {namespace}tag
    match = re.match(r'\{(.+)\}(.+)', tag)
    assert match, 'This XML root node does not specify a namespace and tag'
    self.namespace = match.group(1)
    tag = match.group(2)
    assert tag == 'pfif', 'The root node must be pfif'

    # the correct pfif url is like: http://zesty.ca/pfif/VERSION where VERSION
    # is 1.1, 1.2, or 1.3
    match = re.match(r'http://zesty\.ca/pfif/(\d\.\d)', self.namespace)
    assert match, ('The XML namespace specified is not correct.  It should be '
                   'in the following format: http://zesty.ca/pfif/VERSION')
    version = float(match.group(1))
    assert (version >= 1.1 and version <= 1.3), (
           'This validator only supports versions 1.1-1.3.')
    return version

  def getroot(self):
    """wrapper for ET.ElementTree.getroot."""
    return self.tree.getroot()

  def findall(self, tag_to_find):
    """wrapper for ET.ElementTree.findall."""
    return self.tree.findall(tag_to_find)

  def add_namespace_to_tag(self, tag):
    """turns a local tag into a fully qualified tag by adding a namespace """
    return '{' + self.namespace + '}' + tag

  def get_all_persons(self):
    """returns a list of all persons in the tree"""
    return self.tree.findall(self.add_namespace_to_tag('person'))

  def get_all_notes(self):
    """returns a list of all notes in the tree"""
    notes = self.tree.findall(self.add_namespace_to_tag('note'))
    for person in self.get_all_persons():
      notes.extend(person.findall(self.add_namespace_to_tag('note')))
    return notes
