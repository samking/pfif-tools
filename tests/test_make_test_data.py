#!/usr/bin/env python
# coding=utf-8
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

"""Tests for make_test_data.py"""

__author__ = 'samking@google.com (Sam King)'

import unittest
from StringIO import StringIO
import make_test_data
import utils
import sys

class FakeStringIo(StringIO):
  """A fake StringIO that cannot be closed.  That way, even though
  make_test_data will properly close the file that it writes, we can still
  examine the contents of the StringIO after it has been written."""

  def close(self):
    """Does nothing."""
    return

class ArgWrapper():
  """Allows easily setting first_person, last_person, first_person_with_notes,
  last_person_with_notes, first_note, and last_note and getting a new argument
  vector out of them."""

  def __init__(self, script_name):
    self.script_name = script_name
    self.first_person = '1'
    self.last_person = '1'
    self.first_person_with_notes = '1'
    self.last_person_with_notes = '1'
    self.first_note = None
    self.last_note = None

  def to_argv(self):
    """Turns the currently saved values into an argument vector."""
    argv = [self.script_name,
            '--first-person', self.first_person,
            '--last-person', self.last_person,
            '--first-person-with-notes', self.first_person_with_notes,
            '--last-person-with-notes', self.last_person_with_notes]
    if self.first_note != None:
      argv.extend(['--first-note', self.first_note,
                   '--last-note', self.last_note])
    return argv

