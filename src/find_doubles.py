#!/usr/bin/env python3

"""
Finding adjacently occurring pairs of letters
"""

################################################################################

import re

from collections import Counter

from input_handling import read_file

double_pat = re.compile(r"([A-Z])\1", re.IGNORECASE)

def get_doubles(source):
    print(double_pat.findall(source))
    return "\n".join("{} occurs {:3} times".
                     format(letter, frequency)
                  for letter, frequency in
                        Counter(
                            match.group(0)
                                for match in 
                                    double_pat.finditer(source)).
                            most_common())

if __name__ == "__main__":
    source = read_file()
    print("Received source:\n{}\n".format(source))
    print("Doubles in source:\n{}\n".format(get_doubles(source)))