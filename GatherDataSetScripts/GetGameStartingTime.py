

def get_game_starting_time_from_comments():

    with open(VIDEOS_DATA_LOCATION) as videos_file:
        videos = convert_json_to_object(videos_file)

        comment_thread_parameters = {
            'part': 'snippet',
            'maxResults': 100,
            'searchTerms': ':'
        }

        for video in videos:
            comment_thread_parameters['videoId'] = video.video_id
            comments_in_video = client.commentThreads().list(**comment_thread_parameters).execute()

            for comment_thread in comments_in_video['items']:
                content_details_video = comment_thread['snippet']['textDisplay']

            break

        print(len(videos))