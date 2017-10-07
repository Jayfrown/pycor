##
# pycor/config.py
#    config parser
#

import os
from ConfigParser import SafeConfigParser


file = "config.cfg"
config = SafeConfigParser()

# generate config file
if not os.path.isfile(file):
    config.add_section('pycor')
    config.set('pycor', 'debug', 'False')

    config.add_section('lxd')
    config.set('lxd', 'path', '/var/lib/lxd')
    config.set('lxd', 'storage_pool', 'default')
    config.set('lxd', 'subuid', '1000000')
    config.set('lxd', 'subgid', '1000000')

    config.add_section('launch')
    config.set('launch', 'profile', 'default')
    config.set('launch', 'ephemeral', 'True')
    config.set('launch', 'architecture', 'x86_64')

    config.add_section('base')
    config.set('base', 'image', 'centos/6')
    config.set('base', 'source', 'https://images.linuxcontainers.org')
    config.set('base', 'protocol', 'simplestreams')
    config.set('base', 'profile', 'default')

    # write-out
    with open(file, 'w') as f:
        config.write(f)

# parse configuration file
config.read(file)
