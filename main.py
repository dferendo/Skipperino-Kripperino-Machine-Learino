from googleapiclient.discovery import build
import logging
import yaml
import GatherDataSetScripts.GetAllVideosIds as GetAllVideosIds
import GatherDataSetScripts.GetGameStartingTime as GetGameStartingTime
import GatherDataSetScripts.DownloadVideoAndGetImagesFromStartingTime as DownloadVideoAndGetImagesFromStartingTime
import os

config_file_not_loaded = open('config.yaml', 'r')
config_file = yaml.safe_load(config_file_not_loaded)


def gather_video_ids_data_set(api_client):
    # Get all videos Ids
    channel_id = config_file['youtube']['videos_to_track_channel_id']
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])

    GetAllVideosIds.get_videos_ids(api_client, channel_id, data_set_location)


def gather_starting_time_from_youtube_comments(api_client):
    # Try to get starting time of the game from youtube comments
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])
    comment_tracker = config_file['youtube']['comments_to_track_on_videos_channel_id']

    GetGameStartingTime.get_game_starting_time_from_comments(api_client, data_set_location, comment_tracker)


def download_video_and_get_images():
    # Try to get starting time of the game from youtube comments
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])
    data_videos_set_location = os.path.abspath(config_file['youtube']['dataset_videos_location'])
    data_images_set_location = os.path.abspath(config_file['youtube']['dataset_images_location'])

    DownloadVideoAndGetImagesFromStartingTime.handle_video_download_and_conversion_to_images(data_set_location,
                                                                                             data_videos_set_location,
                                                                                             data_images_set_location)


if __name__ == "__main__":

    logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)

    api_service_bane = config_file['google_api']['youtube_api_service_name']
    api_version = config_file['google_api']['youtube_version']
    api_key = config_file['google_api']['api_key']

    client = build(api_service_bane, api_version, developerKey=api_key)
    # gather_video_ids_data_set(client)
    # gather_starting_time_from_youtube_comments(client)
    download_video_and_get_images()
    config_file_not_loaded.close()
