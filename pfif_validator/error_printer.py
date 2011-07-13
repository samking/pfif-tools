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

__author__ = 'samking@google.com (Sam King)'

"""Provides a unified interface for collecting and printing errors."""

# TODO(samking): get xml line number.  errors v warnings.  record_id.  full
# element text.

class Error:
  """A container for information about an error or warning"""

  def __init__(self, message, is_error=True, xml_line_number=None,
               xml_element_text=None, person_record_id="", note_record_id=""):
    self.message = message
    self.is_error = is_error
    self.xml_line_number = xml_line_number
    self.xml_element_text = xml_element_text
    self.person_record_id = person_record_id
    self.note_record_id  = note_record_id

class ErrorPrinter:
  """Collects and prints errors.

  Contains a map, error_messages, from test_name to an array of Errors.  This
  array is reinitialized every time set_current_test is called for a given test.
  Each Error will contain as much information as possible, and each
  print_error_messages call will print as much as set_printing_options
  specifies."""

  def __init__(self, print_output=True):
    self.error_messages = {}
    self.test_name = None
    self.print_output = print_output

  def set_printing_options(self, print_output=None):
    """Turns printing on if print_output is True"""
    if print_output != None:
      self.print_output = print_output

  @staticmethod
  def print_arr(arr):
    """Prints out each elem in the arr on its own line"""
    for elem in arr:
      print elem

  def set_current_test(self, test_name):
    """Sets the current test, for the purposes of printing and error messages,
    to test_name.  Also, clears data from a previous run of the same test."""
    self.test_name = test_name
    if test_name in self.error_messages:
      del self.error_messages[test_name]

  def get_errors(self):
    """Returns a list of all errors for the specified test."""
    assert self.test_name
    if self.test_name in self.error_messages:
      return self.error_messages[self.test_name]
    else:
      return []

  #TODO(samking): allow fine grained error printing
  def print_errors(self):
    """Prints out all errors from a given test, per the options in
    set_printing_options"""
    assert self.test_name
    if self.print_output:
      print "****" + self.test_name + "****"
      if self.test_name in self.error_messages:
        self.print_arr(self.error_messages[self.test_name])
      print

  def add_error(self, error):
    """Adds a message to the error message list"""
    assert self.test_name
    if self.test_name not in self.error_messages:
      test_error_list = []
      self.error_messages[self.test_name] = test_error_list
    test_error_list = self.error_messages[self.test_name]
    test_error_list.append(error)
