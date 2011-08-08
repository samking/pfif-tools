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

  def write_header(self, title):
    """Writes an HTML page header."""
    self.response.out.write("""<!DOCTYPE HTML>
  <html>
    <head>
      <meta charset="utf-8">
      <title>""" + title + """</title>
      <link rel="stylesheet" type="text/css" href="/static/style.css" />
    </head>""")

  def write_footer(self):
    """Closes the body and html tags."""
    self.response.out.write('</body></html>')

  def write_missing_input_file(self):
    """Writes that there is a missing input file."""
    self.response.out.write('<body><h1>Missing Input File</h1>')

  def get_file(self, file_number=1):
    """Gets a file that was pasted in, uploaded, or given by a URL.  If multiple
    files are provided, specify the number of the desired file as file_number.
    Returns None if there is no file."""
    paste_name = 'pfif_xml_' + str(file_number)
    upload_name = 'pfif_xml_file_' + str(file_number)
    url_name = 'pfif_xml_url_' + str(file_number)

    for file_location in [paste_name, upload_name]:
      if self.request.get(file_location):
        return StringIO(self.request.get(file_location))
    if self.request.get(url_name):
      url = self.request.get(url_name)
      # make a file-like object out of the URL's xml so we can seek on it
      return StringIO(utils.open_url(url).read())

    return None

class DiffController(PfifController):
  """Displays the diff results page."""

  def post(self):
    file_1 = self.get_file(1)
    file_2 = self.get_file(2)
    self.write_header('PFIF Diff: Results')
    # TODO(samking): Add description of 'old' verses 'new' file.  Custom name?
    # TODO(samking): Add summary-by-record (6 records in A but not B, 11 are
    # present in both but different...)
    if file_1 is None or file_2 is None:
      self.write_missing_input_file()
    else:
      messages = pfif_diff.pfif_file_diff(file_1, file_2)
      self.response.out.write(
          '<body><h1>Diff: ' + str(len(messages)) + ' Messages</h1>')
      self.response.out.write(
          utils.MessagesOutput.messages_to_str(messages, is_html=True))
    self.write_footer()

class ValidatorController(PfifController):
  """Displays the validation results page."""

  def post(self):
    xml_file = self.get_file()
    self.write_header('PFIF Validator: Results')
    if xml_file is None:
      self.write_missing_input_file()
    else:
      print_options = self.request.get_all('print_options')
      validator = pfif_validator.PfifValidator(xml_file)
      messages = validator.run_validations()
      self.response.out.write('<body><h1>Validation: ' +
                              str(len(messages)) + ' Messages</h1>')
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
    [('/validate/results', ValidatorController),
     ('/diff/results', DiffController)],
    debug=True)

def main():
  """Sets up the controller."""
  run_wsgi_app(APPLICATION)

if __name__ == "__main__":
  main()
