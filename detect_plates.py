from ultralytics import YOLO
import cv2
import os
import glob

# YOLO pretrained model
model = YOLO("yolo11n.pt")

FRAME_DIR = "frames"
OUTPUT_DIR = "plate_crops"

os.makedirs(OUTPUT_DIR, exist_ok=True)

image_files = glob.glob(
    os.path.join(FRAME_DIR, "**", "*.jpg"),
    recursive=True
)

print(f"Found {len(image_files)} frames")

for image_path in image_files:

    frame = cv2.imread(image_path)

    if frame is None:
        continue

    results = model(frame, verbose=False)

    for result in results:

        boxes = result.boxes

        for i, box in enumerate(boxes):

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            # COCO vehicle classes:
            # 2 = car
            # 3 = motorcycle
            # 5 = bus
            # 7 = truck
            vehicle_classes = [2, 3, 5, 7]

            if class_id not in vehicle_classes:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            vehicle_crop = frame[y1:y2, x1:x2]

            if vehicle_crop.size == 0:
                continue

            video_name = os.path.basename(
                os.path.dirname(image_path)
            )

            frame_name = os.path.splitext(
                os.path.basename(image_path)
            )[0]

            output_folder = os.path.join(
                OUTPUT_DIR,
                video_name
            )

            os.makedirs(
                output_folder,
                exist_ok=True
            )

            output_path = os.path.join(
                output_folder,
                f"{frame_name}_vehicle_{i}.jpg"
            )

            cv2.imwrite(
                output_path,
                vehicle_crop
            )

print("Vehicle detection completed.")