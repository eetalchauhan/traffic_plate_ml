import glob
import os
import shutil

SOURCE_DIR = "plate_quality/good"
OUTPUT_DIR = "labeling_set"

MAX_PER_VIDEO = 40

files = glob.glob(
    os.path.join(SOURCE_DIR, "**", "*.jpg"),
    recursive=True
)

videos = {}

for file in files:
    video = os.path.basename(
        os.path.dirname(file)
    )

    if video not in videos:
        videos[video] = []

    videos[video].append(file)

total = 0

for video, images in videos.items():

    images.sort()

    selected = images[:MAX_PER_VIDEO]

    for image in selected:

        destination = os.path.join(
            OUTPUT_DIR,
            video,
            os.path.basename(image)
        )

        os.makedirs(
            os.path.dirname(destination),
            exist_ok=True
        )

        shutil.copy2(image, destination)
        total += 1

    print(video, "->", len(selected))

print("\nTotal labeling images:", total)
print("Done.")