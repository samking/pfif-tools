There are differences in PFIF XML that can't be captured in a simple textual or XML based diff.  For instance, a note that is embedded in a person can have or omit a person\_record\_id, or that note could be a top level note.

PFIF Diff turns two PFIF files into objects with a standardized format and compares them to each other, outputting how they differ.

To use the web frontend, go to http://pfif-tools.appspot.com/diff and input two files.

The output will differ depending on whether or not Group Messages By Record is checked.  If it is, there will be one message for any records added, one message for any records deleted, and one message for each record changed.  If it is not checked, there will be one message for every issue.  Thus, if one record has 20 fields changed, then that will be 1 message if grouped or 20 messages if not.

A case sensitive diff will compare body text case sensitively.  XML specifies that XML tags are case sensitive, so that cannot be turned off.

You should check Omit Blank Fields if you are getting differences because you have records that are blank, another repository has those records omitted, and you want to treat those two documents as the same.

You can also ignore fields entirely.  This is useful if, for instance, your repository tries to load the picture from every photo\_url, which would cause problems if the url points to example.org.

The command line tool works the same.  Pass it the path to two files and any of the options described above.