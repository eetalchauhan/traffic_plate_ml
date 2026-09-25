import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import os

CSV_FILE = "labeling_manifest.csv"

# Load manifest
with open(CSV_FILE, "r", newline="") as f:
    rows = list(csv.DictReader(f))

index = 0

# -----------------------------
# Save current row
# -----------------------------

def save_current():
    global index

    rows[index]["true_plate_text"] = plate_entry.get().strip().upper()

    tags = []

    if day_var.get():
        tags.append("day")
    if night_var.get():
        tags.append("night")
    if rain_var.get():
        tags.append("rain")
    if clear_var.get():
        tags.append("clear")
    if angled_var.get():
        tags.append("angled")
    if straight_var.get():
        tags.append("straight")
    if blur_var.get():
        tags.append("motion_blur")
    if two_line_var.get():
        tags.append("two_line")

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


# -----------------------------
# Load image
# -----------------------------

def load_image():
    global photo

    path = rows[index]["image_path"]

    image = Image.open(path)

    # Keep image large enough to inspect
    image.thumbnail((800, 500))

    photo = ImageTk.PhotoImage(image)

    image_label.config(image=photo)

    counter_label.config(
        text=f"Image {index + 1} / {len(rows)}"
    )

    path_label.config(
        text=os.path.basename(path)
    )

    # Clear fields
    plate_entry.delete(0, tk.END)

    for var in [
        day_var,
        night_var,
        rain_var,
        clear_var,
        angled_var,
        straight_var,
        blur_var,
        two_line_var
    ]:
        var.set(False)

    # Restore existing values if already labeled
    existing_text = rows[index]["true_plate_text"]

    if existing_text:
        plate_entry.insert(0, existing_text)

    existing_tags = rows[index]["condition_tags"]

    if existing_tags:
        tags = existing_tags.split(",")

        day_var.set("day" in tags)
        night_var.set("night" in tags)
        rain_var.set("rain" in tags)
        clear_var.set("clear" in tags)
        angled_var.set("angled" in tags)
        straight_var.set("straight" in tags)
        blur_var.set("motion_blur" in tags)
        two_line_var.set("two_line" in tags)


# -----------------------------
# Next image
# -----------------------------

def next_image():
    global index

    save_current()

    if index < len(rows) - 1:
        index += 1
        load_image()
    else:
        messagebox.showinfo(
            "Finished",
            "You have reached the end of the dataset!"
        )


# -----------------------------
# Previous image
# -----------------------------

def previous_image():
    global index

    save_current()

    if index > 0:
        index -= 1
        load_image()


# -----------------------------
# Skip unreadable
# -----------------------------

def skip_image():
    plate_entry.delete(0, tk.END)
    save_current()
    next_image()


# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()
root.title("License Plate Labeling")
root.geometry("950x750")

counter_label = tk.Label(
    root,
    text="",
    font=("Arial", 16)
)

counter_label.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

path_label = tk.Label(
    root,
    text="",
    font=("Arial", 10)
)

path_label.pack(pady=5)

plate_frame = tk.Frame(root)
plate_frame.pack(pady=10)

tk.Label(
    plate_frame,
    text="Plate Number:",
    font=("Arial", 14)
).pack(side=tk.LEFT)

plate_entry = tk.Entry(
    plate_frame,
    width=25,
    font=("Arial", 16)
)

plate_entry.pack(side=tk.LEFT, padx=10)

# Conditions

condition_frame = tk.LabelFrame(
    root,
    text="Conditions",
    padx=10,
    pady=10
)

condition_frame.pack(pady=10)

day_var = tk.BooleanVar()
night_var = tk.BooleanVar()
rain_var = tk.BooleanVar()
clear_var = tk.BooleanVar()
angled_var = tk.BooleanVar()
straight_var = tk.BooleanVar()
blur_var = tk.BooleanVar()
two_line_var = tk.BooleanVar()

conditions = [
    ("Day", day_var),
    ("Night", night_var),
    ("Rain", rain_var),
    ("Clear", clear_var),
    ("Angled", angled_var),
    ("Straight", straight_var),
    ("Motion Blur", blur_var),
    ("Two Line", two_line_var)
]

for name, variable in conditions:
    tk.Checkbutton(
        condition_frame,
        text=name,
        variable=variable
    ).pack(side=tk.LEFT, padx=5)

# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Previous",
    command=previous_image,
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="SKIP / UNREADABLE",
    command=skip_image,
    width=18
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="SAVE + NEXT",
    command=next_image,
    width=15
).pack(side=tk.LEFT, padx=5)

load_image()

root.mainloop()