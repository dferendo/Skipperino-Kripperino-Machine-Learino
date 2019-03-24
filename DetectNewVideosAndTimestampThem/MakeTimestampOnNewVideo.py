import youtube_dl
import tempfile
import os


def make_timestamp_on_new_video(video_id, new_videos_location):
    video_location = get_and_download_video_local_location(video_id, new_videos_location)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get images from video
        os.system(f"ffmpeg -i \"{video_location}\" -r 1/2 \"{tmp_dir}\\%03d.jpg\"")

        for filename in os.listdir(tmp_dir):
            print(filename)


def get_and_download_video_local_location(video_id, new_videos_location):
    youtube_videos_urls = "http://www.youtube.com/watch?v="
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': new_videos_location + '\\%(id)s.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Download video
        ydl.download([youtube_videos_urls + video_id])

    return f"{new_videos_location}\\{video_id}.mp4"
