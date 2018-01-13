##
# pycor/dispatch.py
#    dispatch function based on cli args
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

from pycor.loghandler import logger
from pycor.lxdClient import lxd
from pycor.lxdClient import lxdException


# dispatch based on cli args
def dispatch(cmd, args):

    # launch a new container
    if cmd == "launch":
        from pycor import overlay

        # create base if it doesn't exist
        try:
            logger.debug("testing for base container")
            lxd.containers.get('base')
        except lxdException.NotFound:
            logger.info("initializing environment")
            overlay.create_base()

        # new overlay
        if args:
            overlay.launch(args[0])
        else:
            import requests
            link = "https://frightanic.com/goodies_content/docker-names.php"
            logger.debug("fetching docker-like name")
            generatedName = requests.get(link).text.strip().replace("_", "-")
            overlay.launch(generatedName)


    # delete overlain container
    elif cmd == "delete":
        from pycor import overlay

        if args:
            overlay.delete(args[0])
        else:
            raise RuntimeError("{}: need a container name".format(cmd))


    # catch-all
    else:
        raise RuntimeError("unknown action: {}".format(cmd))
