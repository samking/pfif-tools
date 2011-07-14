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
from error_printer import ErrorPrinter, Message

class PrintingTests(unittest.TestCase):
  """Tests the ErrorPrinter class methods"""

  def test_printer_init(self):
    """Tests that initializing an ErrorPrinter doesn't raise any exceptions and
    returns a new object"""
    self.assertTrue(ErrorPrinter())

  def test_error_storage(self):
    """For a given test, each call to add_error is stored such that get_error
    will return it in the order added."""
    printer = ErrorPrinter()
    printer.set_current_test("Test")
    self.assertEqual(len(printer.get_errors()), 0)
    printer.add_error(Message("Message"))
    printer.add_error(Message("More Message"))
    printer.add_error(Message("Hey"))
    self.assertEqual(len(printer.get_errors()), 3)
    self.assertEqual(printer.get_errors()[2].message, "Hey")

  def test_must_set_current_test(self):
    """If set_current_test is not called, add_error, get_errors, and
    print_errors should raise exceptions"""
    printer = ErrorPrinter()
    self.assertRaises(Exception, printer.add_error, Message("Message"))
    self.assertRaises(Exception, printer.print_errors)
    self.assertRaises(Exception, printer.get_errors)

  def test_resetting_test_deletes_old_data(self):
    """If set_current_test is called twice with the same test name, any data
    stored between the first and second call should be deleted"""
    printer = ErrorPrinter()
    printer.set_current_test("Test")
    printer.add_error(Message("Old"))
    printer.set_current_test("Test")
    printer.add_error(Message("New"))
    self.assertEqual(len(printer.get_errors()), 1)
    self.assertEqual(printer.get_errors()[0].message, "New")

  def test_print_options(self):
    """Tests that each of the printing options in set_printing_options changes
    the behavior of print_errors"""
    printer = ErrorPrinter()

    # mock stdout so that we can tell what gets printed
    old_stdout = sys.stdout
    fake_stdout = StringIO.StringIO()
    sys.stdout = fake_stdout

    # set up the printer with errors
    printer.set_current_test("Test")
    printer.add_error(Message("Message 1", is_error=True, xml_line_number=333,
                              xml_element_text="Text",
                              person_record_id="Person", note_record_id="Note"))
    printer.add_error(Message("Message 2", is_error=False))
    printer.add_error(Message("Message 3"))
    printer.set_printing_options(output=False, errors=False, warnings=False,
                                 xml_line_numbers=False, xml_text=False,
                                 record_ids=False)

    # output is off, so nothing should print
    printer.print_errors()
    self.assertEqual(fake_stdout.tell(), 0)

    # with output on but errors and warnings off, only test names should print
    printer.set_printing_options(output=True)
    printer.print_errors()
    self.assertEqual(fake_stdout.getvalue().find("Message"), -1)
    self.assertNotEqual(fake_stdout.getvalue().find("Test"), -1)

    # with only errors on, only errors should print
    printer.set_printing_options(errors=True)
    printer.print_errors()
    self.assertNotEqual(fake_stdout.getvalue().find("Message 1"), -1)
    self.assertEqual(fake_stdout.getvalue().find("Message 2"), -1)
    # the default value of is_error should be True, so Message 3 should print
    self.assertNotEqual(fake_stdout.getvalue().find("Message 3"), -1)

    # with warnings on, warnings should print
    printer.set_printing_options(warnings=True)
    printer.print_errors()
    self.assertNotEqual(fake_stdout.getvalue().find("Message 2"), -1)

    # line numbers, xml text, and record IDs should not print with them off and
    # should print with them on
    self.assertEqual(fake_stdout.getvalue().find("333"), -1)
    printer.set_printing_options(xml_line_numbers=True)
    printer.print_errors()
    self.assertNotEqual(fake_stdout.getvalue().find("333"), -1)

    self.assertEqual(fake_stdout.getvalue().find("Text"), -1)
    printer.set_printing_options(xml_text=True)
    printer.print_errors()
    self.assertNotEqual(fake_stdout.getvalue().find("Text"), -1)

    self.assertEqual(fake_stdout.getvalue().find("Person"), -1)
    self.assertEqual(fake_stdout.getvalue().find("Note"), -1)
    printer.set_printing_options(record_ids=True)
    printer.print_errors()
    self.assertNotEqual(fake_stdout.getvalue().find("Person"), -1)
    self.assertNotEqual(fake_stdout.getvalue().find("Note"), -1)

    sys.stdout = old_stdout

if __name__ == '__main__':
  unittest.main()
