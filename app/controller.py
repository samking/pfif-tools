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

"""Provides a web interface for pfif_tools."""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from StringIO import StringIO
import pfif_validator
import pfif_diff
import utils

class PfifController(webapp.RequestHandler):
  """Provides common functionality to the different PFIF Tools controllers."""

  # TODO(samking): maybe use Django?
  def write_header(self, title):
    """Writes an HTML page header and open the body."""
    self.response.out.write("""<!DOCTYPE HTML>
  <html>
    <head>
      <meta charset="utf-8">
      <title>""" + title + """</title>
      <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>
    <body>""")

  def write_footer(self):
    """Closes the body and html tags."""
    self.response.out.write('</body></html>')

  def write_missing_input_file(self):
    """Writes that there is a missing input file."""
    self.response.out.write('<h1>Missing Input File</h1>')

  def get_file(self, file_number=1, return_filename=False):
    """Gets a file that was pasted in, uploaded, or given by a URL.  If multiple
    files are provided, specify the number of the desired file as file_number.
    Returns None if there is no file.  If return_filename is True, returns a
    tuple: (desired_file, filename)."""
    paste_name = 'pfif_xml_' + str(file_number)
    upload_name = 'pfif_xml_file_' + str(file_number)
    url_name = 'pfif_xml_url_' + str(file_number)
    desired_file = None
    filename = None

    for file_location in [paste_name, upload_name]:
      if self.request.get(file_location):
        desired_file = StringIO(self.request.get(file_location))
        if file_location is upload_name:
          filename = self.request.POST[file_location].filename
    if self.request.get(url_name):
      url = self.request.get(url_name)
      # make a file-like object out of the URL's xml so we can seek on it
      desired_file = StringIO(utils.open_url(url).read())
      filename = url

    if desired_file is not None:
      if return_filename and filename is not None:
        return (desired_file, filename)
      elif return_filename:
        return (desired_file, None)
      else:
        return desired_file
    else:
      if return_filename:
        return (None, None)
      else:
        return None

  def write_filename(self, filename, shorthand_name):
    """Writes out a mapping from shorthand_name to filename."""
    self.response.out.write('<p>File ' + shorthand_name + ': ')
    if filename is None:
      self.response.out.write('pasted in')
    else:
      self.response.out.write(filename)
    self.response.out.write('</p>\n')

  def write_filenames(self, filename_1, filename_2):
    """Writes the names of filename_1 and filename_2."""
    self.write_filename(filename_1, 'A')
    self.write_filename(filename_2, 'B')

class Diff(PfifController):
  """Displays the diff results page."""

  def post(self):
    file_1, filename_1 = self.get_file(1, return_filename=True)
    file_2, filename_2 = self.get_file(2, return_filename=True)
    self.write_header('PFIF Diff: Results')
    if file_1 is None or file_2 is None:
      self.write_missing_input_file()
    else:
      options = self.request.get_all('options')
      ignore_fields = self.request.get('ignore_fields').split()
      messages = pfif_diff.pfif_file_diff(
          file_1, file_2,
          text_is_case_sensitive='text_is_case_sensitive' in options,
          ignore_fields=ignore_fields,
          omit_blank_fields='omit_blank_fields' in options)
      self.response.out.write(
          '<h1>Diff: ' + str(len(messages)) + ' Messages</h1>')
      self.response.out.write(
          utils.MessagesOutput.generate_message_summary(messages, is_html=True))
      self.write_filenames(filename_1, filename_2)
      if 'group_messages_by_record' in options:
        self.response.out.write(
            utils.MessagesOutput.messages_to_str_by_id(messages, is_html=True))
      else:
        self.response.out.write(
            utils.MessagesOutput.messages_to_str(
                messages, show_error_type=False, is_html=True))
    self.write_footer()

