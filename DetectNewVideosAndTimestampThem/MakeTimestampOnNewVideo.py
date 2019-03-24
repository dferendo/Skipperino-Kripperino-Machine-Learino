import youtube_dl
import tempfile
import os


def make_timestamp_on_new_video(api_client, channel_id, video_id, new_videos_location):
    frames_per_second = 0.5
    video_location = get_and_download_video_local_location(video_id, new_videos_location)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get images from video
        os.system(f"ffmpeg -i \"{video_location}\" -vf fps={frames_per_second} \"{tmp_dir}\\%05d.jpg\"")

        for filename in os.listdir(tmp_dir):
            # TODO: get which file we care
            timestamp_in_string = get_timestamp_in_minutes_and_seconds(filename, frames_per_second)

            # TODO: Upload video
            '''
            insert_timestamp_to_video(api_client,
                                      {'snippet.channelId': channel_id,
                                       'snippet.videoId': video_id,
                                       'snippet.topLevelComment.snippet.textOriginal': timestamp_in_string},
                                      part='snippet')
            '''
            break


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


def insert_timestamp_to_video(client, properties, **kwargs):
    resource = build_resource(properties)

    response = client.commentThreads().insert(
        body=resource,
        **kwargs
    ).execute()

    print(response)

    # TODO: Check if successfully


def build_resource(properties):
    resource = {}
    for p in properties:
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

            if key[-2:] == '[]':
                key = key[0:len(key) - 2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                ref[key] = {}
                ref = ref[key]
            else:
                ref = ref[key]
    return resource

