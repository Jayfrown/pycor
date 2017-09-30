##
# pycor/dispatch.py
#    dispatch function based on cli args
#

from pycor import interact as i


# dispatch based on cli args
def dispatch(cmd, args):

    # launch a new container
    if cmd == "launch":
        from pycor import overlay

        # init local pylxd connection
        try:
            from pylxd import Client, exceptions
            conn = Client()
        except exceptions.ClientConnectionFailed:
            raise RuntimeError("local lxd connection failed")

        # create base if it doesn't exist
        try:
            conn.containers.get('base')
        except exceptions.NotFound:
            i.bMsg("no base container found, initializing environment")
            overlay.create_base(conn)

        # new overlay
        if args:
            overlay.launch(conn, args[0])
        else:
            import requests
            link = "https://frightanic.com/goodies_content/docker-names.php"
            generatedName = requests.get(link).text.strip().replace("_", "-")
            overlay.launch(conn, generatedName)

    # delete overlain container
    elif cmd == "delete":
        from pycor import overlay

        try:
            from pylxd import Client, exceptions
            conn = Client()
        except exceptions.ClientConnectionFailed:
            raise RuntimeError("local lxd connection failed")

        if args:
            overlay.delete(conn, args[0])
        else:
            raise RuntimeError(cmd + ": need a container name")

    # catch-all
    else:
        raise RuntimeError("unknown action: " + str(cmd))
