"""
Apply a columnar permutation transposition to a text
"""

import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("permutation", type=str,
                            help="keyword for permutation - can use digits")
    return parser.parse_args()

def chunk(it, n):
    return zip(*[iter(it)] * n)

def clean(plain):
    return plain.strip().replace(" ", "")

def build_perm(kw):
    if len(set(kw)) != len(kw):
        raise ValueError("keyword has repeated letters")
    vals = {i: ind for ind, i in enumerate(sorted(kw))}
    return [vals[i] for i in kw]

def perm_transp(plain, perm):
    return "".join("".join(row[i] for i in perm) for row in chunk(strpd, len(perm)))

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.exit("this is a command line script requiring stdin")
    args = parse_args()
    strpd = clean(sys.stdin.read())
    perm = build_perm(args.permutation)
    print("using permutation {}".format(perm))
    print(perm_transp(strpd, perm))