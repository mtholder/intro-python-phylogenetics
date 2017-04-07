#!/usr/bin/env python
"""Simple script to have a similar interface as the query scripts, but which is very fast to run

It will:
    - exit with non-zero exit code if given something other than 3 different strings as arguments
    - exit with exit code 0, and write 0 if all 3 arguments have the same length. Otherwise,
    - exit with an exit code of zero and write a 1-based index for the "lowest" argument 
        where the "lowest" is defined to be:
          * the shortest argument, and
          * (if there is a two-way tie for shortest length) the alphabetically lowest string is
            lowest.

"""
import sys
args = sys.argv[1:]
assert len(args) == 3, "Expecting 3 args"
assert len(set(args)) == 3, "Expecting the 3 args to be distinct"

len_name_pair_list = []
for a in args:
    len_name_pair_list.append([len(a), a])

len_name_pair_list.sort()

chosen_len, chosen_name = len_name_pair_list[0]
last_len = len_name_pair_list[2][0]
if chosen_len == last_len:
    print(0)
else:
    for index, name in enumerate(args):
        if name == chosen_name:
            print(index + 1)