class MakeDataTests(unittest.TestCase):
  """Tests that make_test_data.py successfully makes a test data file."""

  def prepare_main(self, argv):
    """Mocks files and argv so that main can be tested."""
    self.old_argv = sys.argv # pylint: disable=w0201
    sys.argv = argv

    output_file = FakeStringIo('')
    utils.set_file_for_test(output_file)

    return output_file

  def restore_main(self):
    """Undoes the argv mocking from prepare_main."""
    sys.argv = self.old_argv

  def test_versions(self):
    """main should succeed when asked to create a PFIF 1.2 or 1.3 data set and
    raise an exception when asked to create any other version."""
    argv = ['make_test_data.py', '--last-person', '1',
            '--last-person-with-notes', '1', '--pfif-version', '1.2']
    outfile = self.prepare_main(argv)
    make_test_data.main()
    self.assertTrue('1.2' in outfile.getvalue())
    self.restore_main()

    argv[-1] = '1.3'
    outfile = self.prepare_main(argv)
    make_test_data.main()
    self.assertTrue('1.3' in outfile.getvalue())
    self.restore_main()

    argv[-1] = '9.9'
    outfile = self.prepare_main(argv)
    self.assertRaises(Exception, make_test_data.main)
    self.restore_main()

  def test_omit_field(self):
    """Passing the omit-field flag should result in that field not existing in
    the resulting document.  This should also work for multiple fields."""
    argv = ['make_test_data.py', '--last-person', '1',
            '--last-person-with-notes', '1']
    outfile = self.prepare_main(argv)
    make_test_data.main()
    self.assertTrue('photo_url' in outfile.getvalue())
    self.assertTrue('home_city' in outfile.getvalue())
    self.restore_main()

    argv.extend(['--omit-field', 'photo_url'])
    outfile = self.prepare_main(argv)
    make_test_data.main()
    self.assertTrue('photo_url' not in outfile.getvalue())
    self.assertTrue('home_city' in outfile.getvalue())
    self.restore_main()

    argv.extend(['--omit-field', 'home_city'])
    outfile = self.prepare_main(argv)
    make_test_data.main()
    self.assertTrue('photo_url' not in outfile.getvalue())
    self.assertTrue('home_city' not in outfile.getvalue())
    self.restore_main()

  def verify_make_record(self, person_id, note_id=None, include=(), exclude=()):
    """Creates a test data set with one person and one note, specified by
    person_id and note_id.  Verifies that every string in the include list is in
    the output and that no string in the exclude list is in the output."""
    args = ArgWrapper('make_test_data.py')
    args.first_person = person_id
    args.last_person = person_id
    if note_id != None:
      args.first_person_with_notes = person_id
      args.last_person_with_notes = person_id
      args.first_note = note_id
      args.last_note = note_id
    outfile = self.prepare_main(args.to_argv())
    make_test_data.main()
    output = outfile.getvalue()
    for string in include:
      self.assertTrue(string in output, string + ' should be in the output: ' +
                      output)
    for string in exclude:
      self.assertTrue(string not in output, string + ' should not be in the '
                      'output: ' + output)
    self.restore_main()

  def test_data_follows_spec(self):
    """The file created should include data that follows the test conformance
    spec."""
    # expiry_date should only be on fields with P<1000
    self.verify_make_record('999', include=['expiry_date'])
    self.verify_make_record('1000', exclude=['expiry_date'])

    # sex.  P=4k+1: female, P=4k+2:male, P=4k+3:other P=4k:none.
    # "male" is represented as >male when needed to disambiguate from female.
    # "other" is represented as >other when needed to disambiguate from the
    # pfif:other field name (whereas this is a value).
    self.verify_make_record('1', include=['sex', 'female'], exclude=['>male',
                                                                     '>other'])
    self.verify_make_record('2', include=['sex', 'male'], exclude=['female',
                                                                   '>other'])
    self.verify_make_record('3', include=['sex', '>other'], exclude=['male',
                                                                     'female'])
    self.verify_make_record('4', exclude=['sex', 'male', 'female', '>other'])

    # date_of_birth: P<98 has no dob; P=98 has dob=1900, P=99 has dob=1900-01,
    # P>99 has dob=1900-01-01 + 30 * id (so P=100 has dob=1908-03-20)
    self.verify_make_record('97', exclude=['date_of_birth'])
    self.verify_make_record('98', include=['date_of_birth', '1900'])
    self.verify_make_record('99', include=['date_of_birth', '1900-01'])
    self.verify_make_record('100', include=['date_of_birth', '1908-03-20'])

    # age: P=1 has age=34-56, P<98 has age=P, P=[98, 99] has age=111, P>99 has
    # no age
    self.verify_make_record('1', include=['age', '34-56'])
    self.verify_make_record('97', include=['age', '97'])
    self.verify_make_record('98', include=['age', '111'])
    self.verify_make_record('99', include=['age', '111'])
    self.verify_make_record('100', exclude=['age'])

    # person_record_id: example.org/pP.  author_email: P@example.com.
    # author_phone: 0000P.  other: description: P.
    # photo_url: http://photo.example.org/P.  home_postal_code: 0P.
    # source_date: 2011-01-01T01:01:01Z.  source_url: http://example.org/P
    # home_country and home_state: present.
    self.verify_make_record(
        '1234', include=['person_record_id', 'example.org/p1234',
                         'author_email', '1234@example.com',
                         'author_phone', '00001234',
                         'other', 'description: 1234',
                         'photo_url', 'http://photo.example.org/1234',
                         'home_postal_code', '01234',
                         'source_date', '2011-01-01T01:01:01Z',
                         'source_url', 'http://example.org/1234',
                         'entry_date',
                         'home_country',
                         'home_state'])

    # note_record_id: example.org/nPN.  author_email: PN@example.com.
    # author_phone: 0000PN.
    self.verify_make_record(
        '56', note_id='55', include=['note_record_id', 'example.org/n5655',
                                     'author_email', '5655@example.com',
                                     'author_phone', '00005655'])

    # P+N is odd: found is true, email_of_found_person present,
    # phone_of_found_person present. P+N is even: found is false, email and
    # phone of found person not present.
    self.verify_make_record(
        '47', note_id='32', include=['found', 'true',
                                     'email_of_found_person',
                                     'phone_of_found_person'])
    self.verify_make_record(
        '47', note_id='33', include=['found', 'false'],
        exclude=['email_of_found_person', 'phone_of_found_person'])


    # status: N=6k+1: information_sought.  N=6k+2: is_note_author.
    # N=6k+3: believed_alive.  N=6k+4: believed_missing.  N=6k+5: believed_dead.
    # N=6k: no status.
    self.verify_make_record('6', note_id='1', include=['status',
                                                       'information_sought'])
    self.verify_make_record('6', note_id='2', include=['status',
                                                       'is_note_author'])
    self.verify_make_record('6', note_id='3', include=['status',
                                                       'believed_alive'])
    self.verify_make_record('6', note_id='4', include=['status',
                                                       'believed_missing'])
    self.verify_make_record('6', note_id='5', include=['status',
                                                       'believed_dead'])
    self.verify_make_record('6', note_id='6', exclude=['status'])

    # linked_person_record_id: not present if P=1.  not present if N>1.
    # example.org/p(P+1) if P is even.  example.org/p(P-1) if P is odd.
    self.verify_make_record('1', note_id='1',
                            exclude=['linked_person_record_id'])
    self.verify_make_record('2', note_id='2',
                            exclude=['linked_person_record_id'])
    self.verify_make_record(
        '2', note_id='1', include=['linked_person_record_id',
                                   'example.org/p0003'])
    self.verify_make_record(
        '3', note_id='1', include=['linked_person_record_id',
                                   'example.org/p0002'])

  def test_get_after_record(self):
    """get_[persons|notes]_after_record should return new persons|notes that
    have all records up to and including record removed."""
    persons = make_test_data.generate_persons(first_person=9, last_person=13)
    notes = make_test_data.generate_notes(first_person_with_notes=9,
                                          last_person_with_notes=13,
                                          first_note=2, last_note=5)

    # there should be two persons in existence (12 and 13) and those two persons
    # should each have notes.
    excluded_record = make_test_data.make_person_id(11)
    recent_persons, recent_notes = make_test_data.get_persons_after_record(
        persons, notes, excluded_record)

    self.assertEqual(len(recent_persons), 2)
    self.assertEqual(len(recent_notes), 2)

    correct_person_ids = []
    for person_num in [12, 13]:
      correct_person_ids.append(make_test_data.make_person_id(person_num))

    for person in recent_persons:
      self.assertTrue(person['person_record_id'] in correct_person_ids)

    for person_id in correct_person_ids:
      self.assertTrue(person_id in recent_notes)
      self.assertEqual(len(recent_notes[person_id]), 4)

    # with persons greater than 99, there should be no notes.
    persons = make_test_data.generate_persons(first_person=98, last_person=101)
    excluded_record = make_test_data.make_person_id(99)
    recent_persons, recent_notes = make_test_data.get_persons_after_record(
        persons, notes, excluded_record)
    self.assertEqual(len(recent_persons), 2)
    self.assertEqual(recent_notes, {})

    # there should be three persons with four notes and one person with one
    # note.
    excluded_record = make_test_data.make_note_id(10, 4)
    recent_notes = make_test_data.get_notes_after_record(notes, excluded_record)

    self.assertEqual(len(recent_notes), 4)

    correct_person_ids = []
    for person_num, num_notes in [(10, 1), (11, 4), (12, 4), (13, 4)]:
      person_id = make_test_data.make_person_id(person_num)
      self.assertTrue(person_id in recent_notes)
      self.assertEqual(len(recent_notes[person_id]), num_notes)

if __name__ == '__main__':
  unittest.main()
