PFIF XML that passes all tests in this validator should be usable by any missing persons database that can read PFIF.

To use the validator frontend, go to http://pfif-tools.appspot.com/validate.  You can upload a file, paste in PFIF XML, or provide the URL for PFIF XML.

ATOM-embedded PFIF XML is not yet supported.

You can uncheck any of the check boxes to show less output if you're only interested in a subset of the information about each error.

The output should be grouped by error, with a summary at the top.

Large files or URLs might not work due to limits on the request and response size in App Engine.

Files with many errors of a given type (ie, if you have a thousand records and all of them are out of order in a PFIF 1.1 document) will be truncated so that the response does not run into App Engine's limits.  Truncation happens on a per-error-type basis, so if you have 1000 records that are out of order and 1000 records that are missing required fields, you will see the first 100 messages of both.

To use the command line validator, download the source and python 2.6 and run python pfif\_validator your-pfif-xml-file.xml.  Unless the file you want to validate is too big for the web tool, there is no compelling reason to use the command line tool.