import os
import random
import shutil

SOURCE = "ocr_dataset"
TRAIN = "ocr_train"
TEST = "ocr_test"

os.makedirs(TRAIN, exist_ok=True)
os.makedirs(TEST, exist_ok=True)

files = [
    f for f in os.listdir(SOURCE)
    if f.endswith(".jpg")
]

# Group images by plate number
groups = {}

for f in files:
    plate = f.rsplit("_", 1)[0]

    if plate not in groups:
        groups[plate] = []

    groups[plate].append(f)

# Shuffle unique plates
plates = list(groups.keys())
random.seed(42)
random.shuffle(plates)

# 80% plates for training, 20% for testing
split = int(len(plates) * 0.8)

train_plates = set(plates[:split])
test_plates = set(plates[split:])

for plate, images in groups.items():

    destination = TRAIN if plate in train_plates else TEST

    for image in images:
        shutil.copy2(
            os.path.join(SOURCE, image),
            os.path.join(destination, image)
        )

print("Training plates:", len(train_plates))
print("Testing plates:", len(test_plates))
print("Training images:", sum(len(groups[p]) for p in train_plates))
print("Testing images:", sum(len(groups[p]) for p in test_plates))