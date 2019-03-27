import os


class GatherDataConfigs:
    data_set_location = ""
    videos_set_location = ""
    intro_location = ""
    card_select_location = ""
    draft_location = ""
    game_play_location = ""
    other_location = ""

    def __init__(self, config_file):
        self.data_set_location = os.path.abspath(config_file['youtube']['dataset_location'])
        self.videos_set_location = os.path.abspath(config_file['youtube']['dataset_videos_location'])
        self.intro_location = os.path.abspath(config_file['youtube']['dataset_images_location_intro'])
        self.card_select_location = os.path.abspath(config_file['youtube']['dataset_images_location_card_select'])
        self.draft_location = os.path.abspath(config_file['youtube']['dataset_images_location_draft'])
        self.game_play_location = os.path.abspath(config_file['youtube']['dataset_images_location_game_play'])
        self.other_location = os.path.abspath(config_file['youtube']['dataset_images_location_other'])
