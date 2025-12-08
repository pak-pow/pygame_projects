# 🐍 Snake Game

A classic Snake game built with Python and Pygame. Control the snake, eat apples, grow longer, and try not to crash into yourself!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)

## 📋 Description

This is a modern implementation of the classic Snake game where you control a snake that grows longer each time it eats an apple. The game features smooth gameplay, progressive difficulty, and a clean user interface.

## ✨ Features

- **Smooth Controls**: Use arrow keys or WASD to control the snake
- **Progressive Difficulty**: Snake speeds up as you collect more apples
- **Score Tracking**: Keep track of your current score
- **Screen Wrapping**: Snake wraps around screen edges for continuous play
- **Collision Detection**: Game ends when snake collides with itself
- **Visual Grid**: Clear grid overlay for better gameplay visibility
- **Game Over & Restart**: Easy restart with spacebar after game over

## 🎮 Controls

| Key | Action |
|-----|--------|
| `↑` or `W` | Move Up |
| `↓` or `S` | Move Down |
| `←` or `A` | Move Left |
| `→` or `D` | Move Right |
| `SPACE` | Restart Game (after game over) |

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Pygame 2.0 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pak-pow/snake-game.git
cd snake-game
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python snake_game.py
```

## 🎯 How to Play

1. Run the game and the snake will start moving automatically
2. Use the arrow keys or WASD to change direction
3. Eat the red apples to grow longer and increase your score
4. Avoid running into yourself
5. The snake speeds up slightly with each apple eaten
6. Press SPACE to restart after game over

## 🏆 Scoring

- Each apple collected: **+10 points**
- The game gets progressively faster as you score more points

## 📁 Project Structure

```
snake-game/
│
├── snake_game.py          # Main game file
├── README.md              # This file
└── requirements.txt       # Python dependencies (optional)
```

## 🛠️ Technical Details

### Game Mechanics

- **Grid System**: The game uses a 20x20 pixel grid system
- **Movement**: Snake moves in discrete steps on the grid
- **Collision**: Uses coordinate comparison for collision detection
- **Rendering**: 60 FPS with delta time for smooth movement

### Code Structure

- `Snake` class: Handles snake movement, growth, and collision
- `Apple` class: Manages apple spawning and positioning
- `Main` class: Game loop, event handling, and rendering

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

### To Contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📝 Future Improvements

- [ ] High score tracking
- [ ] Multiple difficulty levels
- [ ] Sound effects
- [ ] Power-ups (speed boost, invincibility, etc.)
- [ ] Obstacles and walls
- [ ] Different game modes
- [ ] Leaderboard system

## 👨‍💻 Author

veee (pak-pow) - [@pak-pow](https://github.com/pak-pow)

## 🙏 Acknowledgments

- Inspired by the classic Snake game from Nokia phones
- Built with [Pygame](https://www.pygame.org/)

## 📞 Contact

Feel free to reach out if you have any questions or suggestions!

- GitHub: [@pak-pow](https://github.com/pak-pow)

---

**Enjoy the game! 🎮🐍**
