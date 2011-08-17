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

"""Tests client-repo interoperability for a PFIF repository.

Full descriptions of all tests are available at:
https://docs.google.com/a/google.com/document/d/1HoCtiKjmp6j2d4d2U9QBJtehuVoANcWc6ggxthacPRY/edit?hl=en_US&authkey=CMaK1qsI
"""

__author__ = 'samking@google.com (Sam King)'

import utils
import urllib

class ClientTester():
  """Contains information about a repository API to run tests."""

  def __init__(self, api_key=''):
    self.api_key = api_key

  def expand_url(self, url, person_record_id='', note_record_id=''):
    """Given a URL, replaces symbolic markup with the desired pieces of data.
    $k = API key
    $p = person record id
    $n = note record id
    For example, when ClientTester has been initialized with key='hello',
    calling this function with the following arguments:
      url='example.org/api/person?key=$k&person=$p',
      person_record_id='example.com/person1'
    will return the following url:
      'example.org/api/person/key=hello&person=example.org%2Fperson1'
    Assumes that the key and url are properly URL encoded and that any record_id
    needs to be URL encoded."""
    encoded_person = urllib.quote_plus(person_record_id)
    encoded_note = urllib.quote_plus(note_record_id)
    output_url = url.replace('$k', self.api_key)
    output_url = output_url.replace('$p', encoded_person)
    output_url = output_url.replace('$n', encoded_note)
    return output_url

  def check_retrieve_person_record(self):
    """Test 1.1/3.1.  Requesting person with id "example.org/p0001" should match
    the record from the test data set."""
    url = self.expand_url(self.person_record_url, person_id='example.org/p0001')
    response = utils.open_url(url)
    # desired_response = write_file(self.persons['example.org/p0001'])
    # messages = diff(response, desired_response)
    messages = []
    return messages

# def main():

if __name__ == '__main__':
  main()
