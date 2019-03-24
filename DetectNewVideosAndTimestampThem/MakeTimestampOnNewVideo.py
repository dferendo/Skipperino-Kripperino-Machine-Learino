import youtube_dl


def make_timestamp_on_new_video(video_id, new_videos_location):
    video_location = get_and_download_video_local_location(video_id, new_videos_location)

    return


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
