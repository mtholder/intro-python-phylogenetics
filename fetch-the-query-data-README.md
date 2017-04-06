# fetch the query data

After a little googling around, it was apparent that this is trivial
    and can be done with `cURL` or `wget` by adding appropriate arguments
    to the URL of the document.  
The `download-google-sheet-as-csv.py` script was just written to 
    demonstrate how to use `argparse` and `re` from the standard
    library and the `requests` package
    to implement this in python.
The only real advantage over curl is that this version will take 2 
    forms of URLs used to denote a google doc, and succeed regardless
    of which is provided.

    pip install --upgrade requests
    python download-google-sheet-as-csv.py \
        --output=text.csv \
        --url=https://drive.google.com/open?id=16AZ9Po7h8Qa3ink55bZn4GaiS2pBPVQMMuDd2TBIByA