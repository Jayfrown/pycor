##
# pycor/overlay.py
#    container/overlay magic
#

import os

from ctypes import *
from ctypes.util import *
from pycor.lxdClient import lxd
from pycor.loghandler import logger
from pycor.configparser import config


# use ctypes to call libc mount
def mount(source, overlay, tmp, target):

    # make sure directories exist
    for dir in overlay, tmp, target:
        if not os.path.exists(dir):
            os.makedirs(dir)

    libcPath = find_library("c")
    libc = CDLL(libcPath, use_errno=True, use_last_error=True)
    mopts = "lowerdir={},upperdir={},workdir={}".format(source, overlay, tmp)

    # mount overlayfs
    try:
        return libc.mount("overlay", target, "overlay", 0, mopts)
    finally:
        errno = get_errno()
        if errno:
            raise RuntimeError(
                "error mounting overlay: {}".format(os.strerror(errno)))


# create base container
def create_base():

    conf = {
        'name': 'base',
        'architecture': config.get('base', 'architecture'),
        'profiles': [config.get('base', 'profile')],
        'ephemeral': False,
        'source': {
            'type': 'image',
            'mode': 'pull',
            'server': config.get('base', 'source'),
            'protocol': config.get('base', 'protocol'),
            'alias': config.get('base', 'image')
        }
    }

    logger.info("creating base container for r/o overlay rootfs")
    lxd.containers.create(conf, wait=True)


# launch a new overlain container
def launch(containerName):

    conf = {
        'name': containerName,
        'architecture': config.get('launch', 'architecture'),
        'profiles': [config.get('launch', 'profile')],
        'ephemeral': config.getboolean('launch', 'ephemeral'),
        'source': {
            'type': 'none'
        }
    }

    # some dirty variable addition
    lxdPath = config.get('lxd', 'path')
    lxdPool = config.get('lxd', 'storage_pool')
    containerPath = "{}/storage-pools/{}/containers".format(lxdPath, lxdPool)

    basePath = "{}/base/rootfs".format(containerPath)
    overlayPath = "{}/{}/upper".format(containerPath, containerName)
    workPath = "{}/{}/work".format(containerPath, containerName)
    mergePath = "{}/{}/rootfs".format(containerPath, containerName)

    # create skeleton container
    logger.info("launching {}".format(containerName))
    container = lxd.containers.create(conf, wait=True)

    # mount overlay
    try:
        mount(basePath, overlayPath, workPath, mergePath)
    except Exception:
        logger.debug("overlayfs mount failed, deleting broken container")
        delete(containerName)
        raise

    container.start(wait=True)
    logger.info("{} state {}".format(containerName, container.status))


# delete overlay
def delete(containerName):
    container = lxd.containers.get(containerName)
    logger.debug("{} state {}".format(containerName, container.status))

    # test if we need to stop it
    if container.status == "Running":
        logger.info("stopping {}".format(containerName))
        container.stop(wait=True)
        logger.debug("{} state {}".format(containerName, container.status))

    # wait=True or test if it's already stopped
    logger.info("deleting {}".format(containerName))
    logger.info("note: umount not yet implemented")
    container.delete(wait=True)
