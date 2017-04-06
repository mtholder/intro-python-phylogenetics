# Sketch of the pipeline

The basic steps to answer our question are:
  1. Download the query data from Google.
  2. Interpret each line of the csv file as query about 3 species
  3. `for` each query:
      1. Call a **query-open-tree** procedure and interpret its results
      2. Call the **query-wikipedia** procedure and interpret its results
      3. Transform the results into a summary such as "the 2 phylogeny sources agreed",
       "the 2 phylogeny sources disagreed", or "there was an error"
  4. Report a summary of all of the queries the user.

Since we are writing the control script and the scripts for the queries to Open Tree and
    Wikipedia, we can decide on how the protocol for how the pieces of the pipeline "talk"
    to each other.


#### 3A: fetch-query-data team
The  **fetch-the-query-data** task is to 
  1. download the spreadsheet from Google Drive, and
  2. write it as a comma-separated-value file on our local filesystem.

We can easily do this operation through the **File >> Download As** menu option
  of the Google spreadsheet if no one wants to learn how to do this programmatically.
  It is nice to know how to do this programmatically, so that you can have a pipeline that
  is easy to re-run.

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

#### 3C: query-wikipedia team
A **query-wikipedia** task that will need to:
 1. fetch the wikipedia page for each species
 2. find the classification "box" on each page
 3. interpret that classification box to figure out the phylogenetic relationships.
 4. Convert that phylogenetic tree to the same easy-to-process form as used by the **query-open-tree** group
  

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


