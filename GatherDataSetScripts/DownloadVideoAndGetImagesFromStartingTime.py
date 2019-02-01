import youtube_dl
import GatherDataSetScripts.Video as VideoClass
import logging
import os


def handle_video_download_and_conversion_to_images(data_set_location, data_videos_set_location,
                                                   data_images_set_location):
    youtube_videos_urls = "http://www.youtube.com/watch?v="
    seconds_after_starting_comments = 20

    ydl_opts = {
        'outtmpl': data_videos_set_location + '\\%(id)s',
    }

    with open(data_set_location, 'r') as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        for video in videos:

            if video.is_video_downloaded:
                continue

            try:

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # Download video
                    ydl.download([youtube_videos_urls + video.video_id])

                # Get the video part we care about
                input_file_location = f"{data_videos_set_location}\\{video.video_id}.mkv"

                for i in range(0, len(video.game_starting_time)):
                    output_video_file_location = f"{data_videos_set_location}\\{video.video_id}_{i + 1}"
                    output_images_file_location = f"{data_images_set_location}\\{video.video_id}_{i + 1}"

                    # Get the range of the video we need
                    os.system(f"ffmpeg -i \"{input_file_location}\" -ss {video.game_starting_time[i]} "
                              f"-t {seconds_after_starting_comments} -c copy \"{output_video_file_location}.mkv\"")

                    os.makedirs(output_images_file_location)

                    # Convert to images
                    os.system(f"ffmpeg -i \"{output_video_file_location}.mkv\" -r 1/2 "
                              f"{output_images_file_location}\\%03d.bmp")

                os.remove(input_file_location)

            except Exception as error:
                logging.error(error)
