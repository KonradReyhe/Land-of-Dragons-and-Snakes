# Background System Documentation

## 📁 Background Structure
```
assets/images/backgrounds/
├── home/              # Scene 1 backgrounds
│   ├── corrupted/     # Corrupted state
│   │   └── bg_home_corrupted.png
│   ├── neutral/       # Neutral state
│   │   └── bg_home_neutral.png
│   └── cleansed/      # Cleansed state
│       └── bg_home_cleansed.png
│
└── market/            # Scene 2 backgrounds
    ├── corrupted/     # Corrupted state
    │   └── bg_market_corrupted.png
    ├── neutral/       # Neutral state
    │   └── bg_market_neutral.png
    └── cleansed/      # Cleansed state
        └── bg_market_cleansed.png
```

## 🎨 Background States

### Scene 1: Home
- **Corrupted State** (house_state_score = 0)
  - Dark, shadowy atmosphere
  - Spiderwebs and corruption visible
  - File: `backgrounds/home/corrupted/bg_home_corrupted.png`

- **Neutral State** (house_state_score = 1-3)
  - Clean but not purified
  - Some shadows remain
  - File: `backgrounds/home/neutral/bg_home_neutral.png`

- **Cleansed State** (house_state_score >= 4)
  - Bright, purified atmosphere
  - Glowing effects
  - File: `backgrounds/home/cleansed/bg_home_cleansed.png`

### Scene 2: Marketplace
- **Corrupted State** (awakened_npcs = 0)
  - Dark, empty marketplace
  - Shadows and corruption
  - File: `backgrounds/market/corrupted/bg_market_corrupted.png`

- **Neutral State** (awakened_npcs = 1-2)
  - Some activity visible
  - Partial cleansing
  - File: `backgrounds/market/neutral/bg_market_neutral.png`

- **Cleansed State** (awakened_npcs = 3)
  - Bright, active marketplace
  - Full purification
  - File: `backgrounds/market/cleansed/bg_market_cleansed.png`

## 🔄 Transition System
- Fade duration: 1.5 seconds
- Transition curve: Smooth ease-in-out
- State change triggers:
  - Home: When house_state_score changes
  - Market: When awakened_npcs count changes

## 💻 Technical Implementation
```python
class BackgroundManager:
    def __init__(self):
        self.current_background = None
        self.target_background = None
        self.transition_alpha = 0
        self.is_transitioning = False
        
    def set_background(self, scene: str, state: str):
        """Set new background with transition"""
        path = f"assets/images/backgrounds/{scene}/{state}/bg_{scene}_{state}.png"
        self.target_background = pygame.image.load(path).convert()
        self.is_transitioning = True
        
    def update(self, delta_time: float):
        """Update transition state"""
        if self.is_transitioning:
            self.transition_alpha += delta_time * (255 / 1.5)  # 1.5 second transition
            if self.transition_alpha >= 255:
                self.current_background = self.target_background
                self.is_transitioning = False
                
    def draw(self, screen: pygame.Surface):
        """Draw current background with transition"""
        if self.current_background:
            screen.blit(self.current_background, (0, 0))
        if self.is_transitioning and self.target_background:
            self.target_background.set_alpha(int(self.transition_alpha))
            screen.blit(self.target_background, (0, 0))
```

## 📍 Integration Points
1. Scene1: Update in `_check_house_state()`
2. Scene2: Update in `_check_market_state()`
3. Both scenes: Call `update()` and `draw()` in main loop 