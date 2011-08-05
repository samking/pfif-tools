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

class Validator(webapp.RequestHandler):
  """Displays the validation results page."""

  RESULTS_HEADER = """<!DOCTYPE HTML>
<html>
  <head>
    <meta charset="utf-8">
    <title>PFIF Validator: Results</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css" />
  </head>"""

  def post(self):
    xml_file = None
    for file_location in ['pfif_xml', 'pfif_xml_file']:
      if self.request.get(file_location):
        xml_file = StringIO(self.request.get(file_location))
    if self.request.get('pfif_xml_url'):
      url = self.request.get('pfif_xml_url')
      # make a file-like object out of the URL's xml so we can seek on it
      xml_file = StringIO(utils.open_url(url).read())
    self.response.out.write(Validator.RESULTS_HEADER)
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

APPLICATION = webapp.WSGIApplication([('/validate/results', Validator)],
                                     debug=True)

def main():
  """Sets up the controller."""
  run_wsgi_app(APPLICATION)

if __name__ == "__main__":
  main()
