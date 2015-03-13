# Introduction #

This tool will validate that text follows the PFIF XML specification.  If it does not follow the specification, this tool will tell what part of the text is malformed.  This involves several tasks, as specified by http://zesty.ca/pfif/1.1/, http://zesty.ca/pfif/1.2/, and http://zesty.ca/pfif/1.3/

# Details #
  1. Is the text valid XML?
  1. Is the root node a pfif element?
  1. Is there at least one child of the root node?
  1. (1.1) Are all children of the root node person elements?  (1.2, 1.3) Are all children of the root node person or note elements?
  1. Does each person node have all mandatory children?
    * person\_record\_id
    * source\_date
    * (1.3) full\_name
    * (1.1, 1.2) first\_name
    * (1.1, 1.2) last\_name
  1. Does each note node have all mandatory children?
    * note\_record\_id
    * author\_name
    * source\_date
    * text
  1. Are all included fields in all persons in the correct format?
    * person\_record\_id (ASCII string)
      * a lowercase ASCII domain name followed by a slash and a local identifier
    * entry\_date (ASCII string in the form "yyyy-mm-ddThh:mm:ssZ")
    * expiry\_date (ASCII string in the form "yyyy-mm-ddThh:mm:ssZ")
    * author\_name (Unicode string)
    * author\_email (ASCII string)
      * an email
    * author\_phone (ASCII string)
      * a phone number
    * source\_name (Unicode string)
    * source\_date (ASCII string in the form "yyyy-mm-ddThh:mm:ssZ")
    * source\_url (ASCII string)
      * a url
    * (1.3) full\_name (Unicode string)
    * (1.1, 1.2) first\_name
    * (1.1, 1.2) last\_name
    * first\_name (Unicode string)
    * last\_name (Unicode string)
    * (1.2+) sex (ASCII string)
      * female, male, or other
    * (1.2+) date\_of\_birth (ASCII string in the form "yyyy", "yyyy-mm", or "yyyy-mm-dd")
    * (1.2+) age (integer, or ASCII string in the form "min-max")
      * a single decimal integer or min-max
    * home\_street (Unicode string)
    * home\_city (Unicode string)
    * home\_neighborhood (Unicode string)
    * home\_state (Unicode string)
      * ISO 3166-2 code.
    * home\_postal\_code (ASCII string; home\_zip in 1.1)
    * (1.2+) home\_country (ASCII string)
      * uppercase two-letter ISO-3166-1 country code
    * photo\_url (ASCII string)
    * a url
    * other (large Unicode string)
  1. Are all fields in all notes in the correct format?
    * note\_record\_id (ASCII string)
      * a domain name followed by a slash and a local identifier
    * (1.2+) person\_record\_id (ASCII string)
      * a lowercase ASCII domain name followed by a slash and a local identifier
    * (1.2+) linked\_person\_record\_id (ASCII string)
      * a lowercase ASCII domain name followed by a slash and a local identifier
    * entry\_date (ASCII string in the form "yyyy-mm-ddThh:mm:ssZ")
    * author\_name (Unicode string)
    * author\_email (ASCII string)
      * an email address
    * author\_phone (ASCII string)
      * a phone number
    * source\_date (string in the form "yyyy-mm-ddThh:mm:ssZ")
    * found (ASCII string)
      * true or false
    * (1.2+) status
      * information\_sought, is\_note\_author, believed\_alive, believed\_missing, or believed\_dead
    * email\_of\_found\_person (ASCII string)
      * an email address
    * phone\_of\_found\_person (ASCII string)
      * a phone number
    * last\_known\_location (Unicode string)
    * text (large string)
  1. Are the person\_record\_id's unique?
  1. Are the note\_record\_id's unique?
  1. Are all notes correctly associated with persons?
    * if a note is outside a person, the note must contain a person\_record\_id
    * if a note is inside a person and has a person\_record\_id, it must match the person\_record\_id of the enclosing person
  1. (1.1, 1.2) Do person and note fields occur in the proper order?
    * (1.1, 1.2) The person\_record\_id and note\_record\_id must appear first
    * (1.1) All fields must be in the order described above
  1. (1.3) Are there any records that are expired but have not been removed? If the expiry\_date is at least one day in the past, the person and associated notes must only be placeholders:
    * All fields other than person\_record\_id, expiry\_date, source\_date, and entry\_date must be empty or omitted
    * Source date and entry date must be set to the time that the placeholder was created
  1. (Warning) Are all linked records matched?  That is, if person A has note X that links to person B, then person B should have a note Y that links to person A.
  1. (Warning) Are there any extraneous or duplicate fields, including fields that were added in 1.2 and 1.3 for a PFIF XML 1.1 document?