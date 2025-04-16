# Asset Structure Documentation

## 📁 Root Structure
```
assets/
└── images/
    ├── objects/          # All interactive objects
    ├── characters/       # Character sprites and animations
    └── backgrounds/      # Background images and environments
```

## 🪑 Objects Structure
```
objects/
├── furniture/           # Large room objects with state variations
│   ├── bed/            # Bed with 3 states
│   │   ├── bed_neutral.png     # Default wooden bed with linen
│   │   ├── bed_corrupted.png   # Tattered with spiderwebs
│   │   └── bed_purified.png    # Clean with glowing effect
│   │
│   ├── mirror/         # Mirror with 3 states
│   │   ├── mirror_broken.png   # Cracked and rusted
│   │   ├── mirror_dirty.png    # Covered in grime
│   │   └── mirror_purified.png # Clean and glowing
│   │
│   ├── table/          # Table with 3 states
│   │   ├── table_neutral.png   # Simple wooden table
│   │   ├── table_corrupted.png # Stained with spiderwebs
│   │   └── table_cleansed.png  # Clean and glowing
│   │
│   ├── drawer/         # Drawer with 3 states
│   │   ├── drawer_neutral.png  # Simple wooden drawer
│   │   ├── drawer_corrupted.png # Damaged and dirty
│   │   └── drawer_cleansed.png # Restored and clean
│   │
│   └── altar/          # Altar with 3 states
│       ├── altar_neutral.png   # Simple wooden altar
│       ├── altar_corrupted.png # Dark and damaged
│       └── altar_cleansed.png  # Clean and holy
│
├── creatures/          # Enemy/monster creatures
│   ├── shadow_serpent.png      # Black serpent with red eyes
│   └── large_black_spider.png  # Sinister spider with glowing marks
│
└── items/             # Interactive items
    ├── scroll/        # Scroll related items
    │   ├── scroll_whole.png    # Complete scroll
    │   └── scroll_fragment.png # Torn piece of scroll
    │
    ├── candles/       # Candle items
    │   ├── candle_lit.png      # Burning holy candle
    │   └── candle_unlit.png    # Unlit candle
    │
    ├── cloth_oil.png          # Cloth soaked in sacred oil
    ├── puzzle_box.png         # Mysterious puzzle box
    └── feather_duster.png     # Cleaning tool
```

## 📝 Asset Descriptions

### 🛏️ Furniture
- **Bed**: Represents the player's state of rest/awakening
  - States: neutral → corrupted → purified
  - Associated with spider creature
  - Position: (150, 600)

- **Mirror**: Represents self-reflection
  - States: broken → dirty → purified
  - Used for final test
  - Position: (1400, 300)

- **Table**: Holds important items
  - States: neutral → corrupted → cleansed
  - Contains candle and oil
  - Position: (600, 580)

- **Drawer**: Contains hidden items
  - States: neutral → corrupted → cleansed
  - Holds matches and puzzle box
  - Position: (800, 600)
  - Associated with shadow serpent

- **Altar**: Spiritual centerpiece
  - States: neutral → corrupted → cleansed
  - Holds scroll_whole
  - Position: (900, 400)

### 🧀 Creatures
- **Shadow Serpent**
  - File: `shadow_serpent.png`
  - Position: (740, 620)
  - Tied to drawer corruption
  - Disappears when drawer is cleansed

- **Black Spider**
  - File: `large_black_spider.png`
  - Position: (180, 640)
  - Tied to bed corruption
  - Disappears when bed is cleansed

### 🧐 Items
- **Scrolls**
  - `scroll_whole.png`: Complete lore scroll
  - `scroll_fragment.png`: Used for puzzle box
  - Positions: (940, 460) and (1400, 460)

- **Candles**
  - `candle_unlit.png`: Can be lit with matches
  - `candle_lit.png`: Used for illumination
  - Position: (620, 570)

- **Tools**
  - `cloth_oil.png`: Used for cleansing
  - `feather_duster.png`: Used on mural
  - `puzzle_box.png`: Requires scroll fragment

## 🎨 Technical Specifications
- All images are PNG format with transparency
- Resolution: Varies by object (maintain aspect ratio)
- Color depth: 32-bit RGBA
- File naming convention: `objectname_state.png`

## 🔄 State Transitions
Each furniture piece follows this pattern:
1. Start in corrupted state
2. Can be cleansed using oil-soaked cloth
3. Transitions to purified/cleansed state
4. Associated creature disappears
5. Object gains faint glow effect

## 📍 Coordinates
All coordinates are in screen space (1280x720):
- Bed: (150, 600)
- Table: (600, 580)
- Mirror: (1400, 300)
- Altar: (900, 400)
- Drawer: (800, 600) 