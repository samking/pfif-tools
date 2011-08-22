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

# pylint: disable=c0301
"""Tests client-repo interoperability for a PFIF repository.

Full descriptions of all tests are available at:
https://docs.google.com/a/google.com/document/d/1HoCtiKjmp6j2d4d2U9QBJtehuVoANcWc6ggxthacPRY/edit?hl=en_US&authkey=CMaK1qsI
"""
# pylint: enable=c0301

__author__ = 'samking@google.com (Sam King)'

import utils
import urllib
import personfinder_pfif
import make_test_data
from StringIO import StringIO
import pfif_diff

class ClientTester():
  """Contains information about a repository API to run checks on the
  repository's client API.  All checks assume that the repository has been set
  up with a copy of the test data set."""

  def __init__(self, retrieve_person_url='', retrieve_note_url='',
               retrieve_persons_url='', retrieve_notes_url='', api_key='',
               version_str = '1.3', omitted_fields=(),
               first_person=make_test_data.FIRST_PERSON,
               last_person=make_test_data.LAST_PERSON,
               first_person_with_notes=make_test_data.FIRST_PERSON_WITH_NOTES,
               last_person_with_notes=make_test_data.LAST_PERSON_WITH_NOTES,
               first_note=make_test_data.FIRST_NOTE,
               last_note=make_test_data.LAST_NOTE_PLACEHOLDER,
               initialize_now=True):
    self.api_key = api_key
    self.version = personfinder_pfif.PFIF_VERSIONS[version_str]
    self.retrieve_person_url = retrieve_person_url
    self.retrieve_note_url = retrieve_note_url
    self.retrieve_persons_url = retrieve_persons_url
    self.retrieve_notes_url = retrieve_notes_url
    self.persons = []
    self.notes = {}

    if initialize_now:
      self.init_data(omitted_fields, first_person, last_person,
                     first_person_with_notes, last_person_with_notes,
                     first_note, last_note)

  def init_data(self, omitted_fields, first_person, last_person,
                first_person_with_notes, last_person_with_notes, first_note,
                last_note):
    """Generates test data."""
    self.persons = make_test_data.generate_persons(
        self.version, omitted_fields, first_person, last_person)
    self.notes = make_test_data.generate_notes(
        self.version, omitted_fields, first_person_with_notes,
        last_person_with_notes, first_note, last_note)


  def expand_url(self, url, person_record_id='', note_record_id='', skip=''):
    """Given a URL, replaces symbolic markup with the desired pieces of data.
    $k = API key
    $p = person record id
    $n = note record id
    $s = skip
    For example, when ClientTester has been initialized with key='hello',
    calling this function with the following arguments:
      url='example.org/api/person?key=$k&person=$p',
      person_record_id='example.com/person1'
    will return the following url:
      'example.org/api/person/key=hello&person=example.org%2Fperson1'
    Assumes that the key, url, and skip are properly URL encoded and that any
    record_id needs to be URL encoded."""
    encoded_person = urllib.quote_plus(person_record_id)
    encoded_note = urllib.quote_plus(note_record_id)
    output_url = url.replace('$k', self.api_key)
    output_url = output_url.replace('$p', encoded_person)
    output_url = output_url.replace('$n', encoded_note)
    output_url = output_url.replace('$s', skip)
    return output_url

  def run_diff(self, response, desired_persons, desired_notes):
    """Runs a pfif_diff between response and a PFIF XML document created from
    derised_persons and desired_notes."""
    desired_response = StringIO('')
    make_test_data.write_records(self.version, desired_response,
                                 desired_persons, desired_notes)
    messages = pfif_diff.pfif_file_diff(response, desired_response)
    return messages

  def check_retrieve_record(self, record, record_id_tag, desired_record_id,
                            url_template, person_list, note_map):
    """Checks the API for retrieving one record for tests 1.1/3.1 and 1.2/3.2.
    record: a person or note in the format used by make_test_data.write_records
    record_id_tag: if record is a person, 'person_record_id'.  If record is a
        note, 'note_record_id'
    desired_record_id: record should have this record_id
    url_template: a url template in the format used by expand_url that can
        retrieve a record using the API.
    person_list: a list of persons that should be in the response.  Since there
        is only one record, this should be [] if record is a note and [record]
        if record is a person.  In the format used by write_records.
    note_map: like person_list but for notes.  Should be either an empty map or
        a map from record's person_record_id to record."""
    assert record[record_id_tag] == desired_record_id
    url = self.expand_url( # pylint: disable=w0142
        url_template, **{record_id_tag : desired_record_id})
    response = utils.open_url(url)
    return self.run_diff(response, person_list, note_map)

  def check_retrieve_person_record(self):
    """Test 1.1/3.1.  Requesting person with id "example.org/p0001" should match
    the record from the test data set."""
    return self.check_retrieve_record(
        self.persons[0], 'person_record_id', 'example.org/p0001',
        self.retrieve_person_url, [self.persons[0]], {})

  def check_retrieve_note_record(self):
    """Test 1.2/3.2.  Requesting a note with id "example.org/n0101" should match
    the record from the test data set."""
    first_note = self.notes['example.org/p0001'][0]
    return self.check_retrieve_record(
        first_note, 'note_record_id', 'example.org/n0101',
        self.retrieve_note_url, [], {'example.org/p0001' : [first_note]})

  def compile_all_responses(self, template_url, is_person_feed):
    """Makes requests on the provided URL until no more responses come.
    Compiles all of these together into one PFIF document."""
    # Inspired by download_feed.py from Person Finder
    # TODO(samking): doesn't yet support min_date.  also, needs a parameter to
    # check if it's forward or reverse chronological so that it knows whether or
    # not to keep updating the min_date.
    skip = 0
    all_persons = []
    all_notes_arr = []
    persons = ['emulate do while loop!']
    notes_arr = []
    while len(persons) > 0 or len(notes_arr) > 0:
      # Get the response
      response = utils.open_url(self.expand_url(template_url, skip=str(skip)))
      persons, notes_arr = personfinder_pfif.parse_file(response)

      # Add the response to our list
      all_persons.extend(persons)
      all_notes_arr.extend(notes_arr)

      # Update skip so that we only get the responses we want next time
      if is_person_feed:
        skip += len(persons)
      else:
        skip += len(notes_arr)

    all_notes_map = utils.note_arr_to_map(all_notes_arr)

    # Turn all_persons and all_notes into a file
    all_responses_file = StringIO('')
    make_test_data.write_records(self.version, all_responses_file, all_persons,
                                 all_notes_map)
    return all_responses_file, all_persons, all_notes_map

  def check_retrieve_all_persons(self):
    """Test 1.3/3.3.  Requesting all persons should match all persons or all
    persons and all notes."""
    response, _, notes_response = (
        self.compile_all_responses(self.retrieve_persons_url, True))
    # It is acceptable for the response to include all persons or all persons
    # and all notes (see http://zesty.ca/pfif/1.3/#atom-person).  If the
    # response includes any notes, ensure that it has all persons and all notes.
    # If the response does not include any notes, only test it against persons.
    if notes_response:
      return self.run_diff(response, self.persons, self.notes)
    else:
      return self.run_diff(response, self.persons, {})

  # def check_retrieve_all_persons_since_time(self):

  # def check_retrieve_all_notes_from_person(self):

  # def check_retrieve_all_notes_since_time(self):

  # def check_retrieve_all_persons_and_notes(self):

  # def check_retrieve_all_changed_persons(self):

  def check_retrieve_all_notes(self):
    """Test not in the conformance doc.  Requesting all notes should match all
    notes."""
    response = self.compile_all_responses(self.retrieve_notes_url, False)[0]
    return self.run_diff(response, [], self.notes)
