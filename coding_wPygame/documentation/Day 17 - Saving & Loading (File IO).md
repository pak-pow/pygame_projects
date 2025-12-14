Tags: [[Programming]], [[Python]], [[PyGame]], [[Game]]

---
### 1) Learning Goal

You will learn to use Python's built-in `json` library to **Save** game data (High Score, Level, Coins) to a file and **Load** it back when the game restarts.

### 2) Clear Overview

- **The Problem:** Variables live in **RAM**. When you close the game (`sys.exit()`), RAM is cleared. Your high score is deleted.
    
- **The Solution:** We must write the data to the **Hard Drive** (Disk).
    
- **The Format:** We use **JSON** (JavaScript Object Notation). It looks exactly like a Python Dictionary `{"score": 100, "level": 5}` but stored as text.
    

### 3) Deep Explanation

**A. The json Module**

Python makes this easy.

- `json.dump(data, file)`: Dumps a dictionary into a file (Saving).
- `json.load(file)`: Loads a file back into a dictionary (Loading).

**B. The try...except Block**

When you run the game for the very first time, the save file doesn't exist yet. If you try to load it, Python will crash (FileNotFoundError).

We wrap our load code in a try block:

1. **Try** to load the file.
2. **Except** (if it fails): Create a default file (Score: 0).

**C. Context Managers (with open...)**

Always open files like this:

``` Python
with open('save_file.json', 'w') as f:
    # do stuff
```

The `with` keyword automatically closes the file even if your game crashes, preventing data corruption.

---
### 4) Runnable Pygame Code Example

Here is a **High Score Saver**.

- **Space:** Increase Score.    
- **R:** Reset Score to 0.
- **S:** Force Save (It also saves automatically on Quit).
- **Concept:** Close the game, run it again. **Your score will still be there!**

``` Python
import pygame, sys, json, os

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)
pygame.display.set_caption("Day 17: Save System")

# --- SAVE/LOAD FUNCTIONS ---
SAVE_FILE = "game_data.json"

def load_game():
    # Check if file exists first
    if not os.path.exists(SAVE_FILE):
        print("No save file found. Creating new one.")
        return {"high_score": 0, "coins": 0}
    
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            print("Loaded:", data)
            return data
    except:
        print("Save file corrupted. Starting fresh.")
        return {"high_score": 0, "coins": 0}

def save_game(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
            print("Game Saved!")
    except:
        print("Error saving game.")

# 2. Game Variables
game_data = load_game()
current_score = 0

# --- GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # AUTO-SAVE ON QUIT
            # Check if we beat the high score before saving
            if current_score > game_data["high_score"]:
                game_data["high_score"] = current_score
            
            save_game(game_data)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Increase Score
            if event.key == pygame.K_SPACE:
                current_score += 10
            
            # Reset
            if event.key == pygame.K_r:
                current_score = 0
                
            # Manual Save
            if event.key == pygame.K_s:
                if current_score > game_data["high_score"]:
                    game_data["high_score"] = current_score
                save_game(game_data)

    # Logic: Real-time High Score update (Visual only)
    display_high = max(current_score, game_data["high_score"])

    # Drawing
    screen.fill((30, 30, 40))
    
    txt_curr = font.render(f"Score: {current_score}", True, (0, 255, 0))
    txt_high = font.render(f"High Score: {display_high}", True, (255, 200, 50))
    txt_instr = font.render("SPACE=Score, S=Save", True, (200, 200, 200))
    
    screen.blit(txt_curr, (50, 100))
    screen.blit(txt_high, (50, 160))
    screen.blit(txt_instr, (50, 300))

    pygame.display.update()
    clock.tick(60)
```
### 5) 20-Minute Drill

**Your Task:** Add a **Level Unlock** system.

1. Modify `load_game` to include `"level": 1` in the default dictionary.
2. Add a key (e.g., **L**) that increases the level.
3. Save the game. Close it. Reopen it.    
4. **Goal:** Verify that the Level number remembers it was increased.

---

### 6) Quick Quiz

1. **What happens if you open a file with mode `'w'` (Write) that already has data in it?**    
2. **Why do we use `json` instead of just writing `f.write("Score: 10")`?**
3. **When is the best time to save the game?**

**Answers:**

1. It **wipes** the file completely clean and writes new data. Be careful!
2. JSON handles structure automatically. Parsing a raw text string like "Score: 10" requires messy string splitting code.
3. On specific events (beating a level), or on `QUIT`. Saving every frame (60 times a second) will destroy your hard drive speed.

---
### 7) Homework for Tomorrow

**Add High Scores to your Shooter or Platformer.**

- Load the high score at start. 
- Display it in the corner.
- If the player dies, compare `score > high_score`.
- If true, update the variable and save to disk.

---

### 8) Progress to Mastery

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 **56%**

---

### 9) Obsidian Note

# Day 17 – Saving & Loading (File I/O)

## 🧠 CONCEPT SUMMARY

#### Persistence:
Data in variables is temporary (RAM). Data in files is permanent (Disk). To save progress, we must move data from RAM to Disk.

#### JSON (JavaScript Object Notation):
The industry-standard format for saving game data. It looks identical to a Python Dictionary.
> [!note] 
> `import json`
> `json.dump(data, file)` -> Save
> `json.load(file)` -> Load

#### Handling Errors:
Files might not exist (first run) or be corrupted. Always use safeguards.
> [!important] Pattern
> ```python
> if os.path.exists(file):
>     load()
> else:
>     create_default_save()
> ```

---

## 🛠️ WHAT I DID TODAY

* **Imported JSON:** Used the standard library to handle data serialization.
* **Created a Save System:** Wrote a function to write a dictionary to a `.json` file.
* **Created a Load System:** Wrote a function to read the file back into a variable.
* **Handled First Run:** Added logic to create a default save file if one is missing so the game doesn't crash on a new computer.

---

## 💻 SOURCE CODE

> [!example]- SAVE/LOAD FUNCTIONS
> ```python
> import json
> 
> def save_data(score):
>     data = {"highscore": score}
>     with open("save.json", "w") as f:
>         json.dump(data, f)
> 
> def load_data():
>     try:
>         with open("save.json", "r") as f:
>             return json.load(f)
>     except FileNotFoundError:
>         return {"highscore": 0}
> ```

---

## 🧠 LEARNED TODAY

* **The `with` keyword:** This Context Manager ensures files are closed properly, preventing data corruption if the game crashes during a save.
* **Auto-Save:** Calling the save function inside the `if event.type == QUIT:` block creates a seamless user experience.

---

## 🎯 GOALS FOR TOMORROW

> [!todo] 💡 **Day 18: Lighting & Special Effects**
> * Learn to use "Blend Modes" (Add, Multiply).
> * Create a flashlight effect (Fog of War).
> * Make glowing particles.
