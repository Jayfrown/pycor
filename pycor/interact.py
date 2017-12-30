##
# pycor/interact.py
#    functions for user interaction
#

from __future__ import print_function

import sys
import textwrap

try:
    from termcolor import colored
except Exception:
    def colored(args, bogus):
        return args

# message types
def gMsg(args, **kwargs):
    print(colored("pycor", 'blue') + ':', args, file=sys.stdout, **kwargs)
def bMsg(args, **kwargs):
    print(colored("pycor",  'red') + ':', args, file=sys.stderr, **kwargs)

# program header
def print_header():
    print(colored("Container", 'magenta') + "/" + colored("Overlay", 'magenta'))
    print("leverage overlayfs with lxd containers")
    print()

# usage hints
def print_usage():
    print("usage: " + sys.argv[0] + " [-h|--help] action [args]")

def full_usage():
    print_usage()
    print("available actions:")
    print(textwrap.dedent("""
    {containers}:
        launch [{name}]        - new overlain container
        delete  {name}         - umount and delete container
    """).format(name=colored("name", 'magenta'),
          containers=colored("containers", 'blue')))

# help messages
def print_help(topic):
    raise NotImplementedError("help is not implemented")
