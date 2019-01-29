import youtube_dl
import GatherDataSetScripts.Video as VideoClass


def handle_video_download_and_convertion(client, data_set_location):
    youtube_videos_urls = "http://www.youtube.com/watch?v="

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with open(data_set_location, 'r') as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        for video in videos:

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_videos_urls + video.video_id])
