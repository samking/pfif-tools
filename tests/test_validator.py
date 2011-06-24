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
import pfif_validator

class ValidatorTests(unittest.TestCase):

  def test_valid_xml(self):
    """A string of valid XML should be turned into an object"""
    VALID_XML = cStringIO("""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:pfif>""")

    #TODO(samking): make the python object version of that xml
    python_object =  []
    #TODO(samking): run the function to make an #object
    self.assertEqual(python_object, pfif-valid(VALID_XML))

  def test_invalid_xml(self):
    """A string of invalid XML should print out an error and return none"""
    INVALID_XML = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>"""


if __name__ == '__main__':
  unittest.main()
