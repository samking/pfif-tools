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

# regular expressions to match acceptable formats for a particular type of field
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

# a map from the name of a field to a regular expression matching valid formats
# for that field
VALID_FORMATS = {1.1 : {'person_record_id' : RECORD_ID,
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

# the xml namespace without the version
NAMESPACE_BASE = 'http://zesty.ca/pfif/'

def validate_xml_or_die(xml_file):
  """Returns an XML tree of the xml file.  If the XML file is invalid, the XML
  library will raise an exception."""
  return ET.parse(xml_file)

def validate_root_is_pfif_or_die(tree):
  """Validates that tree refers to a PFIF XML file.  Returns the version.
  Raises an exception if unsuccessful."""
  root = tree.getroot()
  tag = root.tag
  # xml.etree.Element.tag is formatted like: {namespace}tag
  match = re.match(r'\{(.+)\}(.+)', tag)
  namespace = match.group(1)
  tag = match.group(2)
  assert match, "This XML root node doesn't specify a namespace and tag"
  assert tag == "pfif", "The root node must be pfif"

  # the correct pfif url is like: http://zesty.ca/pfif/VERSION where VERSION is
  # 1.1, 1.2, or 1.3
  match = re.match(r'http://zesty\.ca/pfif/(\d\.\d)', namespace)
  assert match, "The XML namespace specified is not correct.  It should be in" \
                "the following format: http://zesty.ca/pfif/VERSION"
  version = float(match.group(1))
  assert (version >= 1.1 and version <= 1.3), "This validator only supports" \
                                              "versions 1.1-1.3."
  return version

def validate_root_has_child_or_die(tree):
  """If there is at least one child, returns a list of children.  Else, raises
  an exception."""
  root = tree.getroot()
  children = root.getchildren()
  assert len(children) > 0, "There must be at least one child of the root node"

def validate_root_has_mandatory_children(tree, version):
  """In 1.1, the root must have at least a person node.  In 1.2+, the root must
  either have a person or note node.  Returns true if the tree has the required
  node.  Note that extraneous nodes will not be reported here, but in a later
  test, so if the root has a person and a note node in version 1.1, that will
  return true."""
  children = tree.getroot().getchildren()
  result = False
  for child in children:
    tag = xml_utils.extract_tag(child.tag)
    if tag == "person" or (version >= 1.2 and tag == "note"):
      result = True
      break
  if not result:
    print """ERROR: Having a person tag (or a note tag in PFIF 1.2+) as one of
             the children of the root node is mandatory."""
    print "Your version: " + str(version)
    print "All children: " + str(children)
  return result

def add_namespace_to_tag(tag, version):
  """turns a local tag into a fully qualified tag by adding a namespace """
  return '{' + NAMESPACE_BASE + str(version) + '}' + tag

def validate_has_mandatory_children(parent_tag, tree, version):
  """Validates that every parent node has all mandatory children specified by
  MANDATORY_CHILDREN.  Returns a list with the names of all mandatory children
  missing from any parent found.
  parent_tag should be a string of the local tag of the node to check."""
  mandatory_children = MANDATORY_CHILDREN[version][parent_tag]
  parents = tree.findall(add_namespace_to_tag(parent_tag, version))
  missing_children = []
  for parent in parents:
    for child_tag in mandatory_children:
      child = parent.find(add_namespace_to_tag(child_tag, version))
      if child is None:
        if not child_tag in missing_children:
          missing_children.append(child_tag)
  return missing_children

def validate_fields_have_correct_format(tree, version):
  """Validates that every field in FIELD_FORMATS follows the correct format (ie,
  that the dates are in yyyy-mm-ddThh:mm:ssZ format).  Returns a list of the
  fields that have improperly formatted data."""

def main():
  if (not len(sys.argv()) == 2):
    print "Usage: python pfif-validator.py my-pyif-xml-file"
  tree = validate_xml_or_die(sys.argv(1))
  version = validate_root_is_pfif_or_die(tree)
  validate_root_has_child_or_die(tree)
  validate_root_has_mandatory_children(tree, version)
  validate_person_has_mandatory_children(tree, version)
  validate_has_mandatory_children('person', tree, version)
  validate_has_mandatory_children('note', tree, version)
  validate_fields_have_correct_format(tree, version)

if __name__ == '__main__':
  main()
