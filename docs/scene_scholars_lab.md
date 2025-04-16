# 🔭 Scene Plan: The Scholar's Laboratory
*Act IV: When Knowledge Forgets the Logos*

## 🏛️ OVERVIEW
A once-sacred observatory and spiritual study now consumed by pride and inverted knowledge. Scrolls are scattered, lenses cracked, and the sky map defiled. The Rationalist Alchemist believes only in what he sees — and he no longer sees the heavens rightly.

Access is granted after solving the Performer's illusion riddle in the marketplace.

## 🎭 CORE THEMES
- Arrogance, envy, and the fall of sacred knowledge
- The betrayal of divine insight for worldly prestige
- Reorienting the heavens — restoring spiritual cosmology

## 🧑‍🔬 NPC: The Rationalist Alchemist
- Speaks in equations and paradoxes
- Refers to old teachings as "superstition"
- Dragon of Envy wraps around his telescope — silent and smirking

## 📊 STATE VARIABLES
```python
lab_unlocked: bool
cipher_solved: bool
mirror_lens_revealed: bool
constellations_aligned: bool
dragon_expelled: bool
helmet_salvation_collected: bool
```

## 🧱 ROOM STRUCTURE
| Layer | Elements |
|-------|----------|
| Background | Night sky dome, broken telescope, torn scrolls |
| Furniture | Astrological altar, central armillary, dust-covered shelves |
| Interactables | Cipher board, broken lens case, scroll rack, tuning dial |
| Creatures | Envy Dragon (invisible until cipher solved) |

## 🔍 FURNITURE AND ITEMS
| Name | File | Pos | Interactable | Use |
|------|------|-----|--------------|-----|
| Cipher Scroll | `cipher_scroll.png` | (500, 580) | Yes | Needed to solve celestial cipher |
| Celestial Dial | `celestial_dial.png` | (900, 620) | Yes | Aligns constellations |
| Mirror Lens | `mirror_lens.png` | (1250, 600) | Yes | Reveals hidden glyphs |
| Altar of Logos | `altar_dusty.png` → `altar_glowing.png` | (1400, 500) | Yes | Must be realigned |
| Telescope | `telescope_broken.png` | (1000, 520) | No | Used symbolically |

## 🐉 CREATURE
- **Envy Dragon**
  - Initially invisible
  - Becomes visible after cipher is solved
  - Twists around the telescope
  - Fades when constellations aligned + altar reactivated

## 🧩 PUZZLE FLOW
1. Player finds **cipher scroll** and examines it (must rotate once)
2. Uses scroll to decipher the **Celestial Dial** — aligns 3 symbolic constellations:
   - Crown (wisdom)
   - Serpent (knowledge)
   - Cross (Logos)
3. Discovers **Mirror Lens** in sealed shelf
   - Allows them to see true glyphs on dusty altar
4. Aligns altar with star glyphs
   - Light spills from cracks in observatory
5. Envy Dragon hisses and slithers away into sky
6. NPC stares at the stars and whispers, "I had forgotten who made them."
7. Gives the **Helmet of Salvation**

## 🎨 VISUAL STATES
- Corrupted: red sky glow, lens cracked, shelves dusty
- Neutral: soft night blue, glyphs glow faintly
- Cleansed: golden-white constellations rotate, lens shines

## ✉️ DIALOGUE SAMPLES
**Before:**
- "We no longer need metaphors. We have mathematics."
- "My formula eclipses your scroll."

**During:**
- "What are these alignments…? I never saw them before."
- "It's beautiful… but it doesn't fit."

**After:**
- "Even the stars remember."
- "Take it. Salvation is a crown worn inside."

## 🔑 EXIT CONDITION
- Dragon removed
- Logos altar glowing
- Player receives helmet in inventory
- Can exit through starlit door behind telescope

## 🎁 ARMOR REWARD
- **Item**: `helmet_salvation.png`
- Visual: Silver with glowing star mark
- Symbolism: Salvation is clear sight of the heavens

## 🛠️ IMPLEMENTATION NOTES
- Cipher puzzle uses click-to-rotate or match interaction
- All celestial symbols drawn in sacred geometry
- Inventory updated with mirror lens and helmet when acquired
- Dialogue presented through message box

## 🎵 SOUND DESIGN
- Ambient: Distant star hum, rustling scrolls
- SFX: Telescope creaking, dragon hissing, glyphs aligning
- Music: Shifts from dissonant to harmonious as constellations align

## 🎮 INTERACTION LOGIC
```python
def handle_celestial_alignment(dial, constellation):
    if constellation in ["crown", "serpent", "cross"]:
        dial.align(constellation)
        return True
    return False

def check_puzzle_completion():
    return (
        cipher_solved and 
        constellations_aligned and 
        mirror_lens_revealed and 
        dragon_expelled
    )
```

## 📦 ASSET REQUIREMENTS
- Furniture sprites (telescope, altar, shelves)
- Item sprites (scroll, lens, dial)
- Creature animations (dragon)
- Visual effects (constellation rotation, glyph glow)
- UI elements (cipher interface, inventory icons)

## 🎨 ASSET PROMPTS
1. **Observatory Dome**:
   - "A grand observatory dome with a cracked glass ceiling, showing a distorted night sky. The walls are covered in ancient astronomical charts and equations. The floor is made of polished dark wood with inlaid celestial patterns."

2. **Celestial Dial**:
   - "An ornate brass celestial dial with three concentric rings, each engraved with different constellations. The outer ring shows the Crown, middle ring the Serpent, and inner ring the Cross. The dial has a central pivot point with a small crystal that catches the light."

3. **Envy Dragon**:
   - "A sleek, serpentine dragon made of shifting shadows and starlight. Its scales shimmer with a dark purple hue, and its eyes glow with an envious green light. It wraps around the telescope like a living shadow, occasionally revealing glimpses of its true form."

4. **Mirror Lens**:
   - "A circular lens made of polished silver, etched with tiny celestial symbols around its edge. When held up to light, it projects these symbols onto surfaces. The glass has a slight blue tint and catches the light in a way that reveals hidden patterns."

5. **Helmet of Salvation**:
   - "A silver helmet with a star-shaped mark on the forehead. The metal has a subtle blue sheen, and the star mark glows with a soft white light. The design is simple but elegant, with a slight curve to the visor that suggests wisdom and clarity." 