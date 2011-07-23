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
            <div><textarea name="pfif_xml" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Validate PFIF XML"></div>
          </form>
        </body>
      </html>""")


class Validator(webapp.RequestHandler):
  def post(self):
    self.response.out.write('<html><body><p>You wrote:</p><pre>')
    xml_file = StringIO.StringIO(self.request.get('pfif_xml'))
    messages = pfif_validator.PfifValidator.run_validations(xml_file)
    output = pfif_validator.PfifValidator.messages_to_str(messages)
    self.response.out.write(cgi.escape(output))
    self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/validate', Validator)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
