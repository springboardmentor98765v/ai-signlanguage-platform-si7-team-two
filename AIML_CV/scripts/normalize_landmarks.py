from pathlib import Path
import pandas as pd

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "dataset" / "merged_landmarks.csv"

OUTPUT_FILE = BASE_DIR / "dataset" / "merged_landmarks_normalized.csv"

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)

# =====================================================
# NORMALIZE USING WRIST (LANDMARK 0)
# =====================================================

for i in range(1, 21):

    df[f"x{i}"] = df[f"x{i}"] - df["x0"]

    df[f"y{i}"] = df[f"y{i}"] - df["y0"]

    df[f"z{i}"] = df[f"z{i}"] - df["z0"]

# Set wrist as origin

df["x0"] = 0.0
df["y0"] = 0.0
df["z0"] = 0.0

# =====================================================
# SAVE
# =====================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\nNormalization Complete")

print("Saved to:")

print(OUTPUT_FILE)

print("\nDataset Shape:")

print(df.shape)