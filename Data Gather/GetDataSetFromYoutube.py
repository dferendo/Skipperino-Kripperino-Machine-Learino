import configparser
import os
import logging

currentPath = os.path.dirname(os.path.realpath(__file__))
configFileLocation = currentPath + '\\..\\configs.conf'

config = configparser.ConfigParser()
config.sections()
config.read(configFileLocation)

logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
