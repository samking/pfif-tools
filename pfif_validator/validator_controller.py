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
    self.response.out.write('<html><body>You wrote:<pre>')
    xml_file = StringIO.StringIO(self.request.get('pfif_xml'))
    old_stdout = sys.stdout
    fake_stdout = StringIO.StringIO()
    sys.stdout = fake_stdout
    pfif_validator.run_all_validations(xml_file)
    sys.stdout = old_stdout
    self.response.out.write(cgi.escape(fake_stdout.getvalue()))
    #self.response.out.write(cgi.escape(self.request.get('pfif_xml')))
    self.response.out.write('</pre></body></html>')

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/validate', Validator)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