class ClientInput(PfifController):
  """Displays the input page for the client repo interoperability tests."""

  CLIENT_INPUT = [('API Key', 'api_key',
                   'If an API key is needed, put it here'),
                  ('PFIF Version', 'version_str',
                   'Should be 1.1, 1.2, or 1.3'),
                  ('Ignore These Fields', 'omitted_fields',
                   'Space delimited list (ie, "source_date age photo_url")'),
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
                   'retrieve_person_with_notes_url',
                   'The URL to retrieve all persons where notes associated '
                   'with these persons must be included')]

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
      ('$cs$', 'current skip', 'See note at bottom.'),
      ('$cm$', 'current min_date', 'See note at bottom.')]

  TITLE = 'Test Client-Repo API Interoperability'

  CLIENT_HEADER = '<h1>' + TITLE + """</h1>
      <div>The Write URL is used to set up your repository with the test data
      set.  There will be records written to it, so you should create a new
      repository.  All other URLs will be tested and should not modify the
      repository.</div>
      <div>The following strings in your URLs will be substituted with the
      relevant fields</div>
      <table>"""

  END_INSTRUCTIONS = '</table>'

  FORM_START = """<br>
      <form action="/client_test/results" method="post"
      enctype="multipart/form-data">
      <table>"""

  FORM_END = """</table>
      <div><input type="submit"
                  value="Test Client-Repository Intepoperability"></div>
      </form>"""
  INSTRUCTIONS_FOOTER = """<br>
      <div>Global and Current skip and min_date probably shouldn't be used with
      each other. There are two algorithms implemented to retrieve records since
      a given date:</div>
      <ol>
        <li>Put in the (global) min_date for the first query and keep it the
        same for all successive queries, monotonically increasing the (global)
        skip.  This strategy should work as long as the API implements a skip
        and min_date feature, but it might be less efficient if your repository
        implements skip by generating all results and excluding skipped results
        from the output.</li>
        <li>Put in (current) min_date for the first query.  For each successive
        query, update the (current) min_date to the most recent record.  The
        (current) skip is equal to the number of received records that have the
        same min_date as the most recent record (this should always be 1 unless
        two records have the same entry_date, which violates the PFIF spec),
        which can be more efficient.  This strategy requires all URLs that use
        current_min_date to return results forward chronologically rather than
        reverse chronologically (the norm for ATOM feeds).</li>
      </ol>
      <div>For example, with
      <a href="http://code.google.com/p/googlepersonfinder/wiki/DataAPI">Person
      Finder's API</a>, we could use
      <pre>https://subdomain.googlepersonfinder.appspot.com/feeds/person?key=$k$&amp;skip=$cs$&amp;min_entry_date=$cm$</pre>
      for the Retrieve Persons After Date URL or 
      <pre>https://subdomain.googlepersonfinder.appspot.com/feeds/notes?key=$k$&amp;skip=$gs$&amp;person_record_id=$p$</pre>
      for the Retrieve Notes from Person URL.</div>"""

  def get(self):
    self.write_header(ClientInput.TITLE)
    self.response.out.write(ClientInput.CLIENT_HEADER)
    for symbol, element_substituted, help_text in ClientInput.URL_SUBSTITUTIONS:
      self.response.out.write('<tr><td>' + symbol + '</td><td>' +
                              element_substituted + '</td><td>' +
                              help_text + '</td></tr>')
    self.response.out.write(ClientInput.END_INSTRUCTIONS)
    self.response.out.write(ClientInput.FORM_START)
    for name, form, help_text in ClientInput.CLIENT_INPUT:
      self.response.out.write(
          '<tr><td>' + name + '</td><td>' + '<input type="text" name="' + form +
          '"></td><td>' + help_text + '</td></tr>')
    self.response.out.write(ClientInput.FORM_END)
    self.response.out.write(ClientInput.INSTRUCTIONS_FOOTER)
    self.write_footer()

class Validator(PfifController):
  """Displays the validation results page."""

  def post(self):
    xml_file = self.get_file()
    self.write_header('PFIF Validator: Results')
    if xml_file is None:
      self.write_missing_input_file()
    else:
      validator = pfif_validator.PfifValidator(xml_file)
      messages = validator.run_validations()
      self.response.out.write('<h1>Validation: ' +
                              str(len(messages)) + ' Messages</h1>')
      self.response.out.write(
          utils.MessagesOutput.generate_message_summary(messages, is_html=True))
      # print_options is a list of all printing options passed in via
      # checkboxes.  It will contain 'show_errors' if the user checked that box,
      # for instance.  Thus, saying show_errors='show_errors' in print_options
      # will set show_errors to True if the box was checked and false otherwise.
      print_options = self.request.get_all('print_options')
      marked_up_message = validator.validator_messages_to_str(
          messages,
          show_errors='show_errors' in print_options,
          show_warnings='show_warnings' in print_options,
          show_line_numbers='show_line_numbers' in print_options,
          show_record_ids='show_record_ids' in print_options,
          show_xml_tag='show_xml_tag' in print_options,
          show_xml_text='show_xml_text' in print_options,
          show_full_line='show_full_line' in print_options,
          is_html=True)
      # don't escape the message since is_html escapes all input and contains
      # html that should be interpreted as html
      self.response.out.write(marked_up_message)
    self.write_footer()

APPLICATION = webapp.WSGIApplication(
    [('/validate/results', Validator),
     ('/diff/results', Diff),
     #('/client_test/results', ClientResults),
     ('/client_test', ClientInput)],
    debug=True)

def main():
  """Sets up the controller."""
  run_wsgi_app(APPLICATION)

if __name__ == "__main__":
  main()
