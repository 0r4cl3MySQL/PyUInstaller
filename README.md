# PyUInstaller

**PyUInstaller** is a graphical interface (GUI) for PyInstaller, designed to make it easier to **convert** your **Python scripts** into standalone executable applications — with **zero** need to write command-line arguments manually.

## Features

- Easy selection of script, icon, and output folder
- Full support for additional scripts, hidden imports, and data files
- Auto-detects and handles `.spec` files
- Command preview panel for transparency
- Build configuration presets (save/load)
- Auto-save session support
- Output log viewer
- Built-in help dialog (Ctrl+H)

---

## Requirements

- **Python 3.7+**
- **PyInstaller** (`pip install pyinstaller`)
- **wxPython** (`pip install wxPython`)

> `wxPython` can be large. If you're on Linux, consider installing it via your system package manager for better performance.

---

## Installation

- clone git repo to folder using: https://github.com/0r4cl3MySQL/PyUInstaller.git
- run in **cmd** pip install -r requirements.txt
- run in **cmd** python PyUInstaller.py

---

# Usage
Select your main Python script with Browse Script

Optionally pick an icon file (.ico)

Choose the output folder where your .exe should be saved

Add hidden imports or data files if needed

Adjust build flags like:

--onefile, --onedir

--noconsole, --debug, --strip

Click Compile or press F5 to start!

You can also use .spec files and toggle between script-based and spec-based builds.

---

## Build Options (Checkboxes)
Option	PyInstaller Flag	Description
One File	--onefile	Package everything into a single file
One Dir	--onedir	Package output into a folder
No Console	--noconsole	Suppress terminal window for GUI apps
Debug Mode	--debug	Enable debug info
Clean Build	--clean	Delete temp build files
Confirm Overwrite	--confirm-overwrite	Ask before overwriting files
Strip Binaries	--strip	Reduce binary size
No UPX	--noupx	Disable UPX compression
Force No-Cache	--no-cache	Skip caching compiled bytecode

---

## Presets
Save build configurations to JSON files

Automatically restore your last session

Useful when switching between multiple projects

---

## Tips
You cannot use --onefile and --onedir together

--clean and --noupx are mutually exclusive

Add hidden imports manually if PyInstaller misses modules

Data format: dest;src (e.g. assets;assets)

---

## Keyboard Shortcuts
Ctrl + H → Help

Ctrl + T → Toggle Auto-Save

F5 → Compile

Alt + F4 → Quit

---

## Powered by:

wxPython

PyInstaller
