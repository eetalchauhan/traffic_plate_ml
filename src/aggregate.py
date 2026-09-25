import pandas as pd
import re
from pathlib import Path

INPUT = Path("data/ocr_predictions.csv")
OUTPUT = Path("results/final_track_predictions.csv")

CONFIDENCE_THRESHOLD = 0.60


def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).upper()
    text = re.sub(r"[^A-Z0-9]", "", text)

    return text


df = pd.read_csv(INPUT)

# Extract video and track ID
parts = df["image_path"].str.split("/")

df["video"] = parts.str[-3]
df["track_id"] = parts.str[-2]

# Normalize OCR text
df["text"] = df["predicted_text"].apply(normalize)

# Keep only useful predictions
df = df[
    (df["confidence"] >= CONFIDENCE_THRESHOLD)
    & (df["text"] != "")
].copy()

results = []

for (video, track), group in df.groupby(["video", "track_id"]):

    # Score each candidate using confidence-weighted voting
    scores = (
        group.groupby("text")["confidence"]
        .agg(["sum", "count", "max"])
        .reset_index()
    )

    scores["weighted_score"] = (
        scores["sum"] * 0.7
        + scores["count"] * 0.2
        + scores["max"] * 0.1
    )

    best = scores.sort_values(
        "weighted_score",
        ascending=False
    ).iloc[0]

    results.append({
        "video": video,
        "track_id": track,
        "final_prediction": best["text"],
        "prediction_count": int(best["count"]),
        "confidence_sum": round(best["sum"], 4),
        "best_confidence": round(best["max"], 4),
        "weighted_score": round(best["weighted_score"], 4),
    })


result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    ["video", "track_id"]
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

result_df.to_csv(
    OUTPUT,
    index=False
)

print("Saved:", OUTPUT)
print("Tracks with usable OCR:", len(result_df))
print()

print(result_df.to_string(index=False))
