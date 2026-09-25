import cv2
import glob
import os
import shutil

SOURCE_DIR = "plate_crops"
OUTPUT_DIR = "plate_quality"

image_files = glob.glob(
    os.path.join(SOURCE_DIR, "**", "*.jpg"),
    recursive=True
)

good = 0
review = 0
blurry = 0

for image_path in image_files:

    image = cv2.imread(image_path, 0)

    if image is None:
        continue

    sharpness = cv2.Laplacian(
        image,
        cv2.CV_64F
    ).var()

    if sharpness >= 500:
        category = "good"
        good += 1

    elif sharpness >= 100:
        category = "review"
        review += 1

    else:
        category = "blurry"
        blurry += 1

    relative_path = os.path.relpath(
        image_path,
        SOURCE_DIR
    )

    destination = os.path.join(
        OUTPUT_DIR,
        category,
        relative_path
    )

    os.makedirs(
        os.path.dirname(destination),
        exist_ok=True
    )

    shutil.copy2(image_path, destination)

print("Sorting complete!")
print("Good:", good)
print("Review:", review)
print("Blurry:", blurry)
print("Total:", good + review + blurry)