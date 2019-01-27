from googleapiclient.discovery import build
import logging
import json


class Video:
    video_id = ""
    video_published_at = ""
    game_starting_time = ""

    def __init__(self, video_id, video_published_at, game_starting_time):
        self.video_id = video_id
        self.video_published_at = video_published_at
        self.game_starting_time = game_starting_time


API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = 'AIzaSyDBlDO4a5P8oIUENzgS5VPC5lsPrV5Aam0'
CHANNEL_ID = 'UCeBMccz-PDZf6OB4aV6a3eA'
VIDEOS_DATA_LOCATION = './DataSet/videos.json'
TRACK_COMMENTS_ACCOUNT_ID = 'UCsuOjz5JNLAPN4qUMeTUguQ'

logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)


def convert_json_to_object(videos_file):
    videos_in_json = json.load(videos_file)
    videos = []

    for video_in_json in videos_in_json:
        videos.append(Video(video_in_json['video_id'], video_in_json['video_published_at'],
                            video_in_json['game_starting_time']))

    return videos


def get_videos_ids():
    channel_parameters = {
        'part': 'contentDetails',
        'id': CHANNEL_ID
    }

    channel_info = client.channels().list(**channel_parameters).execute()
    playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    page_token = ""
    playlist_parameters = {
        'part': 'contentDetails',
        'playlistId': playlist_id,
        'maxResults': 50
    }

    while True:
        playlist_parameters['pageToken'] = page_token
        uploaded_videos = client.playlistItems().list(**playlist_parameters).execute()

        for video in uploaded_videos['items']:
            content_details_video = video['contentDetails']

            videos.append(Video(content_details_video['videoId'], content_details_video['videoPublishedAt'], ""))

        if 'nextPageToken' in uploaded_videos:
            next_page_token = uploaded_videos['nextPageToken']
            page_token = next_page_token

            if next_page_token == "":
                break
        else:
            break

    with open(VIDEOS_DATA_LOCATION, 'w') as out_file:
        json.dump([video.__dict__ for video in videos], out_file)


def get_game_starting_time_from_comments():

    with open(VIDEOS_DATA_LOCATION) as videos_file:
        videos = convert_json_to_object(videos_file)

        comment_thread_parameters = {
            'part': 'snippet',
            'channelId': TRACK_COMMENTS_ACCOUNT_ID,
            'maxResults': 20
        }

        for video in videos:
            comment_thread_parameters['videoId'] = video.video_id

            comments_in_video = client.commentThreads().list(**comment_thread_parameters).execute()

            break

        print(len(videos))


client = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

if __name__ == "__main__":
    # get_videos_ids()
    get_game_starting_time_from_comments()
