# Asset Pipeline - Land of Dragons and Snakes

## 📁 Directory Structure

```
assets/
├── backgrounds/
│   ├── scenes/
│   │   ├── scene_1_mirror_chamber/
│   │   ├── scene_2_marketplace/
│   │   ├── scene_3_ruined_church/
│   │   ├── scene_4_bell_towers/
│   │   └── scene_5_dragon_cavern/
│   └── ui/
│       ├── menus/
│       └── overlays/
├── characters/
│   ├── npcs/
│   │   ├── justifier/
│   │   ├── mother/
│   │   ├── performer/
│   │   ├── mason/
│   │   └── silent_child/
│   └── player/
├── items/
│   ├── armor/
│   ├── puzzle_items/
│   └── collectibles/
├── ui/
│   ├── buttons/
│   ├── icons/
│   ├── frames/
│   └── fonts/
└── audio/
    ├── music/
    ├── effects/
    └── voice/
```

## 🎨 Asset Creation Guidelines

### Backgrounds
- **Format:** PNG
- **Resolution:** 1920x1080
- **Color Depth:** 32-bit (RGBA)
- **Layers:**
  - Base layer (static elements)
  - Interactive layer (clickable areas)
  - Foreground layer (overlay effects)
- **Naming:** `scene_[number]_[name]_[layer].png`
  - Example: `scene_1_mirror_chamber_base.png`

### Character Sprites
- **Format:** PNG with transparency
- **Animation Requirements:**
  - Idle (4 frames)
  - Talking (8 frames)
  - Special actions (variable)
- **Naming:** `character_[name]_[action]_[frame].png`
  - Example: `character_justifier_talk_1.png`

### UI Elements
- **Format:** PNG with transparency
- **Resolution:** Variable, maintain aspect ratio
- **States:**
  - Normal
  - Hover
  - Pressed
  - Disabled
- **Naming:** `ui_[category]_[name]_[state].png`
  - Example: `ui_button_inventory_hover.png`

### Audio
- **Music:**
  - Format: OGG
  - Bitrate: 192kbps
  - Loop points defined
- **Effects:**
  - Format: WAV
  - Sample Rate: 44.1kHz
  - Bit Depth: 16-bit
- **Voice:**
  - Format: WAV
  - Sample Rate: 44.1kHz
  - Bit Depth: 16-bit
  - Normalized volume

## 🔄 Asset Processing Pipeline

### 1. Creation
- Create assets according to specifications
- Save in source format (PSD, AI, etc.)
- Export to game format

### 2. Optimization
- Compress images without quality loss
- Trim audio silence
- Optimize sprite sheets

### 3. Integration
- Place in correct directory
- Update asset manifest
- Test in game engine

### 4. Version Control
- Commit to repository
- Tag with version
- Document changes

## 📝 Asset Manifest

### JSON Structure
```json
{
  "version": "1.0.0",
  "assets": {
    "backgrounds": {
      "scene_1": {
        "base": "scene_1_mirror_chamber_base.png",
        "interactive": "scene_1_mirror_chamber_interactive.png",
        "foreground": "scene_1_mirror_chamber_foreground.png"
      }
    },
    "characters": {
      "justifier": {
        "idle": ["justifier_idle_1.png", "justifier_idle_2.png"],
        "talk": ["justifier_talk_1.png", "justifier_talk_2.png"]
      }
    }
  }
}
```

## 🧪 Quality Assurance

### Image Testing
- Verify transparency
- Check resolution
- Test scaling
- Validate color space

### Audio Testing
- Check volume levels
- Verify loop points
- Test compression
- Validate format

### Performance Testing
- Monitor memory usage
- Check load times
- Verify streaming
- Test compression

## 🔧 Tools & Software

### Required Software
- Adobe Photoshop/Illustrator
- Audacity
- TexturePacker
- Pygame Asset Manager

### Custom Tools
- Asset validator
- Batch processor
- Manifest generator
- Preview tool

## 📋 Asset Checklist

### For Each Asset
- [ ] Meets format requirements
- [ ] Correct naming convention
- [ ] Proper directory placement
- [ ] Manifest entry
- [ ] Version control
- [ ] Quality tested
- [ ] Performance tested

## 🔄 Update Process

1. Create new assets
2. Process and optimize
3. Update manifest
4. Test in development
5. Commit changes
6. Deploy to test
7. Verify in game
8. Release to production 