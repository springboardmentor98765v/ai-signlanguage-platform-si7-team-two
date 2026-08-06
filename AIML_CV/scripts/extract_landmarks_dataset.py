import os
import sys
import csv
import random
from pathlib import Path

import cv2
import mediapipe as mp
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.feature_extractor import extract_features

DATASET_DIR = BASE_DIR / "dataset" / "asl_alphabet_train"
OUTPUT_DIR = BASE_DIR / "dataset" / "generated_landmarks"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_CSV = OUTPUT_DIR / "generated_landmarks.csv"
FAILED_LOG = LOG_DIR / "failed_images.txt"
PROCESSED_LOG = LOG_DIR / "processed_images.txt"

MAX_IMAGES_PER_CLASS = 1000
RANDOM_SEED = 42
BUFFER_SIZE = 500

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True,max_num_hands=1,min_detection_confidence=0.5)

header=[]
for i in range(21):
    header.extend([f'x{i}',f'y{i}',f'z{i}'])
header.append('label')

if not OUTPUT_CSV.exists():
    with open(OUTPUT_CSV,'w',newline='') as f:
        csv.writer(f).writerow(header)

def load_processed():
    if not PROCESSED_LOG.exists():
        return set()
    with open(PROCESSED_LOG) as f:
        return set(line.strip() for line in f)

def save_processed(path):
    with open(PROCESSED_LOG,'a') as f:
        f.write(path+'\n')

def log_failed(path):
    with open(FAILED_LOG,'a') as f:
        f.write(path+'\n')

def get_images(folder):
    imgs=[i for i in os.listdir(folder) if i.lower().endswith(('.jpg','.jpeg','.png','.bmp'))]
    imgs.sort()
    random.Random(RANDOM_SEED).shuffle(imgs)
    return imgs

def process(path):
    img=cv2.imread(str(path))
    if img is None:
        return None
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hands.process(rgb)
    if not res.multi_hand_landmarks:
        return None
    return extract_features(res.multi_hand_landmarks[0])

def generate():
    processed=load_processed()
    total_saved=0
    total_failed=0

    for folder in sorted([f for f in DATASET_DIR.iterdir() if f.is_dir()]):
        label=folder.name
        images=get_images(folder)
        saved=sum(1 for i in images if str(folder/i) in processed)

        if saved>=MAX_IMAGES_PER_CLASS:
            print(f'Skipping {label}')
            continue

        print(f'Processing {label}')
        p=tqdm(total=MAX_IMAGES_PER_CLASS,initial=saved,desc=label)
        buffer=[]

        with open(OUTPUT_CSV,'a',newline='') as csvfile:
            writer=csv.writer(csvfile)

            for image in images:
                if saved>=MAX_IMAGES_PER_CLASS:
                    break
                path=folder/image
                if str(path) in processed:
                    continue
                feat=process(path)
                if feat is None:
                    total_failed+=1
                    log_failed(str(path))
                    continue
                row=list(feat)
                row.append(label)
                buffer.append(row)
                processed.add(str(path))
                save_processed(str(path))
                saved+=1
                total_saved+=1
                p.update(1)
                if len(buffer)>=BUFFER_SIZE:
                    writer.writerows(buffer)
                    buffer.clear()
            if buffer:
                writer.writerows(buffer)
        p.close()
        print(f'{label}: {saved} samples')

    print('Done')
    print('Saved:',total_saved)
    print('Failed:',total_failed)

if __name__=='__main__':
    generate()