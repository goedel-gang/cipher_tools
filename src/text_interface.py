#!/usr/bin/env python3

"""
Hopefully a bit of a script to tie it all together. Should support various
commands and track state, to allow the user to query and edit data.
"""

################################################################################

import shlex
import sys
import re
import textwrap

from input_handling import read_file
from make_subs import parse_subs

from interface_framework import (CipherState, UIError, restrict_args,
                                 show_freq, show_doubles, delete_sub,
                                 show_subbed, show_source, show_table,
                                 general_info, reset_sub)

from collections import namedtuple

opt_pat = re.compile(r"^-(.*?)=(.*)$")

def parse_options(opts):
    arg_acc = []
    opt_acc = {}
    for opt in opts:
        match = opt_pat.match(opt)
        if match:
            opt_acc[match.group(1)] = match.group(2)
        else:
            arg_acc.append(opt)
    return opt_acc, arg_acc

@restrict_args()
def show_help(state):
    """Show help message"""
    return usage

@restrict_args()
def exit_p(state):
    """Exit the program"""
    sys.exit()

@restrict_args(possible=[2])
def update_table(state, new):
    out_t = []
    for k, v in new.items():
        if k in state.subs:
            out_t.append(
                "warning - the value of {} is being changed to {} (it was {})"
                                .format(k, v, state.subs[k]))
        state.subs[k] = v
    return "\n".join(out_t)

commands = [(("frequency", "freq", "f"), show_freq),
            (("doubles", "pairs", "d"), show_doubles),
            (("delete", "remove", "r"), delete_sub),
            (("print", "p"), show_subbed),
            (("source", "s"), show_source),
            (("table", "t"), show_table),
            (("general", "g"), general_info),
            (("reset", "clear", "c"), reset_sub),
            (("help", "h"), show_help),
            (("exit", "quit", "q"), exit_p)]

def format_commands(commands):
    longest = (max(1 + len("|".join(coms)) for coms, _ in commands))
    return "\n".join("!{coms:{length}} - {desc}"
                        .format(coms="|".join(coms), 
                                desc=fun.__doc__,
                                length=longest)
                      for coms, fun in commands)

usage = """\
Anything prefixed with a ! will be considered a command. Anything else will be
interpreted as a series of substitutions to make. The available commands are as
follows:
{}
A command can be given arguments, as space-separated words after the command.
""".format(format_commands(commands))

com_pat = re.compile(r"^!([a-z]+)\b(.*)$")

def parse_com(com):
    match = com_pat.match(com)
    if match:
        return match.group(1), parse_options(shlex.split(match.group(2)))
    else:
        return None, com

def run():
    state = CipherState(source=read_file(),
                        subs={},
                        alt_display=False)
    print(show_help(state))
    while True:
        try:
            com, pargs = parse_com(input("Enter a command/substitutions > "))
            if com:
                for coms, fun in commands:
                    if com in coms:
                        kwargs, args = pargs
                        print(fun(state, *args, **kwargs))
                        break
                else:
                    print("unrecognised command {!r}. see !help for usage"
                                        .format(com))
            else:
                insubs = parse_subs(pargs)
                print(update_table(state, insubs))
                print(show_table(state))

        except UIError as uie:
            print("The following error occurred: {}".format(uie))
        except Exception as e: 
            print("\nThe following critical error occurred: {}".format(e))
            print("Full traceback:")
            raise UIError from e

if __name__ == "__main__":
    run()