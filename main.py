import GatherDataSetScripts.GetAllVideosIds as gather_data_set
from googleapiclient.discovery import build
import logging


if __name__ == "__main__":
    logging.basicConfig(filename="logging.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG)

    client = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
