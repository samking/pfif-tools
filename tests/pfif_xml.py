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

"""PFIF XML for use with tests."""

# This file has raw XML that should NOT follow the 80 character limit, so
# disable that lint check for the whole file.
# pylint: disable=c0301

XML_INVALID = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.2">
  <pfif:person>"""

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
    <pfif:photo_url>https://user:pass@host:999/url_path?var=val#hash</pfif:photo_url>
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
      <pfif:entry_date>1234-56-78T90:12:34Z</pfif:entry_date>
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

XML_DUPLICATE_PERSON_AND_NOTE_ID = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/1</pfif:person_record_id>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>example.org/1</pfif:note_record_id>
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
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:foo />
    <pfif:other />
  </pfif:person>
</pfif:pfif>"""

XML_EXTRANEOUS_FIELD_11_MAP = {
    'example.org/person' : {'person_record_id' : 'example.org/person',
                            'foo' : '',
                            'other' : ''}}

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

XML_MANDATORY_13 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:full_name>Full Name</pfif:full_name>
    <pfif:note>
      <pfif:person_record_id>example.org/person</pfif:person_record_id>
      <pfif:note_record_id>example.org/sub-note</pfif:note_record_id>
      <pfif:author_name>Author Name</pfif:author_name>
      <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
      <pfif:text>Lots of Text</pfif:text>
    </pfif:note>
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>example.org/non-sub-note</pfif:note_record_id>
    <pfif:person_record_id>example.org/person2</pfif:person_record_id>
    <pfif:author_name>Author Name</pfif:author_name>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:text>Lots of Text</pfif:text>
  </pfif:note>
</pfif:pfif>"""

XML_MANDATORY_13_SUBNOTE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:full_name>Full Name</pfif:full_name>
    <pfif:note>
      <pfif:note_record_id>example.org/note</pfif:note_record_id>
      <pfif:author_name>Author Name</pfif:author_name>
      <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
      <pfif:text>Lots of Text</pfif:text>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

XML_MANDATORY_13_NONSUB = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:full_name>Full Name</pfif:full_name>
  </pfif:person>
  <pfif:note>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:note_record_id>example.org/note</pfif:note_record_id>
    <pfif:author_name>Author Name</pfif:author_name>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:text>Lots of Text</pfif:text>
  </pfif:note>
</pfif:pfif>"""

XML_MANDATORY_13_MAP = {
    'example.org/person' : {'person_record_id' : 'example.org/person',
                            'source_date' : '1234-56-78T90:12:34Z',
                            'full_name' : 'Full Name'},
    'example.org/sub-note' : {'person_record_id' : 'example.org/person',
                              'note_record_id' : 'example.org/sub-note',
                              'source_date' : '1234-56-78T90:12:34Z',
                              'author_name' : 'Author Name',
                              'text' : 'Lots of Text'},
    'example.org/non-sub-note' : {'person_record_id' : 'example.org/person2',
                                  'note_record_id' : 'example.org/non-sub-note',
                                  'source_date' : '1234-56-78T90:12:34Z',
                                  'author_name' : 'Author Name',
                                  'text' : 'Lots of Text'}}

# full_name and author_name are ignored
XML_MANDATORY_13_IGNORE_NAMES_MAP = {
    'example.org/person' : {'person_record_id' : 'example.org/person',
                            'source_date' : '1234-56-78T90:12:34Z'},
    'example.org/sub-note' : {'person_record_id' : 'example.org/person',
                              'note_record_id' : 'example.org/sub-note',
                              'source_date' : '1234-56-78T90:12:34Z',
                              'text' : 'Lots of Text'},
    'example.org/non-sub-note' : {'person_record_id' : 'example.org/person2',
                                  'note_record_id' : 'example.org/non-sub-note',
                                  'source_date' : '1234-56-78T90:12:34Z',
                                  'text' : 'Lots of Text'}}

XML_BLANK_FIELDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date></pfif:source_date>
  </pfif:person>
