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


## On to step 3
Head over to [Step3-README.md](./Step3-README.md)