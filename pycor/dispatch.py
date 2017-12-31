##
# pycor/dispatch.py
#    dispatch function based on cli args
#

from pycor import interact as i

# init local pylxd connection
def lxdClient():
    try:
        from pylxd import Client, exceptions
        return Client(), exceptions
    except ImportError:
        raise
    except exceptions.ClientConnectionFailed:
        raise RuntimeError("local lxd connection failed")

# dispatch based on cli args
def dispatch(cmd, args):

    # launch a new container
    if cmd == "launch":
        from pycor import overlay
        conn, lxdException = lxdClient()

        # create base if it doesn't exist
        try:
            conn.containers.get('base')
        except lxdException.NotFound:
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
        conn, lxdException = lxdClient()

        if args:
            overlay.delete(conn, args[0])
        else:
            raise RuntimeError(cmd + ": need a container name")

    # catch-all
    else:
        raise RuntimeError("unknown action: " + str(cmd))
