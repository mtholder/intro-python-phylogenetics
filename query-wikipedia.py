#!/usr/bin/env python
import wikipedia
from bs4 import BeautifulSoup
import sys
import os
import requests

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

def find_first_wikipedia_hit(n):
    results = wikipedia.search(n)
    num_hits = len(results)
    if num_hits == 0:
        raise ValueError('No Wikipedia hits for "{}"'.format(n))
    if num_hits > 1:
        status('Returning only the first of {} Wikipedia hits for "{}"'.format(num_hits, n))
    return results[0]

def get_classification_info_box_from_soup(wiki_soup):
    cib_list = wiki_soup.find_all("table", class_="infobox biota")
    if len(cib_list) != 1:
        raise ValueError('Failed to find "infobox biota" table in Wikipedia page')
    return cib_list[0]

def append_name_from_two_column_row(row, root_to_tip_taxon_list):
    cells = row.find_all("td")
    if len(cells) == 2:
        taxon_name_cell = cells[1]
        taxon_name = taxon_name_cell.get_text().split('[')[0].strip()
        if taxon_name.startswith('.'):
            #weird that some ...... entries are found.
            return
        root_to_tip_taxon_list.append(taxon_name)


def return_or_throw_classification(found_header, root_to_tip_taxon_list):
    if not found_header:
        raise ValueError('Did not find the "Scientific classification" link in a row in the infobox')
    if not root_to_tip_taxon_list:
        raise ValueError('Did not find expected table after "Scientific classification" in the infobox')
    return root_to_tip_taxon_list

def get_classification_from_detailed_taxonomy(url):
    response = requests.get(url)
    response.raise_for_status()
    wiki_soup = BeautifulSoup(response.content, 'html.parser')
    class_info_box = get_classification_info_box_from_soup(wiki_soup)
    found_header = False
    root_to_tip_taxon_list = []
    for row in class_info_box.find_all("tr"):
        if found_header:
            append_name_from_two_column_row(row, root_to_tip_taxon_list)
        elif row.th:
            found_header = True
    return return_or_throw_classification(found_header, root_to_tip_taxon_list)


def get_classification_from_wiki_html(wiki_html):
    wiki_soup = BeautifulSoup(wiki_html, 'html.parser')
    class_info_box = get_classification_info_box_from_soup(wiki_soup)
    found_header = False
    root_to_tip_taxon_list = []
    for row in class_info_box.find_all("tr"):
        if found_header:
            append_name_from_two_column_row(row, root_to_tip_taxon_list)
        else:
            try:
                for link in row.th.find_all("a"):
                    #print('link.get_text() = "{}"'.format(link.get_text()))
                    if 'scientific classification' == link.get_text().strip().lower():
                        found_header = True
                    try:
                        target = link["href"]
                        if target.startswith("/wiki/Template:Taxonomy/"):
                            full_url = "https://en.wikipedia.org" + target
                            return get_classification_from_detailed_taxonomy(full_url)
                    except:
                        pass
            except Exception as x:
                pass
    return return_or_throw_classification(found_header, root_to_tip_taxon_list)

def find_last_ind_of_first_in_second(f, s):
    last = -1
    for n, fel in enumerate(f):
        if fel in s:
            last = n
    return last

def classify_tree_based_on_classification_lists(c_lists):
    first, second, third = c_lists
    f2s = find_last_ind_of_first_in_second(first, second)
    f2t = find_last_ind_of_first_in_second(first, third)
    if f2s == f2t:
        s2f = find_last_ind_of_first_in_second(first, second)
        s2t = find_last_ind_of_first_in_second(first, third)
        if s2f == s2t:
            return 0
        if s2f < s2t:
            return 1
        return 3
    if f2s < f2t:
        return 2
    return 3

if __name__ == '__main__':
    import argparse
    usage = """If given 3 names, this script will try to find a page for each on Wikipedia and 
use the taxonomic classification box on each page to infer the phylogeny for the species.

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
    REAL_RUN = True
    if len(set(names)) != 3:
        sys.exit("Need three unique names as arguments\n")

    try:
        # Here, I use a terse syntax equivalent to:
        #   page_names = []
        #   for i in names:
        #       page_names.append(find_first_wikipedia_hit(i))
        #
        '''

        if REAL_RUN:
            page_names = [find_first_wikipedia_hit(i) for i in names]
        else:
            page_names = names
        if len(set(page_names)) != 3:
            sys.exit("Did not find 3 unique top hits for the species names. Only have {}".format(set(page_names)))
        classification_lists = []
        for pn in page_names:
            try:
                if REAL_RUN:
                    page_obj = wikipedia.page(pn)
                    page_html = page_obj.html()
                else:
                    fn = "/home/mtholder/Downloads/view-source_https___en.wikipedia.org_wiki_Brown_rat.html"
                    page_html = open(fn, 'r').read()
                c = get_classification_from_wiki_html(page_html)
                print(c)
                classification_lists.append(c)
            except:
                error('Error extracting info from Wikipedia page for "{}"'.format(pn))
                raise
        '''
        classification_lists = [
            ['Eukaryota', 'Unikonta', 'Opisthokonta', 'Holozoa', 'Filozoa', 'Animalia', 'Eumetazoa',
         'Bilateria', 'Nephrozoa', 'Deuterostomia', 'Chordata', 'Craniata', 'Vertebrata',
         'Gnathostomata', 'Eugnathostomata', 'Teleostomi', 'Tetrapoda', 'Reptiliomorpha', 'Amniota',
         'Synapsida', '.....', 'Mammaliaformes', 'Mammalia', 'Eutheria', 'Placentalia', '.....',
         'Artiodactyla', 'Cetruminantia', 'Ruminantiamorpha', 'Ruminantia', 'Pecora', 'Cervidae',
         'Capreolinae', 'Alces'],
            ['Animalia', 'Chordata', 'Mammalia', 'Rodentia', 'Muridae', 'Rattus', 'R.\xa0norvegicus'],
            ['Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Mustelidae', 'Meles', 'M.\xa0meles']
        ]
        tree_integer_code = classify_tree_based_on_classification_lists(classification_lists)
        print(tree_integer_code)
    except:
        error("Exiting due to an exception being raised")
        raise