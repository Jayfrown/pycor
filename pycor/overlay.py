##
# pycor/overlay.py
#    container/overlay magic
#

import subprocess
import os

from pycor.configparser import config
from pycor import interact as i


# need a mount function
def mount(base, overlay, workdir, mergedir):

    # create needed directories
    for dir in overlay, workdir, mergedir:
        if not os.path.exists(dir):
            cmd = ['mkdir', dir]

            mkdir = subprocess.Popen(cmd)
            mkdir.communicate()
            if mkdir.returncode != 0:
                raise RuntimeError()

    # mount overlayfs
    opts = "lowerdir=" + base + ",upperdir=" + overlay + ",workdir=" + workdir
    cmd = ['mount', '-t', 'overlay', 'overlay', '-o', opts, mergedir]

    mount = subprocess.Popen(cmd)
    mount.communicate()
    if mount.returncode != 0:
        raise RuntimeError()


# create base container
def create_base(lxd):

    conf = {
        'name': 'base',
        'architecture': 'x86_64',
        'profiles': [config.get('base', 'profile')],
        'ephemeral': False,
        'source': {
            'type': 'image',
            'mode': 'pull',
            'server': config.get('base', 'source'),
            'protocol': config.get('base', 'protocol'),
            'alias': config.get('base', 'alias')
        }
    }

    i.gMsg("creating base container..")
    lxd.containers.create(conf, wait=True)


# launch a new overlain container
def launch(lxd, containerName):

    conf = {
        'name': containerName,
        'architecture': 'x86_64',
        'profiles': [config.get('launch', 'profile')],
        'ephemeral': config.getboolean('launch', 'ephemeral'),
        'source': {'type': 'none'}
    }

    i.gMsg("creating " + containerName + "..")
    container = lxd.containers.create(conf, wait=True)

    # some dirty variable addition
    lxdPath = config.get('lxd', 'path')
    lxdPool = config.get('lxd', 'storage_pool')

    containerBase = lxdPath + "/storage-pools/" + lxdPool + '/containers/'
    basePath = containerBase + "base/rootfs"
    overlayPath = containerBase + containerName + "/upper"
    workPath = containerBase + containerName + "/work"
    mergePath = containerBase + containerName + "/rootfs"

    # mount overlay
    try:
        i.gMsg("enabling overlay mount..")
        mount(basePath, overlayPath, workPath, mergePath)
    except RuntimeError:
        raise RuntimeError("overlay mount failed, are you root?")
        delete(lxd, containerName)

    container.start(wait=True)
    i.gMsg(containerName + " state " + str(container.status).lower())


# delete overlay
def delete(lxd, containerName):
    container = lxd.containers.get(containerName)
    container.stop()
    container.delete(wait=True)
