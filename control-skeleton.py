#!/usr/bin/env python
"""
This script will download a google spreadsheet that represents a series of triples of species
    names.
It will query Open Tree of Life APIs and Wikipedia, and report a summary of how often they
    agree and disagree.
"""

# If you are running python 2, you'll need to uncomment the next line
#from __future__ import print_function

# We import the sys and os modules for some interactions with the operating system.
import sys
import os

# The filepath to the running script is the first argument in the list of command line
#   arguments. These arguments are accessible via the argv variable in the sys module.
# We access a variable from a module using the dot syntax. So sys.argv in this case.
# The variable is a list. Python uses 0-based indexing. So we can get the first
#   element of a list using the syntax:   list_var_name[0]
_script_path = sys.argv[0]

# It is often nice to report the script's name in errors and warning messages.
# We can get this by splitting the filepath by the directory separator.
# This converts a string to a list of strings.
_script_path_fragments = os.path.split(_script_path)

# We can grab the last element of a list by using the -1 index:
SCRIPT_NAME = _script_path_fragments[-1]

# When debugging it is nice to be able to run a script in "normal" mode or "verbose" mode
#   using a command line flag.
# A simple way to do this is to use the convention that if any of the command line
#   arguments is "--verbose" the run in verbose mode (otherwise run in normal mode).
# The Python "in" operator returns True or False if the first operand is inside the collection
#   that is the second argument:
VERBOSE_MODE = '--verbose' in sys.argv

# Now we have some functions to help us output info to the user.
# In Python a line starting with "def " is a function definition. The syntax is:
#   def FUNCTION_NAME_GOES_HERE(SOME_NUMBER, OF_ARGUMENTS_LISTED, HERE):
#       INDENTED INSTRUCTIONS HERE

def warn(msg):
    """Writes `msg` to the stderr stream. Adds the script name as prefix and a newline."""
    # the next line calls a method (which is like a function) of the str class which
    #   Python uses to store character strings.
    # Python interprets the literal "{} WARNING: {}\n" as a object of type str.
    # That object has a format method that can be called.
    # Calling it will return a new str object in which the {} characters are replaces with
    #   the values that are passed into the format method call.
    decorated_message = "{} WARNING: {}\n".format(SCRIPT_NAME, msg)
    sys.stderr.write(decorated_message)
    sys.stderr.flush()

def debug(msg):
    """Writes `msg` to the stderr stream with a prefix and newline, but only if the script
    is being run in verbose mode.
    """
    if not VERBOSE_MODE:
        return
    decorated_message = "{}: {}\n".format(SCRIPT_NAME, msg)
    sys.stderr.write(decorated_message)
    sys.stderr.flush()

# Below here I have written the some "mock" versions of the main functions that
#   we will need to fill in.
# These functions return the write type of data, but are not doing the real analysis.
# It is helpful to have mocks so that we can set up the full pipeline in a piece by piece
#   fashion.
# It will be runnable from the beginning. We should only take the warn() calls out when we think
#   that we have the functions correctly implements.


# Here we have a function with a single argument, but a default value. If
# called without an argument, the function will use the doc_id that you see.
def download_query_data(doc_id="16AZ9Po7h8Qa3ink55bZn4GaiS2pBPVQMMuDd2TBIByA"):
    """Download data as csv and return the filepath of the file to the caller.
    
    If you downloaded the zip archive from GitHub and are running this script
    from the top of the intro-python-phylogenetic directory then this
    example path will work, because I have a tiny query set in that location.
    """
    warn("We still have a dummy version of download_query_data !")
    example_filepath = "/home/mtholder/Downloads/q.csv"
    return example_filepath

def parse_queries_from_csv(the_csv_filepath):
    """Read the local filesystem's copy of the query data are return a list of 
    three species for each query found in the file.
    To do this we return a list of lists.
    """
    query_list = []
    with open(the_csv_filepath, "rU") as input_stream:
        for line in input_stream:
            # line will be bound to a string ending with a newline here.
            line_without_extra_whitespace = line.strip()
            ls = line_without_extra_whitespace.split(',')
            query = ls[1:]
            query_list.append(query)
    return query_list[1:]

def get_phylogeny_according_to_open_tree(first_sp, second_sp, third_sp):
    import subprocess
    command_to_run = [sys.executable, "query-open-tree.py", "--verbose", first_sp, second_sp, third_sp]
    try:
        raw_output = subprocess.check_output(command_to_run)
    except:
        return None
    return int(raw_output)

def get_phylogeny_according_to_wikipedia(first_sp, second_sp, third_sp):
    import subprocess
    command_to_run = [sys.executable, "query-wikipedia.py", first_sp, second_sp, third_sp]
    try:
        raw_output = subprocess.check_output(command_to_run)
    except:
        return None
    return int(raw_output)
def write_summary(results):
    d, a, t = results
    print("{} disagreements".format(d))
    print("{} agreements".format(a))
    print("{} failures or don't know responses".format(t - a -d))


fp = download_query_data()
query_list = parse_queries_from_csv(fp)
q = None
num_agree = 0
num_disagree = 0
for q in query_list:
    first, second, third = q
    ot_r = get_phylogeny_according_to_open_tree(first, second, third)
    wiki_r = get_phylogeny_according_to_wikipedia(first, second, third)
    if (ot_r is not None) and (wiki_r is not None) and (ot_r > 0) and (wiki_r > 0):
        if ot_r == wiki_r:
            num_agree += 1
        else:
            num_disagree = num_disagree + 1
    debug("For the query {}, OT returned {} and Wikipedia returned {}".format(q, ot_r, wiki_r))
write_summary([num_disagree, num_agree, len(query_list)])
