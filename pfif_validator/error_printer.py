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

class ErrorPrinter:

  def __init__(self, print_output=True):
    self.error_messages = {}
    self.test_name = None
    self.print_output = print_output

  def set_printing(self, print_output):
    """Turns printing on if print_output is True"""
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

  def get_error_messages(self):
    """Returns a list of all error messages for the specified test."""
    assert self.test_name
    if self.test_name in self.error_messages:
      return self.error_messages[self.test_name]
    else:
      return []

  def print_error_messages(self):
    """Prints out all messages from a given test"""
    assert self.test_name
    if self.print_output:
      print "****" + self.test_name + "****"
      if self.test_name in self.error_messages:
        self.print_arr(self.error_messages[self.test_name])
      print

  def add_error_message(self, error_message, person_record_id="",
                        note_record_id=""):
    """Adds a message to the error message list"""
    assert self.test_name
    message = error_message
    if person_record_id:
      message += "\tThe relevant person_record_id: " + person_record_id
    if note_record_id:
      message += "\tThe relevant note_record_id: " + note_record_id
    if self.test_name not in self.error_messages:
      test_message_list = []
      self.error_messages[self.test_name] = test_message_list
    test_message_list = self.error_messages[self.test_name]
    test_message_list.append(message)


__author__ = 'samking@google.com (Sam King)'
