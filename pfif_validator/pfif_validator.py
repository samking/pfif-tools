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

def validate_xml_or_die(xml_file):
  """Returns an XML tree of the xml file.  If the XML file is invalid, the XML
  library will raise an exception."""
  return ET.parse(xml_file)

def main():
  if (not len(sys.argv()) == 2):
    print "Usage: python pfif-validator.py my-pyif-xml-file"
  xml_tree = validate_xml_or_die(sys.argv(1))
  # pfif_version = validate_root_is_pfif_or_die(xml)
  # validate_has_child(xml, pfif_version)
  # validate_has_mandatory_children(xml, pfif_version)

if __name__ == '__main__':
  main()
