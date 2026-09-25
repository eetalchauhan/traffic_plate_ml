from pathlib import Path
import re

def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        curr = [i]
        for j, y in enumerate(b, 1):
            curr.append(min(
                curr[-1] + 1,
                prev[j] + 1,
                prev[j-1] + (x != y)
            ))
        prev = curr
    return prev[-1]

gt = {}
for line in Path("../rec_gt_test.txt").read_text().splitlines():
    path, text = line.split("\t")
    gt[Path(path).stem] = text.strip()

lines = Path("../results/fine_tuned_predictions.txt").read_text().splitlines()
preds = {}

for i, line in enumerate(lines):
    if "infer_img:" in line and i + 1 < len(lines):
        path = re.search(r"infer_img:\s+(.+)", line).group(1)
        match = re.search(r"result:\s*(.*?)\s+[0-9.]+$", lines[i+1])
        if match:
            preds[Path(path).stem] = match.group(1).strip()

errors = sum(edit_distance(preds.get(k, ""), v) for k, v in gt.items())
characters = sum(len(v) for v in gt.values())

print("Character errors:", errors)
print("Total characters:", characters)
print("CER:", round(errors / characters * 100, 2), "%")
