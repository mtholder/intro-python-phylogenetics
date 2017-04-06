# Sketch of the pipeline

The basic steps to answer our question are:
  1. Download the query data from Google as a comma-separated-value spreadsheet.
  2. Interpret each line of the csv file as query about 3 species by reading columns 2 - 4
  of the spreadsheet (and ignoring the first, header row).
  3. `for` each query:
      1. Call a [query-open-tree](./query-open-tree-README.md) procedure and interpret
       its results.
      2. Call the [query-wikipedia](./query-wikipedia-README.md) procedure and interpret
       its results.
      3. Transform the results into a summary such as "the 2 phylogeny sources agreed",
       "the 2 phylogeny sources disagreed", or "there was an error in one or both sources".
  4. Report a summary of all of the queries the user.



## Convention for inter-task communication
Since we are writing the control script and the scripts for the queries to Open Tree and
    Wikipedia, we can decide on how the protocol for how the pieces of the pipeline "talk"
    to each other.

In the context of this exercise we want to make it easy for:
  1. the implementers of the [query-open-tree](./query-open-tree-README.md) task to
    express what phylogenetic tree Open Tree reports for the 3 species.
  2. the implementers of the [query-wikipedia](./query-wikipedia-README.md) task to
    express what phylogenetic tree is implied by the Wikipedia taxonomy for the 3 species.
  3. the implementers of the [control-script](./control-script-README.md) task to
    be able to interpret the results of the 2 query tasks.

We need to establish a convention for the query tools to tell the control script the answer, and
    it make sense to use the same convention in the query-open-tree tool and
    the query-wikipedia tool.

We are really defining our an *interface* in our pipeline.
We could think of it as the command line interface (CLI) of our query scripts.
If we think of our query scripts as computational resources, then we could think of our
    convention as a tiny application program interface (API).

## query-tool-interface
MTH suggests:

  * the user (or the [control-script](./control-script-README.md)) 
    will provides the query script with 3 arguments.
    These are the names of the 3 species of interest.
  * A non-zero exit code for the query script if the answer cannot be determined. Non-zero
    exit code for failure of a program is a **very** common convention
    that you should conform to.
    It makes it easy to piece tools together in a robust pipeline.
    A common cause of an error in our pipeline will be the failure of one of our
    phylogeny services to recognize a species name.
  * A zero exit code for success and write the following info to standard output to
    provide the answer returned by the queried web service:
    * `0` means that the web resource (Open Tree of Wikipedia) does not provide a guess
        for which of the 3 species are more closely related.
    * `1` means that the first species name is the most distantly related of the 3 species.
    * `2` means that the second species name is the most distantly related of the 3 species.
    * `3` means that the third species name is the most distantly related of the 3 species.

## Our other interface
The decision to use CSV with columns 2, 3, and 4 as species names can be thought of 
    defining our other interface between components (the 
    [control-script](./control-script-README.md)
    and the [fetch-query-data](fetch-query-data-README.md) task in this case).


# The core tasks

#### 3A: fetch-query-data task
The  **fetch-the-query-data** task is to 
  1. download the spreadsheet from Google Drive, and
  2. write it as a comma-separated-value file on our local filesystem.

See [fetch-query-data-README.md](./fetch-query-data-README.md)


#### 3B: query-wikipedia team
See [query-wikipedia](./query-wikipedia-README.md) for a more detailed description
 of  the component that should:
 1. fetch the wikipedia page for each species
 2. find the classification "box" on each page
 3. interpret that classification box to figure out the phylogenetic relationships.
 4. convert the phylogenetic relationships to the easy-to-process convention
  described in the [Step2-README.md](./Step2-README.md#query-tool-interface)

#### 3V: query-open-tree team
A **query-open-tree** task that will need to use the
    [Open Tree of Life web APIs](https://github.com/OpenTreeOfLife/germinator/wiki/Open-Tree-of-Life-Web-APIs)
    to:
  1. find an taxonomic ID (an OTT ID) for each name, and
  2. fetch Open Tree's phylogenetic relationships for the three species
  3. Convert that tree to some form of easy-to-process response for the control
  script.
  
  This will teach some use of web API's and the lovely [requests](http://docs.python-requests.org/en/master/)
  Python package.
  The last step will probably involve some regular expressions.



#### 3D: control script team
The **control script** will run the whole pipeline and summarizes the
    results.
Specifically, this will entail:
  1. Running the download script once to fetch the data.
  2. Writing a "loop" to walk over every data line in the query data file. For each
    line, the script will:
      1. Call the **query-open-tree** procedure and interpret its results
      2. Call the **query-wikipedia** procedure and interpret its results
      3. Transform the results into a summary such as "the 2 phylogeny sources agreed",
       "the 2 phylogeny sources disagreed", or "there was an error"
  3. Report this summary to the user.
    
This will probably be the most basic python programming. So it might be
    a good choice if you have not done any programming.


