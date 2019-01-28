import GatherDataSetScripts.Video as VideoClass
import json


def get_videos_ids(client, channel_id, data_set_location):
    channel_parameters = {
        'part': 'contentDetails',
        'id': channel_id
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

            videos.append(VideoClass.Video(content_details_video['videoId'], content_details_video['videoPublishedAt'],
                                           [], False, "", False))

        if 'nextPageToken' in uploaded_videos:
            next_page_token = uploaded_videos['nextPageToken']
            page_token = next_page_token

            if next_page_token == "":
                break
        else:
            break

    with open(data_set_location, 'w') as out_file:
        json.dump([video.__dict__ for video in videos], out_file)
