from paddleocr import PaddleOCR
from pathlib import Path
import csv

ocr = PaddleOCR(lang="en")

crop_dir = Path("data/crops")
output_file = Path("data/ocr_predictions.csv")

rows = []

for image_path in crop_dir.rglob("*.jpg"):
    try:
        result = ocr.predict(str(image_path))

        text = ""
        confidence = 0.0

        for res in result:
            texts = res.get("rec_texts", [])
            scores = res.get("rec_scores", [])

            if texts:
                text = str(texts[0]).strip()
                confidence = float(scores[0]) if scores else 0.0

        rows.append([
            str(image_path),
            text,
            confidence
        ])

        print(f"{image_path.name}: {text} ({confidence:.2f})")

    except Exception as e:
        print(f"ERROR: {image_path} -> {e}")

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["image_path", "predicted_text", "confidence"])
    writer.writerows(rows)

print(f"\nDone! Saved {len(rows)} predictions to {output_file}")
