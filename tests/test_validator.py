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

"""Tests for pfif-validator.py"""

import unittest
import StringIO

import os
import sys
# TODO(samking): I'm sure that there is a simpler way to do this...
sys.path.append(os.getcwd() + '/../pfif_validator')
import pfif_validator

class ValidatorTests(unittest.TestCase):

  def test_valid_xml(self):
    """validate_xml_or_die should turn a string of valid XML into an object"""
    valid_xml_file = StringIO.StringIO("""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:pfif>""")
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
    pfif_12_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:pfif>""")
    tree = pfif_validator.validate_xml_or_die(pfif_12_xml_file)
    self.assertEqual(pfif_validator.validate_root_is_pfif_or_die(tree), 1.2)

  def test_root_is_not_pfif(self):
    """validate_root_is_pfif_or_die should raise an exception if the XML root
    is not PFIF"""
    random_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<html>
  <body />
</html>""")
    tree = pfif_validator.validate_xml_or_die(random_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)

  def test_root_is_bad_pfif_version(self):
    """validate_root_is_pfif_or_die should raise an exception if the PFIF
    version is not supported"""
    pfif_9999_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/999.9">
  <pfif:person />
</pfif:pfif>""")
    tree = pfif_validator.validate_xml_or_die(pfif_9999_xml_file)
    self.assertRaises(Exception, pfif_validator.validate_root_is_pfif_or_die,
                      tree)



if __name__ == '__main__':
  unittest.main()