</pfif:pfif>"""

XML_BLANK_FIELDS_MAP =  {
    'example.org/person' : {'person_record_id' : 'example.org/person',
                            'source_date' : ''}}

XML_ONLY_RECORD_MAP =  {
    'example.org/person' : {'person_record_id' : 'example.org/person'}}

XML_ONE_BLANK_RECORD_ID = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id></pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

XML_ONE_PERSON_ONE_FIELD = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

XML_TWO_PERSONS_ONE_FIELD = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/person2</pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

XML_ONE_PERSON_TWO_FIELDS = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
  </pfif:person>
</pfif:pfif>"""

XML_ONE_PERSON_TWO_FIELDS_NEW_VALUE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person</pfif:person_record_id>
    <pfif:source_date>abcd1234-56-78T90:12:34Z</pfif:source_date>
  </pfif:person>
</pfif:pfif>"""

XML_ADDED_DELETED_CHANGED_1 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person1</pfif:person_record_id>
    <pfif:source_date>1234-56-78T90:12:34Z</pfif:source_date>
    <pfif:foo />
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/person2</pfif:person_record_id>
  </pfif:person>
</pfif:pfif>"""

XML_ADDED_DELETED_CHANGED_2 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/person1</pfif:person_record_id>
    <pfif:source_date>1234-56-78t90:12:34z</pfif:source_date>
    <pfif:bar />
  </pfif:person>
  <pfif:note>
    <pfif:note_record_id>example.org/person2</pfif:note_record_id>
  </pfif:note>
</pfif:pfif>"""

XML_EMPTY_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:pfif="http://zesty.ca/pfif/1.3">
  <id>http://pfif.example.org/atom/empty</id>
  <title>Example PFIF Atom Feed</title>
  <subtitle>Produced by Exemplar Examplers</subtitle>
  <updated>1983-03-07T01:23:45Z</updated>
  <link rel='self'>http://pfif.example.org/atom/empty</link>
</feed>"""

# Used in API interoperability tests.  Generated by make_test_data.py.

XML_TEST_ONE_PERSON = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T00:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0001</pfif:author_name>
    <pfif:author_email>0001@example.com</pfif:author_email>
    <pfif:author_phone>00000001</pfif:author_phone>
    <pfif:source_name>source_name0001</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0001</pfif:source_url>
    <pfif:full_name>full_name0001</pfif:full_name>
    <pfif:first_name>first_name0001</pfif:first_name>
    <pfif:last_name>last_name0001</pfif:last_name>
    <pfif:sex>female</pfif:sex>
    <pfif:age>34-56</pfif:age>
    <pfif:home_street>home_street0001</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0001</pfif:home_neighborhood>
    <pfif:home_city>home_city0001</pfif:home_city>
    <pfif:home_state>AE-AJ</pfif:home_state>
    <pfif:home_postal_code>00001</pfif:home_postal_code>
    <pfif:home_country>AF</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0001</pfif:photo_url>
    <pfif:other>description: 0001</pfif:other>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_ONE_PERSON_ONE_NOTE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T00:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0001</pfif:author_name>
    <pfif:author_email>0001@example.com</pfif:author_email>
    <pfif:author_phone>00000001</pfif:author_phone>
    <pfif:source_name>source_name0001</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0001</pfif:source_url>
    <pfif:full_name>full_name0001</pfif:full_name>
    <pfif:first_name>first_name0001</pfif:first_name>
    <pfif:last_name>last_name0001</pfif:last_name>
    <pfif:sex>female</pfif:sex>
    <pfif:age>34-56</pfif:age>
    <pfif:home_street>home_street0001</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0001</pfif:home_neighborhood>
    <pfif:home_city>home_city0001</pfif:home_city>
    <pfif:home_state>AE-AJ</pfif:home_state>
    <pfif:home_postal_code>00001</pfif:home_postal_code>
    <pfif:home_country>AF</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0001</pfif:photo_url>
    <pfif:other>description: 0001</pfif:other>
    <pfif:note>
      <pfif:note_record_id>example.org/n0101</pfif:note_record_id>
      <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
      <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
      <pfif:author_name>author_name0101</pfif:author_name>
      <pfif:author_email>0101@example.com</pfif:author_email>
      <pfif:author_phone>00000101</pfif:author_phone>
      <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
      <pfif:found>false</pfif:found>
      <pfif:status>information_sought</pfif:status>
      <pfif:last_known_location>last_known_location0101</pfif:last_known_location>
      <pfif:text>text0101</pfif:text>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_ONE_NOTE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/n0101</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name0101</pfif:author_name>
    <pfif:author_email>0101@example.com</pfif:author_email>
    <pfif:author_phone>00000101</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>information_sought</pfif:status>
    <pfif:last_known_location>last_known_location0101</pfif:last_known_location>
    <pfif:text>text0101</pfif:text>
  </pfif:note>
