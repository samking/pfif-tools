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
import utils

def generate_header(title):
  """Generates an HTML page header."""
  return ("""<!DOCTYPE HTML>
<html>
  <head>
    <meta charset="utf-8">
    <title>""" + title + """</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css" />
  </head>""")

def get_file(controller, file_number=1):
  """Gets a file that was pasted in, uploaded, or given by a URL.  If multiple
  files are provided, specify the number of the desired file as file_number.
  Returns None if there is no file."""
  paste_name = 'pfif_xml_' + str(file_number)
  upload_name = 'pfif_xml_file_' + str(file_number)
  url_name = 'pfif_xml_url_' + str(file_number)

  for file_location in [paste_name, upload_name]:
    if controller.request.get(file_location):
      return StringIO(controller.request.get(file_location))
  if controller.request.get(url_name):
    url = controller.request.get(url_name)
    # make a file-like object out of the URL's xml so we can seek on it
    return StringIO(utils.open_url(url).read())

  return None

class DiffController(webapp.RequestHandler):
  """Displays the diff results page."""

class ValidatorController(webapp.RequestHandler):
  """Displays the validation results page."""

  def post(self):
    xml_file = get_file(self)
    self.response.out.write(generate_header('PFIF Validator: Results'))
    if xml_file is None:
      self.response.out.write('<body><h1>No Input File</h1></body></html>')
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
      self.response.out.write('</body></html>')

APPLICATION = webapp.WSGIApplication(
    [('/validate/results', ValidatorController),
     ('/diff/results', DiffController)],
    debug=True)

def main():
  """Sets up the controller."""
  run_wsgi_app(APPLICATION)

if __name__ == "__main__":
  main()
