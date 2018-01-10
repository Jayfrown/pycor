##
# pycor/lxdClient.py
#    initialize local pylxd connection
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
