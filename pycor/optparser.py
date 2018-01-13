##
# pycor/docopt.py
#    use docopt to create a stable cli
#
#   This file is a part of the pycor project. To obtain the latest
#   development version, head over to the git repository available
#   at github: https://github.com/Jayfrown/pycor
#
#   Copyright (C) 2018  Jeroen de Boer (info@jayfrown.nl)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Container/Overlay
leverage overlayfs with lxd containers

pycor   Copyright (C) 2018   Jeroen de Boer (info@jayfrown.nl)
This program is free software; you are free to use, modify and/or
redistribute it under certain conditions. See LICENSE for details.

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
