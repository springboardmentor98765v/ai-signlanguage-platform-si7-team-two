import os
import csv

# Get the absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one folder up (AIML_CV)
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Create dataset path
DATASET_PATH = os.path.join(PROJECT_DIR, "dataset", "sign_dataset.csv")
def save_sample(features, label):
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    row = list(features) + [label]

    file_exists = os.path.isfile(DATASET_PATH)
    

    print("Current Working Directory:", os.getcwd())
    print("Dataset Path:", os.path.abspath(DATASET_PATH))
    with open(DATASET_PATH, mode="a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            header = []

            for i in range(21):
                header.extend([f"x{i}", f"y{i}", f"z{i}"])

            header.append("label")

            writer.writerow(header)

        writer.writerow(row)