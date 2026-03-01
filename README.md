# HEIC to JPG Converter

A small Python/Tkinter utility that converts HEIC images to JPEG format.
Users can select one or more `.heic` files as input and specify an output folder.
A progress/status label shows how many images have been converted.

## Features

- Select multiple HEIC files via GUI
- Output converted JPGs to a chosen directory
- Displays conversion status (e.g. "Converted 3 of 10 images")
- Simple, single-window Tkinter interface

## Requirements

- Python 3.8+
- `pillow-heif`, `Pillow`, `tqdm` (for console logging), `tkinter` (standard library)

## Installation

### Using UV (Recommended)

[UV](https://docs.astral.sh/uv/) is a fast Python package installer and resolver.

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or on macOS with Homebrew:
   ```bash
   brew install uv
   ```

2. **Sync dependencies and create virtual environment**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Using venv (Without UV)

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**:
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows** (Command Prompt):
     ```bash
     .venv\Scripts\activate.bat
     ```
   - **Windows** (PowerShell):
     ```bash
     .venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Deactivate the virtual environment** (when done):
   ```bash
   deactivate
   ```

## Usage

```bash
python main.py
```

1. Click **Browse** and choose one or more HEIC files.
2. Pick an output directory by clicking the second **Browse** button.
3. Hit **START CONVERSION** and watch the status label update.

Converted JPGs will appear in the output folder with the same base names.

## Notes

- The app currently only supports file selection (folders are ignored).
- Conversion happens on the main thread; large batches may cause the UI to freeze briefly.

Feel free to extend or modify the utility for additional workflows!