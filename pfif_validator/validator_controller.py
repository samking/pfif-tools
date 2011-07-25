import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import StringIO
import pfif_validator
import sys

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/validate" method="post">
            <p>Put PFIF XML here to validate it:</p>
            <div><textarea name="pfif_xml" rows="3" cols="60"></textarea></div>
            <div><input type="checkbox" name="print_options"
                  value="show_errors" checked>Show Errors</div>
            <div><input type="checkbox" name="print_options"
                  value="show_warnings" checked>Show Warnings</div>
            <div><input type="checkbox" name="print_options"
                  value="show_line_numbers" checked>Show Line Numbers</div>
            <div><input type="checkbox" name="print_options"
                  value="show_record_ids" checked>Show Record IDs</div>
            <div><input type="checkbox" name="print_options"
                  value="show_xml_text" checked>Show XML Text</div>
            <div><input type="submit" value="Validate PFIF XML"></div>
          </form>
        </body>
      </html>""")

class Validator(webapp.RequestHandler):
  def post(self):
    self.response.out.write('<html><body><p>Validation Messages:</p><pre>')
    xml_file = StringIO.StringIO(self.request.get('pfif_xml'))
    messages = pfif_validator.PfifValidator.run_validations(xml_file)
    # Get the output.
    print_options = self.request.get_all('print_options')
    output = pfif_validator.PfifValidator.messages_to_str(
        messages,
        show_errors='show_errors' in print_options,
        show_warnings='show_warnings' in print_options,
        show_line_numbers='show_line_numbers' in print_options,
        show_record_ids='show_record_ids' in print_options,
        show_xml_text='show_xml_text' in print_options)
    self.response.out.write(cgi.escape(output))
    self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/validate', Validator)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
