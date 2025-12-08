# Learning Pygame 🎮

Welcome to my journey into Game Development with Python and Pygame! This repository documents my progress from building simple arcade clones to engineering complex rendering projects.

My goal is to master the fundamentals of game architecture understanding the game loop, managing state, handling user input, and implementing physics before moving on to advanced engines.

## 🗺️ Game Roadmap

This roadmap is structured to introduce one major mechanic at a time. It starts with simple rebounding physics in Pong, moves through array manipulation in Snake, and culminates in complex mathematical rendering with the Raycaster.

| # | Game Project | Status      | Key Concepts & Goals |
|:-:| :--- |:------------| :--- |
| 0 | [**Calculator**](./Calculator) | ✅ Done      | **GUI Fundamentals**: Creating buttons, handling Mouse Input, and logic state management. |
| 1 | [**Pong**](./01_pong) | ✅ Done | Basic collision detection, understanding the Game Loop, and drawing `Rect` objects. |
| 2 | [**Snake**](./02_snake) | ✅ Done | Manipulating `Lists`, handling Grid movement, and random item generation. |
| 3 | [**Breakout**](./03_breakout) | 🟨 On-going     | Advanced physics reflection, managing object state, and score tracking. |
| 4 | [**Space Invaders**](./04_space_invaders) | 🔴 Todo     | Handling projectiles, implementing Enemy AI movement patterns, and collision groups. |
| 5 | [**Flappy Bird**](./05_flappy_bird) | 🔴 Todo     | Simulating Gravity, creating Infinite Scrolling backgrounds, and persistent high scores. |
| 6 | [**Dino Run**](./06_dino_run) | 🔴 Todo     | Sprite Animation cycles, precise Hitboxes, and game speed scaling over time. |
| 7 | [**Tetris**](./07_tetris) | 🔴 Todo     | Logic for 2D Arrays (Matrices), shape Rotation algorithms, and row clearing. |
| 8 | [**Platformer**](./08_platformer) | 🔴 Todo     | Implementing Gravity/Friction, side-scrolling Camera, and loading Levels from files. |
| 9 | [**Top-Down RPG**](./09_rpg) | 🔴 Todo     | Using Tilemaps for world building, Inventory systems, and A* Pathfinding. |
| 10 | [**Raycaster 3D**](./10_raycaster) | 🔴 Todo     | Utilizing Trigonometry for pseudo-3D rendering and raycasting engines. |

## 🛠️ Tech Stack

* **Language: Python 3.x**
    * Chosen for its readability and rapid prototyping capabilities. I am utilizing modern Python features like type hinting to keep the code clean.

* **Library: Pygame Community Edition (`pygame-ce`)**
    * I am using the Community Edition (`ce`) over the standard distribution for its better performance, modern SDL2 features, and more frequent updates.

* **IDE: PyCharm**
    * Used for its robust debugging tools, virtual environment management, and intelligent code completion.

## 🚀 How to Play

### Prerequisites
Before running any games, ensure you have Python installed and the necessary dependencies set up.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/pak-pow/learning_pygame.git](https://github.com/pak-pow/learning_pygame.git)
    cd learning_pygame
    ```

2.  **Install Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

### Running a Game
To play any of the games, navigate to the specific game's folder and run the `main.py` script. For example, to play Pong:

```bash
cd 01_pong
python main.py
