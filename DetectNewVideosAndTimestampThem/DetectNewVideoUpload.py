import sched
import time
import logging
import DetectNewVideosAndTimestampThem.MakeTimestampOnNewVideo as make_timestamp

scheduler = None
delay = 0


def init_scheduler(api_client, scheduler_delay, channel_id, new_videos_location):
    global scheduler, delay
    scheduler = sched.scheduler(time.time, time.sleep)
    delay = scheduler_delay
    playlist_id = get_playlist_of_channel(api_client, channel_id)

    scheduler.enter(delay, 1, check_if_there_is_new_video_upload, (api_client, None, playlist_id, new_videos_location))
    scheduler.run()


def check_if_there_is_new_video_upload(api_client, last_video_id, playlist_id, new_videos_location):
    logging.info("Checking if new video was uploaded recently.")

    # Get the latest video on first call
    current_last_video_id = get_latest_video_from_channel(api_client, playlist_id)
    # TODO: Remove
    make_timestamp.make_timestamp_on_new_video(current_last_video_id, new_videos_location)

    '''
    if last_video_id is None:
        last_video_id = current_last_video_id
    elif last_video_id != current_last_video_id:
        # New video detected
        make_timestamp.make_timestamp_on_new_video(current_last_video_id, new_videos_location)
        last_video_id = current_last_video_id
    '''

    scheduler.enter(delay, 1, check_if_there_is_new_video_upload, (api_client, last_video_id, playlist_id,
                                                                   new_videos_location))


def get_latest_video_from_channel(api_client, playlist_id):
    playlist_parameters = {
        'part': 'contentDetails',
        'playlistId': playlist_id,
        'maxResults': 1
    }

    last_video = api_client.playlistItems().list(**playlist_parameters).execute()

    return last_video['items'][0]['contentDetails']['videoId']


def get_playlist_of_channel(api_client, channel_id):
    channel_parameters = {
        'part': 'contentDetails',
        'id': channel_id
    }

    channel_info = api_client.channels().list(**channel_parameters).execute()
    playlist_id = channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return playlist_id
