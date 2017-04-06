# query Open Tree
Refer to the description of the query-tool-interface in 
  the [Step2-README.md](./Step2-README.md#query-tool-interface) 
  for the rules that this script needs to conform to.

Check out the [http-and-requests-README.md](./http-and-requests-README.md) for background
  on HTTP and using the python `requests` package.
This task will entail talking to the back-end of the Open Tree of Life web application.

## Using the Open Tree web API to get the phylogenetic relationships for 3 taxon names
The [Open Tree API](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)
page describes its web API in detail.
Don't read all of this, just open it in a tab for reference.


## Setup
    pip install --upgrade requests
    

**Instruction 1:** Start with the steps described in:
 [query-script-skeleton-README.md](./query-script-skeleton-README.md)

## Next

**Instruction 2:** Add `import requests` to the top of the script
 
Now, we'll start filling in the code.
Write the output to `stderr` every time you have the next step completed, and 
  run the code frequently.
This makes it much easier to debug than trying to write the whole thing.



### First step - getting an OTT ID
#### A comment on biological nomenclature
An unfortunate aspect of biological taxonomy is the fact that the mapping of a name to a species
 is not unique.
There is not one universally recognized name for each species, and some names apply to more
    than one species (although this is rare).
Figuring out what biological taxon a name string refers to is an obnoxious bioinformatics challenge.
The general solution (used widely in computing, not just by Open Tree) is to convert a problematic
    name to a reliable, unique ID.
Open Tree web API has some ability to help with the complexities of typos, multiple names for the same
    taxon, and multiple species being assigned the same name.

#### Using the API to get an ID
For the purpose of this tutorial, I **strongly** recommend that you write the query tool to simply
    exit with an error code if there is not a unique match for a name.
Check out the [match_names](https://github.com/OpenTreeOfLife/germinator/wiki/TNRS-API-v3#match_names)
    API call to see how you can convert a taxon name to an Open Tree Taxon ID (an "OTT ID" in the
    jargon of the rest of the API).

The API lets you submit a list of names, but I recommend that you just make a seaparate
    API call for each name to make the coding easier on your end.


**Instruction 3:**
For the `first_name` call the appropriate function in `requests`, and print the body of 
the response.

**Instruction 4:**
Temporarily introduce a typo in the URL you are using for the call, and make sure
your script stops with an error message and code when the web service call fails.

**Instruction 5:**
Revert your typo to get the call working again.

**Instruction 6:**
Extract the content of a successful call as a python object.
[This section of the docs](./http-and-requests-README.md#the-HTTP-response-payload) will probably
be helpful.

**Instruction 7:**
Figure out how to extract just the OTT ID from the python object you got from the response.


**Instruction 8:**
Now convert the other two names to OTT IDs.
If you write a function (see http://swcarpentry.github.io/python-novice-inflammation/06-func/)
for the conversion of name to ID, this instruction will be easy to do.

**Instruction 9:**
You should exit with an error if there are <3 distinct IDs (this might happen if you get the
same name from the user twice or if two of the names passed in are synonyms for the same taxon).

### Second step - getting a tree for a set of OTT IDs
If you have 3 OTT IDs, you can get a string representation of phylogenetic tree for the species using
    an [induced_subtree](https://github.com/OpenTreeOfLife/germinator/wiki/Synthetic-tree-API-v3#induced_subtree)
    API method call.
If you tell the server to use the `"id"` form of `label_format`, then the string will be pretty 
    easy to deal with because it will only have the characters found in the "newick" tree 
    representation format (see below) and labels of the form `ott####`.



**Instruction 10:**
Use `requests` to perform the induced subtree call for your OTT Ids.

**Instruction 11:**
Extract the newick string as a variable from the response.


### Third step - interpreting the newick tree representation
In this section we will describe how to interpt the
 [Newick](http://evolution.genetics.washington.edu/phylip/newicktree.html) format for this excercise.
In this text format, parentheses group sets of species that are more closely related to each other
    than they are to any taxon that is listed outside of that group of parentheses.
Commas separate species or groups.
A semicolon marks the end.
Other characters are labels of species or groups of species.

The format is general, but we only have a 3 species, so we don't need to write a general parser
    of the format.
If, for example, the OTT Ids we are interest in are `1`, `2`, and `3` then there are only three
 types of response we could get:
  1. 1 set of parentheses: `(ott1,ott2,ott3)some_label_here;` which indicates that Open Tree does
    not have a guess about which of these 3 species are more closely related to each other.
  2. 2 sets of parentheses. The following 2 trees are equivalent:
     * `(ott1,(ott2,ott3)some_label)some_other_label;`
     * `((ott3,ott2)some_label,ott1)some_other_label;`

So, for our limited purposes, we just need to be able to recognize if the returned newick string
has 2 sets of parentheses.
If it does, we need to find which of the 3 OTT Ids that we asked about is **not** inside the
    inner set of parentheses.
This is the taxon that is furthest from the other 2 species.

### Final step - convert the tree to a number.
Recall that (according to [Step2-README.md](./Step2-README.md#query-tool-interface)), on success
the script should write 0, 1, 2, or 3



**Instruction 12:**
Convert the response newick string to the appropriate number.
Regular expressions (see https://docs.python.org/2/howto/regex.html) may be handy.

Call the result `tree_integer_code`



**Instruction 13:**
Test your script out with a few sets of species names.

