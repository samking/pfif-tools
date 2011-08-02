#!/usr/bin/env python
# Copyright 2010 Google Inc.
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
#
# Slightly Modified from Google Person Finder:
# http://code.google.com/p/googlepersonfinder/

"""Runs the unit tests, with stubs for the datastore API.

Instead of running this script directly, use the 'unit_tests' shell script,
which sets up the PYTHONPATH and other necessary environment variables."""

import os
import sys
import unittest

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub

import remote_api

# Gather the tests from all the test modules.
loader = unittest.defaultTestLoader # pylint: disable=C0103
suites = [] # pylint: disable=C0103
for filename in os.listdir(remote_api.TESTS_DIR):
  if filename.startswith('test_') and filename.endswith('.py'):
    module = filename[:-3]
    suites.append(loader.loadTestsFromName(module))

# Create a new apiproxy and temp datastore to use for this test suite
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
temp_db = datastore_file_stub.DatastoreFileStub( # pylint: disable=C0103
    'PfifToolsUnittestDataStore', None, None, trusted=True)
apiproxy_stub_map.apiproxy.RegisterStub('datastore', temp_db)

# An application id is required to access the datastore, so let's create one
os.environ['APPLICATION_ID'] = 'pfif-tools-unittest'

# Run the tests.
# pylint: disable=C0103
result = unittest.TextTestRunner().run(unittest.TestSuite(suites))
# pylint: enable=C0103
sys.exit(not result.wasSuccessful())
