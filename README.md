# Python tutorial
Prepared for a workshop on Python held on April 8th, 2017 and organized by KU's IMSD program.
Unless otherwise stated, the content was written by Mark T. Holder (MTH);
the content written by MTH can be used under FreeBSD or GPL licenses.

# Motivating project

## Phylogenetics
MTH is a working on the [Open Tree of Life project](http://tree.opentreeoflife.org) which aims
to summarize what we know about the phylogenetic relationships of Life on Earth.
"Phylogenetic relationships" describe which species are more closely related to other
    species where "more closely related" is equivalent to "having a more recent
    ancestral species in common."
The simplest phylogenetic statement is one about three species.
For example: "Humans and chimps are more closely related to each other that they are to
gorillas."
That statement means that the most recent common ancestor of humans and gorillas was a 
species that lived earlier than the most recent common ancestor of humans and chimps.

Frequently we depict these relationships in a tree. See for example, this:
 
<img src="https://pandasthumb.org/uploads/2014/primate-family-tree-780x520_0.gif" width="70%" alt="greatapetree" />

nice image of the phylogenetic tree of Primates that appeared on
[this blog post by Emily Thompson](https://pandasthumb.org/archives/2014/10/the-family-tree.html).

Taxonomic statements can also convey phylogenetic relationships.
For example, one can see that scientists think that humans and chimps
are more closely relate to each other than either is to baboons based
on a taxonomic classification. 
All three of these primates are members of a group called
[Haplorhini](https://en.wikipedia.org/wiki/Haplorhini).
However, while humans and chimps are members of 
[Hominidae](https://en.wikipedia.org/wiki/Hominidae), baboons are not 
members of this group.
Thus sharing a taxonomic group can be used as a proxy for "sharing a more recent common
ancestor" if the classification is a phylogenetic classification.

## Question and Main Task
**How often the the phylogenetic relationships reported by the Open Tree of Life project agree with
the classification used by Wikipedia?**

We will:
  1. build an arbitrary query set by filling out a shared Google Spreadsheet
  2. sketch out a high-level overview of the tasks to be performed
  3. divide into groups to implement each task
  4. combine our code - and hopefully get an answer.

### 1. generating a test data set.
We will use this shared 
[python-tutorial-Apr-2017 folder](https://drive.google.com/drive/folders/0B3YfNFYgyCWkdVRwX0Z1clB4VG8)
on Google Drive to share files.

In the
[phylogenetic-query](https://drive.google.com/open?id=16AZ9Po7h8Qa3ink55bZn4GaiS2pBPVQMMuDd2TBIByA)
spreadsheet you'll find a simple table with 4 columns.
In the next empty row enter your initials, and then the scientific
 names of 3 different species - one in each of the next three columns.
 
### 2. Sketch of tasks to be performed

### 3. Tasks 
We'll need teams to do each of the following tasks.
Ideally, we'd work in pairs.
But if you'd prefer to work alone, just pick a task and come up with your
own implementation.

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


