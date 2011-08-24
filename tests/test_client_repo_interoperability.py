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
    response = tester.expand_url(url='example.org/api?k=$k$&p=$p$&n=$n$&'
                                 'gs=$gs$&cs=$cs$&gm=$gm$&cm=$cm$',
                                 person_record_id='example.com/p1',
                                 note_record_id='example.net/n1',
                                 global_skip='abc', current_skip='def',
                                 global_min_date='ghi', current_min_date='hjk')
    self.assertEqual(
        response,
        'example.org/api?k=aoeu&p=example.com%2Fp1&n=example.net%2Fn1'
        '&gs=abc&cs=def&gm=ghi&cm=hjk')

  def retrieve_record(self, tester, persons_list, notes_map, check_method,
                      persons_list_is_meta=False):
    """check_retrieve_[person|note]_record should return messages if and only if
    the repository output differs from the expected output.  persons_list and
    notes_map are persons and notes in the formats generated by
    personfinder_pfif's parser.  check_method is a client_repo_interoperability
    method that can be called to run a check.  If persons_list_is_meta, then
    persons_list is a list of persons_lists (used for testing
    compile_all_responses, which can issue several requests and expects several
    responses).  If person_list_is_meta, notes_map should be blank."""
    # TODO(samking): per lee's advice, hardcode in the XML rather than
    # generating it.
    correct_xml_files = []
    meta_persons_list = persons_list
    if not persons_list_is_meta:
      meta_persons_list = [meta_persons_list]
    for individual_persons_list in meta_persons_list:
      correct_xml = utils.NonClosingStringIo('')
      make_test_data.write_records(tester.version, correct_xml,
                                   individual_persons_list, notes_map)
      correct_xml.seek(0)
      correct_xml_files.append(correct_xml)
    correct_xml_files.append(StringIO(PfifXml.XML_EMPTY_ATOM))

    # When provided with a record identical to the desired record, there should
    # be no messages
    utils.set_files_for_test(correct_xml_files)
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

  def test_compile_all_responses(self):
    """compile_all_responses should continue calling the API until it gets no
    more records in the response."""
    tester = ClientTester(first_person=1, last_person=6,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    # A list of three persons lists
    meta_persons_list = [tester.persons[0:2], tester.persons[2:5],
                         tester.persons[5:]]
    self.retrieve_record(tester, meta_persons_list, {},
                         tester.check_retrieve_all_persons,
                         persons_list_is_meta=True)

  def test_retrieve_all_persons(self):
    """check_retrieve_all_persons should return messages if and only if the repo
    output differs from the expected output.  The expected output should accept
    a person or a person with notes."""
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.retrieve_record(tester, tester.persons, {},
                         tester.check_retrieve_all_persons)

    # It's okay to have all of the notes
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.retrieve_record(tester, tester.persons, tester.notes,
                         tester.check_retrieve_all_persons)

  def test_retrieve_all_notes(self):
    """check_retrieve_all_notes should return messages if and only if the repo
    output differs from the expected output."""
    tester = ClientTester(first_person=-1, last_person=-2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.retrieve_record(tester, [], tester.notes,
                         tester.check_retrieve_all_notes)

  def test_retrieve_since_time(self):
    """check_retrieve_all_[persons|notes]_since_time should return notes after
    the time of a specified record."""
    tester = ClientTester(first_person=619, last_person=623,
                          first_person_with_notes=49, last_person_with_notes=51,
                          first_note=14, last_note=18)
    self.assertTrue(False)
    self.retrieve_record(tester, #[], tester.notes,
                         tester.check_retrieve_all_persons_since_time)
    self.retrieve_record(tester, #[], tester.notes,
                         tester.check_retrieve_all_notes_since_time)

if __name__ == '__main__':
  unittest.main()
