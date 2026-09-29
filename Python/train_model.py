from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix)

from preprocessing import flatten



# Configuration
DATASET_FOLDER = Path("../prepared_dataset")

MODEL_FOLDER = Path("saved_models")

MODEL_FOLDER.mkdir(exist_ok=True)

TRAIN_RATIO = 0.60
VALIDATION_RATIO = 0.20
TEST_RATIO = 0.20

RANDOM_STATE = 42



# Features

FEATURE_COLUMNS = [

    "Time", "LeftPosX", "LeftPosY", "LeftPosZ", "LeftRotX",
    "LeftRotY", "LeftRotZ", "LeftRotW", "RightPosX",
    "RightPosY", "RightPosZ", "RightRotX", "RightRotY",
    "RightRotZ","RightRotW"

]

POSITION_FEATURES = [

    "LeftPosX", "LeftPosY", "LeftPosZ",
    "RightPosX", "RightPosY", "RightPosZ"

]

POSITION_INDICES = [
    FEATURE_COLUMNS.index(feature)
    for feature in POSITION_FEATURES
]

def load_dataset():

    X = []
    y = []

    participant_folders = sorted(DATASET_FOLDER.glob("Participant_*"))

    participant_count = len(participant_folders)
    sample_count = 0

    for participant in participant_folders:

        gesture_folders = sorted(p for p in participant.iterdir() if p.is_dir())

        for gesture_folder in gesture_folders:

            gesture_name = gesture_folder.name

            csv_files = sorted(gesture_folder.glob("*.csv"))

            for csv_file in csv_files:

                df = pd.read_csv(csv_file)

                df = df[FEATURE_COLUMNS]

                # Keep the 50x15 matrix
                sample = df.to_numpy(dtype=float)

                X.append(sample)
                y.append(gesture_name)

                sample_count += 1

    X = np.array(X)
    y = np.array(y)

    print("Dataset loaded.")
    print()

    print("Participants :", participant_count)
    print("Samples      :", sample_count)
    print("Classes      :", len(np.unique(y)))
    print("Sample shape :", X.shape[1:])

    return X, y


def encode_labels(y):

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(y)

    """ print()
    print("Classes:")

    for i, gesture in enumerate(encoder.classes_):
        print(f"{i:2d} -> {gesture}") """

    return y_encoded, encoder


def split_dataset(X, y):

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=TRAIN_RATIO, stratify=y,
        random_state=RANDOM_STATE
        )

    validation_fraction = VALIDATION_RATIO / (VALIDATION_RATIO + TEST_RATIO)

    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, train_size=validation_fraction,
        stratify=y_temp, random_state=RANDOM_STATE
        )

    """ print()
    print("Dataset split")
    print("--------------------")
    print("Training   :", len(X_train))
    print("Validation :", len(X_val))
    print("Test       :", len(X_test)) """

    return (X_train, X_val, X_test, y_train, y_val, y_test)


def normalize_positions(X_train, X_val, X_test):

    scalers = {}

    for feature_index in POSITION_INDICES:

        scaler = StandardScaler()

        scaler.fit(X_train[:, :, feature_index].reshape(-1, 1))

        X_train[:, :, feature_index] = scaler.transform(X_train[:, :, feature_index].reshape(-1, 1)
        ).reshape(X_train.shape[0], X_train.shape[1])

        X_val[:, :, feature_index] = scaler.transform(X_val[:, :, feature_index].reshape(-1, 1)
        ).reshape(X_val.shape[0], X_val.shape[1])

        X_test[:, :, feature_index] = scaler.transform(X_test[:, :, feature_index].reshape(-1, 1)
        ).reshape(X_test.shape[0], X_test.shape[1])

        scalers[FEATURE_COLUMNS[feature_index]] = scaler

    print()
    print("Position normalization complete.")

    return (X_train, X_val, X_test, scalers)


def train_svm(X_train, y_train, X_val, y_val):

    """ print()
    print("Hyperparameter search")
    print("--------------------") """

    C_values = [0.1, 1, 10, 100]
    gamma_values = [0.01, 0.1, 1]

    best_accuracy = 0
    best_model = None
    best_parameters = None

    for C in C_values:

        for gamma in gamma_values:

            model = SVC(kernel="rbf", C=C, gamma=gamma)
            model.fit(X_train,y_train)
            predictions = model.predict(X_val)
            accuracy = accuracy_score(y_val, predictions)

            """ print(
                f"C={C:<5} "
                f"gamma={gamma:<4} "
                f"Validation={accuracy:.4f}"
            ) """

            if accuracy > best_accuracy:

                best_accuracy = accuracy
                best_model = model
                best_parameters = (C, gamma)

    print()
    print("Best model")
    print(f"C = {best_parameters[0]}")
    print(f"gamma = {best_parameters[1]}")
    print(f"Validation accuracy = {best_accuracy:.4f}")

    return best_model


def evaluate_model(model, X_test, y_test, label_encoder):

    print()
    print("Test evaluation")
    print("--------------------")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy : {accuracy:.4f}")

    print()
    print("Classification report")
    print("--------------------")

    print(classification_report(y_test, predictions, target_names=label_encoder.classes_))

    print()
    print("Confusion matrix")
    print("--------------------")

    print(confusion_matrix(y_test,predictions))

    return accuracy


def save_model(model, position_scalers, label_encoder):

    MODEL_FOLDER.mkdir(exist_ok=True)

    joblib.dump(model, MODEL_FOLDER / "svm.joblib")

    joblib.dump(position_scalers, MODEL_FOLDER / "position_scalers.joblib")

    joblib.dump(label_encoder, MODEL_FOLDER / "label_encoder.joblib")

    print()
    print("Model saved.")


def main():

    print("Loading dataset...\n")

    X, y = load_dataset()

    y, label_encoder = encode_labels(y)

    (X_train, X_val, X_test, y_train, y_val, y_test) = split_dataset(X, y)

    (X_train, X_val, X_test, scalers) = normalize_positions(X_train, X_val, X_test)

    X_train = np.array([flatten(pd.DataFrame(sample, columns=FEATURE_COLUMNS))
        for sample in X_train
        ])

    X_val = np.array([flatten(pd.DataFrame(sample, columns=FEATURE_COLUMNS))
        for sample in X_val
    ])

    X_test = np.array([flatten(pd.DataFrame(sample, columns=FEATURE_COLUMNS))
        for sample in X_test
    ])

    print()
    print("Final shapes")
    print("--------------------")
    print(X_train.shape)
    print(X_val.shape)
    print(X_test.shape)


    model = train_svm(X_train, y_train, X_val, y_val)

    #evaluate_model(model, X_test, y_test, label_encoder)

    save_model(model, scalers, label_encoder)

if __name__ == "__main__":
    main()