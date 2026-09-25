import pandas as pd
from pathlib import Path

INPUT = Path("data/ocr_predictions.csv")
OUTPUT = Path("results/baseline_track_summary.csv")

df = pd.read_csv(INPUT)

# Extract video and track from image path
parts = df["image_path"].str.split("/")

df["video"] = parts.str[-3]
df["track_id"] = parts.str[-2]

# Normalize text
df["predicted_text"] = (
    df["predicted_text"]
    .fillna("")
    .astype(str)
    .str.upper()
    .str.replace(r"[^A-Z0-9]", "", regex=True)
)

# Keep predictions at or above our current 0.60 threshold
df["usable"] = (
    (df["confidence"] >= 0.60)
    & (df["predicted_text"] != "")
)

summary = (
    df.groupby(["video", "track_id"])
    .agg(
        total_frames=("image_path", "count"),
        usable_predictions=("usable", "sum"),
        best_confidence=("confidence", "max"),
    )
    .reset_index()
)

# Most common usable prediction for each track
usable = df[df["usable"]].copy()

if not usable.empty:
    votes = (
        usable.groupby(["video", "track_id", "predicted_text"])
        .agg(
            count=("predicted_text", "size"),
            max_confidence=("confidence", "max"),
            confidence_sum=("confidence", "sum"),
        )
        .reset_index()
    )

    votes = votes.sort_values(
        ["video", "track_id", "count", "confidence_sum"],
        ascending=[True, True, False, False],
    )

    best = votes.drop_duplicates(["video", "track_id"])

    summary = summary.merge(
        best[
            [
                "video",
                "track_id",
                "predicted_text",
                "count",
                "max_confidence",
            ]
        ],
        on=["video", "track_id"],
        how="left",
    )

summary.to_csv(OUTPUT, index=False)

print("Saved:", OUTPUT)
print("Tracks analyzed:", len(summary))
print()
print(summary.to_string(index=False))
