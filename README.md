# Traffic Plate ML

Machine learning pipeline for license-plate detection, OCR, and multi-frame voting.

## Pipeline

Video / Frames → Plate Detection → Plate Cropping → Quality Filtering → PaddleOCR → Confidence Filtering → Plate Format Filtering → Multi-Frame Voting → Final Plate

## Work Completed

- Prepared and filtered license-plate data.
- Created OCR train/test datasets.
- Fine-tuned a PP-OCRv6 Tiny recognition model using PaddleOCR.
- Evaluated baseline and fine-tuned OCR performance.
- Integrated OCR with video plate crops.
- Processed 1,311 quality-filtered plate crops.
- Applied confidence and Indian license-plate format filtering.
- Implemented multi-frame voting.

## OCR Evaluation

| Model | Exact Match | CER |
|---|---:|---:|
| Baseline OCR | 60.00% (9/15) | 12.24% |
| Fine-tuned OCR | 53.33% (8/15) | 18.37% |

The evaluation used a small 15-image test set. On this test set, the baseline performed better than the fine-tuned model.

## Video OCR Demonstration

For one processed video, multi-frame voting produced:

- CH01CS6905 — 4 votes
- CH01CH9193 — 2 votes
- PB10JR9976 — 2 votes
- CH01BB9805 — 2 votes
- PB54H0997 — 1 vote
- PE24H0997 — 1 vote

**Final voted plate: CH01CS6905**

## Project Structure

```text
traffic-ml/
├── src/
├── create_labeling_set.py
├── create_manifest.py
├── detect_license_plates.py
├── detect_plates.py
├── extract_frames.py
├── label_plates.py
├── label_server.py
├── sort_plate_quality.py
├── split_ocr_dataset.py
├── requirements.txt
├── results/
└── README.md
```

## Notes

Large datasets, videos, generated crops, model weights, and the PaddleOCR source tree are excluded from Git using .gitignore.
