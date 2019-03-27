import youtube_dl
import GatherDataSetScripts.Video as VideoClass
import logging
import os
import json
import tempfile
import shutil


# This is an approx
seconds_after_starting_comments = 20
intro_location = ""
card_select_location = ""
draft_location = ""
game_start_location = ""
other_location = ""


def dump_file(data_set_location, videos):
    with open(data_set_location, 'w+') as videos_file:
        # Clear the json file and dump
        videos_file.truncate(0)
        json.dump([video.__dict__ for video in videos], videos_file)


def handle_video_download_and_conversion_to_images(configs):
    youtube_videos_urls = "http://www.youtube.com/watch?v="
    frames_per_second = 0.5
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': configs.videos_set_location + '\\%(id)s.%(ext)s'
    }

    with open(configs.data_set_location, 'r') as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        for video in videos:

            if video.is_video_downloaded:
                continue

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # Download video
                    ydl.download([youtube_videos_urls + video.video_id])

                input_file_location = f"{configs.videos_set_location}\\{video.video_id}.mp4"

                with tempfile.TemporaryDirectory() as tmp_dir:
                    convert_video_to_images(input_file_location, tmp_dir, frames_per_second)
                    place_images_in_the_right_folders(configs, video.video_id, tmp_dir, frames_per_second,
                                                      video.game_starting_time)

                video.is_video_downloaded = True
            except Exception as error:
                logging.error(error)

    # dump_file(data_set_location, videos)


def convert_video_to_images(input_file_location, output_folder, frames_per_second):
    os.system(f"ffmpeg -i \"{input_file_location}\" -vf fps={frames_per_second} \"{output_folder}\\%05d.jpg\"")


def place_images_in_the_right_folders(configs, video_id, images_locations, frames_per_second, game_starting_time):
    game_starting_time_in_seconds = [convert_from_time_to_second(time) for time in game_starting_time]

    for filename in os.listdir(images_locations):
        timestamp_in_seconds = (int(filename.split('.')[0]) - 1) * (1 / frames_per_second)
        full_file_path = f"{images_locations}\\{filename}"

        # Indicates this does not contains game play
        if len(game_starting_time_in_seconds) == 0:
            current_folder_selected = configs.other_location
        elif len(game_starting_time_in_seconds) == 1:
            # This indicates normal game (Intro -> Card Select -> Game Play)
            current_folder_selected = handle_normal_game(configs, timestamp_in_seconds,
                                                         game_starting_time_in_seconds[0])
        elif len(game_starting_time_in_seconds) == 2:
            # This indicates arena game with Draft pick
            current_folder_selected = handle_arena_game(configs, timestamp_in_seconds,
                                                        game_starting_time_in_seconds[0],
                                                        game_starting_time_in_seconds[1])
        else:
            # This is an error
            return

        move_file(full_file_path, current_folder_selected, video_id, filename)


def handle_normal_game(configs, current_time, card_select_start_time):

    if current_time < card_select_start_time:
        return configs.intro_location
    elif current_time < card_select_start_time + seconds_after_starting_comments:
        return configs.card_select_location

    return configs.game_play_location


def handle_arena_game(configs, current_time, draft_start_time, card_select_start_time):

    if current_time < draft_start_time:
        return configs.intro_location
    elif current_time < card_select_start_time:
        return configs.draft_location
    elif current_time < card_select_start_time + seconds_after_starting_comments:
        return configs.card_select_location

    return configs.game_play_location


def convert_from_time_to_second(game_starting_time):
    split_string = game_starting_time.split(':')

    return int(split_string[0]) * 60 + int(split_string[1])


def move_file(current_location, new_location, video_id, file_name):
    shutil.move(current_location, f"{new_location}\\{video_id}_{file_name}")
