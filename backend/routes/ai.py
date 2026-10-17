from flask import Blueprint, request, jsonify
from database import behavior

import pandas as pd
import numpy as np


# ==========================================
# AI BLUEPRINT
# ==========================================

ai_api = Blueprint("ai_api", __name__)


# ==========================================
# CONFIGURATION
# ==========================================

WINDOW_SIZE = 10

LOW_THRESHOLD = 30

MEDIUM_THRESHOLD = 55


# ==========================================
# FEATURE COLUMNS
# ==========================================

FEATURE_COLUMNS = [
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


# ==========================================
# CREATE BEHAVIOR SAMPLE
# ==========================================

def create_behavior_sample(df):

    numeric_columns = [
        "mouse_distance",
        "clicks",
        "scroll_distance",
        "session_duration"
    ]

    for column in numeric_columns:

        if column not in df.columns:
            df[column] = 0

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    if "device" not in df.columns:
        df["device"] = "Desktop"

    mouse_std = df["mouse_distance"].std()

    if pd.isna(mouse_std):
        mouse_std = 0

    sample = {

        "mouse_distance_mean":
            df["mouse_distance"].mean(),

        "mouse_distance_std":
            mouse_std,

        "clicks_mean":
            df["clicks"].mean(),

        "clicks_total":
            df["clicks"].sum(),

        "scroll_distance_mean":
            df["scroll_distance"].mean(),

        "scroll_distance_total":
            df["scroll_distance"].sum(),

        "session_duration":
            df["session_duration"].max(),

        "mouse_activity_rate":
            (df["mouse_distance"] > 0).mean(),

        "click_activity_rate":
            (df["clicks"] > 0).mean(),

        "scroll_activity_rate":
            (df["scroll_distance"] > 0).mean(),

        "device":
            1
            if (
                not df["device"].mode().empty
                and df["device"].mode()[0] == "Mobile"
            )
            else 0
    }

    return sample


# ==========================================
# CREATE BEHAVIOR WINDOWS
# ==========================================

def create_behavior_windows(records):

    if len(records) < WINDOW_SIZE:
        return []

    df = pd.DataFrame(records)

    windows = []

    for start in range(
        0,
        len(df) - WINDOW_SIZE + 1,
        WINDOW_SIZE
    ):

        window = df.iloc[
            start:start + WINDOW_SIZE
        ].copy()

        sample = create_behavior_sample(
            window
        )

        windows.append(sample)

    return windows


# ==========================================
# CALCULATE BASELINE
# ==========================================

def calculate_baseline(samples):

    baseline = {}

    for feature in FEATURE_COLUMNS:

        values = [
            float(
                sample.get(feature, 0)
            )
            for sample in samples
        ]

        values = np.array(values)

        mean = np.mean(values)

        std = np.std(values)

        if std < 0.000001:

            std = max(
                abs(mean) * 0.10,
                1.0
            )

        baseline[feature] = {

            "mean": mean,

            "std": std

        }

    return baseline


# ==========================================
# CALCULATE ANOMALY SCORE
# ==========================================

def calculate_anomaly_score(
    current,
    baseline
):

    weights = {

        "mouse_distance_mean": 1.0,

        "mouse_distance_std": 0.8,

        "clicks_mean": 0.7,

        "clicks_total": 0.7,

        "scroll_distance_mean": 0.8,

        "scroll_distance_total": 0.8,

        "session_duration": 1.4,

        "mouse_activity_rate": 0.9,

        "click_activity_rate": 0.8,

        "scroll_activity_rate": 0.8,

        "device": 0.2

    }

    total_weight = sum(
        weights.values()
    )

    weighted_deviation = 0

    feature_details = {}

    for feature in FEATURE_COLUMNS:

        current_value = float(
            current.get(feature, 0)
        )

        mean = baseline[feature]["mean"]

        std = baseline[feature]["std"]

        # ==================================
        # Z-SCORE
        # ==================================

        z_score = abs(
            current_value - mean
        ) / std

        # ==================================
        # CAP EXTREME VALUES
        # ==================================

        capped_z = min(
            z_score,
            6.0
        )

        # ==================================
        # CONVERT TO FEATURE SCORE
        # ==================================

        feature_score = min(
            (capped_z / 2.0) * 100,
            100
        )

        # ==================================
        # WEIGHTED SCORE
        # ==================================

        weighted_deviation += (
            feature_score *
            weights[feature]
        )

        feature_details[feature] = {

            "current":
                round(
                    current_value,
                    2
                ),

            "baseline_mean":
                round(
                    mean,
                    2
                ),

            "baseline_std":
                round(
                    std,
                    2
                ),

            "z_score":
                round(
                    z_score,
                    2
                ),

            "score":
                round(
                    feature_score,
                    2
                )
        }

    # ==================================
    # FINAL SCORE
    # ==================================

    score = (
        weighted_deviation /
        total_weight
    )

    return score, feature_details


# ==========================================
# REAL BEHAVIOR PREDICTION
# ==========================================

@ai_api.route(
    "/predict-behavior",
    methods=["POST"]
)
def predict_behavior():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message":
                "No data received"

        }), 400

    email = data.get("email")

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email is required"

        }), 400

    # ======================================
    # GET USER BEHAVIOR
    # ======================================

    records = list(

        behavior.find(

            {
                "email": email
            },

            {
                "_id": 0
            }

        ).sort(
            "timestamp",
            1
        )

    )

    if len(records) < 20:

        return jsonify({

            "success": False,

            "message":
                "Not enough behavioral history",

            "records":
                len(records),

            "required":
                20

        }), 400

    # ======================================
    # CREATE WINDOWS
    # ======================================

    windows = create_behavior_windows(
        records
    )

    if len(windows) < 2:

        return jsonify({

            "success": False,

            "message":
                "Not enough behavioral windows",

            "records":
                len(records)

        }), 400

    # ======================================
    # CURRENT WINDOW
    # ======================================

    current_sample = windows[-1]

    # ======================================
    # BASELINE
    # ======================================

    baseline_samples = windows[:-1]

    baseline = calculate_baseline(
        baseline_samples
    )

    # ======================================
    # ANOMALY SCORE
    # ======================================

    anomaly_score, feature_details = (
        calculate_anomaly_score(
            current_sample,
            baseline
        )
    )

    anomaly_score = round(
        anomaly_score,
        2
    )

    # ======================================
    # RISK
    # ======================================

    if anomaly_score < LOW_THRESHOLD:

        risk = "LOW"

        prediction = "Genuine User"

    elif anomaly_score < MEDIUM_THRESHOLD:

        risk = "MEDIUM"

        prediction = "Behavioral Deviation"

    else:

        risk = "HIGH"

        prediction = "Suspicious User"

    # ======================================
    # CONFIDENCE
    # ======================================

    if risk == "LOW":

        confidence = 100 - anomaly_score

    elif risk == "MEDIUM":

        confidence = 50 + abs(
            anomaly_score - 42.5
        )

    else:

        confidence = anomaly_score

    confidence = min(
        max(
            confidence,
            0
        ),
        100
    )

    # ======================================
    # PROBABILITIES
    # ======================================

    suspicious_probability = (
        anomaly_score / 100
    )

    genuine_probability = (
        1 - suspicious_probability
    )

    # ======================================
    # TERMINAL OUTPUT
    # ======================================

    print("\n===================================")
    print(
        "BEHAVIORAL BIOMETRIC ANALYSIS"
    )
    print("===================================")

    print(
        "Email:",
        email
    )

    print(
        "Total records:",
        len(records)
    )

    print(
        "Baseline windows:",
        len(baseline_samples)
    )

    print("\nCurrent behavioral sample:")

    print(
        pd.DataFrame(
            [current_sample]
        ).to_string(
            index=False
        )
    )

    print("\nBehavioral anomaly score:")

    print(
        anomaly_score,
        "%"
    )

    print("\nRisk:")

    print(risk)

    print("\nPrediction:")

    print(prediction)

    print("\nFeature deviations:")

    for feature, details in feature_details.items():

        print(
            f"{feature}: "
            f"current={details['current']} | "
            f"baseline={details['baseline_mean']} | "
            f"z={details['z_score']} | "
            f"score={details['score']}"
        )

    print(
        "===================================\n"
    )

    # ======================================
    # RESPONSE
    # ======================================

    return jsonify({

        "success": True,

        "prediction":
            prediction,

        "confidence":
            round(
                confidence,
                2
            ),

        "genuine_probability":
            round(
                genuine_probability * 100,
                2
            ),

        "suspicious_probability":
            round(
                suspicious_probability * 100,
                2
            ),

        "risk":
            risk,

        "anomaly_score":
            anomaly_score,

        "records_used":
            WINDOW_SIZE,

        "baseline_windows":
            len(baseline_samples),

        "feature_analysis":
            feature_details

    }), 200


