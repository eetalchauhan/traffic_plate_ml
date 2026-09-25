import cv2
import os
import glob

VIDEO_DIR = "videos"
OUTPUT_DIR = "frames"

os.makedirs(OUTPUT_DIR, exist_ok=True)

FPS_TO_EXTRACT = 2

video_files = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))

for video_path in video_files:

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    output_folder = os.path.join(OUTPUT_DIR, video_name)
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        print(f"Could not read FPS: {video_name}")
        continue

    frame_interval = max(1, int(fps / FPS_TO_EXTRACT))

    frame_number = 0
    saved = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_number % frame_interval == 0:

            filename = os.path.join(
                output_folder,
                f"frame_{frame_number:06d}.jpg"
            )

            cv2.imwrite(filename, frame)
            saved += 1

        frame_number += 1

    cap.release()

    print(f"{video_name}: {saved} frames extracted")

print("Done.")