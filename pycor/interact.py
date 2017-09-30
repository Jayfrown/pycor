##
# pycor/interact.py
#    functions for user interaction
#

from __future__ import print_function

import sys
import textwrap

from termcolor import colored


# message types
def gMsg(args, **kwargs):
    print(colored("pycor", 'blue') + ':', args, file=sys.stdout, **kwargs)


def bMsg(args, **kwargs):
    print(colored("pycor", 'red') + ':', args, file=sys.stderr, **kwargs)


# program header
def print_header():
    gMsg(colored("Container", 'magenta') + "/" + colored("Overlay", 'magenta'))
    gMsg("leverage overlayfs with lxd containers")
    print()


# usage hints
def print_usage():
    print("usage: " + sys.argv[0] + " [-h|--help] action [args]")


def full_usage():
    print_usage()
    print("available actions:")

    print(textwrap.dedent("""
    {containers}:
        launch [{name}]        - new container
        delete  {name}         - delete container
    """).format(name=colored("name", 'magenta'),
                containers=colored("containers", 'blue')))


# help messages
def print_help(topic):
    if topic == "launch":
        print("help for launch")

    elif topic == "delete":
        print("help for delete")

    else:
        raise RuntimeError("unknown topic: " + str(topic))
