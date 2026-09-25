import pandas as pd
from PIL import Image, ImageDraw
from pathlib import Path
import math

CSV = Path("results/ocr_review.csv")
OUTPUT = Path("results/ocr_review_sheet.jpg")

df = pd.read_csv(CSV)

# 8 images per row
COLS = 4
CELL_W = 350
CELL_H = 300

rows = math.ceil(len(df) / COLS)

sheet = Image.new(
    "RGB",
    (COLS * CELL_W, rows * CELL_H),
    "white"
)

draw = ImageDraw.Draw(sheet)

for i, row in df.reset_index(drop=True).iterrows():

    path = Path(row["image_path"])

    try:
        img = Image.open(path).convert("RGB")
        img.thumbnail((330, 230))

        x = (i % COLS) * CELL_W
        y = (i // COLS) * CELL_H

        # Center image
        ix = x + (CELL_W - img.width) // 2
        iy = y + 10

        sheet.paste(img, (ix, iy))

        text = f'{row["predicted_text"]}  |  {row["confidence"]:.2f}'

        draw.text(
            (x + 10, y + 250),
            text,
            fill="black"
        )

    except Exception as e:
        print("Could not open:", path, e)

sheet.save(OUTPUT, quality=95)

print("Saved:", OUTPUT)
