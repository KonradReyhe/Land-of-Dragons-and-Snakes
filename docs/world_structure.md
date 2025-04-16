# 🗺️ World Structure & Progression System

## 🌍 Overview
The game world is structured as a series of interconnected locations, each representing different aspects of spiritual corruption and redemption. The player's journey takes them through various districts, each with its own challenges, NPCs, and symbolic meaning.

## 🎪 Central Hub: The Blind Marketplace
The marketplace serves as the game's central hub, connecting to all major locations. Here, the player:
- Gains their first armor piece (Belt of Truth)
- Awakens to the nature of corruption
- Finds access to deeper layers of the city
- Meets three key NPCs:
  - The Justifier (Pride)
  - The Performer (Vanity)
  - The Mother Who Prays to the Wrong Light (Idolatry)

## 🏚️ Major Locations

### 1. House of the Lost Son
- **Location**: Small collapsed home with broken tools outside
- **Access**: Opens after helping one marketplace NPC
- **Interior**: Dimly lit, tools rusted, serpents coil around unfinished work
- **NPC**: The Addicted Craftsman (Gluttony / Despair)
- **Puzzle Elements**:
  - Reforge broken tool
  - Clean oil-stained blueprint
  - Help NPC remember his true self
- **Reward**: Breastplate of Righteousness

### 2. Scholar's Laboratory
- **Location**: Behind locked iron gate with symbols
- **Access**: Requires solving Performer's logic-based illusion puzzle
- **Interior**: Dusty observatory, shattered instruments, prideful quotes
- **NPC**: The Rationalist Alchemist (Arrogance / Envy)
- **Puzzle Elements**:
  - Solve celestial cipher
  - Match 3 old constellations to altar glyphs
  - Reveal inverted truth under scientific label
- **Reward**: Helmet of Salvation

### 3. The Dying Garden
- **Location**: Behind thick ivy-covered wall in southeast alley
- **Access**: Requires market items (seed and sunlight charm)
- **Interior**: Rotting roots, whispering vines, dried sacred pool
- **NPC**: The Apathist Gardener (Sloth / Doubt)
- **Puzzle Elements**:
  - Restore light source to sun mirror
  - Mix water from bell tower with oil
  - Trigger rebirth of divine flower
- **Reward**: Shoes of the Gospel of Peace

### 4. Tower of Jachin (South Bell Tower)
- **Location**: End of winding road, visible from square
- **Access**: Requires cleansing 3 NPC houses
- **Interior**: Mechanism chambers with broken spiritual gears
- **Puzzle Elements**:
  - Solve 3-level bell puzzle
  - Use virtue items from previous NPCs
- **Reward**: Shield of Faith

### 5. Temple of the Dragon (Final Scene)
- **Location**: Accessed from garden gate (requires both towers active)
- **Interior**: Fusion of ruined cathedral and serpent lair
- **Final Puzzle Elements**:
  - Light 6 braziers with armor pieces
  - Dialogue with one's serpent
  - Final moral decision (sacrifice or self)
- **Final Reward**: Sword of the Spirit

## ⚔️ Armor of God Progression
1. **Belt of Truth** (Marketplace)
   - Awarded by the Mother when her false idol crumbles
   - First piece, represents beginning of spiritual journey

2. **Breastplate of Righteousness** (Lost Son's House)
   - Forged from the restored tool
   - Represents moral strength and purpose

3. **Helmet of Salvation** (Scholar's Laboratory)
   - Found in sealed relic case
   - Represents wisdom and understanding

4. **Shoes of the Gospel of Peace** (Dying Garden)
   - Hidden under restored tree
   - Represents spreading truth and healing

5. **Shield of Faith** (Tower of Jachin)
   - Embedded in tower top
   - Represents spiritual protection

6. **Sword of the Spirit** (Final Temple)
   - Only usable when all other pieces are active
   - Represents the power of truth

## 🔔 Bell Tower System
- Two towers must be restored:
  1. **Boaz Tower** (Marketplace)
  2. **Jachin Tower** (South)
- Each tower restoration:
  - Visually restores a district
  - Partially reactivates spiritual protection
  - Unlocks new areas
  - Required for final temple access

## 🎮 Game Progression Flow
1. Awaken in corrupted room (Scene 1)
2. Read father's scroll
3. Enter marketplace (Scene 2)
4. Help marketplace NPCs
5. Access and cleanse NPC houses
6. Restore bell towers
7. Enter final temple
8. Confront the Dragon

## 🛠️ Technical Implementation Notes
- Each location has its own scene file
- Progression flags track:
  - NPCs helped
  - Houses cleansed
  - Towers restored
  - Armor pieces collected
- Inventory system handles:
  - Key items
  - Puzzle components
  - Armor pieces
- Scene transitions use:
  - Door objects
  - Key items
  - Progress requirements

## 📊 State Tracking
```python
# World progression
marketplace_visited: bool
houses_cleansed: Dict[str, bool]  # lost_son, scholars_lab, dying_garden
npcs_helped: Dict[str, bool]  # All six NPCs
bell_towers_restored: Dict[str, bool]  # boaz, jachin

# Armor progression
armor_pieces: Dict[str, bool]  # All six pieces
```

## 🎨 Visual Design Notes
- Each location has distinct color palette
- Corruption represented by:
  - Dark stains
  - Broken objects
  - Shadow creatures
- Cleansing shown through:
  - Light effects
  - Restored objects
  - Vanishing shadows
- Armor pieces glow when collected
- Bell towers emit light when restored 