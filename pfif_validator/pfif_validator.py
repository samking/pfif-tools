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

def validate_xml_or_die(xml_file):
  """Returns an XML tree of the xml file.  If the XML file is invalid, the XML
  library will raise an exception."""
  return ET.parse(xml_file)

def validate_root_is_pfif_or_die(xml_tree):
  """Validates that xml_tree refers to a PFIF XML file.  Returns the version.
  Raises an exception if unsuccessful."""
  root = xml_tree.getroot()
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

def validate_root_has_child_or_die(xml_tree):
  """If there is at least one child, returns a list of children.  Else, raises
  an exception."""
  root = xml_tree.getroot()
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
    if tag == "person" or (version >= 1.2 and  tag == "note"):
      result = True
      break
  if not result:
    print """ERROR: Having a person tag (or a note tag in PFIF 1.2+) as one of
             the children of the root node is mandatory."""
    print "Your version: " + str(version)
    print "All children: " + str(children)
  return result


def main():
  if (not len(sys.argv()) == 2):
    print "Usage: python pfif-validator.py my-pyif-xml-file"
  xml_tree = validate_xml_or_die(sys.argv(1))
  pfif_version = validate_root_is_pfif_or_die(xml_tree)
  validate_root_has_child_or_die(xml_tree)
  validate_root_has_mandatory_children(xml_tree, pfif_version)

if __name__ == '__main__':
  main()
