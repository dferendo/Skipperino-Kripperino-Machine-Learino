import youtube_dl
import tempfile
import os


def make_timestamp_on_new_video(video_id, new_videos_location):
    frames_per_second = 0.5
    video_location = get_and_download_video_local_location(video_id, new_videos_location)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get images from video
        os.system(f"ffmpeg -i \"{video_location}\" -vf fps={frames_per_second} \"{tmp_dir}\\%05d.jpg\"")

        for filename in os.listdir(tmp_dir):
            # TODO: get which file we care
            print(get_timestamp_in_minutes_and_seconds(filename, frames_per_second))


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


def get_timestamp_in_minutes_and_seconds(image_chosen, frames_per_second):
    timestamp_in_seconds = (int(image_chosen.split('.')[0]) - 1) * (1 / frames_per_second)
    timestamp_minutes = int(timestamp_in_seconds / 60)
    timestamp_seconds = int(timestamp_in_seconds % 60)

    if timestamp_seconds < 10:
        return f"{timestamp_minutes}:0{timestamp_seconds}"

    return f"{timestamp_minutes}:{timestamp_seconds}"
