##
# pycor/overlay.py
#    container/overlay magic
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

from pycor.lxdClient import lxd
from pycor.configparser import config


# use ctypes to call libc mount
def mount(containerName):
    import os, ctypes

    # some dirty variable addition
    lxdPath = config.get('lxd', 'path')
    lxdPool = config.get('lxd', 'storage_pool')
    containerPath = "{}/storage-pools/{}/containers".format(lxdPath, lxdPool)
    source = "{}/base/rootfs".format(containerPath)
    target = "{}/{}/rootfs".format(containerPath, containerName)
    overlay = "{}/{}/upper".format(containerPath, containerName)
    tmp = "{}/{}/work".format(containerPath, containerName)

    # make sure directories exist
    for dir in overlay, tmp, target:
        if not os.path.exists(dir):
            os.makedirs(dir)

    libcPath = ctypes.util.find_library("c")
    libc = ctypes.CDLL(libcPath, use_errno=True, use_last_error=True)
    mopts = "lowerdir={},upperdir={},workdir={}".format(source, overlay, tmp)

    # mount overlayfs
    try:
        return libc.mount("overlay", target, "overlay", 0, mopts)
    finally:
        errno = ctypes.get_errno()
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

    return lxd.containers.create(conf, wait=True)


# create a new (empty) container
def launch(containerName):
    conf = {
        'name': containerName,
        'architecture': config.get('launch', 'architecture'),
        'profiles': [config.get('launch', 'profile')],
        'ephemeral': config.getboolean('launch', 'ephemeral'),
        'source': { # empty rootfs to mount on
            'type': 'none'
        }
    }

    return lxd.containers.create(conf, wait=True)
