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

"""Tests for utils.py"""

import os
import sys
# TODO(samking): I'm sure that there is a simpler way to do this...
sys.path.append(os.getcwd() + '/../pfif_validator')
import utils
import unittest

class XmlUtilTests(unittest.TestCase):

  def test_blank_input(self):
    """extract_tag should return an empty string on blank input"""
    self.assertEqual(utils.extract_tag(""), "")

  def test_tag(self):
    """extract_tag should return the original string when the string does not
    start with a namespace"""
    self.assertEqual(utils.extract_tag("foo"), "foo")

  def test_tag_and_namespace(self):
    """extract_tag should return the local tag when the string starts with a
    namespace"""
    self.assertEqual(utils.extract_tag("{foo}bar"), "bar")

if __name__ == '__main__':
  unittest.main()
