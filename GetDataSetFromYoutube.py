from googleapiclient.discovery import build
import logging
import json


class Video:
    video_id = ""
    video_published_at = ""

    def __init__(self, video_id, video_published_at):
        self.video_id = video_id
        self.video_published_at = video_published_at


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

videos = []
pageToken = ""
playlist_parameters = {
    'part': 'contentDetails',
    'playlistId': playlist_id,
    'maxResults': 50
}

while True:
    playlist_parameters['pageToken'] = pageToken
    uploaded_videos = client.playlistItems().list(**playlist_parameters).execute()

    for video in uploaded_videos['items']:
        content_details_video = video['contentDetails']

        videos.append(Video(content_details_video['videoId'], content_details_video['videoPublishedAt']))

    if 'nextPageToken' in uploaded_videos:
        next_page_token = uploaded_videos['nextPageToken']
        pageToken = next_page_token

        if next_page_token == "":
            break
    else:
        break

with open('./DataSet/videos.json', 'w') as out_file:
    json.dump([video.__dict__ for video in videos], out_file)
