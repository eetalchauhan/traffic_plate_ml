from ultralytics import YOLO
import cv2
import os
import glob

MODEL_PATH = "models/license_plate.pt"
FRAME_DIR = "frames"
OUTPUT_DIR = "plate_crops"

os.makedirs(OUTPUT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

image_files = glob.glob(
    os.path.join(FRAME_DIR, "**", "*.jpg"),
    recursive=True
)

print(f"Found {len(image_files)} frames")

total_plates = 0

for image_path in image_files:

    image = cv2.imread(image_path)

    if image is None:
        continue

    results = model.predict(
        image,
        conf=0.30,
        verbose=False
    )

    video_name = os.path.basename(
        os.path.dirname(image_path)
    )

    output_folder = os.path.join(
        OUTPUT_DIR,
        video_name
    )

    os.makedirs(output_folder, exist_ok=True)

    frame_name = os.path.splitext(
        os.path.basename(image_path)
    )[0]

    plate_number = 0

    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            plate = image[y1:y2, x1:x2]

            if plate.size == 0:
                continue

            output_path = os.path.join(
                output_folder,
                f"{frame_name}_plate_{plate_number}.jpg"
            )

            cv2.imwrite(output_path, plate)

            plate_number += 1
            total_plates += 1

print(f"Total plate crops: {total_plates}")
print("Done.")