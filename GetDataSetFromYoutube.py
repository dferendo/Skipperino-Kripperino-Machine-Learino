from googleapiclient.discovery import build
import json
import logging


API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = 'AIzaSyDBlDO4a5P8oIUENzgS5VPC5lsPrV5Aam0'
CHANNEL_ID = 'UCeBMccz-PDZf6OB4aV6a3eA'

logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)

client = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

channel_parameters = {
    'part': 'contentDetails',
    'id': CHANNEL_ID
}

channel_info = client.channels().list(**channel_parameters).execute()
playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']


print(playlist_id)