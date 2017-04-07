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
    example_filepath = "testdata/ex-query.csv"
    return example_filepath

def parse_queries_from_csv(the_csv_filepath):
    """Read the local filesystem's copy of the query data are return a list of 
    three species for each query found in the file.
    To do this we return a list of lists.
    """
    warn("We still have a dummy version of parse_queries_from_csv !")
    warn('We should really be reading from "{}" here!'.format(the_csv_filepath))
    # [] is the "literal syntax" for a empty list. Thus the value of
    # example_data is a list of 3 lists.
    # The first 2 elements are lists that we expect to generate a result from Open Tree and
    #   Wikipedia because these are 3 real species names.
    # The first string in the third list is not a valid name, so we should expect
    #   an error from the query functions.
    example_data = [['Caretta caretta', 'Babirusa babyrussa', 'Zea mays'],
                    ["Rattus norvegicus", "Alces alces", "Meles meles"],
                    ["not really a species name", "Rattus norvegicus", "Alces alces"]
                   ]
    return example_data

def get_phylogeny_according_to_open_tree(first_sp, second_sp, third_sp):
    warn("We still have a dummy version of get_phylogeny_according_to_open_tree !")
    return 1

def get_phylogeny_according_to_wikipedia(first_sp, second_sp, third_sp):
    warn("We still have a dummy version of get_phylogeny_according_to_wikipedia !")
    return 2

def write_summary(results):
    warn("We still have a dummy version of write_summary !")
    sys.stdout.write("You would see some results here, if we had written the script.\n")


warn("Script is not implemented yet - just mock functions at this point.")

print("""If you run the script, you should see this message written to the standard output
stream. You don't see the warnings inside the functions, becuase this script just defines
the functions. They need to be called in order for the instructions placed inside the functions
to be run.

It is possible that you'll see this message intercalated with the warn message above. This is
a side effect of the fact that your shell will write the output of both the standard error
and standard output streams to the same terminal window.
""")


