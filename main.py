"""HEIC to JPG converter GUI application using Tkinter."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

import pillow_heif
from PIL import Image

# Global variable to hold the conversion thread
conversion_thread = None

def convert_images(input_input, output_dir, update_status=None, progress_bar=None):
    """Convert HEIC images and optionally update a status label.

    Args:
        input_input: List of HEIC file paths to convert.
        output_dir: Directory to save converted JPG files.
        update_status: Optional Tkinter label widget to update conversion progress.
        progress_bar: Optional Tkinter progressbar widget to show conversion progress.
    """
    pillow_heif.register_heif_opener()

    # determine list of source files
    # input_input is now guaranteed to be a list of files from start_process
    files = input_input

    if not files: # Should ideally be caught before this function is called in a thread
        return 0 # Indicate no files were processed
    total = len(files)

    if progress_bar is not None:
        progress_bar['maximum'] = total
        progress_bar['value'] = 0

    for idx, filepath in enumerate(files):
        # Schedule UI updates on the main thread
        if update_status is not None:
            root.after(0, lambda i=idx+1, t=total: update_status.config(text=f"Converting {i} of {t} images: {Path(filepath).name}"))
        if progress_bar is not None:
            root.after(0, lambda i=idx+1: progress_bar.config(value=i))

        try:
            image = Image.open(filepath)
            target_path = Path(output_dir) / f"{Path(filepath).stem}.jpg"
            image.convert("RGB").save(target_path, "JPEG", quality=90)
        except (OSError, IOError) as e:
            print(f"Error converting {filepath}: {e}")
            # Optionally, we could track failed conversions and report them.

    return total # Return the total number of files processed (assuming all were attempted)

def _threaded_conversion_task(file_list, output_dir, status_label, progress_bar):
    """Wrapper function to run convert_images in a separate thread."""
    converted_count = convert_images(file_list, output_dir, status_label, progress_bar)
    # Schedule the completion handler on the main thread
    root.after(0, lambda: _on_conversion_complete(converted_count))

def _on_conversion_complete(converted_count):
    """Callback function executed on the main thread after conversion completes."""
    convert_btn.config(state=tk.NORMAL)
    status_label.config(text="Done")
    progress_bar['value'] = 0 # Reset progress bar
    messagebox.showinfo("Success", f"Converted {converted_count} images successfully!")

def _check_conversion_thread():
    """Checks if the conversion thread is still running and schedules itself again."""
    global conversion_thread
    if conversion_thread and conversion_thread.is_alive():
        # If the thread is still running, check again after a short delay
        root.after(100, _check_conversion_thread)
    else:
        # If the thread is no longer alive, and it wasn't explicitly joined,
        # ensure the UI is reset in case _on_conversion_complete wasn't called
        # (e.g., due to an unhandled exception in the thread).
        # For robustness, we can ensure the button is re-enabled.
        # If the thread finished normally, _on_conversion_complete would have been called.
        if convert_btn['state'] == tk.DISABLED:
            _on_conversion_complete(0) # Call with 0 or a more appropriate error state


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
    
    # Pre-process input paths to get a clean list of HEIC files
    pillow_heif.register_heif_opener() # Ensure opener is registered for file checks
    
    files_to_convert = []
    if ';' in in_path:
        potential_files = in_path.split(';')
    elif os.path.isdir(in_path): # This case is unlikely with askopenfilenames, but good to handle
        potential_files = [str(p) for p in Path(in_path).iterdir() if p.suffix.lower() == '.heic']
    else:
        potential_files = [in_path]

    files_to_convert = [f for f in potential_files if str(f).lower().endswith('.heic')]

    if not files_to_convert:
        messagebox.showwarning("No Files", "No HEIC files found in the selected input.")
        return

    convert_btn.config(state=tk.DISABLED)
    status_label.config(text="Starting conversion...")
    progress_bar['value'] = 0

    global conversion_thread
    conversion_thread = threading.Thread(target=_threaded_conversion_task,
                                         args=(files_to_convert, out_path, status_label, progress_bar))
    conversion_thread.start()
    _check_conversion_thread() # Start checking the thread status

# --- GUI Setup ---
root = tk.Tk(className='HEICtoJPGConverter')
root.title("HEIC to JPG Converter")

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

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=(0, 20))

root.mainloop()