# ==========================================
# CONTROLLED ANOMALY TEST
# ==========================================

@ai_api.route(
    "/test-anomaly",
    methods=["POST"]
)
def test_anomaly():

    data = request.get_json()

    if not data or not data.get("email"):

        return jsonify({

            "success": False,

            "message":
                "Email is required"

        }), 400

    email = data.get("email")

    # ======================================
    # GET REAL USER HISTORY
    # ======================================

    records = list(

        behavior.find(

            {
                "email": email
            },

            {
                "_id": 0
            }

        ).sort(
            "timestamp",
            1
        )

    )

    if len(records) < 20:

        return jsonify({

            "success": False,

            "message":
                "Not enough behavioral history",

            "records":
                len(records)

        }), 400

    # ======================================
    # CREATE WINDOWS
    # ======================================

    windows = create_behavior_windows(
        records
    )

    if len(windows) < 2:

        return jsonify({

            "success": False,

            "message":
                "Not enough behavioral windows"

        }), 400

    # ======================================
    # BASELINE
    # ======================================

    baseline_samples = windows[:-1]

    baseline = calculate_baseline(
        baseline_samples
    )

    # ======================================
    # CONTROLLED ABNORMAL SAMPLE
    # ======================================

    abnormal_sample = {

        "mouse_distance_mean":
            baseline[
                "mouse_distance_mean"
            ]["mean"] * 0.02,

        "mouse_distance_std":
            baseline[
                "mouse_distance_std"
            ]["mean"] * 0.02,

        "clicks_mean":
            baseline[
                "clicks_mean"
            ]["mean"] * 0.02,

        "clicks_total":
            0,

        "scroll_distance_mean":
            baseline[
                "scroll_distance_mean"
            ]["mean"] * 0.02,

        "scroll_distance_total":
            0,

        "session_duration":
            baseline[
                "session_duration"
            ]["mean"] * 10,

        "mouse_activity_rate":
            0.0,

        "click_activity_rate":
            0.0,

        "scroll_activity_rate":
            0.0,

        "device":
            1
            if baseline["device"]["mean"] == 0
            else 0
    }

    # ======================================
    # CALCULATE SCORE
    # ======================================

    anomaly_score, feature_details = (
        calculate_anomaly_score(
            abnormal_sample,
            baseline
        )
    )

    anomaly_score = round(
        anomaly_score,
        2
    )

    # ======================================
    # RISK
    # ======================================

    if anomaly_score < LOW_THRESHOLD:

        risk = "LOW"

        prediction = "Genuine User"

    elif anomaly_score < MEDIUM_THRESHOLD:

        risk = "MEDIUM"

        prediction = "Behavioral Deviation"

    else:

        risk = "HIGH"

        prediction = "Suspicious User"

    # ======================================
    # CONFIDENCE
    # ======================================

    confidence = min(
        max(
            anomaly_score,
            0
        ),
        100
    )

    # ======================================
    # TERMINAL OUTPUT
    # ======================================

    print("\n===================================")
    print("CONTROLLED ANOMALY TEST")
    print("===================================")

    print(
        "Email:",
        email
    )

    print("\nAbnormal sample:")

    print(
        pd.DataFrame(
            [abnormal_sample]
        ).to_string(
            index=False
        )
    )

    print("\nAnomaly score:")

    print(
        anomaly_score,
        "%"
    )

    print("\nRisk:")

    print(risk)

    print("\nPrediction:")

    print(prediction)

    print(
        "===================================\n"
    )

    # ======================================
    # RESPONSE
    # ======================================

    return jsonify({

        "success": True,

        "test_mode": True,

        "prediction":
            prediction,

        "confidence":
            round(
                confidence,
                2
            ),

        "risk":
            risk,

        "anomaly_score":
            anomaly_score,

        "feature_analysis":
            feature_details

    }), 200