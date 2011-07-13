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

"""Provides a unified interface for collecting and printing errors."""

__author__ = 'samking@google.com (Sam King)'

class Error:
  """A container for information about an error or warning"""

  def __init__(self, message, is_error=True, xml_line_number=None,
               xml_element_text=None, person_record_id=None,
               note_record_id=None):
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

  def __init__(self):
    self.error_messages = {}
    self.test_name = None
    self.print_properties = {"output" : True, "errors" : True,
                             "warnings" : True, "xml_line_numbers" : True,
                             "xml_text" : False, "record_ids" : True}

  def set_printing_options(self, output=None, errors=None, warnings=None,
                           xml_line_numbers=None, xml_text=None,
                           record_ids=None):
    """Changes printing options for any specified options.

    output: if False, will print nothing
    errors: if False, will not print any Error for which is_error is true
    warnings: if False, will not print any Error for which is_error is
        false
    xml_line_numbers: if True, will print the source line in the XML where
        the error occurred
    xml_text: if True, will print the text element from the XML where the
        error occurred
    record_ids: if True, will print the note_record_id and/or
        person_record_id that caused the error"""
    if output != None:
      self.print_properties["output"] = output
    if errors != None:
      self.print_properties["errors"] = errors
    if warnings != None:
      self.print_properties["warnings"] = warnings
    if xml_line_numbers != None:
      self.print_properties["xml_line_numbers"] = xml_line_numbers
    if xml_text != None:
      self.print_properties["xml_text"] = xml_text
    if record_ids != None:
      self.print_properties["record_ids"] = record_ids

  def set_current_test(self, test_name):
    """Sets the current test, for the purposes of printing and error messages,
    to test_name.  Also, clears data from a previous run of the same test."""
    self.test_name = test_name
    if test_name in self.error_messages:
      del self.error_messages[test_name]

  def get_errors(self):
    """Returns a list of all errors for the current test."""
    assert self.test_name
    if self.test_name in self.error_messages:
      return self.error_messages[self.test_name]
    else:
      return []

  def add_error(self, error):
    """Adds an error to the list"""
    assert self.test_name
    if self.test_name not in self.error_messages:
      test_error_list = []
      self.error_messages[self.test_name] = test_error_list
    test_error_list = self.error_messages[self.test_name]
    test_error_list.append(error)

  def print_errors(self):
    """Prints out all errors from the current test, per the options in
    set_printing_options"""
    assert self.test_name
    if self.print_properties["output"]:
      print "****" + self.test_name + "****"
      if self.test_name in self.error_messages:
        errors = self.error_messages[self.test_name]
        for error in errors:
          if (error.is_error and self.print_properties["errors"]) or (
              not error.is_error and self.print_properties["warnings"]):
            message = ""
            if error.is_error:
              message += "ERROR: "
            else:
              message += "WARNING: "
            message += error.message + " "
            if (self.print_properties["xml_line_numbers"] and
                error.xml_line_number != None):
              message += "XML Line " + str(error.xml_line_number) + ". "
            if self.print_properties["record_ids"]:
              if error.person_record_id != None:
                message += ("The relevant person_record_id is: " +
                            error.person_record_id)
              if error.note_record_id != None:
                message += ("The relevant note_record_id is: " +
                            error.note_record_id)
            if self.print_properties["xml_text"] and error.xml_element_text:
              message += ("The text of the relevant PFIF XML node: " +
                          error.xml_element_text)
            print message
      print
