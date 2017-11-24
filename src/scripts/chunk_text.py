#!/usr/bin/env python3

"""
Splitting text into chunks (a la polybius). Use the value of the -c parameter
to set how long blocks to accumulate are. To assign a letter to each block in
order to allow cryptanalysis with other tools, use -a.
"""

import re
import sys
import string
import argparse
import itertools

acc_codex = string.ascii_uppercase + string.digits

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chunk", default=2, type=int,
                                    help="chunk length")
    parser.add_argument("-a", "--accumulate", action="store_true",
                                    help="accumulate chunks into single characters")
    return parser.parse_args()

def chunk(it, n):
    return itertools.zip_longest(*[iter(it)] * n, fillvalue=" ")

def accumulate_chars(plain, chunk_length):
    combs = {}
    for a in map("".join, chunk(plain, chunk_length)):
        if a not in combs:
            combs[a] = len(combs)
            if len(combs) > len(acc_codex):
                raise IndexError("Ran out of symbols")
        sys.stdout.write(acc_codex[combs[a]])

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("This is a command-line script requiring stdin")
    args = parse_args()
    plain = re.findall("[a-zA-Z]", sys.stdin.read())
    if args.accumulate:
        accumulate_chars(plain, args.chunk)
    else:
        print(" ".join(map("".join, chunk(plain, args.chunk))))
