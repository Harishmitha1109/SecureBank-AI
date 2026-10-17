import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "behavior_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "models",
    "behavior_model.pkl"
)


# ==========================================
# LOAD GENUINE DATA
# ==========================================

df = pd.read_csv(DATASET_PATH)

print("\n===================================")
print("ORIGINAL DATASET")
print("===================================")

print(f"Genuine samples: {len(df)}")


# ==========================================
# FEATURES
# ==========================================

feature_columns = [
    "mouse_distance_mean",
    "mouse_distance_std",
    "clicks_mean",
    "clicks_total",
    "scroll_distance_mean",
    "scroll_distance_total",
    "session_duration",
    "mouse_activity_rate",
    "click_activity_rate",
    "scroll_activity_rate",
    "device"
]


genuine = df[feature_columns].copy()


# ==========================================
# CLEAN DATA
# ==========================================

genuine = genuine.replace(
    [np.inf, -np.inf],
    np.nan
)

genuine = genuine.fillna(0)


# ==========================================
# SPLIT GENUINE DATA
# ==========================================

genuine_train, genuine_test = train_test_split(
    genuine,
    test_size=0.25,
    random_state=42
)


print("\n===================================")
print("GENUINE DATA SPLIT")
print("===================================")

print(
    f"Genuine training samples: {len(genuine_train)}"
)

print(
    f"Genuine testing samples : {len(genuine_test)}"
)


# ==========================================
# CREATE SUSPICIOUS SAMPLE
# ==========================================

def create_suspicious_sample(row, anomaly_type):

    suspicious = row.copy()


    # --------------------------------------
    # 1. LONG SESSION
    # --------------------------------------

    if anomaly_type == "long_session":

        suspicious["session_duration"] *= np.random.uniform(
            2.5,
            4.0
        )

        suspicious["mouse_distance_mean"] *= np.random.uniform(
            0.7,
            1.3
        )

        suspicious["mouse_distance_std"] *= np.random.uniform(
            0.7,
            1.3
        )

        suspicious["clicks_mean"] *= np.random.uniform(
            0.7,
            1.3
        )

        suspicious["clicks_total"] *= np.random.uniform(
            0.7,
            1.3
        )

        suspicious["scroll_distance_mean"] *= np.random.uniform(
            0.7,
            1.3
        )

        suspicious["scroll_distance_total"] *= np.random.uniform(
            0.7,
            1.3
        )


    # --------------------------------------
    # 2. LOW ACTIVITY
    # --------------------------------------

    elif anomaly_type == "low_activity":

        suspicious["mouse_distance_mean"] *= np.random.uniform(
            0.25,
            0.55
        )

        suspicious["mouse_distance_std"] *= np.random.uniform(
            0.30,
            0.65
        )

        suspicious["clicks_mean"] *= np.random.uniform(
            0.15,
            0.50
        )

        suspicious["clicks_total"] *= np.random.uniform(
            0.15,
            0.50
        )

        suspicious["scroll_distance_mean"] *= np.random.uniform(
            0.25,
            0.55
        )

        suspicious["scroll_distance_total"] *= np.random.uniform(
            0.25,
            0.55
        )

        suspicious["mouse_activity_rate"] *= np.random.uniform(
            0.30,
            0.65
        )

        suspicious["click_activity_rate"] *= np.random.uniform(
            0.20,
            0.60
        )

        suspicious["scroll_activity_rate"] *= np.random.uniform(
            0.30,
            0.65
        )


    # --------------------------------------
    # 3. INTERACTION MISMATCH
    # --------------------------------------

    elif anomaly_type == "interaction_mismatch":

        suspicious["mouse_distance_mean"] *= np.random.uniform(
            1.4,
            2.2
        )

        suspicious["mouse_distance_std"] *= np.random.uniform(
            1.4,
            2.2
        )

        suspicious["clicks_mean"] *= np.random.uniform(
            0.15,
            0.45
        )

        suspicious["clicks_total"] *= np.random.uniform(
            0.15,
            0.45
        )

        suspicious["scroll_distance_mean"] *= np.random.uniform(
            1.4,
            2.2
        )

        suspicious["scroll_distance_total"] *= np.random.uniform(
            1.4,
            2.2
        )

        suspicious["click_activity_rate"] *= np.random.uniform(
            0.15,
            0.45
        )


    # --------------------------------------
    # 4. ACTIVITY MISMATCH
    # --------------------------------------

    elif anomaly_type == "activity_mismatch":

        suspicious["mouse_activity_rate"] = np.random.uniform(
            0.85,
            1.0
        )

        suspicious["click_activity_rate"] = np.random.uniform(
            0.0,
            0.20
        )

        suspicious["scroll_activity_rate"] = np.random.uniform(
            0.80,
            1.0
        )

        suspicious["mouse_distance_mean"] *= np.random.uniform(
            1.3,
            2.0
        )

        suspicious["scroll_distance_mean"] *= np.random.uniform(
            1.3,
            2.0
        )


    # ======================================
    # VALIDATE VALUES
    # ======================================

    for column in feature_columns:

        if column != "device":

            suspicious[column] = max(
                0,
                suspicious[column]
            )


    suspicious["mouse_activity_rate"] = np.clip(
        suspicious["mouse_activity_rate"],
        0,
        1
    )

    suspicious["click_activity_rate"] = np.clip(
        suspicious["click_activity_rate"],
        0,
        1
    )

    suspicious["scroll_activity_rate"] = np.clip(
        suspicious["scroll_activity_rate"],
        0,
        1
    )


    return suspicious


