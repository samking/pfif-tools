#!/usr/bin/env python
# coding=utf-8
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

"""Tests for validator_controller.py"""

import unittest
import validator_controller
from StringIO import StringIO
from google.appengine.ext import webapp
import tests.pfif_xml as PfifXml
import utils

class ValidatorControllerTests(unittest.TestCase):
  """Tests for validator_controller."""

  # pylint: disable=C0301
  # advice from
  # http://stackoverflow.com/questions/6222528/unittesting-the-webapp-requesthandler-in-gae-python
  # for testing webapp server
  # pylint: enable=C0301
  @staticmethod
  def make_webapp_request(content):
    """Makes a webapp request for the validator with content as the HTTP POST
    content.  Returns the response."""
    request = webapp.Request({"wsgi.input": StringIO(content),
                              "CONTENT_LENGTH": len(content), "METHOD": "POST",
                              "PATH_INFO": "/validator",
                              "QUERY_STRING" : content})
    response = webapp.Response()
    handler = validator_controller.Validator()
    handler.initialize(request, response)
    handler.post()
    return response

  def test_no_xml_fails_gracefully(self):
    """If the user tries to validate with no input, there should not be an
    exception."""
    response = self.make_webapp_request('')
    self.assertTrue("html" in response.out.getvalue())

  def test_pasting_xml(self):
    """The page should have the correct number of errors in the header when
    using the pfif_xml POST variable to send PFIF XML."""
    response = self.make_webapp_request('pfif_xml=' +
                                        PfifXml.XML_TWO_DUPLICATE_NO_CHILD)
    self.assertTrue("3 Messages" in response.out.getvalue())

  def test_file_upload(self):
    """The page should have the correct number of errors in the header when
    using the pfif_xml_file POST variable to send PFIF XML."""
    response = self.make_webapp_request('pfif_xml_file=' +
                                        PfifXml.XML_TWO_DUPLICATE_NO_CHILD)
    self.assertTrue("3 Messages" in response.out.getvalue())

  def test_url_upload(self):
    """The page should have the correct number of errors in the header when
    using the pfif_xml_url POST variable to send PFIF XML."""
    utils.set_file_for_test(StringIO(PfifXml.XML_TWO_DUPLICATE_NO_CHILD))
    response = self.make_webapp_request('pfif_xml_url=dummy_url')
    self.assertTrue("3 Messages" in response.out.getvalue())

  def test_options(self):
    """The page should have a span or div for each print option."""
    request_base = 'pfif_xml_file=' + PfifXml.XML_EXPIRE_99_EMPTY_DATA

    response = self.make_webapp_request(request_base +
                                        '&print_options=show_errors')
    self.assertTrue('ERROR' in response.out.getvalue())
    self.assertTrue('message_type' in response.out.getvalue())
    self.assertTrue('message_text' in response.out.getvalue())

    response = self.make_webapp_request(request_base +
                                        '&print_options=show_warnings')
    self.assertTrue('WARNING' in response.out.getvalue())

    response = self.make_webapp_request(request_base +
                                        '&print_options=show_line_numbers'
                                        '&print_options=show_warnings')
    self.assertTrue('message_line_number' in response.out.getvalue())

    # EXPIRE_99 doesn't have any errors with xml element text, so we use a
    # different XML file
    response = self.make_webapp_request('pfif_xml_file=' +
                                        PfifXml.XML_INCORRECT_FORMAT_11 +
                                        '&print_options=show_xml_element_text'
                                        '&print_options=show_errors')
    self.assertTrue('message_xml_element_text' in response.out.getvalue())

    response = self.make_webapp_request(request_base +
                                        '&print_options=show_record_ids'
                                        '&print_options=show_warnings')
    self.assertTrue('record_id' in response.out.getvalue())

    response = self.make_webapp_request(request_base +
                                        '&print_options=show_full_line'
                                        '&print_options=show_warnings')
    self.assertTrue('message_full_line' in response.out.getvalue())

  @staticmethod
  def test_main():
    """main should not crash."""
    validator_controller.main()

if __name__ == '__main__':
  unittest.main()
