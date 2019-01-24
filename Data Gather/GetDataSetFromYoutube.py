import configparser
import os
import logging

# Logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

currentPath = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.sections()
config.read(currentPath + '\\..\\config.ini')

print(config['General']['YoutubeChannelId'])
