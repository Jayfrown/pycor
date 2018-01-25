##
# pycor/dispatch.py
#    dispatch function(s) based on cli args
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

# dispatch based on cli args
def dispatch(cmd, args):

    # launch a new container
    if cmd == "launch":
        from pycor.loghandler import logger
        from pycor.lxdClient import lxd
        from pycor.lxdClient import lxdException
        from pycor import overlay

        # get container name
        if args:
            containerName = args[0]
        else:
            import requests
            link = "https://frightanic.com/goodies_content/docker-names.php"
            logger.debug("fetching docker-like name")
            containerName = requests.get(link).text.strip().replace("_", "-")

        # create base if it doesn't exist
        try:
            lxd.containers.get('base')
        except lxdException.NotFound:
            logger.debug("initializing base environment")
            overlay.create_base()

        # new container on overlayfs
        logger.debug("creating {}".format(containerName))
        container = overlay.launch(containerName)
        logger.debug("mounting overlay")
        overlay.mount(container.name)
        container.start(wait=True)
        logger.debug("{} state {}".format(container.name, container.status))
        logger.info("created {}".format(container.name))

    # umount overlay and delete container
    elif cmd == "delete":
        from pycor.loghandler import logger
        from pycor.lxdClient import lxd
        from pycor.lxdClient import lxdException
        from pycor import overlay

        if args:
            container = lxd.containers.get(args[0])
        else:
            raise RuntimeError("which one?")

        # test if we need to stop it
        if container.status == "Running":
            logger.debug("{} state {}".format(container.name, container.status))
            raise RuntimeError("{} is running, refusing to delete".format(container.name))

        logger.info("note: umount not yet implemented")
        container.delete(wait=True)
        logger.info("deleted {}".format(container.name))

    # catch-all
    else:
        raise RuntimeError("{}: unknown action".format(cmd))
