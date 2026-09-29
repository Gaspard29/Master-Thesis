from pathlib import Path

import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
import time

from preprocessing import (interpolate_csv, normalize_positions, flatten)


# CONFIG
# Choose: "cnn" or "svm"
MODEL_TYPE = "svm"

CSV_FOLDER = Path(r"C:\Users\Gaspard\Master_thesis\Recordings")

CSV_FILE = CSV_FOLDER / "Recording_temp.csv"
TRIGGER_FILE = CSV_FOLDER / "Recording_done.txt"
PREDICTION_FILE = CSV_FOLDER / "prediction.txt"


# Select the corresponding model folder
if MODEL_TYPE == "cnn":
    MODEL_FOLDER = Path("saved_models") / "CNN_14"

elif MODEL_TYPE == "svm":
    MODEL_FOLDER = Path("saved_models") / "svm_14"

else:
    raise ValueError(
        f"Unknown MODEL_TYPE: {MODEL_TYPE}"
    )


# PREDICTION
def predict(csv_file, model, position_scalers, label_encoder):

    df = pd.read_csv(csv_file)

    # Preprocessing
    df = interpolate_csv(df)
    df = normalize_positions(df, position_scalers)

    # CNN
    if MODEL_TYPE == "cnn":

        # The CNN was trained on:
        # (50 time steps, 15 features)

        feature_columns = ["Time", "LeftPosX", "LeftPosY", "LeftPosZ", "LeftRotX", "LeftRotY",
            "LeftRotZ", "LeftRotW", "RightPosX", "RightPosY", "RightPosZ", "RightRotX",
            "RightRotY", "RightRotZ", "RightRotW"
        ]

        data = df[feature_columns].to_numpy(dtype=np.float32)

        # Add batch dimension
        data = data.reshape(1, 50, 15)

        # Get probabilities
        probabilities = model.predict(data, verbose=0)

        # Get class with highest probability
        prediction = np.argmax(probabilities, axis=1)[0]

    # SVM
    elif MODEL_TYPE == "svm":

        vector = flatten(df)
        prediction = model.predict(vector.reshape(1, -1))[0]


    # Convert class number to gesture name
    gesture = label_encoder.inverse_transform([prediction])[0]

    return gesture


def main():

    print("========================================")
    print("Gesture Predictor")
    print("========================================")

    print("Selected model:", MODEL_TYPE)
    print("Model folder:", MODEL_FOLDER)

    print("\nLoading model...")

    # Load CNN
    if MODEL_TYPE == "cnn":

        model = tf.keras.models.load_model(MODEL_FOLDER / "gesture_cnn.keras")
        print("Keras CNN loaded.")

    # Load SVM
    elif MODEL_TYPE == "svm":

        model = joblib.load(MODEL_FOLDER / "svm.joblib")
        print("SVM loaded.")

    # Load preprocessing objects
    position_scalers = joblib.load(MODEL_FOLDER / "position_scalers.joblib")
    label_encoder = joblib.load(MODEL_FOLDER / "label_encoder.joblib")

    print("Position scalers loaded.")
    print("Label encoder loaded.")

    print("\nModel loaded successfully.")
    print("Waiting for recordings...\n")


    # WAIT FOR RECORDINGS
    while True:

        if TRIGGER_FILE.exists():

            gesture = predict(CSV_FILE, model, position_scalers, label_encoder)

            # Save prediction
            PREDICTION_FILE.write_text(gesture, encoding="utf-8")
            print("Prediction:", gesture)

            # Remove trigger and temporary recording
            TRIGGER_FILE.unlink()

            if CSV_FILE.exists():
                CSV_FILE.unlink()

        time.sleep(0.05)


if __name__ == "__main__":
    main()