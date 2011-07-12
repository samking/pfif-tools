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

"""Tests for error_printing.py"""

__author__ = 'samking@google.com (Sam King)'

import unittest
import StringIO
import sys
sys.path.append(sys.path[0] + '/../pfif_validator')
from error_printer import ErrorPrinter

class PrintingTests(unittest.TestCase):
  """Tests the ErrorPrinter class methods"""

  def test_printing(self):
    """print_test_start, print_error_message, and add_error_message should
    generate messages if printing is turned on and should not crash.
    get_error_messages should return a list of error messages."""
    old_stdout = sys.stdout
    printer = ErrorPrinter()

    # mock stdout so that we can tell what gets printed
    printer.set_printing(False)
    fake_stdout = StringIO.StringIO()
    sys.stdout = fake_stdout

    # I can't do anything without setting the test name
    self.assertRaises(Exception, printer.add_error_message, "Error Message")
    self.assertRaises(Exception, printer.print_error_messages)
    self.assertRaises(Exception, printer.get_error_messages)

    # start out with no errors
    printer.set_current_test("Printing Test")
    self.assertEqual(len(printer.get_error_messages()), 0)

    # I can add errors and get the back
    printer.add_error_message("Error Message")
    printer.add_error_message("Error Message", person_record_id="ID1",
                              note_record_id="ID2")
    self.assertEqual(len(printer.get_error_messages()), 2)

    # printing doesn't do anything when set_printing is off
    printer.print_error_messages()
    self.assertTrue(fake_stdout.tell() == 0)

    # printing does something when set_printing is on
    printer.set_printing(True)
    printer.print_error_messages()
    self.assertTrue(fake_stdout.tell() > 0)

    sys.stdout = old_stdout

if __name__ == '__main__':
  unittest.main()
