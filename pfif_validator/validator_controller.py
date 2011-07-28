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

"""Provides a web interface for pfif_validator"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import StringIO
import pfif_validator
import urllib

class MainPage(webapp.RequestHandler):
  """Displays the home page."""

  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/validate" method="post" enctype="multipart/form-data">
            <p>Put PFIF XML here to validate it:</p>
            <div><textarea name="pfif_xml" rows="3" cols="60"></textarea></div>
            <div>Or, upload a file: <input name="pfif_xml_file" type="file" />
                  </div>
            <div>Or, choose the URL of a PFIF XML file: <input type="text"
                  name="pfif_xml_url" /> </div>
            <br />
            <div><input type="checkbox" name="print_options"
                  value="show_errors" checked>Show Errors</div>
            <div><input type="checkbox" name="print_options"
                  value="show_warnings" checked>Show Warnings</div>
            <div><input type="checkbox" name="print_options"
                  value="show_line_numbers" checked>Show Line Numbers</div>
            <div><input type="checkbox" name="print_options"
                  value="show_line_text" checked>Show the Line on which the
                                                 Error Happened</div>
            <div><input type="checkbox" name="print_options"
                  value="show_record_ids" checked>Show Record IDs</div>
            <div><input type="checkbox" name="print_options"
                  value="show_xml_text" checked>Show XML Text</div>
            <div><input type="submit" value="Validate PFIF XML"></div>
          </form>
        </body>
      </html>""")

class Validator(webapp.RequestHandler):
  """Displays the validation results page."""

  # Inspiration (and some CSS/HTML) for the output design from the W3 validator.
  # See the W3C Software Notice and Licence at
  # http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
  CSS = """<style media="screen" type="text/css">
div.all_messages {
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding:0;
  border-top: 1px solid #EAEBEE;
  line-height: 135%;
  margin-bottom: .65em;
}

div.message {
  border: 1px solid #EAEBEE;
  border-top: 0;
  list-style-position: inside;
  padding: 1em;
  padding-bottom: 2em;
  clear: both;
}

div.message:hover {
  background-color: #fcfcfc;
}

span.message_line_number {
  font-style:italic;
}

span.message_text {
  font-weight:bold;
}

span.message_xml_line {
  color: black;
  background-color: #EAEBEE;
  font-family: monospace;
  white-space: pre;
  display: block;
}

</style>"""

  def post(self):
    for file_location in ['pfif_xml', 'pfif_xml_file']:
      if self.request.get(file_location):
        xml_file = StringIO.StringIO(self.request.get(file_location))
    if self.request.get('pfif_xml_url'):
      url = self.request.get('pfif_xml_url')
      # make a file-like object out of the URL's xml so we can seek on it
      xml_file = StringIO.StringIO(urllib.urlopen(url).read())
    print_options = self.request.get_all('print_options')
    validator = pfif_validator.PfifValidator(xml_file)
    messages = validator.run_validations()
    self.response.out.write('<html><head>' + Validator.CSS + '</head>'
                            '<body><h1>Validation: ' +
                            str(len(messages)) + ' Messages</h1>')
    marked_up_message = validator.messages_to_str(
        messages,
        show_errors='show_errors' in print_options,
        show_warnings='show_warnings' in print_options,
        show_line_numbers='show_line_numbers' in print_options,
        show_line_text='show_line_text' in print_options,
        show_record_ids='show_record_ids' in print_options,
        show_xml_text='show_xml_text' in print_options,
        is_html=True)
    # don't escape the message since is_html escapes all input and contains html
    # that should be interpreted as html
    self.response.out.write(marked_up_message)
    self.response.out.write('</body></html>')

APPLICATION = webapp.WSGIApplication([('/', MainPage),
                                      ('/validate', Validator)],
                                     debug=True)

def main():
  """Sets up the controller."""
  run_wsgi_app(APPLICATION)

if __name__ == "__main__":
  main()
