import json


class Video:
    video_id = ""
    video_published_at = ""
    game_starting_time = []
    is_game_starting_time_checked = False
    video_file_location = ""
    is_video_downloaded = False

    def __init__(self, video_id, video_published_at, game_starting_time, is_game_starting_time_checked,
                 video_file_location, is_video_downloaded):
        self.video_id = video_id
        self.video_published_at = video_published_at
        self.game_starting_time = game_starting_time
        self.is_game_starting_time_checked = is_game_starting_time_checked
        self.video_file_location = video_file_location
        self.is_video_downloaded = is_video_downloaded


def convert_json_to_object(videos_file):
    videos_in_json = json.load(videos_file)
    videos = []

    for video_in_json in videos_in_json:
        videos.append(Video(video_in_json['video_id'], video_in_json['video_published_at'],
                            video_in_json['game_starting_time'], video_in_json['is_game_starting_time_checked'],
                            video_in_json['video_file_location'], video_in_json['is_video_downloaded']))

    return videos
