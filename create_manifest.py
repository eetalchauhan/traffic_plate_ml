import csv
import glob
import os

files = glob.glob(
    "labeling_set/**/*.jpg",
    recursive=True
)

with open("labeling_manifest.csv", "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "image_path",
        "video_file",
        "true_plate_text",
        "condition_tags"
    ])

    for image in sorted(files):

        video = os.path.basename(
            os.path.dirname(image)
        )

        writer.writerow([
            image,
            video,
            "",
            ""
        ])

print("Manifest created!")
print("Images:", len(files))
print("File: labeling_manifest.csv")