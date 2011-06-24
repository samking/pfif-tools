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
    """A string of valid XML should be turned into an object"""
    valid_xml_file = StringIO.StringIO("""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:pfif>""")
    self.assertTrue(pfif_validator.validate_xml_or_die(valid_xml_file))

  def test_invalid_xml(self):
    """A string of invalid XML should raise an error"""
    invalid_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>""")
    self.assertRaises(Exception, pfif_validator.validate_xml_or_die,
                      invalid_xml_file)



if __name__ == '__main__':
  unittest.main()
