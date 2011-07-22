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

"""Tests for pfif_validator.py"""

import unittest
import StringIO

import os
import sys
# TODO(samking): remove this after adding a test running script
sys.path.append(sys.path[0] + '/../pfif_validator')
from pfif_validator import PfifValidator, Message
import datetime
import utils

class ValidatorTests(unittest.TestCase):
  """Tests each validation function in pfif_validator.py"""

  XML_11_SMALL = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person />
</pfif:pfif>"""

  XML_11_FULL = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id>example.org/local-id.3</pfif:person_record_id>
    <pfif:entry_date>1234-56-78T90:12:34Z</pfif:entry_date>
    <pfif:author_name>author name</pfif:author_name>
    <pfif:author_email>email@example.org</pfif:author_email>
    <pfif:author_phone>+12345678901</pfif:author_phone>
    <pfif:source_name>source name</pfif:source_name>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:source_url>http://source.u.r/l</pfif:source_url>
    <pfif:first_name>FIRST NAME</pfif:first_name>
    <pfif:last_name>LAST NAME</pfif:last_name>
    <pfif:home_city>HOME CITY</pfif:home_city>
    <pfif:home_state>CA</pfif:home_state>
    <pfif:home_neighborhood>HOME NEIGHBORHOOD</pfif:home_neighborhood>
    <pfif:home_street>HOME STREET</pfif:home_street>
    <pfif:home_zip>12345</pfif:home_zip>
    <pfif:photo_url>
      https://user:pass@host:999/url_path?var=val#hash
    </pfif:photo_url>
    <pfif:other>other text</pfif:other>
    <pfif:note>
      <pfif:note_record_id>www.example.org/local-id.4</pfif:note_record_id>
      <pfif:entry_date>1234-56-78T90:12:34Z</pfif:entry_date>
      <pfif:author_name>author name</pfif:author_name>
      <pfif:author_email>author-email@exmaple.org</pfif:author_email>
      <pfif:author_phone>123.456.7890</pfif:author_phone>
      <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
      <pfif:found>true</pfif:found>
      <pfif:email_of_found_person>email@example.org</pfif:email_of_found_person>
      <pfif:phone_of_found_person>(123)456-7890</pfif:phone_of_found_person>
      <pfif:last_known_location>last known location</pfif:last_known_location>
      <pfif:text>large text string</pfif:text>
    </pfif:note>
    <pfif:note>
      <pfif:note_record_id>www.example.org/local-id.5</pfif:note_record_id>
      <pfif:author_name>author name</pfif:author_name>
      <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
      <pfif:found>false</pfif:found>
      <pfif:text>large text string</pfif:text>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_NON_PFIF_ROOT = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:html xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person />
</pfif:html>"""

  XML_NO_NAMESPACE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif>
  <person />
</pfif>"""

  XML_BAD_PFIF_VERSION = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/9.9">
  <pfif:person />
</pfif:pfif>"""

  XML_BAD_PFIF_WEBSITE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.com/pfif/1.2">
  <pfif:person />
</pfif:pfif>"""

  XML_ROOT_LACKS_CHILD = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2" />"""

  XML_ROOT_HAS_BAD_CHILD = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:notAPersonOrNote />
</pfif:pfif>"""

  XML_TOP_LEVEL_NOTE_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:note />
</pfif:pfif>"""

  XML_TOP_LEVEL_NOTE_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:note />
</pfif:pfif>"""

  XML_NOTES_WITH_CHILDREN = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:person_record_id />
    <pfif:note_record_id />
    <pfif:author_name />
    <pfif:source_date />
    <pfif:text />
  </pfif:note>
  <pfif:person>
    <pfif:note>
      <pfif:note_record_id />
      <pfif:author_name />
      <pfif:source_date />
      <pfif:text />
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_NOTES_NO_CHILDREN = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note />
  <pfif:person>
    <pfif:note />
  </pfif:person>
</pfif:pfif>"""

  XML_PERSON_WITH_CHILDREN_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:first_name />
    <pfif:last_name />
  </pfif:person>
</pfif:pfif>"""

  XML_PERSON_WITH_CHILDREN_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:source_date />
    <pfif:full_name />
  </pfif:person>
</pfif:pfif>"""

  XML_PERSON_NO_CHILDREN_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person />
