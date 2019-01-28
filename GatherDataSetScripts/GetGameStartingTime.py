import GatherDataSetScripts.Video as VideoClass
import re


def get_game_starting_time_from_comments(client, data_set_location, comment_tracker):
    time_stamp_regex = "[0-9]+:[0-9]+"

    with open(data_set_location) as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)
        page_token = ""
        comment_thread_parameters = {
            'part': 'snippet',
            'maxResults': 100,
            'searchTerms': ':'
        }

        for video in videos:
            # comment_thread_parameters['videoId'] = video.video_id
            while True:
                comment_thread_parameters['videoId'] = 'pYn1x5RM9kg'
                comment_thread_parameters['pageToken'] = page_token

                comments_in_video = client.commentThreads().list(**comment_thread_parameters).execute()

                for comment_thread in comments_in_video['items']:
                    author = comment_thread['snippet']['topLevelComment']['snippet']['authorChannelId']['value']

                    # Comment found, save it
                    if comment_tracker == author:
                        comment = comment_thread['snippet']['topLevelComment']['snippet']['textDisplay']
                        video.game_starting_time = re.findall(time_stamp_regex, comment)
                        video.is_game_starting_time_checked = True
                        break

                # If we found the comment, stop looking (Assumption the user posts once, he usually does post once)
                if video.is_game_starting_time_checked:
                    break

                if 'nextPageToken' in comments_in_video:
                    next_page_token = comments_in_video['nextPageToken']
                    page_token = next_page_token

                    if next_page_token == "":
                        break
                else:
                    break

            break
