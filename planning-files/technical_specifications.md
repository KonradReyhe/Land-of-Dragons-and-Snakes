# Technical Specifications - Land of Dragons and Snakes

## 🖥️ Display & Resolution

- **Base Resolution:** 1920x1080 (16:9)
- **Minimum Resolution:** 1280x720
- **Scaling:** Maintain aspect ratio, letterbox if necessary
- **Fullscreen Support:** Optional, with proper scaling
- **VSync:** Enabled by default

## 🎮 Input Handling

- **Primary Input:** Mouse (point-and-click)
- **Secondary Input:** Keyboard for:
  - ESC: Pause menu
  - SPACE: Skip dialogue
  - F: Toggle fullscreen
  - S: Toggle serpent vision
  - I: Toggle inventory
  - C: Toggle codex

## 🎨 Asset Specifications

### Backgrounds
- Format: PNG
- Resolution: 1920x1080
- Color Depth: 32-bit (RGBA)
- Naming: `scene_[number]_[name].png`
  - Example: `scene_1_mirror_chamber.png`

### Character Sprites
- Format: PNG with transparency
- Resolution: Variable, maintain aspect ratio
- Animation Frames: 4-8 frames per animation
- Naming: `character_[name]_[action]_[frame].png`
  - Example: `character_justifier_talk_1.png`

### UI Elements
- Format: PNG with transparency
- Resolution: Variable, maintain aspect ratio
- Naming: `ui_[category]_[name].png`
  - Example: `ui_inventory_slot.png`

### Audio
- Format: OGG (music), WAV (effects)
- Sample Rate: 44.1kHz
- Bit Depth: 16-bit
- Naming: `audio_[category]_[name].[ext]`
  - Example: `audio_music_serpent_theme.ogg`

## 🚀 Performance Targets

- **Target FPS:** 60 FPS
- **Minimum FPS:** 30 FPS
- **Memory Usage:** < 1GB
- **Load Times:** < 3 seconds per scene

## 💾 Save System

- **Save Format:** JSON
- **Auto-save Points:**
  - Scene transitions
  - Major puzzle completions
  - Item acquisitions
- **Manual Save:** Available in pause menu
- **Save Slots:** 3 slots minimum

## 🛠️ Development Tools

- **Python Version:** 3.9+
- **Pygame Version:** 2.5.2
- **IDE:** Cursor
- **Version Control:** Git
- **Testing Framework:** pytest

## 🔍 Debug Features

- **Debug Mode:** Accessible via command line flag
- **Features:**
  - FPS counter
  - Scene boundaries
  - Collision boxes
  - Item spawner
  - Skip puzzles
  - Unlock all items

## 📱 Accessibility Options

- **Text Size:** Adjustable (3 sizes)
- **Color Blind Mode:** Available
- **Audio:**
  - Volume controls
  - Subtitles for all dialogue
  - Visual indicators for sound cues
- **Controls:**
  - Mouse sensitivity
  - Keyboard remapping
  - Touch screen support (optional)

## 🧪 Testing Requirements

- **Unit Tests:** Core systems
- **Integration Tests:** Scene transitions
- **Performance Tests:** Memory usage, FPS
- **Compatibility Tests:** Different resolutions
- **Accessibility Tests:** All accessibility features

## 📦 Build & Distribution

- **Platforms:** Windows, Linux, macOS
- **Installation:** Single executable
- **Dependencies:** Bundled with game
- **Updates:** Optional auto-update system 