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
import sys
import utils

class DiffTests(unittest.TestCase):
  """Defines tests for pfif_diff.py"""

  # objectify

  @staticmethod
  def xml_to_object(xml_string):
    """Objectifies the xml_string."""
    return pfif_diff.objectify_pfif_xml(StringIO(xml_string))

  def compare_reference_object(self, test_xml, reference_object):
    """The object generated by objectifying test_xml should be the same as the
    reference_object."""
    xml_object = self.xml_to_object(test_xml)
    transformed_reference_object = pfif_diff.change_record_ids(reference_object)
    self.assertEqual(xml_object, transformed_reference_object)


  def test_objectify_basic(self):
    """objectify_pfif_xml should turn PFIF XML into a map from record_id to
    a map from fieldname to value with the correct number of records and
    fields."""
    self.compare_reference_object(PfifXml.XML_MANDATORY_13,
                                  PfifXml.XML_MANDATORY_13_MAP)

  def test_objectify_blank_values(self):
    """objectify_pfif_xml should store an empty string for any blank values."""
    self.compare_reference_object(PfifXml.XML_BLANK_FIELDS,
                                  PfifXml.XML_BLANK_FIELDS_MAP)

  def test_objectify_accepts_weird_fields(self):
    """objectify_pfif_xml should be agnostic to the names of fields (except for
    person, note, person_record_id, and note_record_id), so it should accept
    fields with weird names."""
    self.compare_reference_object(PfifXml.XML_EXTRANEOUS_FIELD_11,
                                  PfifXml.XML_EXTRANEOUS_FIELD_11_MAP)

  def test_objectify_accepts_persons_and_notes_with_similar_ids(self):
    """objectify_pfif_xml should store unique entries if there is a note and a
    person with the same record_id."""
    xml_object = self.xml_to_object(PfifXml.XML_DUPLICATE_PERSON_AND_NOTE_ID)
    self.assertEqual(len(xml_object), 2)

  # TODO(samking): what should we do here?  Silently ignore, print a
  # warning, or assert?
  def test_objectify_fails_gracefully_without_record_id(self):
    """objectify_pfif_xml should fail gracefully when presented with a record
    that has no record_id.  This test will pass if the record is included
    despite having no id or if the record is not included at all."""
    xml_object = self.xml_to_object(PfifXml.XML_ONE_BLANK_RECORD_ID)
    self.assertTrue(len(xml_object) == 1 or len(xml_object) == 2)

  # diff

  @staticmethod
  def run_diff(xml_str_1, xml_str_2, text_is_case_sensitive=None):
    """Runs pfif_file_diff on the two xml strings.  Returns the message list of
    differences."""
    xml_file_1 = StringIO(xml_str_1)
    xml_file_2 = StringIO(xml_str_2)
    if text_is_case_sensitive is not None:
      return pfif_diff.pfif_file_diff(xml_file_1, xml_file_2,
                                      text_is_case_sensitive)
    else:
      return pfif_diff.pfif_file_diff(xml_file_1, xml_file_2)

  def test_diff_same_file(self):
    """pfif_obj_diffing a file against itself should return no differences."""
    messages = self.run_diff(PfifXml.XML_11_FULL, PfifXml.XML_11_FULL)
    self.assertEqual(len(messages), 0)

  def test_diff_added_record(self):
    """pfif_obj_diffing a file against a file with one extra record should
    return one message."""
    messages = self.run_diff(PfifXml.XML_ONE_PERSON_ONE_FIELD,
                             PfifXml.XML_TWO_PERSONS_ONE_FIELD)
    self.assertEqual(len(messages), 1)

  def test_diff_deleted_record(self):
    """pfif_obj_diffing a file against a file with one fewer record should
    return one message."""
    messages = self.run_diff(PfifXml.XML_TWO_PERSONS_ONE_FIELD,
                             PfifXml.XML_ONE_PERSON_ONE_FIELD)
    self.assertEqual(len(messages), 1)

  def test_diff_added_field(self):
    """pfif_obj_diffing a file against a file with one extra field should
    return one message."""
    messages = self.run_diff(PfifXml.XML_ONE_PERSON_ONE_FIELD,
                             PfifXml.XML_ONE_PERSON_TWO_FIELDS)
    self.assertEqual(len(messages), 1)

  def test_diff_deleted_field(self):
    """pfif_obj_diffing a file against a file with one fewer field should
    return one message."""
    messages = self.run_diff(PfifXml.XML_ONE_PERSON_TWO_FIELDS,
                             PfifXml.XML_ONE_PERSON_ONE_FIELD)
    self.assertEqual(len(messages), 1)

  def test_diff_changed_value(self):
    """pfif_obj_diffing a file against a file with one changed value should
    return one message."""
    messages = self.run_diff(PfifXml.XML_ONE_PERSON_TWO_FIELDS,
                             PfifXml.XML_ONE_PERSON_TWO_FIELDS_NEW_VALUE)
    self.assertEqual(len(messages), 1)

  def test_diff_stress_test(self):
    """pfif_obj_diffing a file against a file with one record added, one record
    deleted, one field added, one field deleted, and one field changed should
    result in five messages."""
    messages = self.run_diff(PfifXml.XML_ADDED_DELETED_CHANGED_1,
                             PfifXml.XML_ADDED_DELETED_CHANGED_2)
    self.assertEqual(len(messages), 5)

  def test_diff_case_insensitive(self):
    """pfif_obj_diffing the files described in test_diff_stress_test should
    result in 4 messages when the text_is_case_sensitive flag is off and the
    change is from a difference is case."""
    messages = self.run_diff(PfifXml.XML_ADDED_DELETED_CHANGED_1,
                             PfifXml.XML_ADDED_DELETED_CHANGED_2,
                             text_is_case_sensitive=False)
    self.assertEqual(len(messages), 4)

  # main

  def run_main(self, argv):
    """Mocks files and runs main after setting sys.argv to the provided argv."""
    old_argv = sys.argv
    old_stdout = sys.stdout
    sys.argv = argv
    sys.stdout = StringIO('')

    utils.set_file_for_test(StringIO(PfifXml.XML_11_FULL))
    pfif_diff.main()
    self.assertFalse('all_messages' in sys.stdout.getvalue())

    sys.stdout = old_stdout
    sys.argv = old_argv

  def test_main(self):
    """main should not raise an exception under normal circumstances."""
    self.run_main(['pfif_diff.py', 'mocked_file', 'same_mocked_file'])

  def test_main_options(self):
    """main should not raise an exception when passed the --no-grouping
    or --text-is-case-insensitive options."""
    self.run_main(['pfif_diff.py', 'mocked_file', 'same_mocked_file',
                   '--no-grouping', '--text-is-case-insensitive'])

  def test_main_no_args(self):
    """main should give an assertion if it is given the wrong number of args."""
    old_argv = sys.argv

    sys.argv = ['pfif_diff.py']
    self.assertRaises(Exception, pfif_diff.main)

    sys.argv = ['pfif_diff.py', 'a_file']
    self.assertRaises(Exception, pfif_diff.main)

    sys.argv = old_argv

if __name__ == '__main__':
  unittest.main()
