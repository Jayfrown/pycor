##
# pycor/interact.py
#    functions for user interaction
#

from __future__ import print_function

import sys


# message types
def gMsg(string):
    print("pycor: ", string, file=sys.stdout)
def bMsg(string):
    print("pycor: ", string, file=sys.stderr)
