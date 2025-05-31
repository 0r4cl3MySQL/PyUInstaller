# PyUInstaller

**PyUInstaller** is a graphical interface (GUI) for **PyInstaller**, designed to make it easier to **convert** your **Python scripts** into **standalone executable** applications — with **zero** need to write command-line arguments manually

## Features

- Easy selection of script, icon, and output folder
- Full support for additional scripts, hidden imports and data files
- Option to use `.spec` files instead of .py with built-in SpecFile Creator
- Command preview panel for transparency
- Build configuration presets (save/load)
- Auto-save session support
- Output log viewer
- Built-in help dialog

---

## Requirements

- **Python 3.7+**
- **PyInstaller** (`pip install pyinstaller`)
- **wxPython** (`pip install wxPython`)

> `wxPython` can be large. If you're on Linux, consider installing it via your system package manager for better performance

---

## Installation using CMD

- clone git repo to folder using: https://github.com/0r4cl3MySQL/PyUInstaller.git
- run pip install -r requirements.txt
- run python PyUInstaller.py

---

# Usage

- Select your main Python script with Browse Script
- Pick an icon file (.ico)
- Choose the output folder where your .exe should be saved
- Optionaly add hidden imports or data files if needed
- Adjust build flags like:

  - `--onefile`
  - `--onedir`
  - `--noconsole`
  - `--debug`
  - `--strip`

- Click Compile or press F5 to start
- You can also use .spec files and toggle between script-based and spec-based builds

---

## Build Options

PyInstaller Flags	Description in app:

- One File `--onefile` Package everything into a single file
- One Dir `--onedir` Package output into a folder
- No Console `--noconsole` Suppress terminal window for GUI apps
- Debug Mode `--debug` Enable debug info
- Clean Build `--clean` Delete temp build files
- Confirm Overwrite	`--confirm-overwrite` Ask before overwriting files
- Strip Binaries	`--strip` Reduce binary size
- No UPX	`--noupx` Disable UPX compression
- Force No-Cache	`--no-cache` Skip caching compiled bytecode

## Spec File Creator (Advanced)
Need full control? Use the Spec File Creator:

Open it from the main window

Fill in:

- Script path, app name, icon path
- Hidden imports, binaries, data, excludes, etc.
- Get a live preview of the .spec content
- Save the spec file to any location
- Return to the main UI and toggle "Use .spec file" to build using it
- This gives you full power over PyInstaller’s lower-level configurations.

---

## Presets

- Save build configurations to JSON files and load them on fly
- Automatically restore your last session (can be dissabled)
- Useful when switching between multiple projects

---

## Tips and Limitations

- Limitations:
  - `--onefile` and `--onedir` can´t be used together
  - `--clean` and `--noupx` are mutually exclusive also

- Add hidden imports manually if PyInstaller misses modules
- Data format: dest;src (e.g. assets;assets)

---

## Keyboard Shortcuts

- `Ctrl + H` → Help
- `Ctrl + T` → Toggle Auto-Save
- `F5` → Compile
- `Alt + F4` → Quit

---

## Powered by

- [wxPython](https://wxpython.org/)
- [PyInstaller](https://pyinstaller.org/)

---

## Made by

- [MySQL](https://github.com/0r4cl3MySQL)
- [ChatGPT](https://chat.openai.com/)
- [wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder)
