import os
import pillow_heif
from PIL import Image
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm

def convert_images(input_dir, output_dir):
    pillow_heif.register_heif_opener()
    files = [f for f in os.listdir(input_dir) if f.lower().endswith('.heic')]
    
    if not files:
        messagebox.showwarning("No Files", "No HEIC files found in the selected folder.")
        return

    for filename in tqdm(files, desc="Converting", unit="photo"):
        try:
            image = Image.open(Path(input_dir) / filename)
            target_path = Path(output_dir) / f"{Path(filename).stem}.jpg"
            image.convert("RGB").save(target_path, "JPEG", quality=90)
        except Exception as e:
            print(f"Error converting {filename}: {e}")

    messagebox.showinfo("Success", f"Converted {len(files)} images successfully!")

def select_input():
    path = filedialog.askdirectory()
    if path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, path)

def select_output():
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)

def start_process():
    in_path = input_entry.get()
    out_path = output_entry.get()
    
    if not in_path or not out_path:
        messagebox.showerror("Error", "Please select both folders.")
        return
        
    convert_images(in_path, out_path)

# --- GUI Setup ---
root = tk.Tk()
root.title("HEIC to JPG Converter")
root.geometry("500x250")

# Input Section
tk.Label(root, text="Source Folder (HEIC):").pack(pady=(20, 0))
input_entry = tk.Entry(root, width=50)
input_entry.pack(side=tk.TOP, padx=10)
tk.Button(root, text="Browse", command=select_input).pack(pady=5)

# Output Section
tk.Label(root, text="Destination Folder (JPG):").pack(pady=(10, 0))
output_entry = tk.Entry(root, width=50)
output_entry.pack(side=tk.TOP, padx=10)
tk.Button(root, text="Browse", command=select_output).pack(pady=5)

# Convert Button
tk.Button(root, text="START CONVERSION", bg="green", fg="white", 
          font=('Helvetica', 10, 'bold'), command=start_process).pack(pady=20)

root.mainloop()