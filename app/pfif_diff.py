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

"""Displays the difference between two PFIF XML files.

* Differences in field order are ignored regardless of PFIF version.
* Notes that are children of persons automatically have the person_record_id
  added to them, so children of persons and top-level notes are considered the
  same.
* This tool assumes that both files are valid PFIF XML.  That means that this
  tool is not guaranteed to notice if, for instance, one file has a child of the
  root that is neither a person nor a note and the other child is missing that.
* The output will include one message per person or note that is missing or
  added.  These messages will specify whether it is a person or note and whether
  it was missing or added in addition to the id of the note.  The output will
  also include one message per person or note field that is missing, added, or
  changed.  For each of these, it will display the id of the containing person
  or note, the field name, whether the field was missing, added, or changed, the
  current text (if present), and the expected text (if present)."""

__author__ = 'samking@google.com (Sam King)'

import xml.etree.ElementTree as ET
import utils

class PfifDiffTool:
  """Allows the user to get the diff between two files and control the output"""

  # TODO(samking): Add --ignore-field flag.  Add --blank-is-nonexistent flag.

  def objectify_pfif_xml(self, file_to_objectify):
    """Turns a file of PFIF XML into a map."""
    # read the file into an XML tree
    tree = utils.PfifXmlTree(file_to_objectify)
    # turn the xml trees into a persons and notes map for each file.  They will
    # map from record_id to a map from field_name to value
    object_map = {}
    persons = tree.get_all_persons()
    for person in persons:
      person_record_id = tree.get_field_text(person, 'person_record_id')
      if person_record_id is None:
        # TODO(samking): make it a real message
        print "error!"
      else:
        object_map[person_record_id] = {}
        for child in person.getchildren():
          field_name = utils.extract_tag(child.tag)
          field_value = child.text
          if field_name == 'note':
            # get the note record id
            # force-add the person_record_id to it if it's absent
            # do the same stuff as with a person
          else:
            object_map[person_record_id][field_name] = field_value


  def pfif_diff(self, file1, file2):

    # Compute the Diff
    # foreach id in map1
      # is that id in map2?
      # foreach field in map1
        # is the field present in map2?
        # is the field value in map2 the same as the field value in map1?
    # do the same as above from map2 to map1 instead of map1 to map2

    # Output the Diff
