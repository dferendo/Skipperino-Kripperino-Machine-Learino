import configparser
import os
import logging
import logging.config

currentPath = os.path.dirname(os.path.realpath(__file__))
configFileLocation = currentPath + '\\..\\configs.conf'

config = configparser.ConfigParser()
config.sections()
config.read(configFileLocation)

logging.config.fileConfig(configFileLocation)

logging.debug("TEST")