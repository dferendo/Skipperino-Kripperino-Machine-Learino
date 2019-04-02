from googleapiclient.discovery import build
import logging
import yaml
import os
import argparse
import GatherDataSetScripts.GetAllVideosIds as GetAllVideosIds
import GatherDataSetScripts.GetGameStartingTime as GetGameStartingTime
import GatherDataSetScripts.DownloadVideoAndGetImagesFromStartingTime as DownloadVideoAndGetImagesFromStartingTime
import DetectNewVideosAndTimestampThem.DetectNewVideoUpload as DetectNewVideoUpload
import TrainBot.LabelImage as LabelImage
from GatherDataSetScripts.__init__ import GatherDataConfigs

config_file_not_loaded = open('config.yaml', 'r')
config_file = yaml.safe_load(config_file_not_loaded)
client = None


def gather_video_ids_data_set():
    api_client = build_google_client()

    # Get all videos Ids
    channel_id = config_file['youtube']['videos_to_track_channel_id']
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])
    published_after = config_file['youtube']['published_after']

    GetAllVideosIds.get_videos_ids(api_client, channel_id, data_set_location, published_after)


def gather_starting_time_from_youtube_comments():
    api_client = build_google_client()

    # Try to get starting time of the game from youtube comments
    data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])
    comment_tracker = config_file['youtube']['comments_to_track_on_videos_channel_id']

    GetGameStartingTime.get_game_starting_time_from_comments(api_client, data_set_location, comment_tracker)


def download_video_and_get_images():
    configs = GatherDataConfigs(config_file)

    DownloadVideoAndGetImagesFromStartingTime.handle_video_download_and_conversion_to_images(configs)


def train_cnn():
    training_data_set = os.path.abspath(config_file['training']['train_data_set'])
    training_steps = config_file['training']['training_steps']
    graph_location = os.path.abspath(config_file['training']['trained_graph_location'])
    labels_location = os.path.abspath(config_file['training']['labels'])

    os.system(f"python ./TrainBot/Retrain.py "
              f"--image_dir=\"{training_data_set}\" "
              f"--how_many_training_steps={training_steps} "
              f"--output_graph={graph_location} "
              f"--output_labels={labels_location} ")


def validate_cnn():
    trained_model = os.path.abspath(config_file['training']['trained_model_location'])
    labels_location = os.path.abspath(config_file['training']['labels'])
    test_location = os.path.abspath(config_file['training']['test_data_set'])

    LabelImage.label_images(trained_model, test_location, labels_location)


def detect_new_videos():
    api_client = build_google_client()

    # Try to get starting time of the game from youtube comments
    delay = config_file['detect_new_upload']['delay']
    new_videos_location = os.path.abspath(config_file['detect_new_upload']['videos_download'])
    channel_id = config_file['youtube']['videos_to_track_channel_id']

    DetectNewVideoUpload.init_scheduler(api_client, delay, channel_id, new_videos_location)


def build_google_client():
    api_service_bane = config_file['google_api']['youtube_api_service_name']
    api_version = config_file['google_api']['youtube_version']
    api_key = config_file['google_api']['api_key']

    return build(api_service_bane, api_version, developerKey=api_key)


if __name__ == "__main__":
    logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()

    functions = {'gather-video-ids': gather_video_ids_data_set,
                 'gather-starting-time': gather_starting_time_from_youtube_comments,
                 'download-videos-and-convert-to-images': download_video_and_get_images,
                 'train-cnn': train_cnn,
                 'validate-cnn': validate_cnn,
                 'run': detect_new_videos}

    parser.add_argument('command', choices=functions.keys())

    args = parser.parse_args()

    action = functions[args.command]
    action()

    config_file_not_loaded.close()
