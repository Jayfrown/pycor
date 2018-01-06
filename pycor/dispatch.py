##
# pycor/dispatch.py
#    dispatch function based on cli args
#

from pycor import interact as i
from pycor.lxdClient import lxd
from pycor.lxdClient import lxdException


# dispatch based on cli args
def dispatch(cmd, args):

    # launch a new container
    if cmd == "launch":
        from pycor import overlay

        # create base if it doesn't exist
        try:
            lxd.containers.get('base')
        except lxdException.NotFound:
            i.bMsg("initializing environment")
            overlay.create_base()

        # new overlay
        if args:
            overlay.launch(args[0])
        else:
            import requests
            link = "https://frightanic.com/goodies_content/docker-names.php"
            generatedName = requests.get(link).text.strip().replace("_", "-")
            overlay.launch(generatedName)

    # delete overlain container
    elif cmd == "delete":
        from pycor import overlay

        if args:
            overlay.delete(args[0])
        else:
            raise RuntimeError(cmd + ": need a container name")

    # catch-all
    else:
        raise RuntimeError("unknown action: " + str(cmd))
