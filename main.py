"""HEIC to JPG converter GUI application using Tkinter."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import pillow_heif
from PIL import Image


def convert_images(input_input, output_dir, update_status=None):
    """Convert HEIC images and optionally update a status label.

    Args:
        input_input: File path(s) or list of HEIC files to convert.
        output_dir: Directory to save converted JPG files.
        update_status: Optional Tkinter label widget to update conversion progress.
    """
    pillow_heif.register_heif_opener()

    # determine list of source files
    if isinstance(input_input, (list, tuple)):
        files = list(input_input)
    else:
        if os.path.isdir(input_input):
            files = [str(p) for p in Path(input_input).iterdir() if p.suffix.lower() == '.heic']
        else:
            files = input_input.split(';') if ';' in input_input else [input_input]

    files = [f for f in files if str(f).lower().endswith('.heic')]

    if not files:
        messagebox.showwarning("No Files", "No HEIC files found in the selected input.")
        return

    total = len(files)

    for idx, filepath in enumerate(files):
        try:
            image = Image.open(filepath)
            target_path = Path(output_dir) / f"{Path(filepath).stem}.jpg"
            image.convert("RGB").save(target_path, "JPEG", quality=90)
        except (OSError, IOError) as e:
            print(f"Error converting {filepath}: {e}")

        # update status label if provided
        if update_status is not None:
            update_status.config(text=f"Converted {idx+1} of {total} images")
            root.update_idletasks()

    messagebox.showinfo("Success", f"Converted {total} images successfully!")


def select_input():
    """Open file dialog to select HEIC files for conversion."""
    # prompt for one or more HEIC files only
    paths = filedialog.askopenfilenames(
        title="Select HEIC files",
        filetypes=[("HEIC files", "*.heic")]
    )
    if paths:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, ';'.join(paths))


def select_output():
    """Open directory dialog to select output folder for JPGs."""
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)


def start_process():
    """Validate inputs and start the image conversion process."""
    in_path = input_entry.get()
    out_path = output_entry.get()

    if not in_path or not out_path:
        messagebox.showerror("Error", "Please select both input and output.")
        return

    convert_btn.config(state=tk.DISABLED)
    status_label.config(text="Starting...")
    convert_images(in_path, out_path, status_label)
    convert_btn.config(state=tk.NORMAL)
    status_label.config(text="Done")

# --- GUI Setup ---
root = tk.Tk()
root.title("HEIC to JPG Converter")
# height can be smaller now that bar is gone
root.geometry("550x340")
# allow user to resize if desired
root.resizable(True, True)

# Input Section
tk.Label(root, text="Source (HEIC files):").pack(pady=(20, 0))
input_entry = tk.Entry(root, width=50)
input_entry.pack(side=tk.TOP, padx=10)
tk.Button(root, text="Browse", command=select_input).pack(pady=5)

# Output Section
tk.Label(root, text="Destination Folder (JPG):").pack(pady=(10, 0))
output_entry = tk.Entry(root, width=50)
output_entry.pack(side=tk.TOP, padx=10)
tk.Button(root, text="Browse", command=select_output).pack(pady=5)

# Convert Button
convert_btn = tk.Button(root, text="START CONVERSION", bg="lightblue", fg="black",
          font=('Helvetica', 14, 'bold'), width=25, height=2, command=start_process)
convert_btn.pack(pady=20)

# status label below the convert button
status_label = tk.Label(root, text="", font=('Helvetica', 12))
status_label.pack(pady=(0,20))

root.mainloop()
