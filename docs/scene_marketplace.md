# 🎪 Scene Plan: The Blind Marketplace
*Act II: Where the People See Nothing*

## 🏙️ OVERVIEW
The Blind Marketplace is the first explorable district after the player leaves their home. Once vibrant, it now lies in symbolic ruin: stalls crumble, statues mock old symbols, and people go about their day under the influence of unseen serpents and dragons.

This is the **central hub** of the entire game. It connects to all major houses and locations.

## 🔍 CORE THEMES
- Spiritual blindness
- Cultural pride, vanity, idolatry
- Re-awakening of community through individual healing

## 🧍‍♂️ NPCs
The player meets 3 key NPCs here, each representing a dominant spiritual sin:

### 1. 🧑‍⚖️ The Justifier (Pride)
- Believes the market thrives because of him
- Dragon: Golden and beautiful, perched like a crown
- Puzzle:
  - Show him the broken scale (item from past justice)
  - Dialogue confronts imbalance in his 'justice'
  - He weeps → dragon vanishes

### 2. 🧑‍🎤 The Performer (Vanity)
- Feeds on crowd attention
- Dragon: Thin, ghostly, invisible until confronted
- Puzzle:
  - Use mirror shard or recorded echo to turn crowd attention
  - Performer sees self, crowd fades
  - Dragon flees

### 3. 🧕 The Mother Who Prays to the Wrong Light (Idolatry)
- Kneels before a glowing false statue (serpent beneath)
- Dragon: Coiled around the idol
- Puzzle:
  - Use candle and scroll verse to light true altar nearby
  - Statue cracks, dragon melts

## 🧩 MARKETPLACE PUZZLE FLOW
- Market is corrupted visually (gray sky, broken bells, no music)
- Once all 3 NPCs are helped:
  - Small bell rings faintly
  - Central bell tower unlocks → **Boaz Tower**

## 🛍️ FURNITURE & ITEMS
| Name | File | Pos | Interactable | Notes |
|------|------|-----|--------------|-------|
| Broken Scale | `scale_broken.png` | (450, 620) | Yes | Needed for Justifier |
| Mirror Shard | `mirror_shard.png` | (800, 650) | Yes | Needed for Performer |
| Unlit Candle | `candle_unlit.png` | (980, 580) | Yes | Needed for Mother |
| Scroll Fragment | `scroll_fragment.png` | (1200, 620) | Yes | Helps reveal false altar |

## 🧠 STATE VARIABLES
```python
marketplace_visited: bool
justifier_awakened: bool
performer_awakened: bool
mother_awakened: bool
boaz_tower_accessible: bool
armor_truth_collected: bool
```

## 🎁 ARMOR REWARD
- **Item**: `belt_truth.png`
- Given by the Mother once her idol collapses
- Symbol: Truth wraps around the core — beginning of awareness

## 🔔 BOAZ BELL TOWER (UNLOCK)
- Visually dormant, covered in grime and vines
- Opens only after 3 NPCs helped
- Requires sacred oil + gear item to ring
- Cleansing triggers:
  - Music change
  - Sky clears
  - Scene changes to partial light version

## 🐍 DRAGONS & EFFECTS
- Dragons attached to NPCs visible only to player
- When they vanish:
  - NPC visually transforms (clothes, face, posture)
  - Dialogue changes to gratitude
  - Market stalls glow faintly

## ✉️ DIALOGUE HIGHLIGHTS
**Before:**
- "This is the best of all possible times."
- "Nothing is wrong. Stop asking."

**After:**
- "I forgot what it felt like to be… awake."
- "Did the bell just ring?"

## 🎨 VISUAL STATES
- Corrupted: muted tones, smoke, dragons circling
- Partial Cleanse: golden haze, stall cloths reappear, music
- Fully Cleansed: sky opens, bells shimmer, townsfolk still and peaceful

## 🛠️ TECHNICAL IMPLEMENTATION NOTES
- All NPCs have visible sin dragon attached as cutout
- Market transitions visually based on bell tower state
- Item use requires inventory selection → drag to object
- Dialogue trees are fully scripted

## 🎵 SOUND DESIGN
- Ambient: Distant market chatter, wind through broken stalls
- SFX: Bell tolling, dragon whispers, crowd murmurs
- Music: Shifts from discordant to harmonious as NPCs awaken

## 🎮 INTERACTION LOGIC
```python
def handle_npc_interaction(npc, item):
    if npc == "justifier" and item == "broken_scale":
        return "awaken_justifier"
    elif npc == "performer" and item == "mirror_shard":
        return "awaken_performer"
    elif npc == "mother" and item == "candle":
        return "awaken_mother"
    return False

def check_marketplace_completion():
    return (
        justifier_awakened and 
        performer_awakened and 
        mother_awakened
    )
```

## 📦 ASSET REQUIREMENTS
- NPC sprites (3 main characters + crowd)
- Item sprites (scale, mirror, candle, scroll)
- Creature animations (3 dragons)
- Visual effects (bell tower glow, market transformation)
- UI elements (inventory, dialogue boxes)

## 🎨 ASSET PROMPTS
1. **Marketplace Background**:
   - "A once-grand marketplace now in decay, with broken stalls and faded banners. The sky is gray and oppressive, with faint dragon shadows circling overhead. The central bell tower looms in the background, covered in vines and grime."

2. **The Justifier**:
   - "A tall, proud figure in ornate robes, with a golden dragon perched on his shoulders like a crown. His face is stern and self-assured, but his eyes show a hint of doubt. The dragon's scales shimmer with a false light."

3. **The Performer**:
   - "A flamboyant character in colorful, tattered clothes, surrounded by a ghostly crowd. A thin, translucent dragon wraps around their neck like a scarf. Their face is painted with exaggerated expressions, but their eyes are empty."

4. **The Mother**:
   - "A kneeling figure in simple robes, praying before a glowing false idol. A serpentine dragon coils around the idol's base, its eyes glowing with a deceptive light. The mother's face shows devotion, but her posture suggests weariness."

5. **Belt of Truth**:
   - "A simple leather belt with a golden buckle shaped like a scale. The leather is worn but strong, and the buckle glows with a soft, steady light. The design suggests both humility and strength." 