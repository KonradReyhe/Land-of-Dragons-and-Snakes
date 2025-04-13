# 🐉 Land of Dragons and Snakes

A spiritually symbolic point-and-click adventure game built with Python and Pygame.

## 🎮 Game Description
Land of Dragons and Snakes is an atmospheric adventure game that combines medieval aesthetics with spiritual symbolism. Players navigate through mystical chambers, solve intricate puzzles, and uncover deep spiritual meanings through their journey.

### Current Features
- Starting Screen with medieval-themed UI
- Mirror Chamber puzzle scene
- Advanced puzzle logic system
- Resource management system
- Scene transition system
- Interactive UI elements

## 🛠️ Setup Instructions
1. Ensure you have Python 3.x installed
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Run the game:
```bash
python run_game.py
```

## 🔧 Technical Requirements
- Python 3.x
- Pygame-CE 2.5.3
- Additional dependencies listed in requirements.txt

## 🎨 Assets
The game uses custom assets for:
- Backgrounds
- UI elements
- Sound effects
- Character sprites

## 🚀 Development Status
Currently in active development with Scene 1 (Mirror Chamber) implemented.

## Project Structure

```
land_of_dragons/
├── src/                    # Source code
│   ├── game/              # Game core
│   │   ├── core/          # Core systems
│   │   ├── scenes/        # Game scenes
│   │   ├── ui/            # UI components
│   │   ├── items/         # Item system
│   │   └── puzzles/       # Puzzle system
│   └── data/              # Game data
│       ├── dialogues/     # Dialogue trees
│       ├── items/         # Item definitions
│       └── puzzles/       # Puzzle configurations
├── assets/                # Game assets
│   ├── backgrounds/       # Scene backgrounds
│   ├── characters/        # Character sprites
│   ├── items/            # Item sprites
│   ├── ui/               # UI elements
│   └── audio/            # Sound effects and music
└── docs/                 # Documentation
    └── design/           # Game design documents
```

## Development

- Follow PEP 8 style guide
- Use type hints for better code clarity
- Document all public functions and classes
- Keep game logic separate from rendering code

## License

This project is licensed under the MIT License - see the LICENSE file for details. 