</pfif:pfif>"""

  XML_INCORRECT_FORMAT_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id>example.org/</pfif:person_record_id>
    <pfif:entry_date>123456-78T90:12:34Z</pfif:entry_date>
    <pfif:author_email>@example.org</pfif:author_email>
    <pfif:author_phone>123defghi</pfif:author_phone>
    <pfif:source_date>1234-56-7890:12:34Z</pfif:source_date>
    <pfif:source_url>!.%^*</pfif:source_url>
    <pfif:first_name>lowercase first name</pfif:first_name>
    <pfif:last_name>LOWEr</pfif:last_name>
    <pfif:home_city>lOWER</pfif:home_city>
    <pfif:home_state>LONG</pfif:home_state>
    <pfif:home_neighborhood>lower</pfif:home_neighborhood>
    <pfif:home_street>loWer</pfif:home_street>
    <pfif:home_zip>NOT NUMERIC</pfif:home_zip>
    <pfif:photo_url>bad.port:foo</pfif:photo_url>
    <pfif:note>
      <pfif:note_record_id>/local-id.4</pfif:note_record_id>
      <pfif:entry_date>1234-56-78T90:12:34</pfif:entry_date>
      <pfif:author_email>author-email</pfif:author_email>
      <pfif:author_phone>abc-def-ghij</pfif:author_phone>
      <pfif:source_date>123a-56-78T90:12:34Z</pfif:source_date>
      <pfif:found>not-true-or-false</pfif:found>
      <pfif:email_of_found_person>email@</pfif:email_of_found_person>
      <pfif:phone_of_found_person>abc1234567</pfif:phone_of_found_person>
    </pfif:note>
    <pfif:note>
      <pfif:note_record_id>http://foo/bar</pfif:note_record_id>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_FULL_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:sex>male</pfif:sex>
    <pfif:date_of_birth>1990-09-15</pfif:date_of_birth>
    <pfif:age>20</pfif:age>
    <pfif:home_country>US</pfif:home_country>
    <pfif:home_state>OR</pfif:home_state>
    <pfif:home_postal_code>94309</pfif:home_postal_code>
    <pfif:first_name>lowercase first</pfif:first_name>
    <pfif:last_name>lower last</pfif:last_name>
    <pfif:home_city>lower city</pfif:home_city>
    <pfif:home_neighborhood>lower neighborhood</pfif:home_neighborhood>
    <pfif:home_street>lower street</pfif:home_street>
    <pfif:note>
      <pfif:status>information_sought</pfif:status>
    </pfif:note>
  </pfif:person>
  <pfif:person>
    <pfif:sex>female</pfif:sex>
    <pfif:home_street>street address</pfif:home_street>
    <pfif:date_of_birth>1990-09</pfif:date_of_birth>
    <pfif:age>3-100</pfif:age>
    <pfif:home_state>71</pfif:home_state>
    <pfif:note>
      <pfif:status>believed_alive</pfif:status>
    </pfif:note>
  </pfif:person>
  <pfif:person>
    <pfif:sex>other</pfif:sex>
    <pfif:date_of_birth>1990</pfif:date_of_birth>
    <pfif:home_state>ABC</pfif:home_state>
    <pfif:note>
      <pfif:status>believed_dead</pfif:status>
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:person_record_id>example.org/local1</pfif:person_record_id>
    <pfif:linked_person_record_id>example.org/id2</pfif:linked_person_record_id>
    <pfif:status>is_note_author</pfif:status>
  </pfif:note>
  <pfif:note>
    <pfif:status>believed_missing</pfif:status>
  </pfif:note>
</pfif:pfif>"""

  XML_INCORRECT_FORMAT_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:sex>not-male-or-female-or-other</pfif:sex>
    <pfif:date_of_birth>09-15-1990</pfif:date_of_birth>
    <pfif:age>20.5</pfif:age>
    <pfif:home_country>abc</pfif:home_country>
    <pfif:home_state>1234</pfif:home_state>
    <pfif:home_postal_code>foo</pfif:home_postal_code>
    <pfif:note>
      <pfif:status>weird_belief</pfif:status>
    </pfif:note>
  </pfif:person>
  <pfif:person>
    <pfif:date_of_birth>September 15, 1990</pfif:date_of_birth>
    <pfif:age>3,100</pfif:age>
  </pfif:person>
  <pfif:person>
    <pfif:date_of_birth>1900-ab</pfif:date_of_birth>
  </pfif:person>
  <pfif:note>
    <pfif:person_record_id>example.org</pfif:person_record_id>
    <pfif:linked_person_record_id>/id2</pfif:linked_person_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_CORRECT_FORMAT_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:full_name>john doe</pfif:full_name>
    <pfif:expiry_date>1234-56-78T90:12:34Z</pfif:expiry_date>
  </pfif:person>
</pfif:pfif>"""

  XML_INCORRECT_FORMAT_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:expiry_date>12a4-56-78T90:12:34Z</pfif:expiry_date>
  </pfif:person>
</pfif:pfif>"""

  XML_UNIQUE_PERSON_IDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/2</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.com/1</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.com/2</pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

  XML_UNIQUE_NOTE_IDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/1</pfif:note_record_id>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/2</pfif:note_record_id>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.com/1</pfif:note_record_id>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.com/2</pfif:note_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_DUPLICATE_PERSON_IDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.com/2</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.com/2</pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

  XML_DUPLICATE_NOTE_IDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/1</pfif:note_record_id>
  </pfif:note>
  <pfif:person>
    <pfif:note>
      <pfif:note_record_id>example.org/1</pfif:note_record_id>
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>example.com/1</pfif:note_record_id>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.com/1</pfif:note_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_NOTES_BELONG_TO_PEOPLE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
  </pfif:note>
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
    <pfif:note>
      <pfif:person_record_id>example.org/1</pfif:person_record_id>
    </pfif:note>
    <pfif:note />
  </pfif:person>
</pfif:pfif>"""

  XML_NOTES_WITHOUT_PEOPLE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note />
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
    <pfif:note>
      <pfif:person_record_id>example.org/2</pfif:person_record_id>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_MISSING_FIELDS_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
    <pfif:other>other</pfif:other>
    <pfif:note>
      <pfif:note_record_id>example.org/2</pfif:note_record_id>
      <pfif:text>text</pfif:text>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_INCORRECT_FIELD_ORDER_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:note>
      <pfif:note_record_id />
      <pfif:text />
      <pfif:found />
    </pfif:note>
    <pfif:other />
  </pfif:person>
  <pfif:person>
    <pfif:note>
      <pfif:text />
      <pfif:note_record_id />
    </pfif:note>
    <pfif:person_record_id />
  </pfif:person>
  <pfif:person>
    <pfif:home_state />
    <pfif:home_city />
  </pfif:person>
</pfif:pfif>"""

  XML_EXTRANEOUS_FIELD_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:foo />
    <pfif:other />
  </pfif:person>
