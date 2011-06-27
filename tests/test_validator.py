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

"""Tests for pfif_validator.py"""

import unittest
import StringIO

import os
import sys
# TODO(samking): I'm sure that there is a simpler way to do this...
sys.path.append(os.getcwd() + '/../pfif_validator')
import pfif_validator

class ValidatorTests(unittest.TestCase):

  VALID_XML_11_SMALL = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person />
</pfif:pfif>"""

  def setUp(self):
    """Some of the tests will run code that prints stuff out.  This prevents it
    from printing next to the clean dots from the unit tests."""
    sys.stdout = open(os.devnull, "w")

  def set_up_xml_tree(self, xml):
    """Turns xml into a tree.  Does validation that all other tests rely on"""
    pfif_file = StringIO.StringIO(xml)
    tree = pfif_validator.validate_xml_or_die(pfif_file)
    version = pfif_validator.validate_root_is_pfif_or_die(tree)
    pfif_validator.validate_root_has_child_or_die(tree)
    return (tree, version)

  def test_valid_xml(self):
    """validate_xml_or_die should turn a string of valid XML into an object"""
    valid_xml_file = StringIO.StringIO(ValidatorTests.VALID_XML_11_SMALL)
    self.assertTrue(pfif_validator.validate_xml_or_die(valid_xml_file))

  def test_invalid_xml(self):
    """validate_xml_or_die should raise an error on a string of invalid XML"""
    invalid_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>""")
    self.assertRaises(Exception, pfif_validator.validate_xml_or_die,
                      invalid_xml_file)

  def test_root_is_pfif(self):
    """validate_root_is_pfif_or_die should return the PFIF version if the XML
    root is PFIF"""
    pfif_12_xml_file = StringIO.StringIO(ValidatorTests.VALID_XML_11_SMALL)
    tree = pfif_validator.validate_xml_or_die(pfif_12_xml_file)
    self.assertEqual(pfif_validator.validate_root_is_pfif_or_die(tree), 1.1)

  def test_root_is_not_pfif(self):
    """validate_root_is_pfif_or_die should raise an exception if the XML root
    is not PFIF"""
    random_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:html xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:html>""")
    tree = pfif_validator.validate_xml_or_die(random_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)

  def test_root_lacks_namespace(self):
    """validate_root_is_pfif_or_die should raise an exception if the XML root
    doesn't specify a namespace"""
    no_namespace_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif>
  <person />
</pfif>""")
    tree = pfif_validator.validate_xml_or_die(no_namespace_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)


  def test_root_is_bad_pfif_version(self):
    """validate_root_is_pfif_or_die should raise an exception if the PFIF
    version is not supported"""
    pfif_99_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/9.9">
  <pfif:person />
</pfif:pfif>""")
    tree = pfif_validator.validate_xml_or_die(pfif_99_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)

  def test_root_is_bad_pfif_website(self):
    """validate_root_is_pfif_or_die should raise an exception if the PFIF
    website is wrong"""
    pfif_bad_website_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.com/pfif/1.2">
  <pfif:person />
</pfif:pfif>""")
    tree = pfif_validator.validate_xml_or_die(pfif_bad_website_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)

  def test_root_has_child(self):
    """validate_root_has_child_or_die should do nothing if the root node has at
    least one child"""
    pfif_file = StringIO.StringIO(ValidatorTests.VALID_XML_11_SMALL)
    tree = pfif_validator.validate_xml_or_die(pfif_file)
    self.assertEqual(pfif_validator.validate_root_has_child_or_die(tree),
                        None)

  def test_root_lacks_child(self):
    """validate_root_has_child_or_die should raise an exception if the root node
    does not have at least one child"""
    pfif_file = StringIO.StringIO("""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2" />""")
    tree = pfif_validator.validate_xml_or_die(pfif_file)
    self.assertRaises(Exception, pfif_validator.validate_root_has_child_or_die,
                      tree)

  def test_root_has_mandatory_children(self):
    """validate_root_has_mandatory_children should return true if one of the
    children is a person"""
    (tree, version) = self.set_up_xml_tree(ValidatorTests.VALID_XML_11_SMALL)
    self.assertTrue(
        pfif_validator.validate_root_has_mandatory_children(tree, version))


  def test_root_lacks_mandatory_children(self):
    """validate_root_has_mandatory_children should return false if the only
    children are not notes or persons"""
    (tree, version) = self.set_up_xml_tree(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:notAPersonOrNote />
</pfif:pfif>""")
    self.assertFalse(
        pfif_validator.validate_root_has_mandatory_children(tree, version))

  def test_root_has_note_child_11(self):
    """validate_root_has_mandatory_children should return false if the only
    children are notes and the version is 1.1"""
    (tree, version) = self.set_up_xml_tree(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:note />
</pfif:pfif>""")
    self.assertFalse(
        pfif_validator.validate_root_has_mandatory_children(tree, version))

  def test_root_has_note_child_12(self):
    """validate_root_has_mandatory_children should return true if the only
    children are notes and the version is greater than 1.1"""
    (tree, version) = self.set_up_xml_tree(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:note />
</pfif:pfif>""")
    self.assertTrue(
        pfif_validator.validate_root_has_mandatory_children(tree, version))

  def test_note_has_mandatory_children(self):
    """validate_has_mandatory_children should return an empty list if it is
    given a note with all mandatory children"""
    (tree, version) = self.set_up_xml_tree(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id />
    <pfif:author_name />
    <pfif:source_date />
    <pfif:text />
  </pfif:note>
</pfif:pfif>""")
    self.assertEqual(
        len(validate_has_mandatory_children('note', tree, version)), 0)

  def test_note_has_no_mandatory_children(self):
    """validate_has_mandatory_children should return a list with four missing
    children when given a note with no children"""
    (tree, version) = self.set_up_xml_tree(
         """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note />
</pfif:pfif>""")
    self.assertEqual(
        len(validate_has_mandatory_children('note', tree, version)), 4)

  #def test_person_has_mandatory_children_11(self):
  #def test_person_has_mandatory_children_13(self):
  #def test_person_has_no_mandatory_children_11(self):
  #def test_person_has_no_mandatory_children_13(self):

if __name__ == '__main__':
  unittest.main()
