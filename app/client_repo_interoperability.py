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
import optparse
from xml.parsers.expat import ExpatError
from urllib2 import HTTPError

# TODO(samking): something, somewhere is unsorted, and as a result, diff is
# outputting messages in an unintuitive order.  It doesn't impact correctness,
# but the output of messages should be in order of the id that is affected
# (where person id is different from note id)

class Check():
  """The check method, requirements for that method, and human readable output
  for that method."""

  def __init__(self, method, required_urls, name, test_number):
    self.method = method
    self.required_urls = required_urls
    self.name = name
    self.test_number = test_number

class HelpText(): # pylint: disable=w0232
  """Makes help text for Client Repo Interoperability Tests."""

  API_HELP_INFO = [('API Key', 'api_key',
                    'If an API key is needed, put it here'),
                   ('PFIF Version', 'version_str',
                    'Should be 1.1, 1.2, or 1.3'),
                   ('Ignore These Fields', 'omitted_fields',
                    'Space delimited list (ie, "source_date age photo_url")'),
                   ('Max Records to Post', 'max_records_to_post',
                    'When writing the test records to your database (using '
                    'the Write Records URL), we will only send this many '
                    'records at a time.'),
                   ('Write Records URL', 'write_records_url',
                    'A URL to POST a PFIF file to to add records to the repo'),
                   ('Retrieve Person URL', 'retrieve_person_url',
                    'The URL to retrieve one person by record id'),
                   ('Retrieve Note URL', 'retrieve_note_url',
                    'The URL to retrieve one note by record id'),
                   ('Retrieve Persons URL', 'retrieve_persons_url',
                    'The URL to retrieve all persons'),
                   # ('Retrieve Notes URL', 'retrieve_notes_url',
                   #  'The URL to retrieve all notes'),
                   ('Retrieve Persons After Date URL',
                    'retrieve_persons_after_date_url',
                    'The URL to retrieve all persons entered after a min_date'),
                   ('Retrieve Notes After Date URL',
                    'retrieve_notes_after_date_url',
                    'The URL to retrieve all notes entered after a min_date'),
                   ('Retrieve Notes from Person URL',
                    'retrieve_notes_from_person_url',
                    'The URL to retrieve all notes associated with a person '
                    '(specified by record id)'),
                   ('Retrieve Person with Notes URL',
                    'retrieve_persons_with_notes_url',
                    'The URL to retrieve all persons where notes associated '
                    'with these persons must be included')]

  DEBUG_HELP_INFO = [('First Person', 'first_person',
                      'The first test person to create.'),
                     ('Last Person', 'last_person',
                      'The last test person to create.'),
                     ('First Person With Notes', 'first_person_with_notes',
                      'The first test person to create that has notes.'),
                     ('Last Person With Notes', 'last_person_with_notes',
                      'The last test person to create that has notes.'),
                     ('First Note', 'first_note',
                      'The first test note to create.'),
                     ('Last Note', 'last_note',
                      'The last test note to create.')]

  URL_SUBSTITUTIONS = [
      ('$k$', 'API key', 'The key, if needed, should be used on every URL'),
      ('$p$', 'person_record_id', 'A person_record_id should be used on every '
       'URL that needs to specify a person'),
      ('$n$', 'note_record_id', 'A note_record_id should be used on every URL '
       'that needs to specify a note'),
      ('$gs$', 'global skip', 'This should be used if multiple repeated '
       'queries are needed to get a large set of records.'),
      ('$gm$', 'global min_date', 'This should be used for all URLs that need '
       'to specify a date.'),
      ('$cs$', 'current skip', 'See note.'),
      ('$cm$', 'current min_date', 'See note.')]

  GLOBAL_CURRENT_HELP = [
      """Global and Current skip and min_date probably shouldn't be used with
each other. There are two algorithms implemented to retrieve records since a
given date.""",
      """Put in the (global) min_date for the first query and keep it the same
for all successive queries, monotonically increasing the (global) skip.  This
strategy should work as long as the API implements a skip and min_date feature,
but it might be less efficient if your repository implements skip by generating
all results and excluding skipped results from the output.""",
      """Put in (current) min_date for the first query.  For each successive
query, update the (current) min_date to the most recent record.  The (current)
skip is equal to the number of received records that have the same min_date as
the most recent record (this should always be 1 unless two records have the same
entry_date, which violates the PFIF spec), which can be more efficient.  This
strategy requires all URLs that use current_min_date to return results forward
chronologically rather than reverse chronologically (the norm for ATOM
feeds)."""]

  # pylint: disable=c0301
  GLOBAL_CURRENT_EXAMPLE_TEXT = (
      """For example, with Person Finder's API
(http://code.google.com/p/googlepersonfinder/wiki/DataAPI), we could use
https://subdomain.googlepersonfinder.appspot.com/feeds/person?key=$k$&skip=$cs$&min_entry_date=$cm$
for the Retrieve Persons After Date URL or
https://subdomain.googlepersonfinder.appspot.com/feeds/notes?key=$k$&skip=$gs$&person_record_id=$p$
for the Retrieve Notes from Person URL.""")

  GLOBAL_CURRENT_EXAMPLE_HTML = (
      """For example, with
<a href="http://code.google.com/p/googlepersonfinder/wiki/DataAPI">Person
Finder's API</a>, we could use
<pre>https://subdomain.googlepersonfinder.appspot.com/feeds/person?key=$k$&amp;skip=$cs$&amp;min_entry_date=$cm$</pre>
for the Retrieve Persons After Date URL or
<pre>https://subdomain.googlepersonfinder.appspot.com/feeds/notes?key=$k$&amp;skip=$gs$&amp;person_record_id=$p$</pre>
for the Retrieve Notes from Person URL.""")
  # pylint: enable=c0301

  TEST_INTRO = (
      """Each URL provided will be used, primarily, for one test.  None of these
tests should have any side effects on your database, except for the test of
changing records (which should be the only test that uses the API url to write
records).  The write URL will also be used to add test data to the repository
before running any test.  Thus, before running these tests, you should create a
new repository with no records in it.  All URLs should follow the templating
guidelines described here.  You can use the debug values to create a smaller
test set, but if you do so, you will NOT be fully testing your conformance.""")

  @staticmethod
  def make_intro_text(is_html):
    """Describes the tests."""
    output = utils.MessagesOutput(is_html=is_html, html_class='intro')
    output.make_message_part_division(HelpText.TEST_INTRO, 'intro_text')
    output.make_new_line()
    return output.get_output()

  @staticmethod
  def make_url_template_help(is_html):
    """Generates a help text string for URL template expansion rules."""
    output = utils.MessagesOutput(is_html=is_html,
                                  html_class='url_substitution_help')
    output.start_table(['Symbol to Substitute', 'Element Substituted', 'Help'])
    for substitution_info in HelpText.URL_SUBSTITUTIONS:
      output.make_table_row(substitution_info)
    output.end_table()
    return output.get_output()

  @staticmethod
  def make_tabular_form(is_html, html_class, headers, help_data):
    """Generates help text over the provided help_data.
    is_html: True if you want a form.  If so, you must already have an opening
      form tag.
    html_class: the html_class to be provided to utils.MessagesOutput
    headers: the table headers, provided to MessagesOutput.start_table
    help_data: An iterable of 3-tuples where each tuple should have Name, Form,
      Help Text."""
    output = utils.MessagesOutput(is_html=is_html, html_class=html_class)
    output.start_table(headers)
    for name, form, help_text in help_data:
      if is_html:
        form = '<input type="text" name="' + form + '">'
      output.make_table_row([name, form, help_text])
    output.end_table()
    return output.get_output()


  @staticmethod
  def make_api_help(is_html):
    """Generates a help text string for API URLs.  If is_html, also generates
    form elements (which require a form to already have been started)."""
    return HelpText.make_tabular_form(is_html=is_html, html_class='api_help',
                                      headers=('Name', 'Field', 'Help'),
                                      help_data=HelpText.API_HELP_INFO)

  @staticmethod
  def make_debug_help(is_html):
    """Generates a help text string for debug parameters.  If is_html, also
    generates form elements."""
    return HelpText.make_tabular_form(is_html=is_html, html_class='debug_help',
                                      headers=('Debug Value', 'Field', 'Help'),
                                      help_data=HelpText.DEBUG_HELP_INFO)

  @staticmethod
  def make_global_current_help(is_html):
    """Generates a help text string for the difference between global and
    current min_date and skip."""
    output = utils.MessagesOutput(is_html=is_html,
                                  html_class='global_current_help')
    for text in HelpText.GLOBAL_CURRENT_HELP:
      output.make_message_part_division(text, 'global_current_help_text')
    if is_html:
      output.make_message_part_division(HelpText.GLOBAL_CURRENT_EXAMPLE_HTML,
                                        'global_current_help_text',
                                        escape=False)
    else:
      output.make_message_part_division(HelpText.GLOBAL_CURRENT_EXAMPLE_TEXT,
                                        'global_current_help_text')
    return output.get_output()

