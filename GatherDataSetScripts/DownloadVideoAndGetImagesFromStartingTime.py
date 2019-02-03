import youtube_dl
import GatherDataSetScripts.Video as VideoClass
import logging
import os
import json


def dump_file(data_set_location, videos):
    with open(data_set_location, 'w+') as videos_file:
        # Clear the json file and dump
        videos_file.truncate(0)
        json.dump([video.__dict__ for video in videos], videos_file)


def handle_video_download_and_conversion_to_images(data_set_location, data_videos_set_location,
                                                   data_images_set_location):
    youtube_videos_urls = "http://www.youtube.com/watch?v="
    seconds_after_starting_comments = 20
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

                for i in range(0, len(video.game_starting_time)):
                    output_video_file_location = f"{data_videos_set_location}\\{video.video_id}_{i + 1}"

                    # Get the range of the video we need
                    os.system(f"ffmpeg -i \"{input_file_location}\" -ss {video.game_starting_time[i]} "
                              f"-t {seconds_after_starting_comments} -c copy \"{output_video_file_location}.mp4\"")

                    # Convert to images
                    os.system(f"ffmpeg -i \"{output_video_file_location}.mp4\" -r 1/2 "
                              f"{data_images_set_location}\\{video.video_id}_{i + 1}_%03d.bmp")

                os.remove(input_file_location)

                video.is_video_downloaded = True
            except Exception as error:
                logging.error(error)

    dump_file(data_set_location, videos)
