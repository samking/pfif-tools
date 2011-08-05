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

"""Tests for pfif_diff.py"""

import unittest
from StringIO import StringIO
import tests.pfif_xml as PfifXml
import pfif_diff

class DiffTests(unittest.TestCase):
  """Defines tests for pfif_diff.py"""

  def test_objectify(self):
    """objectify_pfif_xml should turn PFIF XML into a map from record_id to
    a map from fieldname to value with the correct number of records and
    fields."""
    xml_file = StringIO(PfifXml.XML_MANDATORY_13)
    xml_object = pfif_diff.objectify_pfif_xml(xml_file)
    reference_object = pfif_diff.change_record_ids(
        PfifXml.XML_MANDATORY_13_MAP.items())
    self.assertEqual(xml_object, reference_object)

  #TODO(samking): implement these tests.  And more.
  #def test_objectify_blank_values(self):
  #  """objectify_pfif_xml should store an empty string for any blank values."""

  #def test_objectify_fails_gracefully_without_record_id(self):
  #  """objectify_pfif_xml should fail gracefully when presented with a record
  #  that has no record_id."""

  #def test_objectify_accepts_weird_fields(self):
  #  """objectify_pfif_xml should be agnostic to the names of fields (except for
  #  person, note, person_record_id, and note_record_id), so it should accept
  #  fields with weird names."""

  #def test_objectify_accepts_persons_and_notes_with_similar_ids(self):
  #  """objectify_pfif_xml should store unique entries if there is a note and a
  #  person with the same record_id."""





if __name__ == '__main__':
  unittest.main()
