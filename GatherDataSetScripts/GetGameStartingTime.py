import GatherDataSetScripts.Video as VideoClass


def get_game_starting_time_from_comments(client, data_set_location, comment_tracker):

    with open(data_set_location) as videos_file:
        videos = VideoClass.convert_json_to_object(videos_file)

        comment_thread_parameters = {
            'part': 'snippet',
            'maxResults': 100,
            'searchTerms': ':'
        }

        for video in videos:
            comment_thread_parameters['videoId'] = video.video_id
            comments_in_video = client.commentThreads().list(**comment_thread_parameters).execute()

            for comment_thread in comments_in_video['items']:
                author = comment_thread['snippet']['topLevelComment']['snippet']['authorChannelId']['value']

                if comment_tracker == author:
                    comment = comment_thread['snippet']['topLevelComment']['snippet']['textDisplay']

                    print(comment)

            break
