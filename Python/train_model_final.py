from pathlib import Path
import time

import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix)

from preprocessing import flatten

# Config

DATASET_FOLDER = Path("../prepared_dataset")

MODEL_FOLDER = Path("saved_models")
RESULTS_FOLDER = Path("experiments/svm")

MODEL_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 20

NUMBER_OF_TEST_PARTICIPANTS = 2
NUMBER_OF_CV_FOLDS = 5

# SVM parameters

KERNELS = ["linear", "poly", "rbf", "sigmoid"]
C_VALUES = [0.1, 1, 10, 100]
GAMMA_VALUES = [0.01, 0.1, 1]

# Polynomial kernel parameter.
POLY_DEGREE = 3

# Features

FEATURE_COLUMNS = [
    "Time", "LeftPosX", "LeftPosY", "LeftPosZ", "LeftRotX", "LeftRotY", "LeftRotZ", "LeftRotW",
    "RightPosX", "RightPosY", "RightPosZ", "RightRotX", "RightRotY", "RightRotZ", "RightRotW"
    ]


POSITION_FEATURES = [
    "LeftPosX", "LeftPosY", "LeftPosZ",
    "RightPosX", "RightPosY", "RightPosZ"
]


POSITION_INDICES = [FEATURE_COLUMNS.index(feature) for feature in POSITION_FEATURES]


# Load dataset

def load_dataset():

    X = []
    y = []
    participants = []

    participant_folders = sorted(DATASET_FOLDER.glob("Participant_*"))

    participant_count = len(participant_folders)
    sample_count = 0

    for participant in participant_folders:

        participant_name = participant.name
        gesture_folders = sorted(p for p in participant.iterdir() if p.is_dir())

        for gesture_folder in gesture_folders:

            gesture_name = gesture_folder.name
            csv_files = sorted(gesture_folder.glob("*.csv"))

            for csv_file in csv_files:

                df = pd.read_csv(csv_file)
                df = df[FEATURE_COLUMNS]

                # Keep the original sequence
                sample = df.to_numpy(dtype=float)

                X.append(sample)
                y.append(gesture_name)
                participants.append(participant_name)
                sample_count += 1

    X = np.array(X)
    y = np.array(y)
    participants = np.array(participants)

    print("Dataset loaded.")
    print()
    print("Participants :", participant_count)
    print("Samples      :", sample_count)
    print("Classes      :", len(np.unique(y)))
    print("Sample shape :", X.shape[1:])

    return X, y, participants


# Encode labels
def encode_labels(y):

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    print()
    print("Classes")
    print("--------------------")

    for i, gesture in enumerate(encoder.classes_):
        print(f"{i:2d} -> {gesture}")

    return y_encoded, encoder


# Split participants
def split_participants(X, y, participants):

    unique_participants = np.unique(participants)

    rng = np.random.default_rng(RANDOM_STATE)

    shuffled_participants = unique_participants.copy()
    rng.shuffle(shuffled_participants)

    test_participants = np.sort(shuffled_participants[:NUMBER_OF_TEST_PARTICIPANTS])
    development_participants = np.sort(shuffled_participants[NUMBER_OF_TEST_PARTICIPANTS:])

    test_mask = np.isin(participants, test_participants)
    development_mask = np.isin(participants, development_participants)

    print()
    print("Participant split")
    print("--------------------")

    print("Test participants:")
    for participant in test_participants:
        print(f"  {participant}")

    print()
    print("Development participants:")
    for participant in development_participants:
        print(f"  {participant}")

    return (X[development_mask], y[development_mask], X[test_mask], y[test_mask], test_participants)


# Normalize positions
def normalize_positions(X_train, X_other):

    X_train = X_train.copy()
    X_other = X_other.copy()

    scalers = {}

    for feature_index in POSITION_INDICES:

        scaler = StandardScaler()

        scaler.fit(X_train[:, :, feature_index].reshape(-1, 1))

        X_train[:, :, feature_index] = (scaler.transform(X_train[:, :, feature_index].reshape(-1, 1))
            .reshape(X_train.shape[0], X_train.shape[1]))

        X_other[:, :, feature_index] = (scaler.transform(X_other[:, :, feature_index].reshape(-1, 1))
            .reshape(X_other.shape[0], X_other.shape[1]))

        scalers[FEATURE_COLUMNS[feature_index]] = scaler

    return X_train, X_other, scalers


