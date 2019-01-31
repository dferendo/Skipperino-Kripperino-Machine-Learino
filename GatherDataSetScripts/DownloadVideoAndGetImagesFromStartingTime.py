import youtube_dl
import GatherDataSetScripts.Video as VideoClass
import logging
import subprocess
import os


def handle_video_download_and_conversion_to_images(data_set_location, data_videos_set_location):
    youtube_videos_urls = "http://www.youtube.com/watch?v="

    ydl_opts = {
        'outtmpl': data_videos_set_location + '\\%(id)s',
    }

    with open(data_set_location, 'r') as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        for video in videos:

            if video.is_video_downloaded:
                continue

            try:

                #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # Download video
                #    ydl.download([youtube_videos_urls + video.video_id])

                    # Get the video part we care about
                input_file_location = data_videos_set_location + '\\' + video.video_id + '.mkv'
                # TODO: use subprocess
                
                os.system(f"ffmpeg -ss 30 -i {input_file_location} -c copy -t 10 output.wmv")

                print(input_file_location)
                # Convert to images
                # ffmpeg -i file.mpg -r 1/1 $filename%03d.bmp
            except Exception as error:
                logging.error(error)
