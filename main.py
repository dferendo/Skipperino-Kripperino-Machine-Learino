from googleapiclient.discovery import build
import logging
import yaml
import GatherDataSetScripts.GetAllVideosIds as GetAllVideosIds
import os

config_file_not_loaded = open('config.yaml', 'r')
config_file = yaml.safe_load(config_file_not_loaded)


def gather_data_set(api_client):
    # Get all videos Ids
    channel_id = config_file['youtube']['videos_to_track_channel_id']
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])

    GetAllVideosIds.get_videos_ids(api_client, channel_id, data_set_location)


if __name__ == "__main__":

    logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)

    api_service_bane = config_file['google_api']['youtube_api_service_name']
    api_version = config_file['google_api']['youtube_version']
    api_key = config_file['google_api']['api_key']

    client = build(api_service_bane, api_version, developerKey=api_key)
    gather_data_set(client)
    config_file_not_loaded.close()
