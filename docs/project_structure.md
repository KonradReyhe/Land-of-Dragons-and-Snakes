# Project Structure Documentation 🗂️

## Overview
This document outlines the standard file structure for the Land of Dragons and Snakes project. Following this structure helps maintain consistency and prevents duplicate implementations.

## Directory Structure

```
Land of Dragons and Snakes/
├── assets/                    # All game assets
│   ├── images/               # Image assets
│   │   ├── backgrounds/      # Background images
│   │   ├── objects/         # Object sprites
│   │   │   ├── creatures/   # Creature sprites
│   │   │   ├── furniture/   # Furniture sprites
│   │   │   └── items/      # Item sprites
│   │   └── ui/             # UI elements
│   ├── sounds/              # Sound effects and music
│   └── fonts/              # Font files
│
├── docs/                    # Documentation
│   ├── world_structure.md  # Game world design
│   ├── scene_*.md         # Individual scene documentation
│   └── project_structure.md # This file
│
├── src/                    # Source code
│   ├── game/              # Core game mechanics
│   │   ├── objects.py     # Game object classes
│   │   ├── character.py   # Player character
│   │   └── background_manager.py # Background handling
│   │
│   ├── scenes/            # Scene implementations
│   │   ├── base_scene.py  # Base scene class
│   │   ├── scene1.py     # House of the Lost Son
│   │   └── starting_scene.py # Initial scene
│   │
│   ├── ui/               # User interface
│   │   └── ui_manager.py # UI management
│   │
│   ├── engine/           # Game engine components
│   │   └── game_engine.py # Main game engine
│   │
│   ├── tools/            # Development tools
│   │   └── asset_processor.py # Asset processing utilities
│   │
│   └── main.py          # Game entry point
│
└── requirements.txt      # Python dependencies

```

## Key Components

### Scenes (`src/scenes/`)
- All scene-related code must be in this directory
- `base_scene.py` provides the base class for all scenes
- Each scene should have its own file (e.g., `scene1.py`, `marketplace_scene.py`)
- Scene documentation goes in `docs/scene_*.md`

### Game Objects (`src/game/`)
- Core game mechanics and object definitions
- Includes character controls, object behaviors, and game state management
- No scene implementations should be here

### Assets
- All game assets must be organized in the appropriate subdirectory under `assets/`
- Use consistent naming conventions:
  - Backgrounds: `location_state.png` (e.g., `house_corrupted.png`)
  - Creatures: `creature_name.png` (e.g., `shadow_serpent.png`)
  - Items: `item_name.png` (e.g., `scroll_ancient.png`)

### Documentation
- Each major feature should have corresponding documentation in `docs/`
- Scene documentation follows the template in existing scene files
- Keep this structure document updated when adding new directories or features

## Best Practices

1. **File Organization**
   - Keep related files together
   - Don't create duplicate directories for the same purpose
   - Use clear, descriptive names for files and directories

2. **Code Structure**
   - Scene implementations go in `src/scenes/` only
   - Core game mechanics belong in `src/game/`
   - UI elements should be in `src/ui/`

3. **Asset Management**
   - Always place assets in the correct subdirectory
   - Use consistent naming conventions
   - Keep original assets in a separate backup location

4. **Documentation**
   - Update this document when making structural changes
   - Document new features in appropriate markdown files
   - Keep scene documentation current

## Version Control
- `.gitignore` should exclude:
  - `__pycache__/`
  - `.pyc` files
  - IDE-specific files
  - Temporary files

## Future Considerations
- Consider adding:
  - `tests/` directory for unit tests
  - `config/` for configuration files
  - `scripts/` for build and deployment scripts 