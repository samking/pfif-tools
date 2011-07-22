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

"""Validates that text follows the PFIF XML Specification at zesty.ca/pfif"""

import lxml.etree as ET
import re
import utils
from urlparse import urlparse
import datetime
import inspect
import sys

class Message:
  """A container for information about an error or warning message"""

  def __init__(self, main_text, is_error=True, xml_line_number=None,
               xml_element_text=None, person_record_id=None,
               note_record_id=None):
    self.main_text = main_text
    self.is_error = is_error
    self.xml_line_number = xml_line_number
    self.xml_element_text = xml_element_text
    self.person_record_id = person_record_id
    self.note_record_id  = note_record_id

class PfifValidator:
  """A validator that can run tests on a PFIF XML file."""

  # A map from version to parent : required-children mappings.
  MANDATORY_CHILDREN = {1.1 : {'person' : ['person_record_id', 'first_name',
                                           'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text'],
                               'top_note' : ['person_record_id',
                                             'note_record_id', 'author_name',
                                             'source_date', 'text']
                              },
                        1.2 : {'person' : ['person_record_id', 'first_name',
                                           'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text'],
                               'top_note' : ['person_record_id',
                                             'note_record_id', 'author_name',
                                             'source_date', 'text']
                              },
                        1.3 : {'person' : ['person_record_id', 'source_date',
                                         'full_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text'],
                               'top_note' : ['person_record_id',
                                             'note_record_id', 'author_name',
                                             'source_date', 'text']
                              }
                       }

  # regular expressions to match valid formats for each field type
  # Domain Name Spec: http://tools.ietf.org/html/rfc1034 (see sections 3.1, 3.5)
  # A label is a sequence of 1-63 letters, digits, or hyphens that starts with a
  # letter and ends with a letter or number.  A domain name is any number of
  # labels, separated by dots, that total up to 255 characters.
  # We allow the final dot to be optional since pepole usually omit it.
  # TODO(samking): require domain name to be at most 255 characters
  DOMAIN_LABEL = r'[a-zA-Z]([-a-zA-Z0-9]{0,61}[a-zA-Z0-9])?'
  DOMAIN_NAME = r'(' + DOMAIN_LABEL + r'\.)*' + DOMAIN_LABEL + '\.?'
  RECORD_ID = r'^' + DOMAIN_NAME + r'/.+$'
  DATE = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$'
  TEXT = r'^.*$'
  EMAIL = r'^.+@.+$' #TODO(samking): make more specific
  # Allow there to be any number of delimiters (space, hyphen, dot, plus, and
  # parentheses) around each digit
  # Phone numbers can also have an extension if there is an x or pound sign at
  # the end of the number.
  # We are permissive about delimiters because validation on a missing person
  # database could annoy users, and we are permissive about number of digits
  # allowed because there are multiple standards (ie,
  # http://tools.ietf.org/html/rfc4933#section-2.5 and
  # http://en.wikipedia.org/wiki/E.164)
  PHONE = r'^([-\.+() ]*\d[-\.+() ]*)+([#x]\d+)?$'
  URL = 'URL'
  CAPS = r'^[A-Z ]+$'
  US_STATE = r'^[A-Z][A-Z]$'
  ISO31661_COUNTRY = US_STATE
  ISO31662_STATE = r'^[a-zA-Z0-9]{1,3}$'
  INTEGER = r'^\d+$'
  BOOLEAN = r'^(true|false)$'
  STATUS = r'^(information_sought|is_note_author|believed_alive|' \
           r'believed_missing|believed_dead)$'
  SEX = r'^(male|female|other)$'
  # YYYY, YYYY-MM, or YYYY-MM-DD
  DATE_OF_BIRTH = r'^\d{4}(-\d{2}(-\d{2})?)?$'
  # one integer or a range between two integers
  AGE = r'^\d+(-\d+)?$'

  # a map from field name to a regular expression matching valid formats for
  # that field
  FORMATS = {1.1 : {'person' : {'person_record_id' : RECORD_ID,
                                'entry_date' : DATE,
                                'author_name' : TEXT,
                                'author_email' : EMAIL,
                                'author_phone' : PHONE,
                                'source_name' : TEXT,
                                'source_date' : DATE,
                                'source_url' : URL,
                                'first_name' : CAPS,
                                'last_name' : CAPS,
                                'home_city' : CAPS,
                                'home_state' : US_STATE,
                                'home_neighborhood' : CAPS,
                                'home_street' : CAPS,
                                'home_zip' : INTEGER,
                                'photo_url' : URL,
                                'other' : TEXT
                               },
                    'note' : {'note_record_id' : RECORD_ID,
                              'entry_date' : DATE,
                              'author_name' : TEXT,
                              'author_email' : EMAIL,
                              'author_phone' : PHONE,
                              'source_date' : DATE,
                              'found' : BOOLEAN,
                              'email_of_found_person' : EMAIL,
                              'phone_of_found_person' : PHONE,
                              'last_known_location' : TEXT,
                              'text' : TEXT
                             }
                   },
             1.2 : {'person' : {'person_record_id' : RECORD_ID,
                                'entry_date' : DATE,
                                'author_name' : TEXT,
                                'author_email' : EMAIL,
                                'author_phone' : PHONE,
                                'source_name' : TEXT,
                                'source_date' : DATE,
                                'source_url' : URL,
                                'first_name' : TEXT,
                                'last_name' : TEXT,
                                'sex' : SEX,
                                'date_of_birth' : DATE_OF_BIRTH,
                                'age' : AGE,
                                'home_street' : TEXT,
                                'home_city' : TEXT,
                                'home_neighborhood' : TEXT,
                                'home_state' : ISO31662_STATE,
                                'home_postal_code' : INTEGER,
                                'home_country' : ISO31661_COUNTRY,
                                'photo_url' : URL,
                                'other' : TEXT
                               },
                    'note' : {'note_record_id' : RECORD_ID,
                              'person_record_id' : RECORD_ID,
                              'linked_person_record_id' : RECORD_ID,
                              'entry_date' : DATE,
                              'author_name' : TEXT,
                              'author_email' : EMAIL,
                              'author_phone' : PHONE,
                              'source_date' : DATE,
                              'found' : BOOLEAN,
                              'status' : STATUS,
                              'email_of_found_person' : EMAIL,
                              'phone_of_found_person' : PHONE,
                              'last_known_location' : TEXT,
                              'text' : TEXT
                             }
                   },
             1.3 : {'person' : {'person_record_id' : RECORD_ID,
                                'entry_date' : DATE,
                                'expiry_date' : DATE,
                                'author_name' : TEXT,
                                'author_email' : EMAIL,
                                'author_phone' : PHONE,
                                'source_name' : TEXT,
                                'source_date' : DATE,
                                'source_url' : URL,
                                'full_name' : TEXT,
                                'first_name' : TEXT,
                                'last_name' : TEXT,
                                'sex' : SEX,
                                'date_of_birth' : DATE_OF_BIRTH,
                                'age' : AGE,
                                'home_street' : TEXT,
                                'home_city' : TEXT,
                                'home_neighborhood' : TEXT,
                                'home_state' : ISO31662_STATE,
                                'home_postal_code' : INTEGER,
                                'home_country' : ISO31661_COUNTRY,
                                'photo_url' : URL,
                                'other' : TEXT
                               },
                    'note' : {'note_record_id' : RECORD_ID,
                              'person_record_id' : RECORD_ID,
                              'linked_person_record_id' : RECORD_ID,
                              'entry_date' : DATE,
                              'author_name' : TEXT,
                              'author_email' : EMAIL,
                              'author_phone' : PHONE,
                              'source_date' : DATE,
                              'found' : BOOLEAN,
                              'status' : STATUS,
                              'email_of_found_person' : EMAIL,
                              'phone_of_found_person' : PHONE,
                              'last_known_location' : TEXT,
                              'text' : TEXT
                             }
                   }
            }

  FIELD_ORDER = {1.1 : {'person' : {'person_record_id' : 1,
                                    'entry_date': 2,
                                    'author_name' : 3,
                                    'author_email' : 4,
                                    'author_phone' : 5,
                                    'source_name' : 6,
                                    'source_date' : 7,
                                    'source_url' : 8,
                                    'first_name' : 9,
                                    'last_name' : 10,
                                    'home_city' : 11,
                                    'home_state' : 12,
                                    'home_neighborhood' : 13,
                                    'home_street' : 14,
                                    'home_zip' : 15,
                                    'photo_url' : 16,
                                    'other' : 17,
                                    'note' : 18
                                   },
                        'note' : {'note_record_id' : 1,
                                  'entry_date' : 2,
                                  'author_name' : 3,
                                  'author_email' : 4,
                                  'author_phone' : 5,
                                  'source_date' : 6,
                                  'found' : 7,
                                  'email_of_found_person' : 8,
                                  'phone_of_found_person' : 9,
                                  'last_known_location' : 10,
                                  'text' : 11
                                 }
                       },
                 1.2 : {'person' : {'person_record_id' : 1,
                                    'entry_date': 2,
                                    'author_name' : 2,
                                    'author_email' : 2,
                                    'author_phone' : 2,
                                    'source_name' : 2,
                                    'source_date' : 2,
                                    'source_url' : 2,
                                    'first_name' : 2,
                                    'last_name' : 2,
                                    'home_city' : 2,
                                    'home_state' : 2,
                                    'home_neighborhood' : 2,
                                    'home_street' : 2,
                                    'home_postal_code' : 2,
                                    'home_country' : 2,
                                    'sex' : 2,
                                    'date_of_birth' : 2,
                                    'age' : 2,
                                    'photo_url' : 2,
                                    'other' : 2,
                                    'note' : 3
                                   },
                        'note' : {'note_record_id' : 1,
                                  'person_record_id' : 2,
                                  'linked_person_record_id' : 3,
                                  'entry_date' : 3,
                                  'author_name' : 3,
                                  'author_email' : 3,
                                  'author_phone' : 3,
                                  'source_date' : 3,
                                  'found' : 3,
                                  'email_of_found_person' : 3,
                                  'phone_of_found_person' : 3,
                                  'last_known_location' : 3,
                                  'text' : 3
                                 }
                       }
                }

  # version : parent : children that will not be marked as extraneous
  ALLOWED_CHILDREN = {1.1 : {'person' : set(['person_record_id', 'entry_date',
                                             'author_name', 'author_email' ,
                                             'author_phone', 'source_name',
                                             'source_date', 'source_url',
                                             'first_name', 'last_name',
                                             'home_city', 'home_state',
                                             'home_neighborhood', 'home_street',
                                             'home_zip', 'photo_url', 'other',
                                             'note'
                                            ]),
                             'note' : set(['note_record_id', 'entry_date',
                                           'author_name', 'author_email',
                                           'author_phone', 'source_date',
                                           'found', 'email_of_found_person',
                                           'phone_of_found_person',
                                           'last_known_location', 'text'
                                          ]),
                             'pfif' : set(['person'])
                            },
                      1.2 : {'person' : set(['person_record_id', 'entry_date',
                                             'author_name', 'author_email',
                                             'author_phone', 'source_name',
                                             'source_date', 'source_url',
                                             'first_name', 'last_name',
                                             'home_city', 'home_state',
                                             'home_neighborhood', 'home_street',
                                             'home_postal_code', 'home_country',
                                             'sex', 'date_of_birth', 'age',
                                             'photo_url', 'other', 'note'
                                            ]),
                             'note' : set(['note_record_id', 'person_record_id',
                                           'linked_person_record_id',
                                           'entry_date', 'author_name',
                                           'author_email', 'author_phone',
                                           'source_date', 'found',
                                           'email_of_found_person',
                                           'phone_of_found_person',
                                           'last_known_location', 'text'
                                          ]),
                             'pfif' : set(['person', 'note'])
                            },
                      1.3 : {'person' : set(['person_record_id', 'entry_date',
                                             'expiry_date', 'author_name',
                                             'author_email', 'author_phone',
                                             'source_name', 'source_date',
                                             'source_url', 'full_name',
                                             'first_name', 'last_name', 'sex',
                                             'date_of_birth', 'age',
                                             'home_street', 'home_city',
                                             'home_neighborhood', 'home_state',
                                             'home_postal_code', 'home_country',
                                             'photo_url', 'other', 'note'
                                            ]),
                             'note' : set(['note_record_id', 'person_record_id',
                                           'linked_person_record_id',
                                           'entry_date', 'author_name',
                                           'author_email', 'author_phone',
                                           'source_date', 'found', 'status',
                                           'email_of_found_person',
                                           'phone_of_found_person',
                                           'last_known_location', 'text'
                                          ]),
                             'pfif' : set(['person', 'note'])
                            }
                     }

  PLACEHOLDER_FIELDS = ['person_record_id', 'expiry_date', 'source_date',
                        'entry_date']

  def __init__(self, xml_file, initialize=True):
    self.xml_file = xml_file
    self.tree = None
    self.namespace = None
    self.version = None
    if initialize:
      self.initialize_xml()
      self.initialize_pfif_version()

  def initialize_xml(self):
    """Reads in the XML tree from the XML file to initialize self.tree.  Returns
    an empty list.  If the XML file is invalid, the XML library will raise an
    exception."""
    self.tree = ET.parse(self.xml_file)
    return []

  def initialize_pfif_version(self):
    """Validates that tree refers to a PFIF XML file with a supported version
    and initializes self.namespace and self.version.  Returns an empty list.
    Raises an exception if unsuccessful."""
    root = self.tree.getroot()
    tag = root.tag
    # xml.etree.Element.tag is formatted like: {namespace}tag
    match = re.match(r'\{(.+)\}(.+)', tag)
    assert match, 'This XML root node does not specify a namespace and tag'
    self.namespace = match.group(1)
    tag = match.group(2)
    assert tag == 'pfif', 'The root node must be pfif'

    # the correct pfif url is like: http://zesty.ca/pfif/VERSION where VERSION
    # is 1.1, 1.2, or 1.3
    match = re.match(r'http://zesty\.ca/pfif/(\d\.\d)', self.namespace)
    assert match, ('The XML namespace specified is not correct.  It should be '
                   'in the following format: http://zesty.ca/pfif/VERSION')
    self.version = float(match.group(1))
    assert (self.version >= 1.1 and self.version <= 1.3), (
           'This validator only supports versions 1.1-1.3.')
    return []

  # helpers

  def add_namespace_to_tag(self, tag):
    """turns a local tag into a fully qualified tag by adding a namespace """
    return '{' + self.namespace + '}' + tag

  def get_all_persons(self):
    """returns a list of all persons in the tree"""
    return self.tree.findall(self.add_namespace_to_tag('person'))

  def get_low_level_notes(self):
    """returns a list of all notes that are subnodes of persons"""
    notes = []
    for person in self.get_all_persons():
      notes.extend(person.findall(self.add_namespace_to_tag('note')))
    return notes

  def get_top_level_notes(self):
    """returns a list of all notes that are subnodes of the root node"""
    return self.tree.findall(self.add_namespace_to_tag('note'))

  def get_all_notes(self):
    """returns a list of all notes in the tree"""
    notes = self.get_top_level_notes()
    notes.extend(self.get_low_level_notes())
    return notes

  @staticmethod
  def pfif_date_to_py_date(date_str):
    """Converts a date string in the format yyyy-mm-ddThh:mm:ssZ (where there
    can optionally be a fractional amount of seconds between ss and Z) to a
    Python datetime object"""
    # Fractional seconds are optionally allowed in the time, which means
    # that it would be difficult to use datetime.datetime.strptime.
    # Instead, we manually extract the fields using a regular expression.
    match = re.match(
        r'(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(\.\d+)?Z$',
        date_str)
    time_parts = []
    for i in range(1, 7):
      time_parts.append(int(match.group(i)))
    date = datetime.datetime(time_parts[0], time_parts[1], time_parts[2],
                             time_parts[3], time_parts[4], time_parts[5])
    return date

  def get_expiry_datetime(self, person):
    """Returns the expiry date associated with a given person, adjusted by one
    day to reflect the actual date that data must be removed from PFIF XML.
    Returns None if there is no expiry date."""
    expiry_date_elem = person.find(self.add_namespace_to_tag('expiry_date'))
    if expiry_date_elem != None:
      expiry_date_str = expiry_date_elem.text
      if expiry_date_str:
        expiry_date = PfifValidator.pfif_date_to_py_date(expiry_date_str)
        # Advances the expiry_date one day because the protocol doesn't
        # require removing data until a day after expiration
        expiry_date += datetime.timedelta(days=1)
        return expiry_date
    return None

  def get_field_text(self, parent, child_tag):
    """Returns the text associated with the child node of parent.  Returns none
    if parent doesn't have that child or if the child doesn't have any text"""
    child = parent.find(self.add_namespace_to_tag(child_tag))
    if child != None:
      return child.text
    return None

  def add_linked_record_mapping(self, person_record_id, note, linked_records):
    """if the note contains a linked_record, adds a mapping from
    person_record_id to a dict and a mapping in that dict from the note's
    linked_person_record_id to the note itself (for ease of creating a message
    about the note) in the linked_records map."""
    linked_id = self.get_field_text(note, 'linked_person_record_id')
    if linked_id != None and person_record_id != None:
      linked_dict = linked_records.setdefault(person_record_id, {})
      linked_dict[linked_id] = note

  def get_linked_records(self):
    """Returns a map from person_record_id to a set of
    linked_person_record_ids."""
    linked_records = {}
    # Notes contained inside of persons might not have a person_record_id field,
    # so we need to get that from the person that owns the note rather than just
    # using self.get_all_notes
    for person in self.get_all_persons():
      person_record_id = self.get_field_text(person, 'person_record_id')
      for note in person.findall(self.add_namespace_to_tag('note')):
        self.add_linked_record_mapping(person_record_id, note, linked_records)
    # Top level notes are required to have their person_record_id, so we can
    # just iterate over them
    for note in self.get_top_level_notes():
      person_record_id = self.get_field_text(note, 'person_record_id')
      self.add_linked_record_mapping(person_record_id, note, linked_records)
    return linked_records

  def make_message(self, error_message, record, element=None, is_error=True):
    """Wrapper for initializing a Message that extracts the person_record_id and
    note_record_id, if present, from a record and the text and line number from
    an element"""
    person_record_id = self.get_field_text(record, 'person_record_id')
    note_record_id = self.get_field_text(record, 'note_record_id')
    line = None
    text = None
    if element != None:
      text = element.text
      line = element.sourceline
    return Message(error_message, is_error=is_error, xml_line_number=line,
                   xml_element_text=text, person_record_id=person_record_id,
                   note_record_id=note_record_id)

  # printing

  @staticmethod
  def print_messages(messages, test_name=None, show_errors=True,
                     show_warnings=True, show_line_numbers=True,
                     show_record_ids=True, show_xml_text=False):
    """Prints out all errors from the current test, per the options in
    set_printing_options"""
    if test_name != None:
      print "****" + test_name + "****"
    for message in messages:
      if (message.is_error and show_errors) or (
          not message.is_error and show_warnings):
        output = []
        if message.is_error:
          output.append("ERROR: ")
        else:
          output.append("WARNING: ")
        output.append(message.main_text + " ")
        if (show_line_numbers and message.xml_line_number != None):
          output.append("XML Line " + str(message.xml_line_number) + ". ")
        if show_record_ids:
          if message.person_record_id != None:
            output.append("The relevant person_record_id is: " +
                           message.person_record_id)
          if message.note_record_id != None:
            output.append("The relevant note_record_id is: " +
                           message.note_record_id)
        if show_xml_text and message.xml_element_text:
          output.append("The text of the relevant PFIF XML node: " +
                         message.xml_element_text)
        print ''.join(output)
    if test_name != None:
      print

  # validation
  # Each validate method can only be run on an initialized validator (the
  # validator will be initialized unless the constructor is called with
  # initialize=False).  Each validate method will return an array of messages,
  # where an empty array means that all validation tests passed.  Only methods
  # that take no arguments (other than self) should be called externally; all
  # other methods should be considered private.

  def validate_root_has_child(self):
    """If there is at least one child, returns an empty list.  Else, returns a
    list with an error message."""
    root = self.tree.getroot()
    children = root.getchildren()
    if not children:
      return [Message("The root node must have at least one child")]
    return []

  def validate_root_has_mandatory_children(self):
    """In 1.1, the root must have at least a person node.  In 1.2+, the root
    must either have a person or note node.  Returns true if the tree has the
    required node.  Note that extraneous nodes will not be reported here, but in
    a later test, so if the root has a person and a note node in version 1.1,
    that will return true."""
    children = self.tree.getroot().getchildren()
    for child in children:
      tag = utils.extract_tag(child.tag)
      if tag == 'person' or (self.version >= 1.2 and tag == 'note'):
        return []
    return [Message('Having a person tag (or a note tag in PFIF 1.2+) as one '
                    'of the children of the root node is mandatory.')]

  def validate_has_mandatory_children(self, parents, mandatory_children):
    """Validates that every parent node has all mandatory children .  Returns a
    list with the names of all mandatory children missing from any parent found.
    parent_tag should be a string of the local tag of the node to check."""
    messages = []
    for parent in parents:
      for child_tag in mandatory_children:
        child = parent.find(self.add_namespace_to_tag(child_tag))
        if child is None:
          messages.append(self.make_message(
              'You do not have all mandatory children.  You were missing the '
              'following tag: ' + child_tag, record=parent))
    return messages

  def validate_person_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that persons have
    all mandatory children."""
    mandatory_children = (
        PfifValidator.MANDATORY_CHILDREN[self.version]['person'])
    persons = self.get_all_persons()
    return self.validate_has_mandatory_children(persons, mandatory_children)

  def validate_note_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that notes have
    all mandatory children."""
    messages = []
    top_level_notes = self.get_top_level_notes()
    top_note_children = (
        PfifValidator.MANDATORY_CHILDREN[self.version]['top_note'])
    messages.extend(self.validate_has_mandatory_children(top_level_notes,
                                                         top_note_children))

    low_notes = self.get_low_level_notes()
    low_note_children = (
        PfifValidator.MANDATORY_CHILDREN[self.version]['note'])
    messages.extend(self.validate_has_mandatory_children(low_notes,
                                                         low_note_children))
    return messages

  def validate_children_have_correct_format(self, parents, formats):
    """validates that every element in parents has valid text, as per the
    specification in formats"""
    messages = []
    for parent in parents:
      for field, field_format in formats.items():
        elements = parent.findall(self.add_namespace_to_tag(field))
        for element in elements:
          if element.text:
            # strip the string so that extra whitespace around the edges won't
            # interfere with matching
            text = element.text.strip()
            if field_format == 'URL':
              url = urlparse(text)
              # The URL should be HTTP or HTTPS.  If the netloc is blank, the
              # URL is probably blank or malformed.
              # pylint: disable=E1101
              failed = url.scheme not in ['http', 'https'] or url.netloc == ''
              # pylint: enable=E1101
            else:
              match = re.match(field_format, text)
              failed = (match is None)
            if failed:
              messages.append(self.make_message(
                  'The text in one of your fields does not match the '
                  'requirement in the specification.  The field: ' + field +
                  '.  The text: ' + element.text,
                  record=parent, element=element))
          else:
            messages.append(self.make_message('You had an empty field.',
                                              is_error=False, record=parent,
                                              element=element))
    return messages

  def validate_fields_have_correct_format(self):
    """Validates that every field in FORMATS follows the correct format
    (ie, that the dates are in yyyy-mm-ddThh:mm:ssZ format).  Returns a list of
    the fields that have improperly formatted data.  Wrapper for
    validate_children_have_correct_format"""
    messages = self.validate_children_have_correct_format(
        self.get_all_persons(), PfifValidator.FORMATS[self.version]['person'])
    messages.extend(self.validate_children_have_correct_format(
        self.get_all_notes(), PfifValidator.FORMATS[self.version]['note']))
    return messages

  def validate_ids_are_unique(self, records, field):
    """Validates that all record ids in records are unique.  There should not be
    two persons with the same person_record_id or two notes with the same
    note_record_id.  Field should be 'person_record_id' if records is persons
    and 'note_record_id' if records is notes"""
    ids = []
    messages = []
    for record in records:
      id_field = record.find(self.add_namespace_to_tag(field))
      # If the record is incorrectly missing a record_id field, that should be
      # flagged as a missing mandatory child, not here.
      if id_field is not None:
        curr_id = id_field.text
        if curr_id in ids:
          messages.append(self.make_message('You had a duplicate id.',
                                            record=record, element=record))
        elif curr_id not in ids:
          ids.append(curr_id)
    return messages

  def validate_person_ids_are_unique(self):
    """Wrapper for validate_ids_are_unique to validate that person_record_ids
    are unique"""
    return self.validate_ids_are_unique(self.get_all_persons(),
                                        'person_record_id')

  def validate_note_ids_are_unique(self):
    """Wrapper for validate_ids_are_unique to validate that note_record_ids are
    unique"""
    return self.validate_ids_are_unique(self.get_all_notes(), 'note_record_id')

  def validate_notes_belong_to_persons(self):
    """Validates that every note that is at the top level contains a
    person_record_id and that every note inside a person with a person_record_id
    matches the id of the parent person.  Returns a list of all unmatched
    notes"""
    messages = []
    top_level_notes = self.get_top_level_notes()
    for note in top_level_notes:
      person_id = note.find(self.add_namespace_to_tag('person_record_id'))
      if person_id == None:
        messages.append(self.make_message(
            'A top level note (a note not contained within a person) is '
            'missing a person_record_id.', record=note, element=note))
    persons = self.get_all_persons()
    for person in persons:
      person_id = person.find(self.add_namespace_to_tag('person_record_id'))
      if person_id != None:
        notes = person.findall(self.add_namespace_to_tag('note'))
        for note in notes:
          note_person_id = note.find(
              self.add_namespace_to_tag('person_record_id'))
          if note_person_id != None and note_person_id.text != person_id.text:
            messages.append(Message(
                'You have a note that has a person_record_id that does not '
                'match the person_record_id of the person that owns the note.',
                xml_line_number=note_person_id.sourceline,
                xml_element_text=note_person_id.text,
                person_record_id=self.get_field_text(person,
                                                     'person_record_id'),
                note_record_id=self.get_field_text(note, 'note_record_id')))
    return messages

  def validate_field_order(self, records, field_type):
    """Validates that all subnodes of field_type (either person or note) are in
    the correct order.  For version 1.1, this means that all fields must be in
    the order specified in the spec (the same as the FIELD_ORDER data structure)
    or omitted.  For version 1.2, person_record_id must appear first and notes
    must appear last in a person, and note_record_id and person_record_id must
    appear first in notes"""
    messages = []
    # 1.3 and above don't have order
    if self.version < 1.3:
      field_order = PfifValidator.FIELD_ORDER[self.version][field_type]
      for record in records:
        # foreach field, if this field is lower than the current max field, it
        # represents an invalid order
        curr_max = 0
        for field in record.getchildren():
          tag = utils.extract_tag(field.tag)
          if tag in field_order:
            field_order_num = field_order[tag]
            if field_order_num >= curr_max:
              curr_max = field_order_num
            else:
              messages.append(self.make_message(
                  'One of your fields was out of order.  The field: ' + tag,
                  record=record, element=field))
              break
    return messages

  def validate_person_field_order(self):
    """Wrapper for validate_field_order.  Validates that all fields in all
    persons are in the correct order."""
    return self.validate_field_order(self.get_all_persons(), 'person')

  def validate_note_field_order(self):
    """Wrapper for validate_field_order.  Validates that all fields in all notes
    are in the correct order."""
    return self.validate_field_order(self.get_all_notes(), 'note')

  def validate_placeholder_dates(self, person, expiry_date):
    """Placeholders must be created within one day of expiry, and when they are
    created, the source_date and entry_date must match.  Returns true if those
    conditions hold."""
    messages = []
    source_date = self.get_field_text(person, 'source_date')
    entry_date = self.get_field_text(person, 'entry_date')
    if (not source_date) or (source_date != entry_date):
      messages.append(self.make_message('An expired record has a source date '
                                        'that does not match the entry date.',
                                        record=person, element=person))
    # If source_date > expiry_date, the placeholder was made more than a day
    # after expiry; even though the current PFIF XML is not exposing data, it
    # was exposing data between expiry_date and search_date
    if PfifValidator.pfif_date_to_py_date(source_date) > expiry_date:
      source_element = person.find(self.add_namespace_to_tag('source_date'))
      messages.append(self.make_message(
          'The placeholder for an expired record was created more than a day '
          'after the record expired.', record=person, element=source_element))
    return messages

  def validate_personal_data_removed(self, record):
    """After expiration, a person can only contain placeholder data, which
    includes all fields aside from PLACEHOLDER_FIELDS.  All other data is
    personal data.  Adds an error message if there is any personal data in
    the record"""
    messages = []
    children = record.getchildren()
    for child in children:
      tag = utils.extract_tag(child.tag)
      if tag not in PfifValidator.PLACEHOLDER_FIELDS:
        if child.text:
          # notes with text are okay as long as none of their children have text
          if tag == 'note':
            messages.extend(self.validate_personal_data_removed(child))
          else:
            messages.append(self.make_message("An expired record still has "
                                              "personal data.", record=record,
                                              element=child))
    return messages

  def validate_expired_records_removed(self):
    """Validates that if the current time is at least one day greater than any
    person's expiry_date, all fields other than person_record_id, expiry_date,
    source_date, and entry_date must be empty or omitted.  Also, source_date and
    entry_date must be the time that the placeholder was created.  Returns a
    list with the person_record_ids of any persons that violate those
    conditions"""
    # TODO(samking): if a person is expired, then there should not be any notes
    # associated with that person
    messages = []
    if self.version >= 1.3:
      persons = self.get_all_persons()
      for person in persons:
        expiry_date = self.get_expiry_datetime(person)
        curr_date = utils.get_utcnow()
        # if the record is expired
        if expiry_date != None and expiry_date < curr_date:
          messages.extend(self.validate_personal_data_removed(person))
          messages.extend(self.validate_placeholder_dates(person, expiry_date))
    return messages

  def validate_linked_records_matched(self):
    """Validates that if a note has a linked_person_record_id field, that the
    person that it points to has a note pointing back.  If A links to B, B
    should link to A.  Returns a list of any notes that point to nowhere"""
    messages = []
    linked_records = self.get_linked_records()
    for person_record_id, linked_dict in linked_records.items():
      for linked_id, linking_note in linked_dict.items():
        # if B doesn't exist or B doesn't point to A, then A points to nowhere
        if (linked_id not in linked_records or
            person_record_id not in linked_records[linked_id]):
          link_field = linking_note.find(
              self.add_namespace_to_tag('linked_person_record_id'))
          messages.append(self.make_message(
              'There is an asymmetric linked record.  That is, a note has a'
              'linked_person_record_id to another person, but that person '
              'does not link back.', record=linking_note, element=link_field,
              is_error=False))
    return messages

  def validate_extraneous_children(self, parents, approved_tags):
    """For each parent in parents, ensures that every child's tag is in
    approved_tags and is not a duplicate (except for notes and persons).
    Returns a list of all extraneous tags."""
    messages = []
    for parent in parents:
      used_tags = []
      for child in parent.getchildren():
        tag = utils.extract_tag(child.tag)
        if tag in used_tags and tag != 'note' and tag != 'person':
          messages.append(self.make_message('Duplicate Tag.', record=parent,
                                            element=child))
        elif tag not in approved_tags:
          messages.append(self.make_message('Extraneous Tag.', record=parent,
                                            element=child))
        else:
          used_tags.append(tag)
    return messages

  def validate_extraneous_fields(self):
    """Validates that all fields present are in the specification.  Returns a
    list with every extraneous or duplicate field.  This includes fields added
    in a more recent version of the specification."""
    messages = []

    pfif_fields = PfifValidator.ALLOWED_CHILDREN[self.version]['pfif']
    messages.extend(self.validate_extraneous_children(
        [self.tree.getroot()], pfif_fields))

    person_fields = PfifValidator.ALLOWED_CHILDREN[self.version]['person']
    messages.extend(self.validate_extraneous_children(
        self.get_all_persons(), person_fields))

    note_fields = PfifValidator.FORMATS[self.version]['note'].keys()
    messages.extend(self.validate_extraneous_children(
        self.get_all_notes(), note_fields))

    return messages

  @staticmethod
  def run_validations(file_path):
    """Runs all validations on the file specified by file_path.  Returns a list
    of all errors generated.  file_path can be anything that lxml will accept,
    including file objects and file-like objects."""
    validator = PfifValidator(file_path)
    methods = inspect.getmembers(validator, inspect.ismethod)
    messages = []
    for name, method in methods:
      # run all validation methods except for any validation method that takes
      # more than one argument (self), because that will have a wrapper method.
      if (name.find('validate_') != -1 and
          len(inspect.getargspec(method).args) == 1):
        messages.extend(method())
    return messages

def main():
  """Runs all validations on the provided PFIF XML file"""
  if (not len(sys.argv) == 2):
    print 'Usage: python pfif-validator.py my-pyif-xml-file'
  PfifValidator.run_validations(sys.argv[1])

if __name__ == '__main__':
  main()
