##
# pycor/config.py
#   config parser
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

import os
from ConfigParser import SafeConfigParser


file = "config.cfg"
config = SafeConfigParser()

# generate config file
if not os.path.isfile(file):
    config.add_section('lxd')
    config.set('lxd', 'path', '/var/lib/lxd')
    config.set('lxd', 'storage_pool', 'default')
    config.set('lxd', 'subuid', '1000000')
    config.set('lxd', 'subgid', '1000000')

    config.add_section('launch')
    config.set('launch', 'architecture', 'x86_64')
    config.set('launch', 'profile', 'default')
    config.set('launch', 'ephemeral', 'True')

    config.add_section('base')
    config.set('base', 'architecture', 'x86_64')
    config.set('base', 'profile', 'default')
    config.set('base', 'image', 'centos/6')
    config.set('base', 'source', 'https://images.linuxcontainers.org')
    config.set('base', 'protocol', 'simplestreams')

    # write-out
    with open(file, 'w') as f:
        config.write(f)

# parse configuration file
config.read(file)
