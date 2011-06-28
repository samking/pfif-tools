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

"""Validates that text follows the PFIF XML Specification at zesty.ca/pfif"""

import xml.etree.ElementTree as ET
import re
import xml_utils

class PfifValidator:

  # a map from version to parent : required-children mappings
  MANDATORY_CHILDREN = {1.1 : {'person' : ['person_record_id', 'source_date',
                                         'first_name', 'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text']
                              },
                        1.2 : {'person' : ['person_record_id', 'source_date',
                                         'first_name', 'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text']
                              },
                        1.3 : {'person' : ['person_record_id', 'source_date',
                                         'full_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text']
                              }
                       }

  # regular expressions to match valid formats for each field type
  RECORD_ID = r'.+/.+' #TODO(samking): make more specific
  DATE = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z'
  TEXT = r'.*' #TODO(samking): do we want to do .+?
  EMAIL = r'.+@.+' #TODO(samking): make more specific
  PHONE = r'[-+()\d]*\d[-+()\d]*' #TODO(samking): make more specific
  URL = r'.+' #TODO(samking): make more specific
  CAPS = r'[A-Z]+'
  STATE = r'[A-Z][A-Z]'
  INTEGER = r'\d+'
  BOOLEAN = r'(true|false)'

  # a map from field name to a regular expression matching valid formats for
  # that field
  FORMATS = {1.1 : {'person_record_id' : RECORD_ID,
                    'entry_date' : DATE,
                    'author_name' : TEXT,
                    'author_email' : EMAIL,
                    'author_phone' : PHONE,
                    'source_name' : TEXT,
                    'source_date' : DATE,
                    'source_url' : URL,
                    'first_name' : CAPS,
                    'last_name' : CAPS,
                    'home_city' : CAPS,
                    'home_state' : STATE,
                    'home_neighborhood' : CAPS,
                    'home_street' : CAPS,
                    'home_zip' : INTEGER,
                    'photo_url' : URL,
                    'other' : TEXT,
                    'note_record_id' : RECORD_ID,
                    'found' : BOOLEAN,
                    'email_of_found_person' : EMAIL,
                    'phone_of_found_person' : PHONE,
                    'last_known_location' : TEXT,
                    'text' : TEXT
                  },
             1.2 : {},
             1.3 : {}
            }

  #TODO(samking): change to true
  def __init__(self, xml_file, initialize=False): 
    self.xml_file = xml_file
    if initialize:
      self.validate_xml_or_die()
      self.validate_root_is_pfif_or_die()

  def validate_xml_or_die(self):
    """Returns an XML tree of the xml file.  If the XML file is invalid, the XML
    library will raise an exception."""
    self.tree = ET.parse(self.xml_file)
    return self.tree

  def validate_root_is_pfif_or_die(self):
    """Validates that tree refers to a PFIF XML file.  Returns the version.
    Raises an exception if unsuccessful."""
    root = self.tree.getroot()
    tag = root.tag
    # xml.etree.Element.tag is formatted like: {namespace}tag
    match = re.match(r'\{(.+)\}(.+)', tag)
    self.namespace = match.group(1)
    tag = match.group(2)
    assert match, "This XML root node doesn't specify a namespace and tag"
    assert tag == "pfif", "The root node must be pfif"

    # the correct pfif url is like: http://zesty.ca/pfif/VERSION where VERSION
    # is 1.1, 1.2, or 1.3
    match = re.match(r'http://zesty\.ca/pfif/(\d\.\d)', self.namespace)
    assert match, "The XML namespace specified is not correct.  It should be " \
                  "in the following format: http://zesty.ca/pfif/VERSION"
    self.version = float(match.group(1))
    assert (self.version >= 1.1 and self.version <= 1.3), (
           "This validator only supports versions 1.1-1.3.")
    return self.version

  def validate_root_has_child(self):
    """If there is at least one child, returns true."""
    root = self.tree.getroot()
    children = root.getchildren()
    if not len(children) > 0:
      print "The root node must have at least one child"
      return False
    return True

  def validate_root_has_mandatory_children(self):
    """In 1.1, the root must have at least a person node.  In 1.2+, the root
    must either have a person or note node.  Returns true if the tree has the
    required node.  Note that extraneous nodes will not be reported here, but in
    a later test, so if the root has a person and a note node in version 1.1,
    that will return true."""
    children = self.tree.getroot().getchildren()
    result = False
    for child in children:
      tag = xml_utils.extract_tag(child.tag)
      if tag == "person" or (self.version >= 1.2 and tag == "note"):
        result = True
        break
    if not result:
      print "ERROR: Having a person tag (or a note tag in PFIF 1.2+) as one " \
            "of the children of the root node is mandatory."
      print "All children: " + str(children)
    return result

  def add_namespace_to_tag(self, tag):
    """turns a local tag into a fully qualified tag by adding a namespace """
    return '{' + self.namespace + '}' + tag

  def validate_has_mandatory_children(self, parent_tag):
    """Validates that every parent node has all mandatory children specified by
    MANDATORY_CHILDREN.  Returns a list with the names of all mandatory children
    missing from any parent found.
    parent_tag should be a string of the local tag of the node to check."""
    mandatory_children = PfifValidator.MANDATORY_CHILDREN[self.version]
    mandatory_children = mandatory_children[parent_tag]
    parents = self.tree.findall(self.add_namespace_to_tag(parent_tag))
    missing_children = []
    for parent in parents:
      for child_tag in mandatory_children:
        child = parent.find(self.add_namespace_to_tag(child_tag))
        if child is None:
          if not child_tag in missing_children:
            missing_children.append(child_tag)
    return missing_children

  def validate_person_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that persons have
    all mandatory children."""
    return self.validate_has_mandatory_children('person')

  def validate_note_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that notes have
    all mandatory children."""
    return self.validate_has_mandatory_children('note')

  def validate_fields_have_correct_format(self):
    """Validates that every field in FORMATS follows the correct format
    (ie, that the dates are in yyyy-mm-ddThh:mm:ssZ format).  Returns a list of
    the fields that have improperly formatted data."""
    failed_matches = []
    for field, field_format in PfifValidator.FORMATS[self.version].items():
      elements = self.tree.findall(self.add_namespace_to_tag(field))
      for element in elements:
        text = element.text
        match = re.match(field_format, text)
        if match is None:
          failed_matches.append((element.tag, element.text))
    print failed_matches
    return failed_matches

#def main():
#  if (not len(sys.argv()) == 2):
#    print "Usage: python pfif-validator.py my-pyif-xml-file"
#  v = PfifValidator(sys.argv(1))
#  v.validate_xml_or_die(sys.argv(1))
#  v.validate_root_is_pfif_or_die()
#  validate_root_has_child_or_die()
#  validate_root_has_mandatory_children()
#  validate_person_has_mandatory_children()
#  validate_note_has_mandatory_children()
#  validate_fields_have_correct_format()
#
#if __name__ == '__main__':
#  main()
