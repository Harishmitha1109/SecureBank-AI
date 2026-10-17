import os
import pandas as pd
from pymongo import MongoClient


# ==========================================
# MongoDB Connection
# ==========================================

client = MongoClient("mongodb://localhost:27017/")

db = client["securebank_ai"]

behavior_collection = db["behavior"]


# ==========================================
# User for Training Data
# ==========================================

EMAIL = "test@gmail.com"


# ==========================================
# Get Behavioral Records
# ==========================================

records = list(
    behavior_collection.find(
        {"email": EMAIL},
        {"_id": 0}
    ).sort("timestamp", 1)
)


print(f"Total behavioral records found: {len(records)}")


if len(records) < 10:
    print("Not enough behavioral data.")
    print("Collect more data from the application.")
    exit()


# ==========================================
# Convert to DataFrame
# ==========================================

df = pd.DataFrame(records)


# Make sure numeric columns are numeric

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


# ==========================================
# Create Behavioral Samples
# ==========================================

# Each 10 records = one behavioral sample

samples = []

window_size = 10


for start in range(
    0,
    len(df) - window_size + 1,
    window_size
):

    window = df.iloc[
        start:start + window_size
    ]

    sample = {

        # Mouse behavior
        "mouse_distance_mean":
            window["mouse_distance"].mean(),

        "mouse_distance_std":
            window["mouse_distance"].std(),

        # Clicking behavior
        "clicks_mean":
            window["clicks"].mean(),

        "clicks_total":
            window["clicks"].sum(),

        # Scrolling behavior
        "scroll_distance_mean":
            window["scroll_distance"].mean(),

        "scroll_distance_total":
            window["scroll_distance"].sum(),

        # Session behavior
        "session_duration":
            window["session_duration"].max(),

        # Activity rates
        "mouse_activity_rate":
            (window["mouse_distance"] > 0).mean(),

        "click_activity_rate":
            (window["clicks"] > 0).mean(),

        "scroll_activity_rate":
            (window["scroll_distance"] > 0).mean(),

        # Device
        "device":
            window["device"].mode()[0]
            if not window["device"].mode().empty
            else "Desktop",

        # Genuine user label
        "label": 1
    }

    samples.append(sample)


# ==========================================
# Create Dataset
# ==========================================

dataset = pd.DataFrame(samples)


# Replace missing standard deviation

dataset["mouse_distance_std"] = (
    dataset["mouse_distance_std"]
    .fillna(0)
)


# Convert device to numeric

dataset["device"] = dataset["device"].map({

    "Desktop": 0,
    "Mobile": 1

}).fillna(0)


# ==========================================
# Save Dataset
# ==========================================

os.makedirs(
    "../dataset",
    exist_ok=True
)

output_path = "../dataset/behavior_dataset.csv"

dataset.to_csv(
    output_path,
    index=False
)


# ==========================================
# Results
# ==========================================

print("\n===================================")
print("Behavior Dataset Created")
print("===================================")

print(
    f"Records used      : {len(df)}"
)

print(
    f"ML samples created: {len(dataset)}"
)

print(
    f"Features           : {len(dataset.columns) - 1}"
)

print(
    f"Saved to           : {output_path}"
)

print("\nDataset preview:")
print(dataset.head())