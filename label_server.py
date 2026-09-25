from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import csv
import json
import os

CSV_FILE = "labeling_manifest.csv"

with open(CSV_FILE, "r", newline="") as f:
    rows = list(csv.DictReader(f))

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/image/"):
            index = int(self.path.split("/")[-1])
            path = rows[index]["image_path"]

            try:
                with open(path, "rb") as f:
                    data = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            except Exception:
                self.send_error(404)

            return

        index = 0

        if "?" in self.path:
            try:
                index = int(parse_qs(self.path.split("?")[1]).get("i", [0])[0])
            except:
                index = 0

        index = max(0, min(index, len(rows) - 1))
        row = rows[index]

        tags = set(row["condition_tags"].split(",")) if row["condition_tags"] else set()

        def checked(tag):
            return "checked" if tag in tags else ""

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>License Plate Labeling</title>

<style>
body {{
    font-family: Arial;
    text-align: center;
    background: #f5f5f5;
}}

img {{
    max-width: 850px;
    max-height: 500px;
    border: 2px solid #333;
    margin: 20px;
}}

input[type=text] {{
    width: 300px;
    padding: 12px;
    font-size: 20px;
}}

button {{
    padding: 12px 20px;
    margin: 8px;
    font-size: 16px;
}}

label {{
    margin: 8px;
    display: inline-block;
}}
</style>
</head>

<body>

<h2>License Plate Labeling</h2>

<h3>Image {index + 1} / {len(rows)}</h3>

<img src="/image/{index}">

<p><b>{os.path.basename(row["image_path"])}</b></p>

<form method="POST">

<input type="hidden" name="index" value="{index}">

<br>

<input
    type="text"
    name="plate"
    value="{row["true_plate_text"]}"
    placeholder="Enter plate number"
    autofocus
>

<h3>Conditions</h3>

<label>
<input type="checkbox" name="day" {checked("day")}>
Day
</label>

<label>
<input type="checkbox" name="night" {checked("night")}>
Night
</label>

<label>
<input type="checkbox" name="rain" {checked("rain")}>
Rain
</label>

<label>
<input type="checkbox" name="clear" {checked("clear")}>
Clear
</label>

<label>
<input type="checkbox" name="angled" {checked("angled")}>
Angled
</label>

<label>
<input type="checkbox" name="straight" {checked("straight")}>
Straight
</label>

<label>
<input type="checkbox" name="motion_blur" {checked("motion_blur")}>
Motion Blur
</label>

<label>
<input type="checkbox" name="two_line" {checked("two_line")}>
Two Line
</label>

<br>

<button type="submit" name="action" value="previous">
Previous
</button>

<button type="submit" name="action" value="skip">
SKIP / UNREADABLE
</button>

<button type="submit" name="action" value="next">
SAVE + NEXT
</button>

</form>

</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        form = parse_qs(data)

        index = int(form.get("index", [0])[0])

        plate = form.get("plate", [""])[0].strip().upper()

        tags = []

        for tag in [
            "day",
            "night",
            "rain",
            "clear",
            "angled",
            "straight",
            "motion_blur",
            "two_line"
        ]:
            if tag in form:
                tags.append(tag)

        rows[index]["true_plate_text"] = plate
        rows[index]["condition_tags"] = ",".join(tags)

        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "image_path",
                    "video_file",
                    "true_plate_text",
                    "condition_tags"
                ]
            )
            writer.writeheader()
            writer.writerows(rows)

        action = form.get("action", ["next"])[0]

        if action == "next":
            new_index = min(index + 1, len(rows) - 1)

        elif action == "previous":
            new_index = max(index - 1, 0)

        else:
            new_index = min(index + 1, len(rows) - 1)

        self.send_response(303)
        self.send_header("Location", f"/?i={new_index}")
        self.end_headers()


server = HTTPServer(("localhost", 8000), Handler)

print("Labeling tool running!")
print("Open: http://localhost:8000")
print("Press Ctrl+C to stop.")

server.serve_forever()