</pfif:pfif>"""

  XML_CORRECT_FIELD_ORDER_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:other />
    <pfif:home_state />
    <pfif:home_city />
    <pfif:note>
      <pfif:note_record_id />
      <pfif:text />
      <pfif:found />
    </pfif:note>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id />
    <pfif:note>
      <pfif:note_record_id />
      <pfif:found />
      <pfif:source_date />
    </pfif:note>
    <pfif:note />
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id />
    <pfif:home_state />
    <pfif:home_city />
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id />
    <pfif:person_record_id />
    <pfif:text />
    <pfif:author_name />
  </pfif:note>
</pfif:pfif>"""

  XML_INCORRECT_PERSON_FIELD_ORDER_12 = """<?xml version="1.0"
  encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:note />
    <pfif:home_city />
  </pfif:person>
  <pfif:person>
    <pfif:home_city />
    <pfif:person_record_id />
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id />
    <pfif:note />
    <pfif:home_city />
    <pfif:note />
  </pfif:person>
</pfif:pfif>"""

  XML_INCORRECT_NOTE_FIELD_ORDER_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:note>
    <pfif:note_record_id />
    <pfif:text />
    <pfif:person_record_id />
  </pfif:note>
  <pfif:note>
    <pfif:text />
    <pfif:note_record_id />
    <pfif:person_record_id />
  </pfif:note>
  <pfif:note>
    <pfif:text />
    <pfif:note_record_id />
  </pfif:note>
  <pfif:note>
    <pfif:text />
    <pfif:person_record_id />
  </pfif:note>
</pfif:pfif>"""

  XML_ODD_ORDER_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id />
    <pfif:note>
      <pfif:note_record_id />
      <pfif:text />
      <pfif:found />
    </pfif:note>
    <pfif:other />
  </pfif:person>
  <pfif:person>
    <pfif:note>
      <pfif:text />
      <pfif:note_record_id />
    </pfif:note>
    <pfif:person_record_id />
  </pfif:person>
  <pfif:person>
    <pfif:home_state />
    <pfif:home_city />
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_HAS_DATA_NONSYNCED_DATES = """<?xml version="1.0"
  encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:source_date>1997-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1998-02-03T04:05:06Z</pfif:entry_date>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:note>
      <pfif:note_record_id>not/deleted</pfif:note_record_id>
    </pfif:note>
    <pfif:other>not deleted or omitted</pfif:other>
  </pfif:person>
  <pfif:note>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:text>this isn't deleted either</pfif:text>
  </pfif:note>
</pfif:pfif>"""

  XML_EXPIRE_99_EMPTY_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:note>
      <pfif:note_record_id></pfif:note_record_id>
    </pfif:note>
    <pfif:other></pfif:other>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_NO_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_HAS_NOTE_SYNCED_DATES = """<?xml version="1.0"
  encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:note>
      <pfif:note_record_id>not/deleted</pfif:note_record_id>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_HAS_DATA_SYNCED_DATES = """<?xml version="1.0"
  encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:other>data still here</pfif:other>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_NO_DATA_NONSYNCED_DATES = """<?xml version="1.0"
  encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1998-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/id2</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-04-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-04-03T04:05:06Z</pfif:entry_date>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:other>data still here</pfif:other>
  </pfif:person>
</pfif:pfif>"""

  XML_EXPIRE_99_HAS_NOTE_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:expiry_date>1999-02-03T04:05:06Z</pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
  </pfif:person>
  <pfif:note>
    <pfif:person_record_id>example.org/id</pfif:person_record_id>
    <pfif:note_record_id>example.org/note/not/deleted</pfif:note_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_NO_EXPIRY_DATE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:other>data still here</pfif:other>
  </pfif:person>
</pfif:pfif>"""

  XML_EMPTY_EXPIRY_DATE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date></pfif:expiry_date>
    <pfif:source_date>1999-02-03T04:05:06Z</pfif:source_date>
    <pfif:entry_date>1999-02-03T04:05:06Z</pfif:entry_date>
    <pfif:other>data still here</pfif:other>
  </pfif:person>
</pfif:pfif>"""

  XML_UNLINKED_RECORDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p1</pfif:person_record_id>
    <pfif:note>
      <pfif:note_record_id>example.com/n1</pfif:note_record_id>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

  XML_CORRECTLY_LINKED_RECORDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p1</pfif:person_record_id>
    <pfif:note>
      <pfif:note_record_id>example.com/n1</pfif:note_record_id>
      <pfif:linked_person_record_id>example.org/p2</pfif:linked_person_record_id>
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>example.com/n2</pfif:note_record_id>
    <pfif:person_record_id>example.org/p2</pfif:person_record_id>
    <pfif:linked_person_record_id>example.org/p1</pfif:linked_person_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_ASYMMETRICALLY_LINKED_RECORDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.com/n2</pfif:note_record_id>
    <pfif:person_record_id>example.org/p2</pfif:person_record_id>
    <pfif:linked_person_record_id>example.org/p1</pfif:linked_person_record_id>
  </pfif:note>
</pfif:pfif>"""

  XML_GIBBERISH_FIELDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date />
    <pfif:field />
    <pfif:foo />
    <pfif:note>
      <pfif:bar />
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:bar />
  </pfif:note>
