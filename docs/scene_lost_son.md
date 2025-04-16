# 🏚️ Scene Plan: House of the Lost Son
*Act III: Forging the Forgotten Self*

## 🏠 OVERVIEW
A ruined blacksmith's home on the outskirts of the marketplace. This house is filled with the echoes of what once was: broken tools, empty bottles, scattered metalwork. Serpents coil around tools, whispering regret and hopelessness.

The player enters this house after helping one NPC in the marketplace.

## 🎭 CORE THEMES
- Despair, gluttony, and spiritual forgetfulness
- The memory of work done in purpose vs. meaningless consumption
- Restoration of identity through divine craftsmanship

## 🧍‍♂️ NPC: The Addicted Craftsman
- Once a gifted forger of symbols and sacred tools
- Now drinks from an empty chalice and mutters about "forgotten blueprints"
- Shadow serpent coils around his back, whispering lies

## 📊 STATE VARIABLES
```python
house_lost_son_entered: bool
craftsman_convinced: bool
tool_forged: bool
shadow_serpent_bound: bool
altar_of_fire_lit: bool
armor_breastplate_collected: bool
```

## 🧱 ROOM STRUCTURE
| Layer | Elements |
|-------|----------|
| Background | Broken forge, rusted shelves, smashed window |
| Furniture | Anvil, furnace (cold), collapsed workbench, altar of fire |
| Interactables | Tool parts, blueprint fragment, holy coal, forge hammer |
| Creatures | Shadow serpent (appears when altar touched), static shadows |

## 🔍 FURNITURE AND ITEMS
| Name | File | Pos | Interactable | Use |
|------|------|-----|--------------|-----|
| Anvil | `anvil_rusted.png` | (800, 800) | Yes | Used to forge item |
| Furnace | `furnace_cold.png` | (1200, 780) | Yes | Must be re-lit |
| Broken Hammer | `hammer_rusted.png` | (1000, 860) | Yes | Needed for forge |
| Blueprint | `blueprint_fragment.png` | (600, 600) | Yes | Unlocks recipe |
| Holy Coal | `holy_coal.png` | (850, 780) | Yes | Needed to relight furnace |
| Empty Chalice | `chalice_empty.png` | (700, 880) | No | Symbolic |
| Altar of Fire | `altar_extinct.png` → `altar_lit.png` | (1300, 600) | Yes | Final forge blessing |

## 🕸️ CREATURES
- **Shadow Serpent**: Appears near the anvil after altar is activated
  - Circles player and NPC
  - Binds if player uses forged tool with altar lit

## 🧩 PUZZLE FLOW
1. Player explores room and finds:
   - Broken hammer
   - Blueprint fragment (must be clicked twice to reveal message: "Shape through the Flame")
   - Holy Coal (hidden behind broken tool chest)
2. Player places coal in furnace
3. Lights altar of fire (can only be done after coal placed)
4. Uses hammer and blueprint on anvil — triggers animation of forging
5. Tool glows — new item: **Forged Mirrorplate**
6. Uses Forged Mirrorplate at altar → serpent hisses and dissolves
7. NPC awakens, stands, begins to clean room
8. Grants player: **Breastplate of Righteousness**

## 🎨 VISUAL STATES
- Corrupted: shadows flicker, ash falls, serpent whispers
- Neutral: furnace glows red, altar lit, no movement
- Cleansed: golden light, clean forge, music changes to solemn choir

## ✉️ DIALOGUE SAMPLES
**Before:**
- "The flame is gone. I drank it away."
- "These tools… they do not speak anymore."

**During:**
- "You hold the fire I once knew."
- "The shape… it remembers!"

**After:**
- "The craft was never mine. I was only its servant."
- "Take this. Righteousness must be worn with humility."

## 🔑 EXIT CONDITION
Once tool is forged and altar ritual completed:
- Shadow serpent removed
- Door glows softly
- Player may exit and world state is updated

## 🎁 ARMOR REWARD
- **Item**: `breastplate_righteousness.png`
- Visual: Glows with inner fire, appears in inventory and on player cutout
- Symbolism: You are now protected in spirit by the work of righteous intent

## 🛠️ IMPLEMENTATION NOTES
- All puzzle steps must use simple click-to-place logic
- Cutout layers: altar must glow when active
- Dialog box appears center-top
- Cursor highlights on all interactables

## 🎵 SOUND DESIGN
- Ambient: Distant hammering, crackling fire
- SFX: Metal clanging, serpent hissing, forge roaring
- Music: Shifts from somber to triumphant as puzzle progresses

## 🎮 INTERACTION LOGIC
```python
def handle_item_interaction(item1, item2):
    if item1 == "holy_coal" and item2 == "furnace":
        furnace.state = "lit"
        return True
    elif item1 == "hammer" and item2 == "anvil":
        if furnace.state == "lit":
            return "forged_mirrorplate"
    return False

def check_puzzle_completion():
    return (
        tool_forged and 
        shadow_serpent_bound and 
        altar_of_fire_lit
    )
```

## 📦 ASSET REQUIREMENTS
- Furniture sprites (anvil, furnace, workbench)
- Item sprites (hammer, coal, blueprint)
- Creature animations (serpent)
- Visual effects (fire, glow, shadows)
- UI elements (dialog box, inventory icons) 