# ==========================================
# GENERATE BALANCED SUSPICIOUS TRAINING DATA
# ==========================================

np.random.seed(42)

anomaly_types = [
    "long_session",
    "low_activity",
    "interaction_mismatch",
    "activity_mismatch"
]


suspicious_train_samples = []


# 24 genuine training samples
# Create 1 suspicious variation per sample
# Therefore:
#
# Genuine    = 24
# Suspicious = 24
#
# Balanced training set.

for _, row in genuine_train.iterrows():

    anomaly_type = np.random.choice(
        anomaly_types
    )

    suspicious_sample = create_suspicious_sample(
        row,
        anomaly_type
    )

    suspicious_train_samples.append(
        suspicious_sample
    )


suspicious_train = pd.DataFrame(
    suspicious_train_samples
)


# ==========================================
# GENERATE BALANCED TEST DATA
# ==========================================

suspicious_test_samples = []


# 8 genuine testing samples
# Create 1 suspicious variation per sample
#
# Genuine    = 8
# Suspicious = 8

for _, row in genuine_test.iterrows():

    anomaly_type = np.random.choice(
        anomaly_types
    )

    suspicious_sample = create_suspicious_sample(
        row,
        anomaly_type
    )

    suspicious_test_samples.append(
        suspicious_sample
    )


suspicious_test = pd.DataFrame(
    suspicious_test_samples
)


# ==========================================
# LABEL DATA
# ==========================================

genuine_train = genuine_train.copy()

genuine_test = genuine_test.copy()


genuine_train["label"] = 1

suspicious_train["label"] = 0

genuine_test["label"] = 1

suspicious_test["label"] = 0


# ==========================================
# COMBINE TRAINING DATA
# ==========================================

train_data = pd.concat(
    [
        genuine_train,
        suspicious_train
    ],
    ignore_index=True
)


# ==========================================
# COMBINE TEST DATA
# ==========================================

test_data = pd.concat(
    [
        genuine_test,
        suspicious_test
    ],
    ignore_index=True
)


# ==========================================
# SHUFFLE
# ==========================================

train_data = train_data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


test_data = test_data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ==========================================
# X / Y
# ==========================================

X_train = train_data[
    feature_columns
]

y_train = train_data[
    "label"
]


X_test = test_data[
    feature_columns
]

y_test = test_data[
    "label"
]


# ==========================================
# DATASET INFORMATION
# ==========================================

print("\n===================================")
print("BALANCED TRAINING DATASET")
print("===================================")

print(
    f"Training samples : {len(train_data)}"
)

print(
    f"Genuine          : {(y_train == 1).sum()}"
)

print(
    f"Suspicious       : {(y_train == 0).sum()}"
)


print("\n===================================")
print("BALANCED TEST DATASET")
print("===================================")

print(
    f"Testing samples  : {len(test_data)}"
)

print(
    f"Genuine          : {(y_test == 1).sum()}"
)

print(
    f"Suspicious       : {(y_test == 0).sum()}"
)


# ==========================================
# TRAIN RANDOM FOREST
# ==========================================

print("\n===================================")
print("TRAINING RANDOM FOREST")
print("===================================")


model = RandomForestClassifier(

    n_estimators=300,

    max_depth=8,

    min_samples_split=4,

    min_samples_leaf=2,

    random_state=42,

    class_weight="balanced"

)


model.fit(
    X_train,
    y_train
)


# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(
    X_test
)


# ==========================================
# EVALUATION
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n===================================")
print("MODEL RESULTS")
print("===================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Suspicious",
            "Genuine"
        ],
        zero_division=0
    )
)


print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print("\n===================================")
print("FEATURE IMPORTANCE")
print("===================================")


importance = pd.DataFrame({

    "feature":
        feature_columns,

    "importance":
        model.feature_importances_

})


importance = importance.sort_values(
    by="importance",
    ascending=False
)


print(
    importance.to_string(
        index=False
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


joblib.dump(
    {
        "model": model,
        "features": feature_columns
    },
    MODEL_PATH
)


print("\n===================================")
print("MODEL SAVED")
print("===================================")

print(
    f"Model path: {MODEL_PATH}"
)

print(
    "\nTraining completed successfully."
)