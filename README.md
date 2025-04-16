# 🐉 Land of Dragons and Snakes

A spiritually symbolic point-and-click adventure game built with Python and Pygame-CE, exploring themes of redemption, purification, and inner transformation.

## 🎮 Game Overview

Land of Dragons and Snakes is an atmospheric adventure game that combines medieval aesthetics with spiritual symbolism. Players navigate through mystical chambers, solve intricate puzzles, and uncover deep spiritual meanings through their journey of cleansing and restoration.

### 🌟 Key Features

- **Rich Symbolism**: Every object, creature, and interaction carries deeper spiritual meaning
- **Dynamic Environment**: Rooms transform as players progress through their spiritual journey
- **Layered Gameplay**: Multiple interaction layers with furniture, items, and creatures
- **Atmospheric Design**: Medieval-themed visuals with dynamic lighting and effects
- **Meaningful Choices**: Player actions affect the spiritual state of the environment

## 🛠️ Technical Requirements

- Python 3.x
- Pygame-CE 2.5.3
- Additional dependencies in `requirements.txt`

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/KonradReyhe/Land-of-Dragons-and-Snakes.git
cd Land-of-Dragons-and-Snakes
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python src/main.py
```

## 🗺️ Project Structure

```
land_of_dragons/
├── assets/                # Game assets
│   ├── images/           # Visual assets
│   │   ├── backgrounds/  # Scene backgrounds
│   │   ├── characters/   # Character sprites
│   │   └── objects/      # Game objects
│   │       ├── creatures/
│   │       ├── doors/
│   │       ├── furniture/
│   │       └── items/
├── docs/                 # Documentation
│   ├── asset_structure.md
│   ├── background_system.md
│   ├── scene1_plan.md
│   └── world_structure.md
└── src/                  # Source code
    ├── engine/          # Game engine components
    ├── game/            # Game mechanics
    ├── scenes/          # Scene implementations
    └── ui/              # User interface components
```

## 🎯 Current Features

### Scene 1: The Waking Room
- Dynamic environment that responds to player actions
- Multiple layers of interactive objects
- Creature encounters with shadow serpents and spiders
- Inventory system with combinable items
- Progressive room cleansing mechanics

### Core Systems
- Advanced background management
- Multi-layered rendering system
- Interactive object framework
- State-based scene transitions
- Dynamic UI system

## 🚀 Development Status

Currently in active development with Scene 1 (The Waking Room) implemented. Future development will focus on:
- Additional scenes (Marketplace, Scholar's Laboratory)
- Enhanced creature behaviors
- Extended puzzle mechanics
- Sound design implementation
- Save/load system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Pygame-CE community for the game engine
- Medieval art and symbolism for inspiration
- Contributors and testers 