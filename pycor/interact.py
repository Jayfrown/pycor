##
# pycor/interact.py
#    functions for user interaction
#

from __future__ import print_function

import sys
import textwrap


# message types
def gMsg(string):
    print("pycor: ", string, file=sys.stdout)
def bMsg(string):
    print("pycor: ", string, file=sys.stderr)

# program header
def print_header():
    print("Container/Overlay")
    print("leverage overlayfs with lxd containers")
    print()

# usage hints
def print_usage():
    print("usage: " + sys.argv[0] + " [-h|--help] action [args]")
    print("available actions:")
    print(textwrap.dedent("""
    containers:
        launch [name]        - new overlain container
        delete  name         - umount and delete container
    """))

# help messages
def print_help(topic):
    raise NotImplementedError("help is not implemented")
