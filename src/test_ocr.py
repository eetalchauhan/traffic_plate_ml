from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")

image_path = "data/crops/13796220_2160_3840_25fps/1/frame_000030.jpg"

result = ocr.predict(image_path)

for res in result:
    print("TEXT:", res.get("rec_texts"))
    print("SCORE:", res.get("rec_scores"))
