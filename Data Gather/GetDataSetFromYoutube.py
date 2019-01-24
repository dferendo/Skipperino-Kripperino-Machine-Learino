import configparser
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.sections()
config.read(currentPath + '\\..\\config.ini')

print(config['DataGather']['YoutubeChannelId'])