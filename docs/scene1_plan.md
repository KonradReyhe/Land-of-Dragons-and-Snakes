# Scene 1: The Waking Room
*Act I: A Soul Awakens in the Dust*

## 🏠 OVERVIEW
The player awakens in a symbolic chamber representing their inner state. The room is corrupted: spiderwebs in the corners, dark stains, broken furniture, and a serpent glimpsed in the shadows. The player must interact with furniture and symbolic objects to begin restoring the space. Each action reflects spiritual purification. This is not a tutorial, but a slow unfolding.

## ✨ CORE THEMES
- The house is a reflection of the player's soul
- Corruption = unresolved sin and spiritual blindness
- Cleansing = repentance, action, and truth
- Each object is symbolic: not just clutter, but metaphysical
- There's no combat, only choices, interactions, and reflection

## 📊 STATE VARIABLES
- `house_state_score` (0–5): tracks how many major pieces of furniture have been cleansed
- `player_inventory`: list of collected item IDs
- `cleansed_objects`: list of cleansed object IDs

## 🔧 GAME OBJECTS
All objects placed statically in the room with known coordinates.

### 🛏️ Furniture (with 3 States: corrupted, neutral, cleansed)
Each starts in **corrupted** state. States are swapped visually by updating the cutout asset.

| Name | File | Pos | Interactable | Notes |
|------|------|-----|---------------|-------|
| Bed | `bed_corrupted.png` | (900, 900) | No | Spider appears nearby |
| Table | `table_corrupted.png` | (600, 900) | Yes | Holds candle, oil |
| Mirror | `mirror_dirty.png` | (1700, 500) | No (yet) | Can be cleansed, used later |
| Altar | `altar_corrupted.png` | (1750, 850) | Yes | Holds scroll_whole |
| Drawer | `drawer_corrupted.png` | (300, 940) | Yes | Holds matches, puzzle_box |

### 🧐 Items (Click to pick up)

| Name | File | Pos | Use |
|------|------|-----|-----|
| Scroll (Whole) | `scroll_whole.png` | (950, 450) | Lore; activates altar interaction |
| Scroll (Fragment) | `scroll_fragment.png` | (1400, 460) | For puzzle box later |
| Candle (Unlit) | `candle_unlit.png` | (600, 580) | Can be lit with matches |
| Matches | `matches.png` | (820, 630) | Lights candle |
| Jar of Oil | `jar_of_oil.png` | (580, 590) | Combine with cloth |
| Oil-Soaked Cloth | `cloth_oil.png` | (140, 630) | Used to cleanse objects |
| Feather Duster | `feather_duster.png` | (450, 590) | Used on mural (future) |
| Puzzle Box | `puzzle_box.png` | (1310, 790) | Requires scroll_fragment to open |

### 🧀 Creatures (Tied to corruption)

| Name | File | Pos | Tied To |
|------|------|-----|----------|
| Shadow Serpent | `shadow_serpent.png` | (780, 650) | Drawer corruption |
| Black Spider | `large_black_spider.png` | (120, 640) | Bed corruption |

## 🎓 PUZZLE FLOW / CLEANSING LOGIC

### ✉️ Basic Flow:
1. Player collects candle, matches, jar_of_oil, cloth_oil
2. Player combines oil + cloth = "sacred cleaning cloth"
3. Player clicks corrupted object (e.g., drawer)
4. If holding cleaning cloth, it is consumed, object changes to `_cleansed.png`
5. Creature (if present) vanishes
6. `house_state_score += 1`
7. If `house_state_score == 4`: trigger dialogue: "The room exhales."

### 🧱 Optional Puzzle: Puzzle Box
- Use scroll_fragment to unlock
- Contents TBD (e.g., key to mirror or candle of true flame)

## 🎨 VISUAL CUES
- Cleansed furniture glows faintly
- Creatures hiss/slither when hovered
- Message box reacts to player actions
- Inventory UI updates visually when combining items

## 🎵 SOUND DESIGN (Suggestions)
- Ambient hum with slight echo
- Faint serpent slither and whisper
- Bell chimes softly when cleansing occurs

## ✉️ DIALOGUE
- Narration only, in-message box
- Examples:
  - "The wood is soaked with sorrow."
  - "You feel watched."
  - "The cloth burns in your hand… then the stain is gone."

## 🌐 TRANSITION CONDITIONS
When `house_state_score >= 4`, and puzzle box opened, player may:
- Clean the mirror (final test)
- See own serpent behind them
- Door fades open (cutout appears clickable)

## 🔑 NEXT SCENE
`door.png` appears → Click → Load: `Scene 2: The Blind Marketplace`

## 💻 IMPLEMENTATION STATUS

### ✅ Completed
- Basic scene structure
- Object placement
- Inventory system
- Basic interaction logic

### 🚧 In Progress
- Item combinations
- Furniture state changes
- Creature removal
- House state tracking

### 📝 To Do
- [ ] Add glowing effect for cleansed furniture
- [ ] Implement sound effects
- [ ] Add hover effects for creatures
- [ ] Create transition to Scene 2
- [ ] Add puzzle box mechanics
- [ ] Implement mirror interaction
- [ ] Add door appearance logic

## 🛠️ TECHNICAL NOTES
- All coordinates are in screen space (1280x720)
- Images should be PNG with transparency
- State changes should be smooth and visually clear
- UI should provide clear feedback for all actions 