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

"""Tests for client_repo_interoperability.py."""

__author__ = 'samking@google.com (Sam King)'

import utils
from client_repo_interoperability import ClientTester
import unittest
from StringIO import StringIO
import tests.pfif_xml as PfifXml
import make_test_data

class ClientRepoTests(unittest.TestCase):
  """Tests each test function in client_repo_interoperability.py"""

  def test_expand_url(self):
    """Verifies that expand_url correctly replaces symbols with data."""
    tester = ClientTester(api_key='aoeu', initialize_now=False)
    response = tester.expand_url(url='example.org/api?k=$k&p=$p&n=$n',
                                 person_record_id='example.com/p1',
                                 note_record_id='example.net/n1')
    self.assertEqual(
        response,
        'example.org/api?k=aoeu&p=example.com%2Fp1&n=example.net%2Fn1')

  def retrieve_record(self, tester, persons_list, notes_map, check_method):
    """check_retrieve_[person|note]_record should return messages if and only if
    the repository output differs from the expected output."""
    # When provided with a record identical to the desired record, there should
    # be no messages
    correct_xml = StringIO('')
    make_test_data.write_records(tester.version, correct_xml,
                                 persons_list, notes_map)
    utils.set_file_for_test(correct_xml)
    messages = check_method()
    self.assertEqual(len(messages), 0)

    # When provided with a record different from to the desired record, there
    # should be some messages
    utils.set_file_for_test(StringIO(PfifXml.XML_11_FULL))
    messages = check_method()
    self.assertTrue(len(messages) > 0)

  def test_retrieve_person_record(self):
    """check_retrieve_person_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=1, last_person=1,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.retrieve_record(tester, tester.persons, {},
                         tester.check_retrieve_person_record)

  def test_retrieve_note_record(self):
    """check_retrieve_note_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=-1, last_person=-2,
                          first_person_with_notes=1, last_person_with_notes=1,
                          first_note=1, last_note=1)
    self.retrieve_record(tester, [], tester.notes,
                         tester.check_retrieve_note_record)

if __name__ == '__main__':
  unittest.main()