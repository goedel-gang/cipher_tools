#!/usr/bin/env python3

"""
Modify the casing of text. Use -l to get lowercased text instead
"""

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType("r"), help="input file")
    parser.add_argument("-l", "--lower", action="store_true",
                                help="make text lowercase rather than uppercase")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.lower:
        sys.stdout.write(args.input.read().lower())
    else:
        sys.stdout.write(args.input.read().upper())
