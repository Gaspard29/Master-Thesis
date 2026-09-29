"""
Configuration file for the Gesture Acquisition Framework

"""

# Folder where Unity exports the temporary recording
RECORDING_FOLDER = r"C:\Users\Gaspard\Master_thesis\Recordings"

# Root folder where the validated dataset will be stored
DATASET_FOLDER = r"C:\Users\Gaspard\Master_thesis\Dataset"

# Number of digits used when naming participants
PARTICIPANT_DIGITS = 2


# Name of the temporary file produced by Unity
# Unity should always overwrite this file.
TEMP_RECORDING_NAME = "Recording_temp.csv"


# GESTURES
GESTURES = [
    "Order", "Pay", "Add", "Remove", "Brewed Coffee", "Cappuccino",
    "Latte", "Espresso", "Milk", "Sugar", "Tea", "Hot Chocolate",
    "Bar", "Table", "Take-Away", "Quantity (1)", "Quantity (2)",
    "Quantity (3)", "Small", "Medium", "Large", "Iced"
]



# VISUALIZATION
LEFT_CONTROLLER_COLORMAP = "Blues"
RIGHT_CONTROLLER_COLORMAP = "Oranges"
LINE_WIDTH = 3
START_MARKER_SIZE = 100
END_MARKER_SIZE = 100



# EXPERIMENT

DEFAULT_REPETITIONS = 5
RANDOMIZE_GESTURE_ORDER = True
FILE_WRITE_DELAY = 0.5
REPETITION_DIGITS = 2