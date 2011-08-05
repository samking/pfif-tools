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

"""Tests for utils.py"""

import utils
import unittest
from StringIO import StringIO
import tests.pfif_xml as PfifXml

class UtilTests(unittest.TestCase):
  """Defines tests for utils.py"""

  # extract_tag

  def test_blank_input(self):
    """extract_tag should return an empty string on blank input"""
    self.assertEqual(utils.extract_tag(""), "")

  def test_tag(self):
    """extract_tag should return the original string when the string does not
    start with a namespace"""
    self.assertEqual(utils.extract_tag("foo"), "foo")

  def test_tag_and_namespace(self):
    """extract_tag should return the local tag when the string starts with a
    namespace"""
    self.assertEqual(utils.extract_tag("{foo}bar"), "bar")

  # PfifXmlTree initialization

  def test_valid_xml(self):
    """initialize_xml should turn a string of valid XML into an object."""
    valid_xml_file = StringIO(PfifXml.XML_11_SMALL)
    tree = utils.PfifXmlTree(valid_xml_file)
    self.assertTrue(tree)
    self.assertTrue(tree.lines)
    self.assertTrue(tree.line_numbers)

  def test_invalid_xml(self):
    """initialize_xml should raise an error on a string of invalid XML."""
    invalid_xml_file = StringIO(PfifXml.XML_INVALID)
    self.assertRaises(Exception, utils.PfifXmlTree, invalid_xml_file)

  # PfifXmlTree.initialize_pfif_version

  def test_root_is_pfif(self):
    """initialize_pfif_version should return the version if the root is PFIF."""
    pfif_11_xml_file = StringIO(PfifXml.XML_11_SMALL)
    tree = utils.PfifXmlTree(pfif_11_xml_file)
    self.assertEqual(tree.version, 1.1)

  def test_root_is_not_pfif(self):
    """initialize_pfif_version should raise an exception if the XML root
    is not PFIF."""
    non_pfif_xml_file = StringIO(PfifXml.XML_NON_PFIF_ROOT)
    self.assertRaises(Exception, utils.PfifXmlTree, non_pfif_xml_file)

  def test_root_lacks_namespace(self):
    """initialize_pfif_version should raise an exception if the XML root
    doesn't specify a namespace."""
    no_namespace_xml_file = StringIO(PfifXml.XML_NO_NAMESPACE)
    self.assertRaises(Exception, utils.PfifXmlTree, no_namespace_xml_file)

  def test_root_is_bad_pfif_version(self):
    """initialize_pfif_version should raise an exception if the PFIF
    version is not supported."""
    pfif_99_xml_file = StringIO(PfifXml.XML_BAD_PFIF_VERSION)
    self.assertRaises(Exception, utils.PfifXmlTree, pfif_99_xml_file)

  def test_root_is_bad_pfif_website(self):
    """initialize_pfif_version should raise an exception if the PFIF
    website is wrong."""
    pfif_bad_website_xml_file = StringIO(PfifXml.XML_BAD_PFIF_WEBSITE)
    self.assertRaises(Exception, utils.PfifXmlTree, pfif_bad_website_xml_file)

if __name__ == '__main__':
  unittest.main()
