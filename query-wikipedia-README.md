# query Wikipedia
Refer to the description of the query-tool-interface in 
  the [Step2-README.md](./Step2-README.md#query-tool-interface) 
  for the rules that this script needs to conform to.

Check out the [http-and-requests-README.md](./http-and-requests-README.md) for background
  on HTTP and using the python `requests` package.
This task will entail "screen scraping" Wikipedia using the
 [wikipedia](https://wikipedia.readthedocs.io/en/latest/quickstart.html#quickstart)
package and [beautiful soup](https://www.crummy.com/software/BeautifulSoup/) a robust
  HTML parser



## Setup
    pip install --upgrade wikipedia
    pip install --upgrade beautifulsoup4


**Instruction 1:** Start with the steps described in:
 [query-script-skeleton-README.md](./query-script-skeleton-README.md)

## Next

**Instruction 2:** Add

    import wikipedia
    from bs4 import BeautifulSoup

to the top of the script.
 
Now, we'll start filling in the code.
Write the output to `stderr` every time you have the next step completed, and 
  run the code frequently.
This makes it much easier to debug than trying to write the whole thing.


### First step - finding the Wikipedia page for a species
Wikipedia pages each have a unique title, but the title of the page for a species is usually its
    common name (not its scientific name).
In most cases, the first search hit for a scientific name will be the Wikipedia page for that
    species.
For the purposes of this tutorial, we can just assume that we want the first hit.

Fortunately, the `wikipedia.search` function will return a list of page titles for a given
    scientific name.

**Instruction 3:**
Write a Python function that takes a string that is the scientific name for a species and
returns the page title of the first search hit for that species name.
If there are no hits, your function should either:
  * write an error message to `sys.stderr` and call `sys.exit(1)`, or
  * raise an exception.

### Second step - fetch the HTML for the page for a species
If you call `wikipedia.page(name)`, Python will perform an HTTP GET operation for the page on 
    Wikipedia that has the value of `name` as its title.
Calling the `.html()` method on the response object returned by the previous function will give you
   the HTML for the page (as a Python string)

**Instruction 4:**
For a page name returned from instruction 3, capture the HTML for that page in a python variable.

### Third step - extract a list of taxonomic names from the HTML
This part is tricky.

We want to find out what taxonomy Wikipedia has for the 3 species that our script has been given.
We are using the classification as a proxy for the phylogeny, but it is not obvious how to 
    get the classification from the page.
Teaching Python to read the English text is out of the question, as "natural language processing"
    is a very challenging problem in computer science.

Fortunately, even though we are processing HTML, Wikipedia has some special structures that it uses
    in certain contexts.
For example, if you look at a page for a species (such as the page for the 
[European badger](https://en.wikipedia.org/wiki/European_badger)), you'll see a box on the right
    side of the page that has a table with a header (somewhere in the box) with the phrase
    "Scientific classification".

So, let's just write a script to look for that box and that classification part of the box.
The formatting for that box is pretty consistent.
Even though most of Wikipedia is edited in a fairly free-form manner by users, these taxoboxes have
a special WikiText syntax.
And they are rendered (by Wikipedia's servers) into a pretty regular style of HTML.
That will make our task alot easier.

A full discussion of HTML is beyond the scope of this workshop, but the key aspect of it is that
    1. HTML consists of nested tags (for example, the `head` and `body` tags are found inside 
        the `html` tag)
    2. A tag can have attributes, other tags, and text inside of it.


We can avoid the details, because the BeautifulSoup library has a good HTML parser, and we can 
    use it to navigate the HTML document.

Look at https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start to see how you can
convert a string containing HTML (which we have from the previous step) into a "parsed"
representation of the document; this representation is named `soup` in those docs.


**Instruction 5:**
Create a "soup" object for the HTML from your first species name.


#### Getting the "taxo box"
It appears that the table with the classification information is always an HTML `table` element with
a `class` attribue that is assigned the value `"infobox biota"`.
Importantly, it appears to be the only table in a page that has that value of the `class` attribute.

I determined this by using my web browser's "View Source" feature, although it is probably documented
    somewhere in Wikipedia.

**Instruction 6:**
Take a look at
    [the documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class)
    for using BeautifulSoup to find any tags that have a particular value of the class attribute.
Using this info, extract a reference to the classification infobox from the "soup" that you created
    in the previous step.

#### Extracting a list of taxonomic names from the "taxo box"
We wanted a referent to the "taxo box" because it has a more regular syntax compared to the rest of
    the page.
But it is not completely regular.

Like all HTML `table` tags, the taxo box table is composed of a series of `tr` tags (`tr` stands 
for "table row")
It appears that the "rules" for these taxo boxes are:
  * some number (perhaps 0) of `tr` tags  with fairly eclectic info (that we can ignore).
  * a key header we can look for.
  * a series of table rows that have 2 or 3 columns. The first holds a taxonomic rank, and the second
    has the taxonomic name that we want to store.
  * possibly more rows with ecletic info

So we can find the names by:
  1. looping over the `tr` elements.
  2. ignoring everything until we find the header.
  3. then storing the text from the second column of every 2 or 3 column row

The row with a header element we are looking is:
  * a `tr` element that contains
  * a `th` (table header) element that contains
  * an `a` (anchor or "link") element that has
  * the text value equal to "Scientific classification"
  
Note that if we captured the table as the variable `x` then a construct like:

    for row in x.find_all("tr"):
        print(row)

is a way to loop over every row of the table.
We can use a boolean to tell whether or not we have found the "magic" header row.
So we can capture the names in the table with something like:

    tax_names = []
    found_header = False
    for row in x.find_all("tr"):
        if not found_header:
            found_header = row_is_the_magic_header(row)
        else:
            if row_has_two_or_three_columns(row):
                tax_names.append(get_text_second_column(row))
    if len(tax_names) == 0:
        raise ValueError("Was not able to find a taxonomy in the 'infobox biota' part of a species page")

**Instruction 7:**
Put that template code (or something equivalent) in your code, and then see if you can
write the functions:
  * `row_is_the_magic_header` to take an object that represents a `tr` tag and return True if
    it has contains a `th` with an `a` with the text "Scientific classification". 
    The [navigating via tag names](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names)
    documentation will probably help you.
  * `row_has_two_or_three_columns` that take an object that represents a `tr` tag and returns True
    if it contains 2 or 3 `td` tags ("td" stands for "table data")
  * `get_text_second_column` should take a `tr` tag, get the second `td` inside it, and return the
    text content of that tag (see [get_text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text)
    and also note that it makes sense to [strip](https://docs.python.org/3/library/stdtypes.html?highlight=str.strip#str.strip)
    any extraneous whitespace from the text).
    
### Fourth step
The taxonomic names extracted in the previous step will be from the most inclusive taxonomic 
name (e.g. "Animals") to the least inclusive (the name of the queried species).

**Instruction 8:**
Run the previous operations on each of your input species names to get 3 lists of taxonomic names.
This will be easiest to do if you have a wrap all of the previous steps in a function, and then
call that function for each input name.

At this point we should have three lists such as:
    
    first = ['Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Mustelidae', 'Meles', 'M.\xa0meles']
    second = ['Animalia', 'Chordata', 'Aves', 'Galliformes', 'Phasianidae', 'Phasianinae', 'Gallus', 'G.\xa0gallus']
    third = ['Animalia', 'Chordata', 'Mammalia', 'Chiroptera', 'Cistugidae', 'Cistugo', 'C.\xa0seabrae']

(the `\xa0` that you may have noticed between the abbreviation of the Genus name and the specific
 epithet in the last element of the list is a code for a
 [non-breaking space](https://en.wikipedia.org/wiki/Non-breaking_space).
I admit that it is ugly, but it won't interfere with the script we are writing).

How can we convert these three lists into a statement of which pair of species is most closely related?

If we find the last (the highest) index in a list that is found in another list, then then that is
    a measure of how similar the species are.
For instance `first` and `second` agree on elements 0 and 1, so 1 is the highest index in `first`
    that denotes an element that is shared with `second`.
However, `first` and `third` share indices 0, 1, and 2 in common.
Thus `first` and `third` are closest relatives.

Recall that our script is supposed to write `0` in the case of a tie, and otherwise the number
that corresponds to the furthest taxon.

**Instruction 9:**
Write a function that takes the 3 lists of taxonomic names and returns a code from 0 - 4 to 
    indicate what Wikipedia has to say about the phylogenetic relationships of the taxa.