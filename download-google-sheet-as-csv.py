#!/usr/bin/env python
import requests
import sys
import os
import re
SCRIPT_PATH = sys.argv[0]
# the script name is the last part of the path to the script
SCRIPT_NAME = os.path.split(SCRIPT_PATH)[-1]

def error(msg):
    """Outputs a message to the standard error stream with the SCRIPT_NAME as a prefix.

    This is good practice, because in a complex pipeline, it lets the users know which tool
        is complaining.
    """
    sys.stderr.write("{}: {}\n".format(SCRIPT_NAME, msg))

def extract_doc_id_from_url(u):
    """This function tries to extract the doc_id from the URL.

    I know of at least 2 forms of google doc URLs that can be used to encapsulate a
    document ID.
    """
    # Here we use 2 regular expressions to match the URL. The doc ID is "captured"
    #   in the first group of each pattern. That is the part of the regex with parentheses.
    # First:
    #   start with https://drive.google.com    . means anything, so we use \. to match a .
    #   followed by nothing or anything       .*
    #   followed by "id="
    #   next comes the doc ID and number of letters and numbers - we add the parentheses to catch a group
    #   and finally (and optionally) "&" and other stuff.
    drive_pattern = re.compile(r"https://drive\.google\.com.*id=([0-9a-zA-Z]+)[&]?.*")
    # Next pattern:
    #   start with https://docs.google.com/spreadsheets/
    #   followed by nothing or anything       .* separated by /
    #   here we capture the doc ID as a 10-120 character sequence of letters or number between /
    #   the last / might be omitted, so we add the ? to make it optional
    doc_pattern = re.compile(r"https://docs\.google\.com/spreadsheets.*/([0-9a-zA-Z]{10,120})/?")

    for pat in [doc_pattern, drive_pattern]:
        m = pat.match(u)
        # a match object is returned it bool(m) will be True if there was a match
        if m:
            # if we matched, return the first (and only) group that was captured.
            return m.group(1)
    # None to signal no match
    return None


def fetch_spreadsheet_as_csv(doc_id):
    fetch_url = "https://docs.google.com/spreadsheets/d/{}/export".format(doc_id)
    args = {"gid": "0",
            "format": "csv"}
    response = requests.get(fetch_url, params=args)
    response.raise_for_status()
    return response.content


if __name__ == '__main__':
    import argparse
    import codecs
    parser = argparse.ArgumentParser(usage="If given a URL to a google spreadsheet that is shared, this script will store a csv export of the spreadsheet")
    parser.add_argument('-o', '--output',
                        type=str,
                        required=False,
                        help="If specified, this filepath with be used to write the e16AZ9Po7h8Qa3ink55bZn4GaiS2pBPVQMMuDd2TBIByAxported sheet. If omitted, the contents will be written to stdout.")
    parser.add_argument('-u', '--url',
                        type=str,
                        required=False,
                        help="Either this or a doc-id must be specified to identify the document to be downloaded.")
    parser.add_argument('-d', '--doc-id',
                        type=str,
                        required=False,
                        help="Either this or a URL must be specified to identify the document to be downloaded.")
    args = parser.parse_args()
    doc_id = args.doc_id
    if (not doc_id) and args.url:
        doc_id = extract_doc_id_from_url(args.url)
        if not doc_id:
            error("Could not extract a doc id from the url. Consider using the --doc-id argument")
            sys.exit(1)
    else:
        error("Either the doc-id or a google doc URL need to be provided!")
        # Exit with a non-zero exit code on errors
        sys.exit(1)
    try:
        csv_content = fetch_spreadsheet_as_csv(doc_id)
        assert csv_content
    except:
        error("Exiting with an exception due to a failure to find fetch the spreadsheet...")
        raise
    if not csv_content:
        error("Could not download the spreadsheet")
        sys.exit(1)
    if args.output:
        with codecs.open(args.output, 'w', encoding='utf-8') as outf:
            outf.write(csv_content)
    else:
        outf = codecs.getwriter('utf-8')(sys.stdout)
        outf.write(csv_content)

