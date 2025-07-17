# Craftomation Progression Points Editor

A simple GUI tool to modify `progressionPoints` in Craftomation101 save files.

This editor locates your save files, reads the current progression value, and allows you to adjust it between 1 and 20 using a slider or numeric input. Changes are saved directly to the file with a click.

## Features

- Automatically detects Craftomation101 save files
- Reads and writes `progressionPoints` values in binary format
- GUI built with PySide6 and themed with `qt-material`
- Input via slider or manual value entry
- Save or reset with one click

## Requirements

Python 3.8+

Install required packages via pip:

```bash
pip install PySide6 qt-material
```
## 🔧 Upcoming Work

The next set of features planned:

- **Save File Identification by UID**  
  Utilize the `uids` file to attach standard save names to `gamestateX` files. This will make it easier to identify which save is which.

- **Manual vs Exit Save Segregation**  
  Craftomation creates both manual saves and automatic "exit" saves. The tool will soon detect and label these separately, allowing you to target specific types more easily.
