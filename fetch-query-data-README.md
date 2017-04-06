#### 3A: fetch-query-data task
The  **fetch-the-query-data** task is to 
  1. download the spreadsheet from Google Drive, and
  2. write it as a comma-separated-value file on our local filesystem.


We can easily do this operation through the **File >> Download As** menu option
  of the Google spreadsheet if no one wants to learn how to do this programmatically.
It is nice to know how to do this programmatically, so that you can have a pipeline that
  is easy to re-run.

See [http-and-requests-README.md](./http-and-requests-README.md) for background on 
    using `requests`

## Google docs convention
An HTTP GET to `https://docs.google.com/spreadsheets/d/XYZ/export?gid=0&format=csv` will
    where `XYZ` is a doc ID of a google doc spreadsheet will return a HTTP response
    with a UTF-8 text payload that can be interpret as a csv representation of the 
    spreadsheet.


## a curl implementation

So, if you have cURL you can complete this task with:

    curl -o desired-outfile-name.csv \
         'https://docs.google.com/spreadsheets/d/XYZ/export?gid=0&format=csv'

the `-o` flag to curl specifies where to write the payload of the HTTP response.

#### *Note:* the quotes are necessary in this URL.
We are using HTTP GET URL-encoding is used here.
The part of the URL after the `?` is a string that is interpreted by the server as 
as set of key-value pairs.
The `=` separates the parameter name (the key) from the value of the argument.
The `&` is the separator between different key-value pairs in URL encoding.
Note that '&' is a special character in `bash` (the tool that reads your command line); it
tells `bash` to run the preceding command in the background.

Failing to quote the URL will result in bash interpreting the line above as 2 commands:

    curl -o desired-outfile-name.csv \
         https://docs.google.com/spreadsheets/d/XYZ/export?gid=0
    format=csv

The second command just sets a  variable in `bash`, which is harmless enough.
But the fact that the `format=csv` was not passed to google means that you'll get
    some binary representation of the spreadsheet instead of csv.

In `bash`, when in doubt, use quotes.


## A Python implementation

You could try to implement this operation in Python as an exercise.

As a more advanced exercise:
  * Checkout the standard [argparse](https://docs.python.org/3/library/argparse.html)
    to specify the command line interface to your script.
  * Make your script handle extended character sets by using the [codecs](https://docs.python.org/3/library/codecs.html) package.
  * Make your script more flexible/user-friendly:
    * take any Google URL that could be used for the doc (`https://drive.google.com/open?id=XYZ` 
    or `https://drive.google.com/open?id=XYZ/edit` are alternative URLs for this doc).
    * extract the doc ID from the URL
    * uses the `https://docs...` syntax above to fetch the document
