import numpy as np
import pandas as pd

TARGET_LENGTH = 50

FEATURE_COLUMNS = [

    "Time", "LeftPosX", "LeftPosY", "LeftPosZ", "LeftRotX", "LeftRotY",
    "LeftRotZ", "LeftRotW", "RightPosX", "RightPosY", "RightPosZ",
    "RightRotX", "RightRotY", "RightRotZ", "RightRotW"

]

QUATERNION_GROUPS = [

    ["LeftRotX", "LeftRotY", "LeftRotZ", "LeftRotW"],
    ["RightRotX", "RightRotY", "RightRotZ", "RightRotW"]

]

POSITION_FEATURES = [

    "LeftPosX", "LeftPosY", "LeftPosZ", "RightPosX", "RightPosY", "RightPosZ"

]

POSITION_INDICES = [FEATURE_COLUMNS.index(feature) for feature in POSITION_FEATURES]


def normalize_quaternions(df):

    for group in QUATERNION_GROUPS:

        q = df[group].to_numpy(dtype=float)
        norms = np.linalg.norm(q, axis=1, keepdims=True)

        # Avoid division by zero
        norms[norms == 0] = 1.0

        df[group] = q / norms

    return df


def interpolate_csv(df):

    # Original timestamps
    old_time = df["Time"].to_numpy(dtype=float)

    # New timestamps
    new_time = np.linspace(old_time[0], old_time[-1], TARGET_LENGTH)

    # Interpolate every column
    new_df = pd.DataFrame()

    for column in df.columns:

        values = df[column].to_numpy(dtype=float)
        new_df[column] = np.interp(new_time, old_time, values)

    new_df = normalize_quaternions(new_df)

    return new_df



def normalize_positions(df, position_scalers):

    for feature_index in POSITION_INDICES:

        column = FEATURE_COLUMNS[feature_index]
        scaler = position_scalers[column]
        values = df[column].to_numpy().reshape(-1, 1)
        df[column] = scaler.transform(values)

    return df


def flatten(df):

    df = df[FEATURE_COLUMNS]
    return df.to_numpy(dtype=float).flatten()