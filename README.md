# Media Deduplication Tool

## Overview

The Media Deduplication Tool is a Python application designed to identify and eliminate duplicate images and videos from specified directories on your disk. It utilizes perceptual hashing to compare files and create a report of similar files. This tool is particularly useful for organizing large media libraries and freeing up disk space.

## Features

- **Deduplication**: Detects and removes duplicate images and videos based on perceptual hashing.
- **Error Handling**: Optionally includes files that could not be processed (e.g., corrupt files).
- **Batch Processing**: Processes multiple directories concurrently for faster performance.
- **CSV Reporting**: Generates a CSV report of similar files for future reference.

## Supported File Types

The Media Deduplication Tool supports the following file extensions:

- **Images**:

  - `.bmp`
  - `.jpg`
  - `.jpeg`
  - `.png`
  - `.gif`
- **Videos**:

  - `.mp4`
  - `.mov`

You can also specify additional file extensions (without hash calculation) at runtime.

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `opencv-python`
  - `Pillow`
  - `imagehash`
  - `tqdm`

You can install the required packages using pip:

```bash
pip install opencv-python Pillow imagehash tqdm
```

## How to Use

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/MediaDeduplicationTool.git
   cd MediaDeduplicationTool
   ```
2. **Run the script**:

   ```bash
   python deduplicate.py
   ```
3. **Input Parameters**:

   - Enter the disk locations to check (separated by commas).
   - Enter the output folder path where unique files will be saved.
   - Optionally include videos with errors in the copy list.
   - Optionally specify file extensions that should not undergo hash calculation (e.g., `mp4, mov`).
4. **Results**:

   - The script will output the number of unique images and videos processed.
   - A CSV file named `similar_files.csv` will be created in the output folder, listing similar files detected during the process.

## Usage Example

When prompted, input your disk locations and output folder as follows:

```
Enter the disk locations to check (separated by commas): D:\Media, E:\Photos
Enter the output folder path: D:\UniqueMedia
Include videos with errors in the copy list? (y/n): y
Enter specific file extensions without hash calculation (separated by commas): mp4, mov
```
