from pathlib import Path
import pandas as pd

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OLD_DATASET = BASE_DIR / "dataset" / "asl_landmarks_final.csv"

NEW_DATASET = BASE_DIR / "dataset" / "generated_landmarks" / "generated_landmarks.csv"

OUTPUT_DATASET = BASE_DIR / "dataset" / "merged_landmarks.csv"

# =====================================================
# LOAD DATASETS
# =====================================================

old_df = pd.read_csv(OLD_DATASET)

new_df = pd.read_csv(NEW_DATASET)

print("Old Dataset :", old_df.shape)

print("New Dataset :", new_df.shape)

# =====================================================
# MERGE
# =====================================================

merged_df = pd.concat(
    [old_df, new_df],
    ignore_index=True
)

print("Merged Dataset :", merged_df.shape)

# =====================================================
# SAVE
# =====================================================

merged_df.to_csv(
    OUTPUT_DATASET,
    index=False
)

print("\nMerged dataset saved successfully!")

print(OUTPUT_DATASET)