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

class ClientRepoTests(unittest.TestCase):
  """Tests each test function in client_repo_interoperability.py"""

  def test_expand_url(self):
    """Verifies that expand_url correctly replaces symbols with data."""
    tester = ClientTester(api_key='aoeu', initialize_now=False)
    response = tester.expand_url(url='example.org/api?k=$k$&p=$p$&n=$n$&'
                                 'gs=$gs$&cs=$cs$&gm=$gm$&cm=$cm$',
                                 person_record_id='example.com/p1',
                                 note_record_id='example.net/n1',
                                 global_skip='abc', current_skip='def',
                                 global_min_date='ghi', current_min_date='hjk')
    self.assertEqual(
        response, 'example.org/api?k=aoeu&p=example.com%2Fp1&n=example.net%2Fn1'
        '&gs=abc&cs=def&gm=ghi&cm=hjk')

  def retrieve_record(self, correct_response_strings, check_method):
    """check_retrieve_[person|note]_record should return messages if and only if
    the repository output differs from the expected output.  The expected
    response from the API is given in correct_response_strings.  check_method is
    a client_repo_interoperability method that can be called to run a check."""
    # it's okay to pass in correct_response_strings as one string or a list of
    # strings, but we always want to be able to iterate over every string, not
    # every character.
    if isinstance(correct_response_strings, basestring):
      correct_response_strings = [correct_response_strings]
    correct_response_files = [StringIO(string) for string in
                              correct_response_strings]
    correct_response_files.append(StringIO(PfifXml.XML_EMPTY_ATOM))

    # When provided with a record identical to the desired record, there should
    # be no messages
    utils.set_files_for_test(correct_response_files)
    messages = check_method()
    self.assertEqual(len(messages), 0)

    # When provided with a record different from to the desired record, there
    # should be some messages
    utils.set_files_for_test([StringIO(PfifXml.XML_11_FULL),
                              StringIO(PfifXml.XML_EMPTY_ATOM)])
    messages = check_method()
    self.assertTrue(len(messages) > 0)

  def test_retrieve_person_record(self):
    """check_retrieve_person_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=1, last_person=1,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.retrieve_record(PfifXml.XML_TEST_ONE_PERSON,
                         tester.check_retrieve_person_record)

    # It's okay to also have a note
    tester = ClientTester(first_person=1, last_person=1,
                          first_person_with_notes=1, last_person_with_notes=1,
                          first_note=1, last_note=1)
    self.retrieve_record(PfifXml.XML_TEST_ONE_PERSON_ONE_NOTE,
                         tester.check_retrieve_person_record)

  def test_retrieve_note_record(self):
    """check_retrieve_note_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=-1, last_person=-2,
                          first_person_with_notes=1, last_person_with_notes=1,
                          first_note=1, last_note=1)
    self.retrieve_record(PfifXml.XML_TEST_ONE_NOTE,
                         tester.check_retrieve_note_record)

  def test_compile_all_responses(self):
    """compile_all_responses should continue calling the API until it gets no
    more records in the response."""
    tester = ClientTester(first_person=1, last_person=6,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    # A list of three persons lists
    correct_xml_strings = [PfifXml.XML_TEST_ONE_PERSON,
                           PfifXml.XML_TEST_PERSON_TWO_THREE,
                           PfifXml.XML_TEST_PERSON_FOUR_THROUGH_SIX]
    self.retrieve_record(correct_xml_strings, tester.check_retrieve_all_persons)

  def test_retrieve_all_persons(self):
    """check_retrieve_all_persons should return messages if and only if the repo
    output differs from the expected output.  The expected output should accept
    a person or a person with notes."""
    tester = ClientTester(first_person=2, last_person=3,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.retrieve_record(PfifXml.XML_TEST_PERSON_TWO_THREE,
                         tester.check_retrieve_all_persons)

    # It's okay to have all of the notes
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.retrieve_record(PfifXml.XML_TEST_TWO_PERSONS_TWO_NOTES,
                         tester.check_retrieve_all_persons)

  def test_retrieve_all_notes(self):
    """check_retrieve_all_notes should return messages if and only if the repo
    output differs from the expected output."""
    tester = ClientTester(first_person=-1, last_person=-2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.retrieve_record(PfifXml.XML_TEST_TWO_NOTES_FOR_PERSONS_ONE_TWO,
                         tester.check_retrieve_all_notes)

  def test_retrieve_since_time(self):
    """check_retrieve_all_[persons|notes]_since_time should return notes after
    the time of a specified record."""
    tester = ClientTester(first_person=619, last_person=623,
                          first_person_with_notes=49, last_person_with_notes=51,
                          first_note=14, last_note=18)
    # We pass in person 621 and note 5016 because, in order to figure out the
    # min_date, the check method will need to get that particular record.
    self.retrieve_record([PfifXml.XML_TEST_PERSON_621,
                          PfifXml.XML_TEST_PERSONS_622_623],
                         tester.check_retrieve_all_persons_since_time)
    self.retrieve_record(
        [PfifXml.XML_TEST_NOTE_5016,
         PfifXml.XML_TEST_NOTES_5017_THROUGH_5118_IN_RANGE_14_18],
        tester.check_retrieve_all_notes_since_time)

if __name__ == '__main__':
  unittest.main()
