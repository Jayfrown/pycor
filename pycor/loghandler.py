##
# pycor/logging.py
#    handle log messages
#

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('pycor-cli: %(levelname)s: %(message)s')

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)
