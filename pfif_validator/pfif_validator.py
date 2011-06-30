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

import xml.etree.ElementTree as ET
import re
import xml_utils
from urlparse import urlparse

class PfifValidator:
  # TODO(samking): should I move a lot of this data stuff at the top into an
  # external file that I would read in?

  # a map from version to parent : required-children mappings
  MANDATORY_CHILDREN = {1.1 : {'person' : ['person_record_id', 'first_name',
                                           'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text']
                              },
                        1.2 : {'person' : ['person_record_id', 'first_name',
                                           'last_name'],
                               'note' : ['note_record_id', 'author_name',
                                         'source_date', 'text']
                              },
                        1.3 : {'person' : ['person_record_id', 'source_date',
                                         'full_name'],
                               'note' : ['note_record_id', 'author_name',
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
  TEXT = r'^.*$' #TODO(samking): do we want to do .+?
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
  URL = "URL"
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

  # helpers

  def add_namespace_to_tag(self, tag):
    """turns a local tag into a fully qualified tag by adding a namespace """
    return '{' + self.namespace + '}' + tag

  def get_all_persons(self):
    """returns a list of all persons in the tree"""
    return self.tree.findall(self.add_namespace_to_tag('person'))

  def get_all_notes(self):
    """returns a list of all notes in the tree"""
    notes = self.tree.findall(self.add_namespace_to_tag('note'))
    for person in self.get_all_persons():
      notes.extend(person.findall(self.add_namespace_to_tag('note')))
    return notes

  # initialization

  def __init__(self, xml_file, initialize=True):
    self.xml_file = xml_file
    if initialize:
      self.validate_xml_or_die()
      self.validate_root_is_pfif_or_die()

  def validate_xml_or_die(self):
    """Returns an XML tree of the xml file.  If the XML file is invalid, the XML
    library will raise an exception."""
    self.tree = ET.parse(self.xml_file)
    return self.tree

  def validate_root_is_pfif_or_die(self):
    """Validates that tree refers to a PFIF XML file.  Returns the version.
    Raises an exception if unsuccessful."""
    root = self.tree.getroot()
    tag = root.tag
    # xml.etree.Element.tag is formatted like: {namespace}tag
    match = re.match(r'\{(.+)\}(.+)', tag)
    self.namespace = match.group(1)
    tag = match.group(2)
    assert match, "This XML root node doesn't specify a namespace and tag"
    assert tag == "pfif", "The root node must be pfif"

    # the correct pfif url is like: http://zesty.ca/pfif/VERSION where VERSION
    # is 1.1, 1.2, or 1.3
    match = re.match(r'http://zesty\.ca/pfif/(\d\.\d)', self.namespace)
    assert match, "The XML namespace specified is not correct.  It should be " \
                  "in the following format: http://zesty.ca/pfif/VERSION"
    self.version = float(match.group(1))
    assert (self.version >= 1.1 and self.version <= 1.3), (
           "This validator only supports versions 1.1-1.3.")
    return self.version

  # validation

  def validate_root_has_child(self):
    """If there is at least one child, returns true."""
    root = self.tree.getroot()
    children = root.getchildren()
    if not len(children) > 0:
      print "The root node must have at least one child"
      return False
    return True

  def validate_root_has_mandatory_children(self):
    """In 1.1, the root must have at least a person node.  In 1.2+, the root
    must either have a person or note node.  Returns true if the tree has the
    required node.  Note that extraneous nodes will not be reported here, but in
    a later test, so if the root has a person and a note node in version 1.1,
    that will return true."""
    children = self.tree.getroot().getchildren()
    result = False
    for child in children:
      tag = xml_utils.extract_tag(child.tag)
      if tag == "person" or (self.version >= 1.2 and tag == "note"):
        result = True
        break
    if not result:
      print "ERROR: Having a person tag (or a note tag in PFIF 1.2+) as one " \
            "of the children of the root node is mandatory."
      print "All children: " + str(children)
    return result

  def validate_has_mandatory_children(self, parent_tag):
    """Validates that every parent node has all mandatory children specified by
    MANDATORY_CHILDREN.  Returns a list with the names of all mandatory children
    missing from any parent found.
    parent_tag should be a string of the local tag of the node to check."""
    mandatory_children = PfifValidator.MANDATORY_CHILDREN[self.version]
    mandatory_children = mandatory_children[parent_tag]
    parents = self.tree.findall(self.add_namespace_to_tag(parent_tag))
    missing_children = []
    for parent in parents:
      for child_tag in mandatory_children:
        child = parent.find(self.add_namespace_to_tag(child_tag))
        if child is None:
          if not child_tag in missing_children:
            missing_children.append(child_tag)
    return missing_children

  def validate_person_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that persons have
    all mandatory children."""
    return self.validate_has_mandatory_children('person')

  def validate_note_has_mandatory_children(self):
    """Wrapper for validate_has_mandatory_children.  Validates that notes have
    all mandatory children."""
    return self.validate_has_mandatory_children('note')

  def validate_children_have_correct_format(self, parents, formats):
    """validates that every element in parents has valid text, as per the
    specification in formats"""
    failed_matches = []
    for parent in parents:
      for field, field_format in formats.items():
        elements = parent.findall(self.add_namespace_to_tag(field))
        for element in elements:
          #TODO(samking): is it correct to strip this string?
          text = element.text.strip()
          failed = False
          if field_format == "URL":
            url = urlparse(text)
            if (url.scheme != "http" and url.scheme != "https"):
              failed = True
            if url.netloc == "":
              failed = True
          else:
            match = re.match(field_format, text)
            if match is None:
              failed = True
          if failed:
            failed_matches.append((element.tag, element.text))
    return failed_matches

  def validate_fields_have_correct_format(self):
    """Validates that every field in FORMATS follows the correct format
    (ie, that the dates are in yyyy-mm-ddThh:mm:ssZ format).  Returns a list of
    the fields that have improperly formatted data.  Wrapper for
    validate_children_have_correct_format"""
    incorrect_formats = self.validate_children_have_correct_format(
        self.get_all_persons(), PfifValidator.FORMATS[self.version]['person'])
    incorrect_formats.extend(self.validate_children_have_correct_format(
        self.get_all_notes(), PfifValidator.FORMATS[self.version]['note']))
    for incorrect_format in incorrect_formats:
      print incorrect_format
    return incorrect_formats

  def validate_ids_are_unique(self, id_type):
    if id_type == 'person':
      collection = self.get_all_persons()
      field = 'person_record_id'
    elif id_type == 'note':
      collection = self.get_all_notes()
      field = 'note_record_id'
    else:
      print "INTERNAL ERROR: We just tried to validate that a type of ID " \
            "other than person or note was unique.  We can't do that."
      return []
    ids = []
    duplicate_ids = []
    for elem in collection:
      curr_id = elem.find(self.add_namespace_to_tag(field)).text
      if curr_id in ids and curr_id not in duplicate_ids:
        duplicate_ids.append(curr_id)
      elif curr_id not in ids:
        ids.append(curr_id)
    return duplicate_ids

  def validate_person_ids_are_unique(self):
    return self.validate_ids_are_unique('person')

  def validate_note_ids_are_unique(self):
    return self.validate_ids_are_unique('note')

  def validate_notes_belong_to_persons(self):
    """Validates that every note that is at the top level contains a
    person_record_id and that every note inside a person with a person_record_id
    matches the id of the parent person.  Returns a list of all unmatched
    notes"""
    unassociated_notes = []
    top_level_notes = self.tree.findall(self.add_namespace_to_tag('note'))
    for note in top_level_notes:
      person_id = note.find(self.add_namespace_to_tag('person_record_id'))
      if person_id == None:
        note_id = note.find(self.add_namespace_to_tag('note_record_id'))
        if note_id == None:
          unassociated_notes.append("A top level note is missing a " \
                                    "person_record_id.  It also doesn't have " \
                                    "a note_record_id, so we can't refer to it")
        else:
          unassociated_notes.append("The following top level note is missing " \
                                    "a person_record_id: " + note_id.text)
    persons = self.get_all_persons()
    for person in persons:
      person_id = person.find(self.add_namespace_to_tag('person_record_id'))
      if person_id != None:
        notes = person.findall(self.add_namespace_to_tag('note'))
        for note in notes:
          note_person_id = note.find(
              self.add_namespace_to_tag('person_record_id'))
          if note_person_id != None and note_person_id.text != person_id.text:
            unassociated_notes.append("Person with ID: " + person_id.text + \
                                      "\nhas a note with person ID: " + \
                                      note_person_id.text)

    return unassociated_notes

  def validate_field_order(self, field_type):
    """Validates that all subnodes of field_type (either person or note) are in
    the correct order.  For version 1.1, this means that all fields must be in
    the order specified in the spec (the same as the FIELD_ORDER data structure)
    or omitted.  For version 1.2, person_record_id must appear first and notes
    must appear last in a person, and note_record_id and person_record_id must
    appear first in notes"""
    # 1.3 and above don't have order
    if self.version > 1.2:
      return []

    if field_type == 'person':
      collection = self.get_all_persons()
    elif field_type == 'note':
      collection = self.get_all_notes()
    else:
      print "INTERNAL ERROR: tried to validate field order for something " \
            "other than a person or note"

    out_of_order_tags = []
    for parent in collection:
      #TODO(samking): this logic only applies to 1.1
      # foreach field, if this field is lower than the current max field, it
      # represents an invalid order
      curr_max = 0
      for field in parent.getchildren():
        tag = xml_utils.extract_tag(field.tag)
        tag_order = PfifValidator.FIELD_ORDER[self.version][field_type][tag]
        if tag_order >= curr_max:
          curr_max = tag_order
        else:
          out_of_order_tags.append(tag)
          break
    print out_of_order_tags
    return out_of_order_tags

  def validate_person_field_order(self):
    """Wrapper for validate_field_order.  Validates that all fields in all
    persons are in the correct order."""
    return self.validate_field_order('person')

  def validate_note_field_order(self):
    """Wrapper for validate_field_order.  Validates that all fields in all notes
    are in the correct order."""
    return self.validate_field_order('note')


#def main():
#  if (not len(sys.argv()) == 2):
#    print "Usage: python pfif-validator.py my-pyif-xml-file"
#  v = PfifValidator(sys.argv(1))
#  v.validate_xml_or_die(sys.argv(1))
#  v.validate_root_is_pfif_or_die()
#  validate_root_has_child_or_die()
#  validate_root_has_mandatory_children()
#  validate_person_has_mandatory_children()
#  validate_note_has_mandatory_children()
#  validate_fields_have_correct_format()
#
#if __name__ == '__main__':
#  main()