class ClientTester(): # pylint: disable=r0902
  """Contains information about a repository API to run checks on the
  repository's client API.  All checks assume that the repository has been set
  up with a copy of the test data set."""

  class ApiLoopError(Exception):
    """An exception that will be raised when the API loops too many times."""
    pass

  # If we have to send more than this many API calls to complete a request, the
  # API is probably bugged.  The test data set contains 1357 persons and 4950
  # notes, which is 6307 records.  MAX_API_CALLS at 130 should be okay even if
  # the API only returns 50 records at a time.
  MAX_API_CALLS = 130

  def __init__(self, retrieve_person_url='', #pylint: disable=r0914
               retrieve_note_url='', retrieve_persons_url='',
               retrieve_notes_url='', retrieve_persons_after_date_url='',
               retrieve_notes_after_date_url='',
               retrieve_notes_from_person_url='',
               retrieve_persons_with_notes_url='', write_records_url='',
               api_key='', version_str='1.3', omitted_fields=(),
               max_records_to_post='50',
               first_person=make_test_data.FIRST_PERSON,
               last_person=make_test_data.LAST_PERSON,
               first_person_with_notes=make_test_data.FIRST_PERSON_WITH_NOTES,
               last_person_with_notes=make_test_data.LAST_PERSON_WITH_NOTES,
               first_note=make_test_data.FIRST_NOTE,
               last_note=make_test_data.LAST_NOTE_PLACEHOLDER,
               initialize_now=True):
    self.api_key = api_key
    self.version = personfinder_pfif.PFIF_VERSIONS[version_str]
    self.max_records_to_post = int(max_records_to_post)
    self.retrieve_person_url = retrieve_person_url
    self.retrieve_note_url = retrieve_note_url
    self.retrieve_persons_url = retrieve_persons_url
    self.retrieve_notes_url = retrieve_notes_url
    self.retrieve_persons_after_date_url = retrieve_persons_after_date_url
    self.retrieve_notes_after_date_url = retrieve_notes_after_date_url
    self.retrieve_notes_from_person_url = retrieve_notes_from_person_url
    self.retrieve_persons_with_notes_url = retrieve_persons_with_notes_url
    self.write_records_url = write_records_url
    self.persons = []
    self.notes = {}
    self.checks = []

    self.init_checks()

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

  @staticmethod
  def method_to_check_name(method):
    """Turns a method into the name of the check that uses that method."""
    full_name = method.__name__
    words = full_name.split('_')
    check_removed = words[1:]
    capitalized_words = [word.title() for word in check_removed]
    return ' '.join(capitalized_words)

  def init_checks(self):
    """Generates a list of checks as an instance variable so that it is possible
    to automatically run all check methods."""
    checks_tuple = (
        (self.check_retrieve_person_record, '1.1/3.1',
         (self.retrieve_person_url, )),
        (self.check_retrieve_note_record, '1.2/3.2',
         (self.retrieve_note_url, )),
        (self.check_retrieve_all_persons, '1.3/3.3',
         (self.retrieve_persons_url, )),
        (self.check_retrieve_all_persons_since_time, '1.4/3.4',
         (self.retrieve_persons_after_date_url, self.retrieve_person_url)),
        (self.check_retrieve_all_notes_from_person, '1.5/3.5',
         (self.retrieve_notes_from_person_url, )),
        (self.check_retrieve_all_notes_since_time, '1.6/3.6',
         (self.retrieve_notes_after_date_url, self.retrieve_note_url)),
        (self.check_retrieve_all_persons_with_notes, '1.7/3.7',
         (self.retrieve_persons_with_notes_url, )),
        (self.check_retrieve_all_changed_persons, '3.8',
         (self.write_records_url, self.retrieve_persons_after_date_url,
          self.retrieve_person_url)))
    # TODO(samking): currently, check_retrieve_all_notes is not here because it
    # is not in the test conformance doc.  If there is a desire to test that
    # functionality, adding it to the checks_tuple would cause the test to be
    # run.
    for method, test_number, required_urls in checks_tuple:
      name = self.method_to_check_name(method)
      check = Check(method, required_urls, name, test_number)
      self.checks.append(check)

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
    There is a more detailed description of all of these parameters in HelpText,
      which explains this information to the user.
    Assumes that the key, url, and skip are properly URL encoded and that any
      record_id or date needs to be URL encoded."""
    encoded_person = urllib.quote_plus(person_record_id)
    encoded_note = urllib.quote_plus(note_record_id)
    encoded_global_min_date = urllib.quote_plus(global_min_date)
    encoded_current_min_date = urllib.quote_plus(current_min_date)
    output_url = url.replace('$k$', self.api_key)
    output_url = output_url.replace('$p$', encoded_person)
    output_url = output_url.replace('$n$', encoded_note)
    output_url = output_url.replace('$gs$', global_skip)
    output_url = output_url.replace('$gm$', encoded_global_min_date)
    output_url = output_url.replace('$cs$', current_skip)
    output_url = output_url.replace('$cm$', encoded_current_min_date)
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
    opened_url = utils.open_url(url)
    return StringIO(opened_url.read())

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
    num_api_calls = 0
    # TODO(samking): Right now, this can loop for a long time if the API is
    # broken and keeps returning the same records.  We should make sure that any
    # records returned are new records.
    while (is_person_feed and len(persons) > 0) or (
        not is_person_feed and len(notes_arr) > 0):
      # Get the response
      response = utils.open_url(self.expand_url(
          template_url, person_record_id=person_record_id,
          global_min_date=min_date, current_min_date=current_min_date,
          global_skip=str(global_skip), current_skip=str(current_skip)))
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
      if num_api_calls == self.MAX_API_CALLS:
        raise self.ApiLoopError()
      num_api_calls += 1

    all_notes_map = utils.note_arr_to_map(all_notes_arr)

    # Turn all_persons and all_notes into a file
    all_responses_file = StringIO('')
    make_test_data.write_records(self.version, all_responses_file, all_persons,
                                 all_notes_map, embed_notes_in_persons=False)
    return all_responses_file, all_persons, all_notes_map

  def truncate_records(self, persons, notes):
    """Returns person_batch, remaining_persons, note_batch, remaining_notes.
    person_batch and remaining_persons, when added together, will be the same as
    persons (the same is true for notes).  There will be at most
    max_records_to_post records between person_batch and note_batch.  Even when
    records remain, there is not guaranteed to be exactly max_records_to_post in
    a batch."""
    if persons:
      batch_persons = persons[:self.max_records_to_post]
      remaining_persons = persons[self.max_records_to_post:]
      return batch_persons, remaining_persons, {}, notes
    if notes:
      new_notes = notes.copy()
      person_record_id, person_notes = new_notes.items()[0]
      batch_notes_arr = person_notes[:self.max_records_to_post]
      remaining_notes_in_arr = person_notes[self.max_records_to_post:]
      if remaining_notes_in_arr:
        new_notes[person_record_id] = remaining_notes_in_arr
      else:
        del new_notes[person_record_id]
      batch_notes_map = {person_record_id : batch_notes_arr}
      return [], [], batch_notes_map, new_notes
    return [], [], {}, {}

  def api_write_records(self, persons, notes):
    """Calls the API to write records to the remote database."""
    url = self.expand_url(self.write_records_url)

    person_batch, remaining_persons, note_batch, remaining_notes = (
        self.truncate_records(persons, notes))
    while person_batch or note_batch:
      pfif_to_write = StringIO('')
      make_test_data.write_records(self.version, pfif_to_write, person_batch,
                                   note_batch, embed_notes_in_persons=False)
      # TODO(samking): if we cared, we could verify stuff about the response and
      # return true if it indicates success and false otherwise.
      utils.post_xml_to_url(url, pfif_to_write.getvalue())
      person_batch, remaining_persons, note_batch, remaining_notes = (
          self.truncate_records(remaining_persons, remaining_notes))

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

  def check_retrieve_all_records_after_record(self, is_person, record_id,
                                              correct_persons, correct_notes):
    """Retrieves all records entered after record_id.  Will retrieve person
    records if is_person or note records if not is_person.  correct_persons and
    correct_notes are all records that should have been entered after
    record_id."""
    # Get the time that we must be after
    min_date = self.get_field_from_record(
        is_person=is_person, record_id=record_id, field='entry_date')
    if min_date is None:
      failure_message = utils.Message(
          'Could not run a time dependent test.  Could not calibrate '
          'min_entry_date for test due to a missing record.',
          xml_tag='entry_date')
      if is_person:
        failure_message.person_record_id = record_id
      else:
        failure_message.note_record_id = record_id
      return [failure_message]

    # Get the list of records after min_date
    if is_person:
      template_url = self.retrieve_persons_after_date_url
    else:
      template_url = self.retrieve_notes_after_date_url
    response = self.compile_all_responses(template_url=template_url,
                                          is_person_feed=is_person,
                                          min_date=min_date)[0]

    # Diff it
    return self.run_diff(response, correct_persons, correct_notes)

  def check_retrieve_all_persons_since_time(self):
    """Test 1.4/3.4.  Requesting all persons since a given time should return
    only those records."""
    last_excluded_person = 'example.org/p0621'
    recent_persons = make_test_data.get_persons_after_record(
        self.persons, self.notes, last_excluded_person)[0]
    # It would be acceptable to have notes associated with any returned persons,
    # but there should be no notes for any persons after 99, so we provide no
    # notes.
    return self.check_retrieve_all_records_after_record(
        is_person=True, record_id=last_excluded_person,
        correct_persons=recent_persons, correct_notes={})

  def check_retrieve_all_notes_since_time(self):
    """Test 1.6/3.6.  Requesting all notes since a given time should return
    only those records."""
    last_excluded_note = 'example.org/n5016'
    recent_notes = make_test_data.get_notes_after_record(
        self.notes, last_excluded_note)
    return self.check_retrieve_all_records_after_record(
        is_person=False, record_id=last_excluded_note, correct_persons=[],
        correct_notes=recent_notes)

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

  def check_retrieve_all_persons_with_notes(self):
    """Test 1.7/3.7.  Retrieve all persons.  These persons must have their
    associated notes."""
    response = self.compile_all_responses(self.retrieve_persons_with_notes_url,
                                          True)[0]
    return self.run_diff(response, self.persons, self.notes)

  def check_retrieve_all_changed_persons(self):
    """Test 3.8.  It should be possible to change a record, which causes its
    entry_date to be higher than the previous entry_date."""
    # Modify the first record to get a baseline time.  No records should be more
    # recent than the just-modified record.
    first_modified_record = 'example.org/p0001'
    assert self.persons[0]['person_record_id'] == first_modified_record
    self.api_write_records([self.persons[0]], {})
    messages = self.check_retrieve_all_records_after_record(
        is_person=True, record_id=first_modified_record, correct_persons=[],
        correct_notes={})

    # Modify the second record.  This should be the only record more recent than
    # the first modified record.
    second_modified_record = 'example.org/p0002'
    assert self.persons[1]['person_record_id'] == second_modified_record
    self.api_write_records([self.persons[1]], {})
    messages.extend(self.check_retrieve_all_records_after_record(
        is_person=True, record_id=first_modified_record,
        correct_persons=[self.persons[1]], correct_notes={}))

    return messages

  def run_all_checks(self, is_html):
    """Runs all check methods that don't take any arguments.  Will pass any
    messages from each test to messages_to_str_by_id.  Will pass messages
    created because of tests being unable to run to messages_to_str.  Returns
    the string generated from running those methods."""
    tests_not_run = []
    check_strings = []
    for check in self.checks:
      can_run_test = True
      for url in check.required_urls:
        if not url:
          can_run_test = False
          tests_not_run.append(utils.Message(
              'One of the tests did not run because it was missing a required '
              'URL.', extra_data='Test Name: ' + check.name))
      if can_run_test:
        messages = []
        try:
          messages = check.method()
          title = check.name + '(Test ' + check.test_number + ')'
        # The diff tool will error out when one of the files is not PFIF XML
        # (ie, it's a 404 or an HTML error page.  Since this is not an
        # acceptable result of any test, outputting a failure message works.  It
        # might be better to make the XML parser used in PfifXmlTree or the
        # objectification of PFIF XML more robust, though.
        except ExpatError:
          tests_not_run.append(utils.Message(
              'Error when parsing XML generated by your API on this request.',
              extra_data='Test Name: ' + check.name))
        # Some possible causes of this issue: the auth key wasn't provided,
        # something was too big, or the URL is bad.
        except HTTPError:
          tests_not_run.append(utils.Message(
              'HTTP Error when trying to access one of your URLs.',
              extra_data='Test Name: ' + check.name))
        except self.ApiLoopError:
          tests_not_run.append(utils.Message(
              'One of your tests took too many loops of API calls to complete.',
              extra_data='Test Name: ' + check.name))
        if messages:
          check_strings.append(
              utils.MessagesOutput.messages_to_str_by_id(
                  messages=messages, title=title, is_html=is_html))
    check_strings.append(
        utils.MessagesOutput.messages_to_str(
            messages=tests_not_run, title='Some Tests Could Not Run',
            is_html=is_html))
    return ''.join(check_strings)

def add_api_test_fields(parser):
  """Adds required API test fields to the command line options."""
  group = optparse.OptionGroup( parser, 'Required API Test Fields')
  group.add_option('--retrieve-person-url', default='')
  group.add_option('--retrieve-note-url', default='')
  group.add_option('--retrieve-persons-url', default='')
  group.add_option('--retrieve-notes-url', default='')
  group.add_option('--retrieve-persons-after-date-url', default='')
  group.add_option('--retrieve-notes-after-date-url', default='')
  group.add_option('--retrieve-notes-from-person-url', default='')
  group.add_option('--retrieve-persons-with-notes-url', default='')
  group.add_option('--write-records-url', default='')
  group.add_option('--api-key', default='')
  parser.add_option_group(group)

def main():
  """Runs client repo interoperability tests."""
  help_text = ('You must provide every argument specified in Required API Test'
               'Fields.  Everything else is optional.')
  parser = optparse.OptionParser(usage=help_text)
  parser.add_option('--verbose-help', action='store_true', default=False,
                    help='Show the full description of required API Test '
                    'Fields')
  add_api_test_fields(parser)
  make_test_data.add_version_and_omit_field(parser)
  make_test_data.add_debug_options(parser)

  options = parser.parse_args()[0]
  if options.verbose_help:
    print (HelpText.make_intro_text(False) +
           HelpText.make_url_template_help(False) +
           HelpText.make_api_help(False) +
           HelpText.make_global_current_help(False))
  else:
    client_tester_options = vars(options)
    del client_tester_options['verbose_help']
    del client_tester_options['embed_notes_in_persons']
    tester = ClientTester(**client_tester_options) # pylint: disable=w0142
    print tester.run_all_checks(False)

if __name__ == '__main__':
  main()
