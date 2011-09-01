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
import client_repo_interoperability
import unittest
from StringIO import StringIO
import tests.pfif_xml as PfifXml
import sys
from urllib2 import HTTPError

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

  def run_test(self, correct_response_strings, check_method):
    """check_method should return messages if and only if the repository output
    differs from the expected output.  The expected response from the API is
    given in correct_response_strings.  check_method is a
    client_repo_interoperability method that can be called to run a check."""
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
    # should be some messages.  Some tests need several queries, so pad it with
    # empty PFIF.
    utils.set_files_for_test([StringIO(PfifXml.XML_11_FULL),
                              StringIO(PfifXml.XML_EMPTY_PFIF),
                              StringIO(PfifXml.XML_EMPTY_PFIF),
                              StringIO(PfifXml.XML_EMPTY_PFIF),
                              StringIO(PfifXml.XML_EMPTY_PFIF)])
    messages = check_method()
    self.assertTrue(len(messages) > 0)

  @staticmethod
  def test_retrieve_record():
    """retrieve_record should return an object that can be used to initialize a
    PFIF XML Tree."""
    tester = ClientTester(initialize_now=False)
    file_for_test = StringIO(PfifXml.XML_11_SMALL)
    def seek(_):
      """URLs can't seek, so neither can this StringIO."""
      assert False
    file_for_test.seek = seek
    utils.set_file_for_test(file_for_test)
    file_obj = tester.retrieve_record('url_template', 'person_record_id', 'id')
    utils.PfifXmlTree(file_obj)

  def test_retrieve_person_record(self):
    """check_retrieve_person_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=1, last_person=1,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.run_test(PfifXml.XML_TEST_ONE_PERSON,
                  tester.check_retrieve_person_record)

    # It's okay to also have a note
    tester = ClientTester(first_person=1, last_person=1,
                          first_person_with_notes=1, last_person_with_notes=1,
                          first_note=1, last_note=1)
    self.run_test(PfifXml.XML_TEST_ONE_PERSON_ONE_NOTE,
                  tester.check_retrieve_person_record)

  def test_retrieve_note_record(self):
    """check_retrieve_note_record should return messages if and only if the
    repository output differs from the expected output."""
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=1, last_person_with_notes=1,
                          first_note=1, last_note=1)
    self.run_test(PfifXml.XML_TEST_ONE_NOTE, tester.check_retrieve_note_record)

  def test_compile_all_responses(self):
    """compile_all_responses should continue calling the API until it gets no
    more records in the response."""
    tester = ClientTester(first_person=1, last_person=6,
                          first_person_with_notes=1, last_person_with_notes=2)
    # A list of three persons lists
    correct_xml_strings = [PfifXml.XML_TEST_ONE_PERSON,
                           PfifXml.XML_TEST_PERSON_TWO_THREE,
                           PfifXml.XML_TEST_PERSON_FOUR_THROUGH_SIX]
    self.run_test(correct_xml_strings, tester.check_retrieve_all_persons)

  def test_retrieve_all_persons(self):
    """check_retrieve_all_persons should return messages if and only if the repo
    output differs from the expected output.  The expected output should accept
    a person or a person with notes."""
    tester = ClientTester(first_person=2, last_person=3,
                          first_person_with_notes=-1, last_person_with_notes=-2,
                          first_note=-1, last_note=-2)
    self.run_test(PfifXml.XML_TEST_PERSON_TWO_THREE,
                  tester.check_retrieve_all_persons)

    # It's okay to have all of the notes
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.run_test(PfifXml.XML_TEST_TWO_PERSONS_TWO_NOTES,
                  tester.check_retrieve_all_persons)

  def test_retrieve_all_notes(self):
    """check_retrieve_all_notes should return messages if and only if the repo
    output differs from the expected output."""
    tester = ClientTester(first_person=1, last_person=2,
                          first_person_with_notes=1, last_person_with_notes=2,
                          first_note=1, last_note=2)
    self.run_test(PfifXml.XML_TEST_TWO_NOTES_FOR_PERSONS_ONE_TWO,
                  tester.check_retrieve_all_notes)

  def test_retrieve_since_time(self):
    """check_retrieve_all_[persons|notes]_since_time should return notes after
    the time of a specified record."""
    tester = ClientTester(first_person=619, last_person=623,
                          first_person_with_notes=49, last_person_with_notes=51,
                          first_note=14, last_note=18)
    # We pass in person 621 and note 5016 because, in order to figure out the
    # min_date, the check method will need to get that particular record.
    self.run_test([PfifXml.XML_TEST_PERSON_621,
                   PfifXml.XML_TEST_PERSONS_622_623],
                  tester.check_retrieve_all_persons_since_time)
    self.run_test([PfifXml.XML_TEST_NOTE_5016,
                   PfifXml.XML_TEST_NOTES_5017_THROUGH_5118_IN_RANGE_14_18],
                  tester.check_retrieve_all_notes_since_time)

  def test_retrieve_all_notes_from_person(self):
    """check_retrieve_all_notes_from_person should return only notes associated
    with the specified person."""
    tester = ClientTester(first_person=98, last_person=100,
                          first_person_with_notes=98, last_person_with_notes=99,
                          first_note=11, last_note=16)
    self.run_test(PfifXml.XML_TEST_NOTES_9911_THROUGH_9916,
                  tester.check_retrieve_all_notes_from_person)

  def test_retrieve_all_persons_with_notes(self):
    """check_retrieve_all_persons_with_notes should return all persons and any
    notes that those persons have."""
    tester = ClientTester(first_person=99, last_person=100,
                          first_person_with_notes=99, last_person_with_notes=99,
                          first_note=98, last_note=99)
    self.run_test(PfifXml.XML_TEST_PERSON_99_100_NOTE_98_99,
                  tester.check_retrieve_all_persons_with_notes)

  def test_retrieve_all_changed_persons(self):
    """check_retrieve_all_changed_persons should verify that changing person 1
    yields no records after person 1 and that changing person 2 yields one
    record changed after person 1."""
    tester = ClientTester(first_person=1, last_person=3,
                          first_person_with_notes=-1, last_person_with_notes=-2)
    # write response, person 1 for min_date calibration, notes updated after
    # person 1 when person 1 is most recent,
    # write response, person 1 for min_date calibration, notes updated after
    # person 1 when person 2 is most recent.
    utils.set_post_xml_responses_for_test([StringIO('Response')])
    responses = [PfifXml.XML_TEST_ONE_PERSON, PfifXml.XML_EMPTY_PFIF,
                 PfifXml.XML_TEST_ONE_PERSON, PfifXml.XML_TEST_PERSON_TWO]
    self.run_test(responses, tester.check_retrieve_all_changed_persons)

  def test_api_write_records(self):
    """api_write_records should post xml to a url and raise an HTTP Error if the
    response is HTTP Error."""
    tester = ClientTester(last_person=1, last_person_with_notes=1)
    utils.set_post_xml_responses_for_test([StringIO('Response')])
    tester.api_write_records(tester.persons, tester.notes)

    utils.set_post_xml_responses_for_test([StringIO('HTTP Error')])
    self.assertRaises(HTTPError, tester.api_write_records, tester.persons,
                      tester.notes)

  def test_truncate_records(self):
    """truncate_records should never return a batch of more than the specified
    number of records at a time, and repeatedly querying it should return all
    records."""
    max_records_to_post = 3
    tester = ClientTester(last_person=10, last_person_with_notes=10,
                          max_records_to_post=str(max_records_to_post))
    all_persons = []
    all_notes = {}

    batch_persons, remaining_persons, batch_notes, remaining_notes = (
        tester.truncate_records(tester.persons, tester.notes))
    while batch_persons or batch_notes:
      total_records = len(batch_persons)
      all_persons.extend(batch_persons)
      for person_record_id, notes_arr in batch_notes.items():
        total_records += len(notes_arr)
        person_notes = all_notes.setdefault(person_record_id, [])
        person_notes.extend(notes_arr)
      self.assertTrue(total_records <= max_records_to_post)
      batch_persons, remaining_persons, batch_notes, remaining_notes = (
          tester.truncate_records(remaining_persons, remaining_notes))
    self.assertEqual(all_persons, tester.persons)
    self.assertEqual(all_notes, tester.notes)

  # main

  @staticmethod
  def test_verbose_help():
    """The verbose help text generators should not crash."""
    old_argv = sys.argv
    sys.argv = ['client_repo_interoperability.py', '--verbose-help']
    client_repo_interoperability.main()
    sys.argv = old_argv

  @staticmethod
  def test_normal_main():
    """Main, run without asking for help, should not crash."""
    old_argv = sys.argv
    sys.argv = ['client_repo_interoperability.py', '--last-person=1',
                '--last-person-with-notes=1']
    client_repo_interoperability.main()
    sys.argv = old_argv

  def test_run_all_checks(self):
    """Run all checks should run checks when provided with URLs and generate
    messages when not provided with URLs."""
    utils.set_post_xml_responses_for_test([StringIO('Response')])
    tester = ClientTester(last_person=1, last_person_with_notes=1,
                          retrieve_person_url='example.org')

    utils.set_file_for_test(StringIO(PfifXml.XML_11_SMALL))
    output = tester.run_all_checks(False)

    missing_url_text = 'missing a required URL'

    # 7 tests, all except for retrieve_person, should be missing a required URL.
    # Some of them might have multiple missing URLs.
    self.assertTrue(output.count(missing_url_text) >= 7)

    # When the API doesn't work, there should be a message saying that person
    # p0001 is missing.
    self.assertTrue('p0001' in output)

    utils.set_file_for_test(StringIO(PfifXml.XML_TEST_ONE_PERSON))
    output = tester.run_all_checks(True)

    # When the API does work, there should not be a message saying that person
    # p0001 is missing
    self.assertFalse('p0001' in output)

    # When the API gives broken XML, it should still work
    utils.set_file_for_test(StringIO(PfifXml.XML_INVALID))
    output = tester.run_all_checks(False)
    self.assertTrue('Error when parsing XML' in output)
    self.assertTrue(output.count(missing_url_text) >= 7)

    # When the API gives an HTTP error, it should still work
    utils.set_post_xml_responses_for_test([StringIO('HTTP Error')])
    utils.set_files_for_test([StringIO(PfifXml.XML_TEST_ONE_PERSON)] * 5)
    tester = ClientTester(
        last_person=1, last_person_with_notes=1,
        retrieve_person_url='example.org/person',
        retrieve_persons_after_date_url='example.org/date',
        write_records_url='example.org/write')
    output = tester.run_all_checks(False)
    self.assertTrue('HTTP Error when trying to access' in output)
    self.assertTrue(output.count(missing_url_text) >= 5)

if __name__ == '__main__':
  unittest.main()
