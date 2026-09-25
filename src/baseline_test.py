from paddleocr import PaddleOCR
from pathlib import Path

ocr = PaddleOCR(lang="en")

for image_path in sorted(Path("../ocr_test").glob("*")):
    if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    result = ocr.predict(str(image_path))

    for res in result:
        text = res.get("rec_texts", [])
        score = res.get("rec_scores", [])
        print(image_path.name, "=>", text, score)
