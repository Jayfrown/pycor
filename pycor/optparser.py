##
# pycor/docopt.py
#    use docopt to create a stable cli

"""Container/Overlay
leverage overlayfs with lxd containers

usage: pycor-cli [-d|--debug] [-h|--help] <action> [<args> ...]

actions:
  launch [<name>]   launch new overlain container
  delete  <name>    umount and delete container

options:
  -h --help     show this screen
  -d --debug    enable debug output
  --version     show version
"""
from docopt import docopt


optargs = docopt(__doc__, version="pycor-cli v0.1-alpha")
