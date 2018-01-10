##
# pycor/dispatch.py
#    dispatch function based on cli args
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
