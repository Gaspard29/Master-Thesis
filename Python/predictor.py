from pathlib import Path

import joblib
import pandas as pd
import time

from preprocessing import (interpolate_csv, normalize_positions, flatten)


# Configuration

CSV_FOLDER = Path(r"C:\Users\Gaspard\Master_thesis\Recordings")
CSV_FILE = CSV_FOLDER / "Recording_temp.csv"
TRIGGER_FILE = CSV_FOLDER / "Recording_done.txt"
PREDICTION_FILE = CSV_FOLDER / "prediction.txt"

MODEL_FOLDER = Path("saved_models/svm_14")


def predict(csv_file, model, position_scalers, label_encoder):

    # read csv
    df = pd.read_csv(csv_file)

    # preprocess
    df = interpolate_csv(df)
    df = normalize_positions(df, position_scalers)
    vector = flatten(df)

    # prediction
    prediction = model.predict(vector.reshape(1, -1))[0]
    gesture = label_encoder.inverse_transform([prediction])[0]  

    return gesture

def main():

    print("Loading model...")

    model = joblib.load(MODEL_FOLDER / "svm.joblib")
    position_scalers = joblib.load(MODEL_FOLDER / "position_scalers.joblib")
    label_encoder = joblib.load(MODEL_FOLDER / "label_encoder.joblib")

    print("Model loaded.\n")

    print("Waiting for recordings...\n")

    while True:

        if TRIGGER_FILE.exists():

            try:

                gesture = predict(CSV_FILE, model, position_scalers, label_encoder)
                PREDICTION_FILE.write_text(gesture, encoding="utf-8")
                print("Prediction:", gesture)

            except Exception as e:

                print("Prediction failed:")
                print(e)

            # Remove the trigger
            TRIGGER_FILE.unlink()
            CSV_FILE.unlink()

        time.sleep(0.05)

if __name__ == "__main__":
    main()