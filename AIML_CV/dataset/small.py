from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "dataset" / "generated_landmarks" / "generated_landmarks.csv"

df = pd.read_csv(csv_path)

print(df.shape)
print(df["label"].value_counts())
print(df.isnull().sum().sum())