</pfif:pfif>"""

XML_TEST_PERSON_TWO_THREE = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T05:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T00:30:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0002</pfif:author_name>
    <pfif:author_email>0002@example.com</pfif:author_email>
    <pfif:author_phone>00000002</pfif:author_phone>
    <pfif:source_name>source_name0002</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0002</pfif:source_url>
    <pfif:full_name>full_name0002</pfif:full_name>
    <pfif:first_name>first_name0002</pfif:first_name>
    <pfif:last_name>last_name0002</pfif:last_name>
    <pfif:sex>male</pfif:sex>
    <pfif:age>2</pfif:age>
    <pfif:home_street>home_street0002</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0002</pfif:home_neighborhood>
    <pfif:home_city>home_city0002</pfif:home_city>
    <pfif:home_state>AE-AZ</pfif:home_state>
    <pfif:home_postal_code>00002</pfif:home_postal_code>
    <pfif:home_country>AX</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0002</pfif:photo_url>
    <pfif:other>description: 0002</pfif:other>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/p0003</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T06:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T01:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0003</pfif:author_name>
    <pfif:author_email>0003@example.com</pfif:author_email>
    <pfif:author_phone>00000003</pfif:author_phone>
    <pfif:source_name>source_name0003</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0003</pfif:source_url>
    <pfif:full_name>full_name0003</pfif:full_name>
    <pfif:first_name>first_name0003</pfif:first_name>
    <pfif:last_name>last_name0003</pfif:last_name>
    <pfif:sex>other</pfif:sex>
    <pfif:age>3</pfif:age>
    <pfif:home_street>home_street0003</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0003</pfif:home_neighborhood>
    <pfif:home_city>home_city0003</pfif:home_city>
    <pfif:home_state>AE-DU</pfif:home_state>
    <pfif:home_postal_code>00003</pfif:home_postal_code>
    <pfif:home_country>AL</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0003</pfif:photo_url>
    <pfif:other>description: 0003</pfif:other>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_PERSON_FOUR_THROUGH_SIX = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0004</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T07:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T01:30:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0004</pfif:author_name>
    <pfif:author_email>0004@example.com</pfif:author_email>
    <pfif:author_phone>00000004</pfif:author_phone>
    <pfif:source_name>source_name0004</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0004</pfif:source_url>
    <pfif:full_name>full_name0004</pfif:full_name>
    <pfif:first_name>first_name0004</pfif:first_name>
    <pfif:last_name>last_name0004</pfif:last_name>
    <pfif:age>4</pfif:age>
    <pfif:home_street>home_street0004</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0004</pfif:home_neighborhood>
    <pfif:home_city>home_city0004</pfif:home_city>
    <pfif:home_state>AE-FU</pfif:home_state>
    <pfif:home_postal_code>00004</pfif:home_postal_code>
    <pfif:home_country>DZ</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0004</pfif:photo_url>
    <pfif:other>description: 0004</pfif:other>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/p0005</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T08:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T02:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0005</pfif:author_name>
    <pfif:author_email>0005@example.com</pfif:author_email>
    <pfif:author_phone>00000005</pfif:author_phone>
    <pfif:source_name>source_name0005</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0005</pfif:source_url>
    <pfif:full_name>full_name0005</pfif:full_name>
    <pfif:first_name>first_name0005</pfif:first_name>
    <pfif:last_name>last_name0005</pfif:last_name>
    <pfif:sex>female</pfif:sex>
    <pfif:age>5</pfif:age>
    <pfif:home_street>home_street0005</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0005</pfif:home_neighborhood>
    <pfif:home_city>home_city0005</pfif:home_city>
    <pfif:home_state>AE-RK</pfif:home_state>
    <pfif:home_postal_code>00005</pfif:home_postal_code>
    <pfif:home_country>AS</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0005</pfif:photo_url>
    <pfif:other>description: 0005</pfif:other>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/p0006</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T09:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T02:30:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0006</pfif:author_name>
    <pfif:author_email>0006@example.com</pfif:author_email>
    <pfif:author_phone>00000006</pfif:author_phone>
    <pfif:source_name>source_name0006</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0006</pfif:source_url>
    <pfif:full_name>full_name0006</pfif:full_name>
    <pfif:first_name>first_name0006</pfif:first_name>
    <pfif:last_name>last_name0006</pfif:last_name>
    <pfif:sex>male</pfif:sex>
    <pfif:age>6</pfif:age>
    <pfif:home_street>home_street0006</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0006</pfif:home_neighborhood>
    <pfif:home_city>home_city0006</pfif:home_city>
    <pfif:home_state>AE-SH</pfif:home_state>
    <pfif:home_postal_code>00006</pfif:home_postal_code>
    <pfif:home_country>AD</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0006</pfif:photo_url>
    <pfif:other>description: 0006</pfif:other>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_TWO_PERSONS_TWO_NOTES = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T00:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0001</pfif:author_name>
    <pfif:author_email>0001@example.com</pfif:author_email>
    <pfif:author_phone>00000001</pfif:author_phone>
    <pfif:source_name>source_name0001</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0001</pfif:source_url>
    <pfif:full_name>full_name0001</pfif:full_name>
    <pfif:first_name>first_name0001</pfif:first_name>
    <pfif:last_name>last_name0001</pfif:last_name>
    <pfif:sex>female</pfif:sex>
    <pfif:age>34-56</pfif:age>
    <pfif:home_street>home_street0001</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0001</pfif:home_neighborhood>
    <pfif:home_city>home_city0001</pfif:home_city>
    <pfif:home_state>AE-AJ</pfif:home_state>
    <pfif:home_postal_code>00001</pfif:home_postal_code>
    <pfif:home_country>AF</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0001</pfif:photo_url>
    <pfif:other>description: 0001</pfif:other>
    <pfif:note>
      <pfif:note_record_id>example.org/n0101</pfif:note_record_id>
      <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
      <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
      <pfif:author_name>author_name0101</pfif:author_name>
      <pfif:author_email>0101@example.com</pfif:author_email>
      <pfif:author_phone>00000101</pfif:author_phone>
      <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
      <pfif:found>false</pfif:found>
      <pfif:status>information_sought</pfif:status>
      <pfif:last_known_location>last_known_location0101</pfif:last_known_location>
      <pfif:text>text0101</pfif:text>
    </pfif:note>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T05:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-01T00:30:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0002</pfif:author_name>
    <pfif:author_email>0002@example.com</pfif:author_email>
    <pfif:author_phone>00000002</pfif:author_phone>
    <pfif:source_name>source_name0002</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0002</pfif:source_url>
    <pfif:full_name>full_name0002</pfif:full_name>
    <pfif:first_name>first_name0002</pfif:first_name>
    <pfif:last_name>last_name0002</pfif:last_name>
    <pfif:sex>male</pfif:sex>
    <pfif:age>2</pfif:age>
    <pfif:home_street>home_street0002</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0002</pfif:home_neighborhood>
    <pfif:home_city>home_city0002</pfif:home_city>
    <pfif:home_state>AE-AZ</pfif:home_state>
    <pfif:home_postal_code>00002</pfif:home_postal_code>
    <pfif:home_country>AX</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0002</pfif:photo_url>
    <pfif:other>description: 0002</pfif:other>
    <pfif:note>
      <pfif:note_record_id>example.org/n0201</pfif:note_record_id>
      <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
      <pfif:linked_person_record_id>example.org/p0003</pfif:linked_person_record_id>
      <pfif:entry_date>2011-02-03T04:35:06Z</pfif:entry_date>
      <pfif:author_name>author_name0201</pfif:author_name>
      <pfif:author_email>0201@example.com</pfif:author_email>
      <pfif:author_phone>00000201</pfif:author_phone>
      <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
      <pfif:found>true</pfif:found>
      <pfif:status>information_sought</pfif:status>
      <pfif:email_of_found_person>0201@example.com</pfif:email_of_found_person>
      <pfif:phone_of_found_person>00000201</pfif:phone_of_found_person>
      <pfif:last_known_location>last_known_location0201</pfif:last_known_location>
      <pfif:text>text0201</pfif:text>
    </pfif:note>
    <pfif:note>
      <pfif:note_record_id>example.org/n0202</pfif:note_record_id>
      <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
      <pfif:entry_date>2011-02-03T05:05:06Z</pfif:entry_date>
      <pfif:author_name>author_name0202</pfif:author_name>
      <pfif:author_email>0202@example.com</pfif:author_email>
      <pfif:author_phone>00000202</pfif:author_phone>
      <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
      <pfif:found>false</pfif:found>
      <pfif:status>is_note_author</pfif:status>
      <pfif:last_known_location>last_known_location0202</pfif:last_known_location>
      <pfif:text>text0202</pfif:text>
    </pfif:note>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_TWO_NOTES_FOR_PERSONS_ONE_TWO = (
"""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/n0201</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
    <pfif:linked_person_record_id>example.org/p0003</pfif:linked_person_record_id>
    <pfif:entry_date>2011-02-03T04:35:06Z</pfif:entry_date>
    <pfif:author_name>author_name0201</pfif:author_name>
    <pfif:author_email>0201@example.com</pfif:author_email>
    <pfif:author_phone>00000201</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>true</pfif:found>
    <pfif:status>information_sought</pfif:status>
    <pfif:email_of_found_person>0201@example.com</pfif:email_of_found_person>
    <pfif:phone_of_found_person>00000201</pfif:phone_of_found_person>
    <pfif:last_known_location>last_known_location0201</pfif:last_known_location>
    <pfif:text>text0201</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n0202</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0002</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T05:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name0202</pfif:author_name>
    <pfif:author_email>0202@example.com</pfif:author_email>
    <pfif:author_phone>00000202</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>is_note_author</pfif:status>
    <pfif:last_known_location>last_known_location0202</pfif:last_known_location>
    <pfif:text>text0202</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n0101</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0001</pfif:person_record_id>
    <pfif:entry_date>2011-02-03T04:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name0101</pfif:author_name>
    <pfif:author_email>0101@example.com</pfif:author_email>
    <pfif:author_phone>00000101</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>information_sought</pfif:status>
    <pfif:last_known_location>last_known_location0101</pfif:last_known_location>
    <pfif:text>text0101</pfif:text>
  </pfif:note>
