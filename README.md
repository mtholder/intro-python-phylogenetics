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
[this blog post by Emily Thompson](https://pandasthumb.org/archives/2014/10/the-family-tree.html);
apparently the image is originally from 
[the human origins exhibit by the Smithsonion](http://humanorigins.si.edu/evidence/genetics).

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

See [Step2-README.md](./Step2-README.md) for details.

### 3. Main tasks
See [Step3-README.md](./Step3-README.md) for details of the 4 main tasks
