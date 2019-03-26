import youtube_dl
import GatherDataSetScripts.Video as VideoClass
import logging
import os
import json
import tempfile


def dump_file(data_set_location, videos):
    with open(data_set_location, 'w+') as videos_file:
        # Clear the json file and dump
        videos_file.truncate(0)
        json.dump([video.__dict__ for video in videos], videos_file)


def handle_video_download_and_conversion_to_images(data_set_location, data_videos_set_location,
                                                   data_images_set_location_intro,
                                                   data_images_set_location_card_select,
                                                   data_images_set_location_draft,
                                                   data_images_set_location_game_start,
                                                   data_images_set_location_other):
    youtube_videos_urls = "http://www.youtube.com/watch?v="
    frames_per_second = 0.5
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': data_videos_set_location + '\\%(id)s.%(ext)s'
    }

    with open(data_set_location, 'r') as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        for video in videos:

            if video.is_video_downloaded or video.game_starting_time == []:
                continue

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # Download video
                    ydl.download([youtube_videos_urls + video.video_id])

                input_file_location = f"{data_videos_set_location}\\{video.video_id}.mp4"

                with tempfile.TemporaryDirectory() as tmp_dir:
                    convert_video_to_images(input_file_location, tmp_dir, frames_per_second)
                    place_images_in_the_right_folders(tmp_dir, frames_per_second, video.game_starting_time,
                                                      data_images_set_location_intro,
                                                      data_images_set_location_card_select,
                                                      data_images_set_location_draft,
                                                      data_images_set_location_game_start,
                                                      data_images_set_location_other)

                video.is_video_downloaded = True
            except Exception as error:
                logging.error(error)

    # dump_file(data_set_location, videos)


def convert_video_to_images(input_file_location, output_folder, frames_per_second):
    os.system(f"ffmpeg -i \"{input_file_location}\" -vf fps={frames_per_second} \"{output_folder}\\%05d.jpg\"")


def place_images_in_the_right_folders(images_locations, frames_per_second, game_starting_time,
                                      data_images_set_location_intro,
                                      data_images_set_location_card_select,
                                      data_images_set_location_draft,
                                      data_images_set_location_game_start,
                                      data_images_set_location_other):
    # This is an approx
    seconds_after_starting_comments = 20

    for filename in os.listdir(images_locations):
        timestamp_in_seconds = (int(filename.split('.')[0]) - 1) * (1 / frames_per_second)

        full_file_path = f"{images_locations}\\{filename}"

        print(timestamp_in_seconds)