</pfif:pfif>""")

XML_TEST_PERSONS_622_623 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0622</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T01:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-13T22:30:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0622</pfif:author_name>
    <pfif:author_email>0622@example.com</pfif:author_email>
    <pfif:author_phone>00000622</pfif:author_phone>
    <pfif:source_name>source_name0622</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0622</pfif:source_url>
    <pfif:full_name>full_name0622</pfif:full_name>
    <pfif:first_name>first_name0622</pfif:first_name>
    <pfif:last_name>last_name0622</pfif:last_name>
    <pfif:sex>male</pfif:sex>
    <pfif:date_of_birth>1951-02-03</pfif:date_of_birth>
    <pfif:home_street>home_street0622</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0622</pfif:home_neighborhood>
    <pfif:home_city>home_city0622</pfif:home_city>
    <pfif:home_state>CL-CO</pfif:home_state>
    <pfif:home_postal_code>00622</pfif:home_postal_code>
    <pfif:home_country>LR</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0622</pfif:photo_url>
    <pfif:other>description: 0622</pfif:other>
  </pfif:person>
  <pfif:person>
    <pfif:person_record_id>example.org/p0623</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T02:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-13T23:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0623</pfif:author_name>
    <pfif:author_email>0623@example.com</pfif:author_email>
    <pfif:author_phone>00000623</pfif:author_phone>
    <pfif:source_name>source_name0623</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0623</pfif:source_url>
    <pfif:full_name>full_name0623</pfif:full_name>
    <pfif:first_name>first_name0623</pfif:first_name>
    <pfif:last_name>last_name0623</pfif:last_name>
    <pfif:sex>other</pfif:sex>
    <pfif:date_of_birth>1951-03-05</pfif:date_of_birth>
    <pfif:home_street>home_street0623</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0623</pfif:home_neighborhood>
    <pfif:home_city>home_city0623</pfif:home_city>
    <pfif:home_state>CL-LI</pfif:home_state>
    <pfif:home_postal_code>00623</pfif:home_postal_code>
    <pfif:home_country>LY</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0623</pfif:photo_url>
    <pfif:other>description: 0623</pfif:other>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_NOTES_5017_THROUGH_5118_IN_RANGE_14_18 = (
"""<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/n5114</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0051</pfif:person_record_id>
    <pfif:entry_date>2011-03-02T00:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name5114</pfif:author_name>
    <pfif:author_email>5114@example.com</pfif:author_email>
    <pfif:author_phone>00005114</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>true</pfif:found>
    <pfif:status>is_note_author</pfif:status>
    <pfif:email_of_found_person>5114@example.com</pfif:email_of_found_person>
    <pfif:phone_of_found_person>00005114</pfif:phone_of_found_person>
    <pfif:last_known_location>last_known_location5114</pfif:last_known_location>
    <pfif:text>text5114</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5115</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0051</pfif:person_record_id>
    <pfif:entry_date>2011-03-02T00:35:06Z</pfif:entry_date>
    <pfif:author_name>author_name5115</pfif:author_name>
    <pfif:author_email>5115@example.com</pfif:author_email>
    <pfif:author_phone>00005115</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>believed_alive</pfif:status>
    <pfif:last_known_location>last_known_location5115</pfif:last_known_location>
    <pfif:text>text5115</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5116</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0051</pfif:person_record_id>
    <pfif:entry_date>2011-03-02T01:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name5116</pfif:author_name>
    <pfif:author_email>5116@example.com</pfif:author_email>
    <pfif:author_phone>00005116</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>true</pfif:found>
    <pfif:status>believed_missing</pfif:status>
    <pfif:email_of_found_person>5116@example.com</pfif:email_of_found_person>
    <pfif:phone_of_found_person>00005116</pfif:phone_of_found_person>
    <pfif:last_known_location>last_known_location5116</pfif:last_known_location>
    <pfif:text>text5116</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5117</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0051</pfif:person_record_id>
    <pfif:entry_date>2011-03-02T01:35:06Z</pfif:entry_date>
    <pfif:author_name>author_name5117</pfif:author_name>
    <pfif:author_email>5117@example.com</pfif:author_email>
    <pfif:author_phone>00005117</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>believed_dead</pfif:status>
    <pfif:last_known_location>last_known_location5117</pfif:last_known_location>
    <pfif:text>text5117</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5118</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0051</pfif:person_record_id>
    <pfif:entry_date>2011-03-02T02:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name5118</pfif:author_name>
    <pfif:author_email>5118@example.com</pfif:author_email>
    <pfif:author_phone>00005118</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>true</pfif:found>
    <pfif:email_of_found_person>5118@example.com</pfif:email_of_found_person>
    <pfif:phone_of_found_person>00005118</pfif:phone_of_found_person>
    <pfif:last_known_location>last_known_location5118</pfif:last_known_location>
    <pfif:text>text5118</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5017</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0050</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T00:35:06Z</pfif:entry_date>
    <pfif:author_name>author_name5017</pfif:author_name>
    <pfif:author_email>5017@example.com</pfif:author_email>
    <pfif:author_phone>00005017</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>true</pfif:found>
    <pfif:status>believed_dead</pfif:status>
    <pfif:email_of_found_person>5017@example.com</pfif:email_of_found_person>
    <pfif:phone_of_found_person>00005017</pfif:phone_of_found_person>
    <pfif:last_known_location>last_known_location5017</pfif:last_known_location>
    <pfif:text>text5017</pfif:text>
  </pfif:note>
  <pfif:note>
    <pfif:note_record_id>example.org/n5018</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0050</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T01:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name5018</pfif:author_name>
    <pfif:author_email>5018@example.com</pfif:author_email>
    <pfif:author_phone>00005018</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:last_known_location>last_known_location5018</pfif:last_known_location>
    <pfif:text>text5018</pfif:text>
  </pfif:note>
