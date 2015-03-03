# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

LVL = {'INFO': logging.INFO,
       'DEBUG': logging.DEBUG,
       'ERROR': logging.ERROR,
       'CRITICAL': logging.CRITICAL}


def setup_log(name=__name__, level='INFO', log=None,
              console=True, form='%(asctime)s [%(levelname)s] %(message)s'):
    """
    Setup logger object for displaying information into console/file

    :param name: Name of the logger object to create
    :type name: str

    :param level: Level INFO/DEBUG/ERROR etc
    :type level: str

    :param log: File to which log information
    :type log: str

    :param console: If log information sent to console as well
    :type console: Boolean

    :param form: The format in which the log will be displayed
    :type form: str

    :returns: The object logger
    :rtype: logger object
    """
    level = level.upper()
    if level not in LVL:
        logging.warning("Option of log level %s incorrect, using INFO." % level)
        level = 'INFO'
    level = LVL[level]
    formatter = logging.Formatter(form)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if log is not None:
        filehdl = logging.FileHandler(log)
        filehdl.setFormatter(formatter)
        logger.addHandler(filehdl)
    if console is True:
        consolehdl = logging.StreamHandler()
        consolehdl.setFormatter(formatter)
        logger.addHandler(consolehdl)
    return logger
