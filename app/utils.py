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
import xml.etree.ElementTree as ET
import urllib

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
def get_utcnow():
  """Return current time in utc, or debug value if set."""
  return _utcnow_for_test or datetime.utcnow()

class FileWithLines:
  """A file that keeps track of its line number.  From
  http://bytes.com/topic/python/answers/535191-elementtree-line-numbers-iterparse
  """

  def __init__(self, source):
    self.source = source
    self.line_number = 0

  def read(self, num_bytes): # pylint: disable=W0613
    """Wrapper around file.readLine that keeps track of line number"""
    self.line_number += 1
    return self.source.readline()

# Doesn't inherit from ET.ElementTree to avoid messing with the
# ET.ElementTree.parse factory method
class PfifXmlTree():
  """An XML tree with PFIF-XML-specific helper functions."""

  def __init__(self, xml_file):
    self.namespace = None
    self.version = None
    self.tree = None
    self.line_numbers = {}
    self.lines = xml_file.readlines()
    xml_file.seek(0)
    self.initialize_tree(xml_file)
    self.initialize_pfif_version()


  def initialize_tree(self, xml_file):
    """Reads in the XML tree from the XML file.  If the XML file is invalid,
    the XML library will raise an exception."""
    file_with_lines = FileWithLines(xml_file)
    tree_parser = iter(ET.iterparse(file_with_lines, events=['start']))
    event, root = tree_parser.next() # pylint: disable=W0612
    self.line_numbers[root] = file_with_lines.line_number

    for event, elem in tree_parser:
      self.line_numbers[elem] = file_with_lines.line_number
    self.tree = ET.ElementTree(root)

  def initialize_pfif_version(self):
    """Initializes the namespace and version.  Raises an exception of the XML
    root does not specify a namespace or tag, if the tag isn't pfif, or if the
    version isn't supported."""
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
    self.version = float(match.group(1))
    assert (self.version >= 1.1 and self.version <= 1.3), (
           'This validator only supports versions 1.1-1.3.')

  def getroot(self):
    """wrapper for ET.ElementTree.getroot."""
    return self.tree.getroot()

  def add_namespace_to_tag(self, tag):
    """turns a local tag into a fully qualified tag by adding a namespace """
    return '{' + self.namespace + '}' + tag

  def get_all_persons(self):
    """returns a list of all persons in the tree"""
    return self.tree.findall(self.add_namespace_to_tag('person'))

  def get_child_notes(self):
    """returns a list of all notes that are subnodes of persons"""
    notes = []
    for person in self.get_all_persons():
      notes.extend(person.findall(self.add_namespace_to_tag('note')))
    return notes

  def get_top_level_notes(self):
    """returns a list of all notes that are subnodes of the root node"""
    return self.tree.findall(self.add_namespace_to_tag('note'))

  def get_all_notes(self):
    """returns a list of all notes in the tree"""
    notes = self.get_top_level_notes()
    notes.extend(self.get_child_notes())
    return notes

  def get_field_text(self, parent, child_tag):
    """Returns the text associated with the child node of parent.  Returns none
    if parent doesn't have that child or if the child doesn't have any text"""
    child = parent.find(self.add_namespace_to_tag(child_tag))
    if child != None:
      return child.text
    return None
