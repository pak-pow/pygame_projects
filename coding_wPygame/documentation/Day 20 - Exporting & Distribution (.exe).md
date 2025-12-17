Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to use **PyInstaller** to "freeze" your Python code, converting your script, assets, and the Python interpreter itself into a standalone **Executable (`.exe`)** that runs on computers without Python installed.

### 2) Clear Overview

- **The Problem:** If you send `main.py` to a friend, they need Python and Pygame installed to run it. Most players don't have that.
    
- **The Solution:** **PyInstaller**. It scans your code, finds every library you used (Pygame, Random, Math), and bundles them all into one folder or file.
    
- **The Trap:** **Relative Paths**. Your code says `load('image.png')`. When packed into an `.exe`, the "current directory" changes, often causing instant crashes if you don't handle assets correctly.
    

### 3) Deep Explanation

A. How Freezing Works

Python is "interpreted," meaning it reads code line-by-line. An .exe is "compiled" machine code. PyInstaller creates a mini-bootloader that extracts a temporary copy of Python into your RAM, runs your script, and cleans up when done.

B. The Dist Folder

When you build your game, you get two folders:

1. `build/`: Temporary files (you can delete this).
    
2. `dist/`: **Distribution**. This is where your final game lives.
    

**C. Console vs. Windowed**

- **Console Mode:** Useful for debugging (if the game crashes, you see the error).
    
- **Windowed Mode (`--noconsole`):** Professional. No black text box appears behind your game.

### 4) The "Exe-Ready" Code Example


``` Python

import pygame, sys, os

# 1. THE ASSET HELPER (CRITICAL FOR EXE)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 2. Standard Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My First Exe")
clock = pygame.time.Clock()

# 3. Load Assets using the Helper
# (Make sure you actually have an icon.png, or remove these lines!)
# icon = pygame.image.load(resource_path("icon.png"))
# pygame.display.set_icon(icon)

font = pygame.font.SysFont("Arial", 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 100, 200))
    
    # Draw instructions
    text = font.render("I AM AN EXE FILE!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(300, 200))
    screen.blit(text, text_rect)
    
    pygame.display.update()
    clock.tick(60)
```

### 5) The 20-Minute Drill (The Build Process)

**Your Task:** Turn the code above into an actual program.

1. Install PyInstaller:
    
    Open your terminal/command prompt and type:
    
    ``` python
    pip install pyinstaller
    ```
    
2. Build It:
    
    Navigate to the folder containing main_export.py and run:
    
    ``` python
    pyinstaller --noconsole --onefile main_export.py
    ```
    
3. Locate It:
    
    Go to the new dist folder. You should see main_export.exe.
    
4. Test It:
    
    Double-click the .exe. Does it open?
    
    - _If it opens:_ Success!
        
    - _If it closes instantly:_ You likely have an asset loading error (e.g., you tried to load an image that isn't next to the exe).
        

### 6) Quick Quiz

1. **What does the `--onefile` flag do?**
    
2. **If my game crashes instantly when opening the `.exe`, what flag should I remove to see the error message?**
    
3. **Does the person playing your game need to install Python?**
    

**Answers:**

1. It bundles all dependencies (DLLs, Python interpreter) into a single `.exe` file instead of a folder full of files.
    
2. Remove `--noconsole`. This will keep the black command window open so you can read the crash report (Traceback).
    
3. **No.** That is the whole point of exporting!
    

### 7) Homework for Tomorrow

**Prepare your Portfolio.**

- Take your best project so far (Shooter or Platformer).
    
- Add a "Game Over" and "Restart" state (Day 14).
    
- Export it as an `.exe`.
    
- Zip the `.exe` (and the assets folder if you didn't use the advanced helper) and upload it to Google Drive or **itch.io** (a popular indie game site).
    

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜ **66%**

### 9) Obsidian Note

## 🧠 CONCEPT SUMMARY

#### Freezing Code:
Python is an interpreted language (requires Python installed to run). "Freezing" or "Compiling" means bundling the Python interpreter *inside* your game folder so anyone can run it.

#### PyInstaller:
The industry-standard tool for converting `.py` to `.exe` (Windows) or `.app` (Mac).
> [!note] Command
> `pyinstaller --noconsole --onefile main.py`

#### Key Flags:
* **`--noconsole`**: Hides the black command prompt window that usually pops up with Python scripts.
* **`--onefile`**: Bundles all code dependencies into a single file (easier to share).

#### The "Dist" Folder:
PyInstaller creates a `build` folder (temp files) and a `dist` folder. Your final game lives in `dist`.

---

## 🛠️ WHAT I DID TODAY

* **Prepped for Release:** Removed debug `print()` statements and added a window caption/icon.
* **Installed PyInstaller:** Used `pip install pyinstaller`.
* **Built an Executable:** Ran the build command to generate a standalone `.exe`.
* **Fixed Paths:** Learned to use `sys._MEIPASS` or place assets in the same folder as the exe to prevent `FileNotFoundError`.

---

## 💻 SOURCE CODE

> [!example]- ASSET PATH HELPER
> Use this function to allow your game to find images whether running in VS Code OR as an Exe.
> ```python
> import sys, os
> 
> def resource_path(relative_path):
>     try:
>         # PyInstaller creates a temp folder and stores path in _MEIPASS
>         base_path = sys._MEIPASS
>     except Exception:
>         base_path = os.path.abspath(".")
> 
>     return os.path.join(base_path, relative_path)
> ```

---

## 🧠 LEARNED TODAY

* **Dependencies:** My game relies on libraries (Pygame, NumPy). PyInstaller automatically finds these and packs them, which is why the file size jumps from 5KB (script) to ~15MB (exe).
* **Debugging Exes:** If an exe crashes, build it *without* `--noconsole` to see the error output.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 🎒 **Day 21: Inventory Systems**
> * Start the "Advanced Phase".
> * Create a data structure for an Inventory (List of Dictionaries).
> * Visualizing the inventory (UI Overlay).
> * Picking up items and adding them to the slots.