# Flatten dataset
def flatten_dataset(X):

    return np.array([flatten(pd.DataFrame(sample,columns=FEATURE_COLUMNS))
        for sample in X])


# Create SVM
def create_svm(kernel, C, gamma):

    if kernel == "poly":

        return SVC(kernel=kernel, C=C, gamma=gamma, degree=POLY_DEGREE)

    else:

        return SVC(kernel=kernel, C=C, gamma=gamma)

# Cross-validation
def cross_validate_svm(X, y, kernel, C, gamma):

    kfold = KFold(n_splits=NUMBER_OF_CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    accuracies = []
    f1_scores = []
    training_times = []

    for train_indices, validation_indices in kfold.split(X):

        X_train = X[train_indices]
        X_val = X[validation_indices]

        y_train = y[train_indices]
        y_val = y[validation_indices]

        # Normalize using training fold only
        X_train, X_val, _ = normalize_positions(X_train, X_val)

        # Flatten
        X_train = flatten_dataset(X_train)
        X_val = flatten_dataset(X_val)

        # Create and train model
        model = create_svm(kernel, C, gamma)

        start_time = time.perf_counter()
        model.fit(X_train, y_train)

        training_time = (time.perf_counter() - start_time)

        # Validation
        predictions = model.predict(X_val)
        accuracy = accuracy_score(y_val, predictions)
        f1 = f1_score(y_val, predictions, average="macro", zero_division=0)

        accuracies.append(accuracy)
        f1_scores.append(f1)
        training_times.append(training_time)

    return {
        "accuracy_mean": np.mean(accuracies),
        "accuracy_std": np.std(accuracies),
        "f1_mean": np.mean(f1_scores),
        "f1_std": np.std(f1_scores),
        "training_time_mean": np.mean(training_times)
    }


# Hyperparameter search
def train_svm(X, y):

    total_experiments = (len(KERNELS) * len(C_VALUES) * len(GAMMA_VALUES))

    print()
    print("SVM hyperparameter search")
    print("--------------------")
    print(f"Experiments : {total_experiments}")
    print(f"CV folds    : {NUMBER_OF_CV_FOLDS}")
    print(f"Total fits  : "
        f"{total_experiments * NUMBER_OF_CV_FOLDS}"
    )

    results = []

    experiment_number = 0

    best_f1 = -1
    best_parameters = None

    for kernel in KERNELS:

        for C in C_VALUES:

            for gamma in GAMMA_VALUES:

                experiment_number += 1

                print(
                    f"[{experiment_number}/{total_experiments}] "
                    f"kernel={kernel}, "
                    f"C={C}, "
                    f"gamma={gamma}"
                )

                metrics = cross_validate_svm(X, y, kernel, C, gamma)

                result = {
                    "kernel": kernel,
                    "C": C,
                    "gamma": gamma,
                    "accuracy_mean": metrics["accuracy_mean"],
                    "accuracy_std": metrics["accuracy_std"],
                    "f1_mean": metrics["f1_mean"],
                    "f1_std": metrics["f1_std"],
                    "training_time_mean": metrics["training_time_mean"]
                }

                results.append(result)

                print(
                    f"    Accuracy: "
                    f"{metrics['accuracy_mean']:.4f} "
                    f"+/- "
                    f"{metrics['accuracy_std']:.4f}"
                )

                print(
                    f"    F1:       "
                    f"{metrics['f1_mean']:.4f} "
                    f"+/- "
                    f"{metrics['f1_std']:.4f}"
                )

                # Select based on macro F1
                if metrics["f1_mean"] > best_f1:

                    best_f1 = metrics["f1_mean"]
                    best_parameters = {"kernel": kernel, "C": C, "gamma": gamma}

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(by="f1_mean", ascending=False)

    # Save all experiments
    results_df.to_csv(RESULTS_FOLDER / "svm_results.csv", index=False)

    print()
    print("Best SVM")
    print("--------------------")
    print(
        f"Kernel : "
        f"{best_parameters['kernel']}"
    )
    print(
        f"C      : "
        f"{best_parameters['C']}"
    )
    print(
        f"gamma  : "
        f"{best_parameters['gamma']}"
    )
    print(
        f"CV F1  : "
        f"{best_f1:.4f}"
    )

    return best_parameters, results_df

# Train final model
def train_final_model(X_train, y_train, parameters):

    # Normalize using all development data
    X_train, _, scalers = normalize_positions(X_train,X_train.copy())
    X_train = flatten_dataset(X_train)

    model = create_svm(parameters["kernel"], parameters["C"], parameters["gamma"])

    print()
    print("Training final model")
    print("--------------------")

    start_time = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = (time.perf_counter() - start_time)

    print(
        f"Training time : "
        f"{training_time:.2f} seconds"
    )

    return model, scalers


# Evaluate final model
def evaluate_model(model, scalers, X_test, y_test, label_encoder, test_participants):

    # Apply scalers fitted on development data
    X_test = X_test.copy()

    for feature_index in POSITION_INDICES:

        feature_name = FEATURE_COLUMNS[feature_index]
        scaler = scalers[feature_name]

        X_test[:, :, feature_index] = (scaler.transform(X_test[:, :, feature_index].reshape(-1, 1))
            .reshape(X_test.shape[0],X_test.shape[1]))

    X_test = flatten_dataset(X_test)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="macro", zero_division=0)
    precision = precision_score(y_test, predictions, average="macro", zero_division=0)

    recall = recall_score(y_test, predictions, average="macro", zero_division=0)

    print()
    print("Final test evaluation")
    print("--------------------")

    print(
        f"Test participants : "
        f"{', '.join(test_participants)}"
    )

    print(
        f"Accuracy          : "
        f"{accuracy:.4f}"
    )

    print(
        f"Precision (macro) : "
        f"{precision:.4f}"
    )

    print(
        f"Recall (macro)    : "
        f"{recall:.4f}"
    )

    print(
        f"F1 (macro)        : "
        f"{f1:.4f}"
    )


    # Classification report
    print()
    print("Classification report")
    print("--------------------")

    report = classification_report(y_test, predictions, target_names=label_encoder.classes_, zero_division=0)

    print(report)

    # Save report
    with open(RESULTS_FOLDER / "test_classification_report.txt", "w") as file:

        file.write(report)

    # Save final metrics
    final_results = pd.DataFrame([{
        "test_participants": ", ".join(test_participants),
        "accuracy": accuracy,
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1

    }])

    final_results.to_csv(RESULTS_FOLDER / "final_test_results.csv", index=False)


# Save model
def save_model(model, position_scalers, label_encoder):

    joblib.dump(model, MODEL_FOLDER / "svm.joblib")
    joblib.dump(position_scalers, MODEL_FOLDER / "position_scalers.joblib")
    joblib.dump(label_encoder, MODEL_FOLDER / "label_encoder.joblib")

    print()
    print("Model saved.")


# Main
def main():

    print()
    print("=" * 60)
    print("SVM TRAINING")
    print("=" * 60)

    X, y, participants = load_dataset()
    y, label_encoder = encode_labels(y)

    (X_development, y_development, X_test, y_test, test_participants) = split_participants(
        X, y, participants)

    # Hyperparameter search
    best_parameters, results_df = train_svm(X_development, y_development)

    # Train final model
    model, scalers = train_final_model(X_development, y_development, best_parameters)

    # Final test evaluation
    evaluate_model(model, scalers, X_test, y_test, label_encoder, test_participants)

    # Save
    save_model(model, scalers, label_encoder)

    print()
    print("=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    print()
    print(
        f"Results saved in: "
        f"{RESULTS_FOLDER}"
    )

if __name__ == "__main__":
    main()