## Main tasks
You'll probably only have time to work on 1 (but 3A is very short, so you might be able
to do that and join another task).

### 3A: fetch-query-data task
See [fetch-query-data-README.md](./fetch-query-data-README.md) for details of the task
to:
  1. download the spreadsheet from Google Drive, and
  2. write it as a comma-separated-value file on our local filesystem.


This will teach:
  * the basics of lovely [requests](http://docs.python-requests.org/en/master/) Python package, and
  * the joys of character encoding (`codecs` package)


### 3B: query-wikipedia team
See [query-wikipedia](./query-wikipedia-README.md) for a more detailed description
 of the component that should:
 1. fetch the wikipedia page for each species
 2. find the classification "box" on each page
 3. interpret that classification box to figure out the phylogenetic relationships.
 4. convert the phylogenetic relationships and write them out to standard out

The script should follow the easy-to-process convention
  described as the query-tool-interface in 
  the [Step2-README.md](./Step2-README.md#query-tool-interface).

This will teach:
  * use of the  [wikipedia](https://wikipedia.readthedocs.io/en/latest/) Python package, and
  * the use of the [beautiful soup](https://www.crummy.com/software/BeautifulSoup/) a robust
  HTML parser useful when "screen scraping" web pages.



#### 3C: query-open-tree team
A **query-open-tree** task that will need to use the
    [Open Tree of Life web APIs](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)
    to:
  1. find an taxonomic ID (an OTT ID) for each name, and
  2. fetch Open Tree's phylogenetic relationships for the three species
  3. convert the phylogenetic relationships and write them out to standard out

The script should follow the easy-to-process convention
  described as the query-tool-interface in 
  the [Step2-README.md](./Step2-README.md#query-tool-interface).

This will teach:
  * some details of using web API's,
  * the lovely [requests](http://docs.python-requests.org/en/master/) Python package, and
  * the last step will probably involve some regular expressions.



#### 3D: control script team
The [control script](./control-script-README.md) will run the whole pipeline and summarizes the
    results.


This will probably be the most basic python programming. So it might be
    a good choice if you have not done any programming.


This will teach:
  * basic python control flow, keywords, and data types
  * Use of the `subprocess` module to run other programs.

