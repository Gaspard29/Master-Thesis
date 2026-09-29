import os
import shutil

import config


class DatasetManager:

    def __init__(self, participant_id):

        self.participant_id = participant_id

        self.participant_folder = os.path.join(config.DATASET_FOLDER,
            f"Participant_{participant_id:0{config.PARTICIPANT_DIGITS}d}"
        )

        os.makedirs(self.participant_folder, exist_ok=True)


    def create_gesture_folder(self, gesture):

        folder = os.path.join(self.participant_folder, gesture)
        os.makedirs(folder, exist_ok=True)

        return folder


    def save_recording(self, temp_csv, gesture, repetition):

        gesture_folder = self.create_gesture_folder(gesture)

        filename = (
            f"{gesture}_"
            f"{repetition:0{config.REPETITION_DIGITS}d}.csv"
        )

        destination = os.path.join(gesture_folder, filename)
        shutil.move(temp_csv, destination)

        return destination


    def reject_recording(self, temp_csv):

        if os.path.exists(temp_csv):
            os.remove(temp_csv)


    def temporary_recording_path(self):

        return os.path.join(config.RECORDING_FOLDER, config.TEMP_RECORDING_NAME)