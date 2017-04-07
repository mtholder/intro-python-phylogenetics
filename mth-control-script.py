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
import subprocess
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
    example_filepath = "testdata/ex-query.csv"
    return example_filepath

def parse_queries_from_csv(the_csv_filepath):
    """Read the local filesystem's copy of the query data are return a list of 
    three species for each query found in the file.
    To do this we return a list of lists.
    """
    header_read = False
    q_list = []
    with open(the_csv_filepath, 'r') as inp:
        for line in inp:
            ls = line.strip()
            ll = ls.split(',')
            if len(ll) < 4:
                warn("Found row with too few columns!:\n{}".format(ls))
                continue
            if not header_read:
                header_read = True
                continue
            q_list.append(ll[1:4])
    return q_list


def get_phylogeny_according_to_open_tree(first_sp, second_sp, third_sp):
    return gen_query("query-open-tree.py", first_sp, second_sp, third_sp)

def gen_query(script_name, first_sp, second_sp, third_sp):
    command_to_run = [sys.executable, script_name, first_sp, second_sp, third_sp]
    try:
        raw_output = subprocess.check_output(command_to_run)
        return int(raw_output)
    except:
        return None

def get_phylogeny_according_to_wikipedia(first_sp, second_sp, third_sp):
    return gen_query("query-wikipedia.py", first_sp, second_sp, third_sp)

def write_summary(results):
    res_mat, num_agreed, num_disagreed = results
    labels = ["failed", "didn't know", "reported a resolved tree"]
    for oi in range(3):
        olabel = labels[oi]
        for wi in range(3):
            wlabel = labels[wi]
            count = res_mat[oi][wi]
            print("# of queries where OT {} and wikipedia {} was: {}".format(olabel, wlabel, count))
    print("# of queries where both resolved the tree and they disagreed: {}".format(num_disagreed))
    print("# of queries where both resolved the tree and they agreed: {}".format(num_agreed))


csv_f = download_query_data()
q_list = parse_queries_from_csv(csv_f)
FAILED = 0
DONT_KNOW = 1
CHOSE_MOST_DISTANT = 2
results = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
          ]
num_agreed, num_disagreed = 0, 0

def res_to_res_ind(r):
    """Converts IPC std out to tuple of (results index, most_distant_tree)
    """
    if r is None:
        return (FAILED, None)
    if r == 0:
        return (DONT_KNOW, None)
    return (CHOSE_MOST_DISTANT, r)

for q in q_list:
    first, second, third = q
    debug(' about to query "{}"'.format('" "'.join(q)))
    ot_res = get_phylogeny_according_to_open_tree(first, second, third)
    ot_i, ot_sp = res_to_res_ind(ot_res)
    wiki_res = get_phylogeny_according_to_wikipedia(first, second, third)
    wiki_i, wiki_sp = res_to_res_ind(wiki_res)
    results[ot_i][wiki_i] += 1
    if wiki_i == CHOSE_MOST_DISTANT and ot_i == CHOSE_MOST_DISTANT:
        if ot_sp == wiki_sp:
            num_agreed += 1
        else:
            num_disagreed += 1
write_summary([results, num_agreed, num_disagreed])