</pfif:pfif>""")

XML_TEST_PERSON_621 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:person>
    <pfif:person_record_id>example.org/p0621</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T00:05:06Z</pfif:entry_date>
    <pfif:expiry_date>2011-04-13T22:00:00Z</pfif:expiry_date>
    <pfif:author_name>author_name0621</pfif:author_name>
    <pfif:author_email>0621@example.com</pfif:author_email>
    <pfif:author_phone>00000621</pfif:author_phone>
    <pfif:source_name>source_name0621</pfif:source_name>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:source_url>http://example.org/0621</pfif:source_url>
    <pfif:full_name>full_name0621</pfif:full_name>
    <pfif:first_name>first_name0621</pfif:first_name>
    <pfif:last_name>last_name0621</pfif:last_name>
    <pfif:sex>female</pfif:sex>
    <pfif:date_of_birth>1951-01-04</pfif:date_of_birth>
    <pfif:home_street>home_street0621</pfif:home_street>
    <pfif:home_neighborhood>home_neighborhood0621</pfif:home_neighborhood>
    <pfif:home_city>home_city0621</pfif:home_city>
    <pfif:home_state>CL-BI</pfif:home_state>
    <pfif:home_postal_code>00621</pfif:home_postal_code>
    <pfif:home_country>LS</pfif:home_country>
    <pfif:photo_url>http://photo.example.org/0621</pfif:photo_url>
    <pfif:other>description: 0621</pfif:other>
  </pfif:person>
</pfif:pfif>"""

XML_TEST_NOTE_5016 = """<?xml version="1.0" encoding="UTF-8"?>
<pfif:pfif xmlns:pfif="http://zesty.ca/pfif/1.3">
  <pfif:note>
    <pfif:note_record_id>example.org/n5016</pfif:note_record_id>
    <pfif:person_record_id>example.org/p0050</pfif:person_record_id>
    <pfif:entry_date>2011-03-01T00:05:06Z</pfif:entry_date>
    <pfif:author_name>author_name5016</pfif:author_name>
    <pfif:author_email>5016@example.com</pfif:author_email>
    <pfif:author_phone>00005016</pfif:author_phone>
    <pfif:source_date>2011-01-01T01:01:01Z</pfif:source_date>
    <pfif:found>false</pfif:found>
    <pfif:status>believed_missing</pfif:status>
    <pfif:last_known_location>last_known_location5016</pfif:last_known_location>
    <pfif:text>text5016</pfif:text>
  </pfif:note>
</pfif:pfif>"""

# pylint: enable=c0301
