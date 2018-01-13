##
# pycor/lxdClient.py
#    initialize local pylxd connection
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

try:
    from pylxd import Client, exceptions as lxdException
    from pycor.loghandler import logger

    logger.debug("intializing pylxd client")
    lxd = Client()
except ImportError:
    raise
except lxdException.ClientConnectionFailed:
    raise RuntimeError("local pylxd connection failed")
