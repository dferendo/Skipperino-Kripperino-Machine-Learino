import sched
import time
import logging

scheduler = None
delay = 0


def init_scheduler(api_client, scheduler_delay):
    global scheduler, delay
    scheduler = sched.scheduler(time.time, time.sleep)
    delay = scheduler_delay

    scheduler.enter(delay, 1, check_if_there_is_new_video_upload, (api_client, None))
    scheduler.run()


def check_if_there_is_new_video_upload(api_client, last_video_id):
    logging.info("Checking if new video was uploaded recently.")

    scheduler.enter(delay, 1, check_if_there_is_new_video_upload, (api_client, last_video_id))
