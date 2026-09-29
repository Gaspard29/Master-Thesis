import os
import random
import time

import config

from dataset_manager import DatasetManager
from gesture_viewer import GestureViewer


# PARTICIPANT

print("====================================")
print(" VR Gesture Acquisition")
print("====================================\n")

participant = int(input("Participant ID : "))

repetitions = input(f"Number of repetitions [{config.DEFAULT_REPETITIONS}] : ")

if repetitions == "":
    repetitions = config.DEFAULT_REPETITIONS
else:
    repetitions = int(repetitions)


# INITIALIZATION
viewer = GestureViewer()
dataset = DatasetManager(participant)
temp_csv = dataset.temporary_recording_path()
gestures = config.GESTURES.copy()

if config.RANDOMIZE_GESTURE_ORDER:
    random.shuffle(gestures)

accepted = 0
rejected = 0

print("\nGesture order :")

for i, g in enumerate(gestures):
    print(f"{i+1}. {g}")

print("\n====================================")

# MAIN LOOP
for gesture_index, gesture in enumerate(gestures):

    print()
    print("====================================")
    print(f"Gesture {gesture_index+1}/{len(gestures)}")
    print(f"Current gesture : {gesture}")
    print("====================================")

    repetition = 1

    while repetition <= repetitions:

        print()
        print(f"Repetition {repetition}/{repetitions}")
        print("Waiting for Unity...")

        # Wait until Unity produces Recording_temp.csv
        while not os.path.exists(temp_csv):
            time.sleep(0.2)

        # Give Unity enough time to finish writing
        time.sleep(config.FILE_WRITE_DELAY)

        # Display recording
        viewer.show(temp_csv)

        # Validation
        while True:

            answer = input(
                "\n"
                "[Y] Accept   "
                "[N] Reject   "
                "[R] Redisplay   "
                "[Q] Quit\n"
            ).strip().lower()

            if answer == "r":

                viewer.show(temp_csv)

            elif answer == "y":

                destination = dataset.save_recording(temp_csv,
                    gesture, repetition
                )

                accepted += 1

                print("\nSaved:")
                print(destination)

                repetition += 1

                break

            elif answer == "n":

                dataset.reject_recording(temp_csv)
                rejected += 1
                print("\nRecording rejected.")
                break

            elif answer == "q":

                print("\nExperiment interrupted.")
                print(f"Accepted : {accepted}")
                print(f"Rejected : {rejected}")

                quit()

            else:

                print("Unknown command.")
                

print()
print("====================================")
print("Experiment completed")
print("====================================")

print(f"Accepted recordings : {accepted}")
print(f"Rejected recordings : {rejected}")

print("\nDataset successfully created.")