</pfif:pfif>"""

  XML_DUPLICATE_FIELDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:expiry_date />
    <pfif:expiry_date />
    <pfif:expiry_date />
    <pfif:note>
      <pfif:note_record_id />
      <pfif:note_record_id />
      <pfif:person_record_id />
    </pfif:note>
    <pfif:note>
      <pfif:note_record_id />
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id />
  </pfif:note>
</pfif:pfif>"""

  XML_TOP_LEVEL_NOTE_PERSON_11 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:note />
  <pfif:person>
    <pfif:person_record_id>example.org/id1</pfif:person_record_id>
    <pfif:note>
      <pfif:note_record_id />
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id />
  </pfif:note>
</pfif:pfif>"""

  XML_TWO_DUPLICATE_NO_CHILD = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.1">
  <pfif:foo />
  <pfif:foo />
</pfif:pfif>"""

  XML_UNICODE_12 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>
    <pfif:person_record_id>not.unicode/person-id</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:author_name>ユニコード名</pfif:author_name>
    <pfif:first_name>اسم يونيكود</pfif:first_name>
    <pfif:last_name>Unicode名称</pfif:last_name>
    <pfif:home_street>Юнікодам вуліцы</pfif:home_street>
    <pfif:home_city>ইউনিকোড শহর</pfif:home_city>
    <pfif:home_neighborhood>Unicode השכונה</pfif:home_neighborhood>
    <pfif:other>ಯುನಿಕೋಡಿನ ಇತರ</pfif:other>
    <pfif:note>
      <pfif:note_record_id>not.unicode/note-id</pfif:note_record_id>
      <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
      <pfif:author_name>유니 코드 이름</pfif:author_name>
      <pfif:last_known_location>محل یونیکد</pfif:last_known_location>
      <pfif:text>Unicode текст</pfif:text>
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>not.unicode/note-id-2</pfif:note_record_id>
    <pfif:person_record_id>note.unicode/person-id</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:author_name>Уницоде имена</pfif:author_name>
    <pfif:last_known_location>யுனிகோட் இடம்</pfif:last_known_location>
    <pfif:text>యూనికోడ్ టెక్స్ట్</pfif:text>
  </pfif:note>
