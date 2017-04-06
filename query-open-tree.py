#!/usr/bin/env python
import requests
import json
import sys
import os
import re

SCRIPT_PATH = sys.argv[0]
# the script name is the last part of the path to the script
SCRIPT_NAME = os.path.split(SCRIPT_PATH)[-1]
verbose_mode = False
API_HEADERS = {"content-type": "application/json",
               "accept": "application/json",
              }


def error(msg):
    """Outputs a message to the standard error stream with the SCRIPT_NAME as a prefix.

    This is good practice, because in a complex pipeline, it lets the users know which tool
        is complaining.
    """
    sys.stderr.write("{}: {}\n".format(SCRIPT_NAME, msg))

def status(msg):
    if verbose_mode:
        error(msg)

def get_taxon_id_from_name(name):
    """Returns the Open Tree Taxonomy ID for the name, or None if there is a problem.

    A problem could be 0 or >1 matches.
    """
    name_list = [name]
    args = {"names": name_list}
    response = requests.post("https://api.opentreeoflife.org/v3/tnrs/match_names",
                             headers=API_HEADERS,
                             data=json.dumps(args))
    response.raise_for_status()
    obj = response.json()
    mn = obj.get("unambiguous_names")
    if mn != name_list:
        error('Could not find the name "{}" in the Open Tree taxonomy services.'.format(name))
        return None
    results = obj["results"]
    if len(results) != 1:
        error('Found {} resulst for the name "{}" in the Open Tree taxonomy services.'.format(len(results), name))
        return None
    the_res = results[0]
    m_list = the_res["matches"]
    if len(m_list) != 1:
        error('Found {} matches for the name "{}" in the Open Tree taxonomy services.'.format(len(m_list), name))
        return None
    the_match = m_list[0]
    the_taxon = the_match["taxon"]
    return the_taxon["ott_id"]

def get_induced_tree_string(id_list):
    args = {"ott_ids": id_list,
            "label_format": "id"
           }
    response = requests.post("https://api.opentreeoflife.org/v3/tree_of_life/induced_subtree",
                             headers=API_HEADERS,
                             data=json.dumps(args))
    response.raise_for_status()
    obj = response.json()
    return obj["newick"]

def classify_tree_output(id_list, tree):
    if tree.count('(') != 2:
        return 0 # just one grouping for all 3 taxa
    assert(tree.count(')') == 2)
    sis_gr_pat = re.compile(r"[(].*[(]ott([0-9]+),ott([0-9]+)[)].*[)].*")
    m = sis_gr_pat.match(tree)
    if not m:
        raise ValueError("tree {} did not match our expected pattern for a resolved tree.".format(tree))
    one_id = int(m.group(1))
    other_id = int(m.group(2))
    for zero_based_index, taxon_id in enumerate(id_list):
        if taxon_id != one_id and taxon_id != other_id:
            return 1 + zero_based_index
    raise ValueError("id_list {} did not contain an ID that was not in the ingroup of {}".format(id_list, tree))

if __name__ == '__main__':
    import argparse
    import codecs
    usage = """If given 3 names, this script will convert them open tree taxonomy IDs, query Open Tree for the induced tree.
Writes to standard output:
  * the argument number (1, 2, or 3) for the "outgroup" if the induced tree is resolved.
  * 0 if the tree is not resolved.

Non-zero exit code (and messages to stderr) occur for network problems, or the failure to reserve
the names to taxonomic IDs
"""
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('names',
                        nargs=3,
                        type=str,
                        help="The names of the taxa that define the phylogenetic triplet")
    parser.add_argument('--verbose',
                        action="store_true",
                        help="run the program in verbose mode")

    args = parser.parse_args()
    verbose_mode = args.verbose
    names = args.names
    if len(set(names)) != 3:
        sys.exit("Need three unique names as arguments\n")
    try:
        id_list = []
        for n in names:
            i = get_taxon_id_from_name(n)
            if i is None:
                sys.exit(1)
            id_list.append(i)
            status('  "{}" -> {}'.format(n, i))
        if len(set(id_list)) != 3:
            sys.exit("There must have been a synonym, only two IDs were found: {}\n".format(id_list))
        tree_string = get_induced_tree_string(id_list)
        status("tree_string = {}".format(tree_string))
        out_code = classify_tree_output(id_list, tree_string)
        print(out_code)
    except:
        error("Exiting due to an exception being raised")
        raise