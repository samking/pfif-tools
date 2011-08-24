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

# TODO(samking): something, somewhere is unsorted, and as a result, diff is
# outputting messages in an unintuitive order.  It doesn't impact correctness,
# but the output of messages should be in order of the id that is affected
# (where person id is different from note id)

class ClientTester(): # pylint: disable=r0902
  """Contains information about a repository API to run checks on the
  repository's client API.  All checks assume that the repository has been set
  up with a copy of the test data set."""

  def __init__(self, retrieve_person_url='', #pylint: disable=r0914
               retrieve_note_url='', retrieve_persons_url='',
               retrieve_notes_url='', retrieve_persons_after_date_url='',
               retrieve_notes_after_date_url='',
               retrieve_notes_from_person_url='', api_key='', version_str =
               '1.3', omitted_fields=(),
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
    self.retrieve_persons_after_date_url = retrieve_persons_after_date_url
    self.retrieve_notes_after_date_url = retrieve_notes_after_date_url
    self.retrieve_notes_from_person_url = retrieve_notes_from_person_url
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


  def expand_url(self, url, person_record_id='', note_record_id='',
                 global_skip='', global_min_date='', current_skip='',
                 current_min_date=''):
    """Given a URL, replaces symbolic markup with the desired pieces of data.
      $k$ = API key
      $p$ = person_record_id
      $n$ = note_record_id
      $gs$ = global skip
      $gm$ = global min_date
      $cs$ = current skip
      $cm$ = current min_date
    For example, when ClientTester has been initialized with key='hello',
      calling this function with the following arguments:
        url='example.org/api/person?key=$k&person=$p',
        person_record_id='example.com/person1'
      will return the following url:
        'example.org/api/person/key=hello&person=example.org%2Fperson1'
    Assumes that the key, url, and skip are properly URL encoded and that any
      record_id needs to be URL encoded.
    Global versus Current skip and min_date:
      If I want to get all records, I will use only the global skip.  To do
      this, I will keep making requests to the URL.  If I get back 10 records, I
      will increment global_skip by 10.  global_skip will monotonically increase
      until the very end.  I can use this same algorithm for getting all records
      since a date by just adding in a global_min_date.
      However, another way to get all records since a date is to request records
      since a date, set the current min date to the most recent record that I
      have (ie, this algorithm only works if your API returns records forword
      chronologically when min_date is set, and the min_date will increase
      monotonically until we get all records), set the current skip to the
      number of records with that same date (ie, current_skip will normally be 1
      unless several records were created at the same instant), and repeat the
      request.
      You can see a description of the second algorithm described in
      http://code.google.com/p/googlepersonfinder/wiki/DataAPI and you can see
      both algorithms implemented in compile_all_responses.  The first algorithm
      (global) should always work. The second algorithm (current) is better to
      use if your repository database will still generate skipped data and,
      thus, you have a reason to keep skip small."""
    encoded_person = urllib.quote_plus(person_record_id)
    encoded_note = urllib.quote_plus(note_record_id)
    output_url = url.replace('$k$', self.api_key)
    output_url = output_url.replace('$p$', encoded_person)
    output_url = output_url.replace('$n$', encoded_note)
    output_url = output_url.replace('$gs$', global_skip)
    output_url = output_url.replace('$gm$', global_min_date)
    output_url = output_url.replace('$cs$', current_skip)
    output_url = output_url.replace('$cm$', current_min_date)
    return output_url

  def run_diff(self, response, desired_persons, desired_notes):
    """Runs a pfif_diff between response and a PFIF XML document created from
    derised_persons and desired_notes."""
    desired_response = StringIO('')
    make_test_data.write_records(self.version, desired_response,
                                 desired_persons, desired_notes,
                                 embed_notes_in_persons=False)
    messages = pfif_diff.pfif_file_diff(response, desired_response)
    return messages

  def run_diff_optional_notes(self, response, desired_persons, desired_notes,
                              response_notes=None, try_both=False):
    """It is acceptable for the response to include all persons or all persons
    and all notes (see http://zesty.ca/pfif/1.3/#atom-person).  If the response
    includes any notes, ensure that it has all persons and all notes.  If the
    response does not include any notes, only test it against persons.  If
    try_both is True, ignores response_notes and tries both."""
    if try_both or response_notes:
      include_notes = self.run_diff(response, desired_persons, desired_notes)
    if try_both or not response_notes:
      exclude_notes = self.run_diff(response, desired_persons, {})

    if try_both:
      if len(include_notes) < len(exclude_notes):
        return include_notes
      return exclude_notes
    else:
      if response_notes:
        return include_notes
      return exclude_notes

  def retrieve_record(self, url_template, record_id_tag, desired_record_id):
    """Returns the response from the API when making a request at url_template
    for the specified record_id.  See check_retrieve_record for parameter
    descriptions."""
    url = self.expand_url( # pylint: disable=w0142
        url_template, **{record_id_tag : desired_record_id})
    return utils.open_url(url)

  def get_field_from_record(self, is_person, record_id, field):
    """Makes an API call to retrieve a record identified by record_id.  Returns
    field from that record.  If that record or field is not present, returns
    None."""
    if is_person:
      record_id_tag = 'person_record_id'
      template_url = self.retrieve_person_url
    else:
      record_id_tag = 'note_record_id'
      template_url = self.retrieve_note_url
    record_file = self.retrieve_record(template_url, record_id_tag, record_id)
    record_obj = pfif_diff.objectify_pfif_xml(record_file)
    record = record_obj.get(pfif_diff.record_id_to_key(record_id, is_person),
                            {})
    return record.get(field, None)

  def compile_all_responses(self, # pylint: disable=r0914
                            template_url, is_person_feed, min_date='',
                            person_record_id=''):
    """Makes requests on the provided URL until no more responses come.
    Compiles all of these together into one PFIF document.  If min_date is
    specified, then the template_url will be expanded with that min_date."""
    # Inspired by download_feed.py from Person Finder
    global_skip = 0
    current_skip = 0
    current_min_date = min_date
    all_persons = []
    all_notes_arr = []
    persons = ['emulate do while loop!']
    notes_arr = ['emulate do while loop!']
    while (is_person_feed and len(persons) > 0) or (
        not is_person_feed and len(notes_arr) > 0):
      # Get the response
      response = utils.open_url(self.expand_url(
          template_url, global_min_date=min_date,
          current_min_date=current_min_date, global_skip=str(global_skip),
          current_skip=str(current_skip)))
      persons, notes_arr = personfinder_pfif.parse_file(response)

      # Add the response to our list
      all_persons.extend(persons)
      all_notes_arr.extend(notes_arr)

      # Update skip and current_min_date so that we only get the responses we
      # want next time.  "Global" means that the min date stays the same and the
      # skip keeps increasing.  "Current" means that the min date keeps going up
      # and the skip will only be something other than 1 if several records have
      # the same min date as the most recent record retrieved.  "Current" also
      # requires the API to return results forward chronologically.
      if is_person_feed:
        if len(persons) > 0:
          global_skip += len(persons)
          current_min_date = max(person['entry_date'] for person in persons)
          current_skip = len([person for person in persons if
                              person['entry_date'] == current_min_date])
      else:
        if len(notes_arr) > 0:
          global_skip += len(notes_arr)
          current_min_date = max(note['entry_date'] for note in notes_arr)
          current_skip = len([note for note in notes_arr if note['entry_date']
                              == current_min_date])

    all_notes_map = utils.note_arr_to_map(all_notes_arr)

    # Turn all_persons and all_notes into a file
    all_responses_file = StringIO('')
    make_test_data.write_records(self.version, all_responses_file, all_persons,
                                 all_notes_map, embed_notes_in_persons=False)
    return all_responses_file, all_persons, all_notes_map

  # checks from the test conformance doc

  def check_retrieve_record(self, record, record_id_tag, desired_record_id,
                            url_template, person_list, note_map,
                            notes_are_optional=False):
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
        a map from record's person_record_id to record.
    notes_are_optional: if True, uses run_diff_optional_notes."""
    assert record[record_id_tag] == desired_record_id
    response = self.retrieve_record(url_template, record_id_tag,
                                    desired_record_id)
    if notes_are_optional:
      return self.run_diff_optional_notes(response, person_list, note_map,
                                          try_both=True)
    else:
      return self.run_diff(response, person_list, note_map)

  def check_retrieve_person_record(self):
    """Test 1.1/3.1.  Requesting person with id "example.org/p0001" should match
    the record from the test data set."""
    first_person = self.persons[0]
    first_person_id = 'example.org/p0001'
    first_note_map = {first_person_id : self.notes.get(first_person_id, [])}
    return self.check_retrieve_record(
        first_person, 'person_record_id', first_person_id,
        self.retrieve_person_url, [first_person], first_note_map,
        notes_are_optional=True)

  def check_retrieve_note_record(self):
    """Test 1.2/3.2.  Requesting a note with id "example.org/n0101" should match
    the record from the test data set."""
    first_note = self.notes['example.org/p0001'][0]
    return self.check_retrieve_record(
        first_note, 'note_record_id', 'example.org/n0101',
        self.retrieve_note_url, [], {'example.org/p0001' : [first_note]})

  def check_retrieve_all_persons(self):
    """Test 1.3/3.3.  Requesting all persons should match all persons or all
    persons and all notes."""
    response, _, response_notes = self.compile_all_responses(
        self.retrieve_persons_url, True)
    return self.run_diff_optional_notes(response, self.persons, self.notes,
                                        response_notes=response_notes)

  def check_retrieve_all_notes(self):
    """Test not in the conformance doc.  Requesting all notes should match all
    notes."""
    response = self.compile_all_responses(self.retrieve_notes_url, False)[0]
    return self.run_diff(response, [], self.notes)

  def check_retrieve_all_persons_since_time(self):
    """Test 1.4/3.4.  Requesting all persons since a given time should return
    only those records."""
    min_date = self.get_field_from_record(
        is_person=True, record_id='example.org/p0621', field='entry_date')
    if min_date is None:
      return [utils.Message(
          'Could not run retrieve_all_persons_since_time test.  Could not '
          'calibrate min_entry_date for test due to a missing record.',
          xml_tag='entry_date', person_record_id='example.org/p0621')]
    response = self.compile_all_responses(
        template_url=self.retrieve_persons_after_date_url, is_person_feed=True,
        min_date=min_date)[0]
    recent_persons = make_test_data.get_persons_after_record(
        self.persons, self.notes, 'example.org/p0621')[0]
    # It would be acceptable to have notes associated with any returned persons,
    # but there should be no notes for any persons after 99
    return self.run_diff(response, recent_persons, {})

  def check_retrieve_all_notes_since_time(self):
    """Test 1.6/3.6.  Requesting all notes since a given time should return
    only those records."""
    min_date = self.get_field_from_record(
        is_person=False, record_id='example.org/n5016', field='entry_date')
    if min_date is None:
      return [utils.Message(
          'Could not run retrieve_all_notes_since_time test.  Could not '
          'calibrate min_entry_date for test due to a missing record.',
          xml_tag='entry_date', person_record_id='example.org/n5016')]
    response = self.compile_all_responses(
        template_url=self.retrieve_notes_after_date_url, is_person_feed=False,
        min_date=min_date)[0]
    recent_notes = make_test_data.get_notes_after_record(
        self.notes, 'example.org/n5016')
    return self.run_diff(response, [], recent_notes)

  def check_retrieve_all_notes_from_person(self):
    """Test 1.5/3.5.  Requesting all notes associated with a person should
    return only those records."""
    person_with_notes = 'example.org/p0099'
    response = self.compile_all_responses(
        template_url=self.retrieve_notes_from_person_url,
        is_person_feed=False, person_record_id=person_with_notes)[0]
    notes_from_person = {person_with_notes :
                         self.notes.get(person_with_notes, [])}
    return self.run_diff(response, [], notes_from_person)

  # TODO(samking): this is test 1.7/3.7, but I'm not sure what the point is.
  # def check_retrieve_all_persons_and_notes(self):

  # def check_retrieve_all_changed_persons(self):