</pfif:pfif>"""

  EXPIRED_TIME = datetime.datetime(1999, 3, 1)

  PRINT_VALIDATOR_OUTPUT = True

  # Set Up

  def setUp(self): # pylint: disable=C0103
    """Some of the tests will run code that prints stuff out.  This prevents it
    from printing next to the clean dots from the unit tests."""
    if not ValidatorTests.PRINT_VALIDATOR_OUTPUT:
      sys.stdout = open(os.devnull, "w")

  @staticmethod
  def set_up_validator(xml):
    """Creates a PFIF validator from XML and initializes it"""
    pfif_file = StringIO.StringIO(xml)
    return PfifValidator(pfif_file, initialize=True)

  # printing

  def test_printing(self):
    """Tests that each of the printing options in set_printing_options changes
    the behavior of print_errors"""
    # mock stdout so that we can tell what gets printed
    old_stdout = sys.stdout
    fake_stdout = StringIO.StringIO()
    sys.stdout = fake_stdout

    # set up the messages to be printed
    messages = []
    messages.append(Message("Message 1", is_error=True, xml_line_number=333,
                            xml_element_text="Text", person_record_id="Person",
                            note_record_id="Note"))
    messages.append(Message("Message 2", is_error=False))
    messages.append(Message("Message 3"))

    # With no test name, errors, or warnings, nothing should print
    PfifValidator.print_messages(messages, show_errors=False,
                                 show_warnings=False)
    self.assertEqual(fake_stdout.tell(), 0)

    # with errors and warnings off, only test names should print
    PfifValidator.print_messages(messages, test_name="Test", show_errors=False,
                                 show_warnings=False)
    self.assertEqual(fake_stdout.getvalue().find("Message"), -1)
    self.assertNotEqual(fake_stdout.getvalue().find("Test"), -1)

    # with only errors on, only errors should print
    PfifValidator.print_messages(messages, show_warnings=False,
                                 show_line_numbers=False, show_record_ids=False,
                                 show_xml_text=False)
    self.assertNotEqual(fake_stdout.getvalue().find("Message 1"), -1)
    self.assertEqual(fake_stdout.getvalue().find("Message 2"), -1)
    # the default value of is_error should be True, so Message 3 should print
    self.assertNotEqual(fake_stdout.getvalue().find("Message 3"), -1)

    # with warnings on, warnings should print
    PfifValidator.print_messages(messages, show_line_numbers=False,
                                 show_record_ids=False, show_xml_text=False)
    self.assertNotEqual(fake_stdout.getvalue().find("Message 2"), -1)

    # line numbers, xml text, and record IDs should not print with them off and
    # should print with them on
    self.assertEqual(fake_stdout.getvalue().find("333"), -1)
    PfifValidator.print_messages(messages, show_line_numbers=True,
                                 show_record_ids=False, show_xml_text=False)
    self.assertNotEqual(fake_stdout.getvalue().find("333"), -1)

    self.assertEqual(fake_stdout.getvalue().find("Text"), -1)
    PfifValidator.print_messages(messages, show_record_ids=False,
                                 show_xml_text=True)
    self.assertNotEqual(fake_stdout.getvalue().find("Text"), -1)

    self.assertEqual(fake_stdout.getvalue().find("Person"), -1)
    self.assertEqual(fake_stdout.getvalue().find("Note"), -1)
    PfifValidator.print_messages(messages, show_record_ids=True)
    self.assertNotEqual(fake_stdout.getvalue().find("Person"), -1)
    self.assertNotEqual(fake_stdout.getvalue().find("Note"), -1)

    sys.stdout = old_stdout

  # initialize_xml

  def test_valid_xml(self):
    """initialize_xml should turn a string of valid XML into an object"""
    valid_xml_file = StringIO.StringIO(ValidatorTests.XML_11_SMALL)
    validator = PfifValidator(valid_xml_file, initialize=False)
    self.assertEqual(len(validator.initialize_xml()), 0)

  def test_invalid_xml(self):
    """initialize_xml should raise an error on a string of invalid XML"""
    invalid_xml_file = StringIO.StringIO(
        """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>""")
    validator = PfifValidator(invalid_xml_file, initialize=False)
    self.assertRaises(Exception, validator.initialize_xml)

  # initialize_pfif_version

  def test_root_is_pfif(self):
    """initialize_pfif_version should return an empty list if the XML
    root is PFIF"""
    pfif_11_xml_file = StringIO.StringIO(ValidatorTests.XML_11_SMALL)
    validator = PfifValidator(pfif_11_xml_file, initialize=False)
    validator.initialize_xml()
    self.assertEqual(len(validator.initialize_pfif_version()), 0)

  def test_root_is_not_pfif(self):
    """initialize_pfif_version should raise an exception if the XML root
    is not PFIF"""
    random_xml_file = StringIO.StringIO(ValidatorTests.XML_NON_PFIF_ROOT)
    validator = PfifValidator(random_xml_file, initialize=False)
    validator.initialize_xml()
    self.assertRaises(Exception, validator.initialize_pfif_version)

  def test_root_lacks_namespace(self):
    """initialize_pfif_version should raise an exception if the XML root
    doesn't specify a namespace"""
    no_namespace_xml_file = StringIO.StringIO(ValidatorTests.XML_NO_NAMESPACE)
    validator = PfifValidator(no_namespace_xml_file, initialize=False)
    validator.initialize_xml()
    self.assertRaises(Exception, validator.initialize_pfif_version)

  def test_root_is_bad_pfif_version(self):
    """initialize_pfif_version should raise an exception if the PFIF
    version is not supported"""
    pfif_99_xml_file = StringIO.StringIO(ValidatorTests.XML_BAD_PFIF_VERSION)
    validator = PfifValidator(pfif_99_xml_file, initialize=False)
    validator.initialize_xml()
    self.assertRaises(Exception, validator.initialize_pfif_version)

  def test_root_is_bad_pfif_website(self):
    """initialize_pfif_version should raise an exception if the PFIF
    website is wrong"""
    pfif_bad_website_xml_file = StringIO.StringIO(
        ValidatorTests.XML_BAD_PFIF_WEBSITE)
    validator = PfifValidator(pfif_bad_website_xml_file, initialize=False)
    validator.initialize_xml()
    self.assertRaises(Exception, validator.initialize_pfif_version)

  # validate_root_has_child

  def test_root_has_child(self):
    """validate_root_has_child should return an empty list if the root node has
    at least one child"""
    validator = self.set_up_validator(ValidatorTests.XML_11_SMALL)
    self.assertEqual(len(validator.validate_root_has_child()), 0)

  def test_root_lacks_child(self):
    """validate_root_has_child should return a list with a message if the root
    node does not have at least one child"""
    validator = self.set_up_validator(ValidatorTests.XML_ROOT_LACKS_CHILD)
    self.assertNotEqual(len(validator.validate_root_has_child()), 0)

  # validate_root_has_mandatory_children

  def test_root_has_mandatory_children(self):
    """validate_root_has_mandatory_children should return an empty list if one
    of the children is a person"""
    validator = self.set_up_validator(ValidatorTests.XML_11_SMALL)
    self.assertEqual(len(validator.validate_root_has_mandatory_children()), 0)

  def test_root_lacks_mandatory_children(self):
    """validate_root_has_mandatory_children should return a list with a message
    if the only children are not notes or persons"""
    validator = self.set_up_validator(ValidatorTests.XML_ROOT_HAS_BAD_CHILD)
    self.assertNotEqual(
        len(validator.validate_root_has_mandatory_children()), 0)

  def test_root_has_note_child_11(self):
    """validate_root_has_mandatory_children should return a list with a message
    if the only children are notes and the version is 1.1"""
    validator = self.set_up_validator(ValidatorTests.XML_TOP_LEVEL_NOTE_11)
    self.assertNotEqual(
        len(validator.validate_root_has_mandatory_children()), 0)

  def test_root_has_note_child_12(self):
    """validate_root_has_mandatory_children should return an empty list if the
    only children are notes and the version is greater than 1.1"""
    validator = self.set_up_validator(ValidatorTests.XML_TOP_LEVEL_NOTE_12)
    self.assertEqual(len(validator.validate_root_has_mandatory_children()), 0)

  # validate_has_mandatory_children

  def test_note_has_mandatory_children(self):
    """validate_has_mandatory_children should return an empty list if it is
    given notes with all mandatory children"""
    validator = self.set_up_validator(ValidatorTests.XML_NOTES_WITH_CHILDREN)
    self.assertEqual(len(validator.validate_note_has_mandatory_children()), 0)

  def test_note_has_no_mandatory_children(self):
    """validate_has_mandatory_children should return a list with nine missing
    children when given one child of a person with no children and one top level
    note (which also must have a person_record_id) with no children."""
    validator = self.set_up_validator(ValidatorTests.XML_NOTES_NO_CHILDREN)
    self.assertEqual(len(validator.validate_note_has_mandatory_children()), 9)

  def test_person_has_mandatory_children_11(self):
    """validate_has_mandatory_children should return an empty list if it is
    given a version 1.1 person with all mandatory children"""
    validator = self.set_up_validator(
        ValidatorTests.XML_PERSON_WITH_CHILDREN_11)
    self.assertEqual(len(validator.validate_person_has_mandatory_children()), 0)

  def test_person_has_mandatory_children_13(self):
    """validate_has_mandatory_children should return an empty list if it is
    given a version 1.3 person with all mandatory children"""
    validator = self.set_up_validator(
        ValidatorTests.XML_PERSON_WITH_CHILDREN_13)
    self.assertEqual(len(validator.validate_person_has_mandatory_children()), 0)

  def test_person_has_no_mandatory_children_11(self):
    """validate_has_mandatory_children should return a list with three missing
    children when given a version 1.1 person with no children"""
    validator = self.set_up_validator(ValidatorTests.XML_11_SMALL)
    self.assertEqual(len(validator.validate_person_has_mandatory_children()), 3)

  def test_person_has_no_mandatory_children_13(self):
    """validate_has_mandatory_children should return a list with three missing
    children when given a version 1.3 person with no children"""
    validator = self.set_up_validator(ValidatorTests.XML_PERSON_NO_CHILDREN_13)
    self.assertEqual(len(validator.validate_person_has_mandatory_children()), 3)

  # validate_fields_have_correct_format

  def test_no_fields_exist(self):
    """validate_fields_have_correct_format should return an empty list when
    passed a tree with no subelements of person or note because no nodes are
    improperly formatted."""
    validator = self.set_up_validator(ValidatorTests.XML_PERSON_NO_CHILDREN_13)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 0)
    validator = self.set_up_validator(ValidatorTests.XML_NOTES_NO_CHILDREN)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 0)

  def test_all_11_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return an empty list when
    passed a tree with all 1.1 elements in the correct formats."""
    validator = self.set_up_validator(ValidatorTests.XML_11_FULL)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 0)

  #TODO(samking): test that non-ascii characters should be rejected
  def test_no_11_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return a list with every
    subnode of person and note when every such subnode is of an incorrect
    format.  This tests all fields in version 1.1 for which incorrect input is
    possible."""
    validator = self.set_up_validator(ValidatorTests.XML_INCORRECT_FORMAT_11)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 23)

  def test_all_12_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return an empty list when
    presented with a document where all fields have the correct format.  This
    tests all fields introduced or changed in 1.2; it does not test fields that
    were unchanged from 1.1."""
    validator = self.set_up_validator(ValidatorTests.XML_FULL_12)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 0)

  def test_no_12_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return a list with every
    element presented to it when all fields have an incorrect format.  This
    tests all fields introduced or changed in 1.2, except ones that are always
    accepted; it does not test fields that were unchanged from 1.1."""
    validator = self.set_up_validator(ValidatorTests.XML_INCORRECT_FORMAT_12)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 12)

  def test_all_13_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return an empty list when
    presented with a document where all fields have the correct format.  This
    tests all fields introduced or changed in 1.3; it does not test fields that
    were unchanged from 1.1 and 1.2."""
    validator = self.set_up_validator(ValidatorTests.XML_CORRECT_FORMAT_13)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 0)

  def test_no_13_fields_have_correct_format(self):
    """validate_fields_have_correct_format should return a list with every
    element presented to it when all fields have an incorrect format.  This
    tests all fields introduced or changed in 1.3, except ones that are always
    accepted; it does not test fields that were unchanged from 1.1 and 1.2."""
    validator = self.set_up_validator(ValidatorTests.XML_INCORRECT_FORMAT_13)
    self.assertEqual(len(validator.validate_fields_have_correct_format()), 1)

  # validate_unique_id
  def test_person_ids_are_unique(self):
    """validate_person_ids_are_unique should return an empty list when all
    person ids are unique"""
    validator = self.set_up_validator(ValidatorTests.XML_UNIQUE_PERSON_IDS)
    self.assertEqual(len(validator.validate_person_ids_are_unique()), 0)

  def test_note_ids_are_unique(self):
    """validate_note_ids_are_unique should return an empty list when all note
    ids are unique"""
    validator = self.set_up_validator(ValidatorTests.XML_UNIQUE_NOTE_IDS)
    self.assertEqual(len(validator.validate_note_ids_are_unique()), 0)

  def test_person_ids_are_not_unique(self):
    """validate_person_ids_are_unique should return a list with all non-unique
    person ids when there are non-unique person ids"""
    validator = self.set_up_validator(ValidatorTests.XML_DUPLICATE_PERSON_IDS)
    self.assertEqual(len(validator.validate_person_ids_are_unique()), 2)

  def test_note_ids_are_not_unique(self):
    """validate_person_ids_are_unique should return a list with all non-unique
    note ids when there are non-unique note ids"""
    validator = self.set_up_validator(ValidatorTests.XML_DUPLICATE_NOTE_IDS)
    self.assertEqual(len(validator.validate_note_ids_are_unique()), 2)

  # validate_notes_belong_to_persons

  def test_notes_belong_to_people(self):
    """validate_notes_belong_to_persons should return an empty list if all top
    level notes have a person_record_id and all notes inside persons have no
    person_record_id or the same person_record_id as the person."""
    validator = self.set_up_validator(ValidatorTests.XML_NOTES_BELONG_TO_PEOPLE)
    self.assertEqual(len(validator.validate_notes_belong_to_persons()), 0)

  def test_notes_do_not_belong_to_people(self):
    """validate_notes_belong_to_persons should return a list with all top level
    notes without a person_record_id and person_record_ids for notes that are
    under a person with a person_record_id that doesn't match the person"""
    validator = self.set_up_validator(ValidatorTests.XML_NOTES_WITHOUT_PEOPLE)
    self.assertEqual(len(validator.validate_notes_belong_to_persons()), 2)

  # validate_field_order

  def test_correct_field_order_11(self):
    """validate_person_field_order and validate_note_field_order should return
    a empty lists if all elements in all persons and notes are in the correct
    order"""
    validator = self.set_up_validator(ValidatorTests.XML_11_FULL)
    self.assertEqual(len(validator.validate_person_field_order()), 0)
    self.assertEqual(len(validator.validate_note_field_order()), 0)

  def test_omitting_fields_is_okay_11(self):
    """validate_person_field_order and validate_note_field_order should return
    a empty lists if all elements in all persons and notes are in the correct
    order, even if some elements are omitted (ie, 1,2,4 is in order even though
    3 is omitted)"""
    validator = self.set_up_validator(ValidatorTests.XML_MISSING_FIELDS_11)
    self.assertEqual(len(validator.validate_person_field_order()), 0)
    self.assertEqual(len(validator.validate_note_field_order()), 0)

  def test_incorrect_field_order_11(self):
    """validate_person_field_order and validate_note_field_order should return
    the first element in every person and note that are out of order"""
    validator = self.set_up_validator(
        ValidatorTests.XML_INCORRECT_FIELD_ORDER_11)
    self.assertEqual(len(validator.validate_person_field_order()), 3)
    self.assertEqual(len(validator.validate_note_field_order()), 2)

  def test_nonexistent_field(self):
    """validate_person_field_order and validate_note_field_order should ignore
    any fields that are not in the spec"""
    validator = self.set_up_validator(ValidatorTests.XML_EXTRANEOUS_FIELD_11)
    self.assertEqual(len(validator.validate_person_field_order()), 0)

  def test_correct_field_order_12(self):
    """validate_person_field_order and validate_note_field_order should return
    a empty lists if person_record_id comes first and any notes come last in
    persons and if note_record_id and person_record_id come first in notes."""
    validator = self.set_up_validator(ValidatorTests.XML_CORRECT_FIELD_ORDER_12)
    self.assertEqual(len(validator.validate_person_field_order()), 0)
    self.assertEqual(len(validator.validate_note_field_order()), 0)

  def test_incorrect_person_field_order_12(self):
    """validate_person_field_order should return a list with one entry for every
    person that does not have notes at the end or that does not have its
    person_record_id at the start"""
    validator = self.set_up_validator(
        ValidatorTests.XML_INCORRECT_PERSON_FIELD_ORDER_12)
    self.assertEqual(len(validator.validate_person_field_order()), 3)

  def test_incorrect_note_field_order_12(self):
    """validate_note_field_order should return a list with one entry for every
    note that does not have note_record_id and person_record_id at the start"""
    validator = self.set_up_validator(
        ValidatorTests.XML_INCORRECT_NOTE_FIELD_ORDER_12)
    self.assertEqual(len(validator.validate_note_field_order()), 4)

  def test_field_order_does_not_matter_13(self):
    """validate_person_field_order and validate_note_field_order should return
    an empty list if the version is greater than 1.2 because order doesn't
    matter"""
    validator = self.set_up_validator(ValidatorTests.XML_ODD_ORDER_13)
    self.assertEqual(len(validator.validate_person_field_order()), 0)
    self.assertEqual(len(validator.validate_note_field_order()), 0)

  # validate_expiry

  def test_unexpired_records(self):
    """validate_expired_records_removed should return an empty list when no
    records are expired"""
    validator = self.set_up_validator(
        ValidatorTests.XML_EXPIRE_99_HAS_DATA_NONSYNCED_DATES)
    not_expired_1998 = datetime.datetime(1998, 11, 1, 1, 1, 1, 1)
    utils.set_utcnow_for_test(not_expired_1998)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)
    just_not_expired = datetime.datetime(1999, 2, 4, 4, 5, 5, 0)
    utils.set_utcnow_for_test(just_not_expired)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

  def test_expired_records_with_empty_data(self):
    """validate_expired_records_removed should return an empty list when all
    expired records have empty fields instead of real data"""
    validator = self.set_up_validator(ValidatorTests.XML_EXPIRE_99_EMPTY_DATA)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

  def test_expired_records_with_omissions(self):
    """validate_expired_records_removed should return an empty list when all
    expired records omit fields instead of exposing real data"""
    validator = self.set_up_validator(ValidatorTests.XML_EXPIRE_99_NO_DATA)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

  def test_expired_records_with_unremoved_data(self):
    """validate_expired_records_removed should return a list with the
    person_record_ids of all expired records that have data that should be
    removed"""
    validator = self.set_up_validator(
        ValidatorTests.XML_EXPIRE_99_HAS_NOTE_SYNCED_DATES)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 1)
    just_expired = datetime.datetime(1999, 2, 4, 4, 5, 7)
    utils.set_utcnow_for_test(just_expired)
    self.assertEqual(len(validator.validate_expired_records_removed()), 1)

    validator = self.set_up_validator(
        ValidatorTests.XML_EXPIRE_99_HAS_DATA_SYNCED_DATES)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 1)

  def test_expired_records_with_unremoved_top_level_note(self):
    """validate_expired_records_removed should return a list with messages for
    each expired record that still had a note referring to its
    person_record_id"""
    validator = (
        self.set_up_validator(ValidatorTests.XML_EXPIRE_99_HAS_NOTE_DATA))
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 1)

  def test_expiration_placeholder_with_bad_source_entry_date(self):
    """validate_expired_records_removed should return a list with the
    person_record_ids of all expired records whose source_date and entry_date
    are not the same value and are not created within a day after expiration"""
    validator = self.set_up_validator(
        ValidatorTests.XML_EXPIRE_99_NO_DATA_NONSYNCED_DATES)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 2)

  def test_no_expiration_before_13(self):
    """validate_expired_records_removed should return an empty list when the
    version is before 1.3"""
    validator = self.set_up_validator(ValidatorTests.XML_EXPIRE_99_12)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

  def test_no_expiration_without_date(self):
    """validate_expired_records_removed should return an empty list when the
    there isn't an expiry_date"""
    validator = self.set_up_validator(ValidatorTests.XML_NO_EXPIRY_DATE)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

    validator = self.set_up_validator(ValidatorTests.XML_EMPTY_EXPIRY_DATE)
    utils.set_utcnow_for_test(ValidatorTests.EXPIRED_TIME)
    self.assertEqual(len(validator.validate_expired_records_removed()), 0)

  # validate_linked_person_records_are_matched

  def test_unlinked_records(self):
    """validate_linked_records_matched should return an empty list when
    evaluating unlinked persons"""
    validator = self.set_up_validator(ValidatorTests.XML_UNLINKED_RECORDS)
    self.assertEqual(len(validator.validate_linked_records_matched()), 0)

  def test_correctly_linked_records(self):
    """validate_linked_records_matched should return an empty list when
    evaluating two persons that each have notes with linked_person_record_ids
    pointing at each other"""
    validator = self.set_up_validator(
        ValidatorTests.XML_CORRECTLY_LINKED_RECORDS)
    self.assertEqual(len(validator.validate_linked_records_matched()), 0)

  def test_asymmetrically_linked_records(self):
    """validate_linked_records_matched should return a list with each
    note_record_id that has a linked_person_record_id that is not matched"""
    validator = self.set_up_validator(
        ValidatorTests.XML_ASYMMETRICALLY_LINKED_RECORDS)
    self.assertEqual(len(validator.validate_linked_records_matched()), 1)

  # validate_extraneous_fields

  def test_no_extra_fields(self):
    """validate_extraneous_fields should return an empty list when presented
    with a list that only includes fields in the PFIF spec"""
    validator = self.set_up_validator(ValidatorTests.XML_11_FULL)
    self.assertEqual(len(validator.validate_extraneous_fields()), 0)

  def test_gibberish_fields(self):
    """validate_extraneous_fields should return a list with every field that is
    not defined anywhere in the PFIF spec.  This includes fields defined in PFIF
    1.3 when using a 1.2 document."""
    validator = self.set_up_validator(ValidatorTests.XML_GIBBERISH_FIELDS)
    self.assertEqual(len(validator.validate_extraneous_fields()), 5)

  def test_duplicate_fields(self):
    """validate_extraneous_fields should return a list with every duplicated
    field (except for multiple <pfif:note> fields in one <pfif:person> or fields
    that are not at the same place in the tree, such as a note and a person with
    a person_record_id or two different notes)"""
    validator = self.set_up_validator(ValidatorTests.XML_DUPLICATE_FIELDS)
    self.assertEqual(len(validator.validate_extraneous_fields()), 3)

  def test_top_level_note_11(self):
    """validate_extraneous_fields should return a list with every top level note
    in a PFIF 1.1 document"""
    validator = self.set_up_validator(
        ValidatorTests.XML_TOP_LEVEL_NOTE_PERSON_11)
    self.assertEqual(len(validator.validate_extraneous_fields()), 2)

  # run_validations

  def test_run_validations_without_errors(self):
    """run_validations should return an empty message list when passed a valid
    file"""
    validation_file = StringIO.StringIO(ValidatorTests.XML_11_FULL)
    self.assertEqual(len(PfifValidator.run_validations(validation_file)), 0)

  def test_run_validations_with_errors(self):
    """run_validations should return a message list with three errors when the
    root doesn't have a mandatory child and there are two duplicate nodes"""
    validation_file = StringIO.StringIO(
        ValidatorTests.XML_TWO_DUPLICATE_NO_CHILD)
    self.assertEqual(len(PfifValidator.run_validations(validation_file)), 3)

  # unicode

  def test_unicode_works(self):
    """none of the validations should fail when processing a field that includes
    unicode text."""
    validation_file = StringIO.StringIO(ValidatorTests.XML_UNICODE_12)
    PfifValidator.print_messages(PfifValidator.run_validations(validation_file))
    self.assertEqual(len(PfifValidator.run_validations(validation_file)), 0)

if __name__ == '__main__':
  unittest.main()
