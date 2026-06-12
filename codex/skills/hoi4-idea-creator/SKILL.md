---
name: hoi4-idea-creator
description: Create Hearts of Iron 4 national spirit ideas (国民精神) through interactive dialogue. Use when the user requests to (1) Create a new national spirit/idea, (2) Add a country modifier/buff, (3) Implement idea effects mentioned in national focus or event context (e.g., "add national spirit granting +10% stability"), or (4) User says phrases like "国民精神作る", "create national spirit", "add idea", "make a buff", etc. Handles complete implementation including idea definition, GFX sprite setup, and localization files.
---

# HOI4 Idea Creator

## Overview

Create complete HOI4 national spirit ideas (国民精神/アイデア) through interactive dialogue. Guides through defining effects, naming, imagery, and automatically implements all required files: idea definition, GFX sprites, and localization.

## When This Skill Triggers

This skill activates when:
- User explicitly requests creating a national spirit/idea
- User mentions adding country modifiers or buffs
- While creating national focuses or events, user specifies adding a national spirit as an effect
- User says trigger phrases: "国民精神作る", "create national spirit", "add idea", "make a country buff"

## Interactive Workflow

Follow this step-by-step process to create a complete idea implementation.

### Step 1: Gather Requirements

Ask the user the following information through interactive questions:

1. **Country/Mod Context**
   - "Which mod are you working on?" (to determine file paths)
   - "Which country is this idea for?" (e.g., JAP, GER, USA)

2. **Idea Identity**
   - "What should the idea ID be?" (internal identifier, snake_case recommended)
   - "What category?" (usually `country` for national spirits)

3. **Localization Language**
   - "What language(s) should I create localization for?" (japanese, english, etc.)
   - This determines the localisation directory: `localisation/<language>/`

4. **Idea Name & Description**
   - "What is the display name?" (shown in game)
   - "What is the description?" (tooltip text explaining effects)

5. **Visual/GFX**
   - "Do you have a custom image, or should I use an existing GFX sprite?"
   - If custom: "What is the image file path?" (e.g., `gfx/interface/ideas/my_idea.png`)
   - If existing: "Which sprite?" (e.g., `generic_production_bonus`)

6. **Effects/Modifiers**
   - "What effects should this idea have?"
   - Consult `references/idea_structure.md` for available modifiers
   - Suggest common effects based on user description
   - Example: "stability boost" → `stability_factor = 0.10`

### Step 2: Confirm Implementation Plan

Present a summary to the user:

```
I will create the following idea:

ID: JAP_economic_boom
Category: country
Name: 経済好況 (Economic Boom)
Description: 経済成長により国家の安定と生産力が向上している。

Effects:
  - stability_factor = 0.10
  - production_speed_industrial_complex_factor = 0.15

Picture: JAP_economic_boom (custom image)
GFX Sprite: GFX_idea_JAP_economic_boom

Files to create/modify:
  1. common/ideas/JAP.txt (add idea definition)
  2. interface/JAP_ideas.gfx (add GFX sprite)
  3. localisation/japanese/JAP_ideas_l_japanese.yml (add localization)

Proceed? (yes/no)
```

### Step 3: Determine File Locations

Based on mod structure, determine where files should be created:

**Idea Definition:**
- Path: `<mod_root>/common/ideas/`
- Filename: Usually `<country_tag>.txt` or existing ideas file
- Check if file exists; if yes, append to it; if no, create new

**GFX Sprite:**
- Path: `<mod_root>/interface/`
- Filename: Usually `<country_tag>_ideas.gfx` or existing .gfx file
- Check if file exists; if yes, append to it; if no, create new

**Localization:**
- Path: `<mod_root>/localisation/<language>/`
- Filename: Usually `<country_tag>_ideas_l_<language>.yml` or existing file
- Check if file exists; if yes, append to it; if no, create new

### Step 4: Implement Idea Definition

Add to `common/ideas/<file>.txt`:

```
ideas = {
    country = {
        <idea_id> = {
            picture = <sprite_name>    # WITHOUT "GFX_idea_" prefix

            modifier = {
                <modifier_1> = <value_1>
                <modifier_2> = <value_2>
            }

            # Optional: Add if needed
            # allowed = { original_tag = <TAG> }
            # cost = 150
            # removal_cost = -1
        }
    }
}
```

**Important:**
- If file already exists and has `ideas = { country = { ... } }`, append inside the `country` block
- Preserve existing formatting and indentation
- Use tabs for indentation (HOI4 convention)

### Step 5: Implement GFX Sprite

Add to `interface/<file>.gfx`:

```
spriteTypes = {
    SpriteType = {
        name = GFX_idea_<sprite_name>    # WITH "GFX_idea_" prefix
        texturefile = "<image_path>"
    }
}
```

**Important:**
- The sprite name MUST start with `GFX_idea_`
- If file exists and has `spriteTypes = { ... }`, append inside the block
- Use the exact image path provided by user

### Step 6: Implement Localization

Add to `localisation/<language>/<file>_l_<language>.yml`:

```yaml
l_<language>:
 <idea_id>:0 "<display_name>"
 <idea_id>_desc:0 "<description>"
```

**Important:**
- File must start with UTF-8 BOM (`﻿`) - if creating new file, ensure proper encoding
- Use format `key:0 "value"` with space after colon
- Append to existing file if present

**Language-specific paths:**
- Japanese: `localisation/japanese/`
- English: `localisation/english/`
- Others: `localisation/<language>/`

### Step 7: Verify Implementation

After creating/modifying files:

1. Confirm all three file types were updated:
   - ✅ Idea definition in `common/ideas/`
   - ✅ GFX sprite in `interface/`
   - ✅ Localization in `localisation/<language>/`

2. Show the user a summary of changes:
   ```
   Created/Modified:
   - common/ideas/JAP.txt (added JAP_economic_boom)
   - interface/JAP_ideas.gfx (added GFX_idea_JAP_economic_boom sprite)
   - localisation/japanese/JAP_ideas_l_japanese.yml (added name and description)

   The idea is ready to use in-game!

   To add this idea to a country, use:
   add_ideas = JAP_economic_boom
   ```

3. Provide usage instructions for common scenarios

## Usage in Game Code

### Adding Idea via National Focus

```
focus = {
    id = JAP_economic_reforms
    ...
    completion_reward = {
        add_ideas = JAP_economic_boom
    }
}
```

### Adding Idea via Event

```
country_event = {
    id = jap.1
    ...
    option = {
        name = jap.1.a
        add_ideas = JAP_economic_boom
    }
}
```

### Removing Idea

```
remove_ideas = JAP_economic_boom
```

### Swapping Ideas

```
swap_ideas = {
    remove_idea = old_idea
    add_idea = new_idea
}
```

## Common Effect Patterns

When user describes desired effects, suggest appropriate modifiers:

**"Stability boost"**
```
modifier = {
    stability_factor = 0.10
}
```

**"Production bonus"**
```
modifier = {
    production_speed_industrial_complex_factor = 0.10
    production_speed_arms_factory_factor = 0.10
}
```

**"Military strength"**
```
modifier = {
    army_org_factor = 0.10
    land_reinforce_rate = 0.05
}
```

**"Political power gain"**
```
modifier = {
    political_power_gain = 0.15
}
```

**"Economic depression"** (negative)
```
modifier = {
    consumer_goods_factor = 0.10
    stability_factor = -0.15
    production_speed_buildings_factor = -0.10
}
```

For complete modifier reference, see `references/idea_structure.md`.

## Handling Multiple Languages

If user requests multiple languages:

1. Ask which languages: "Which languages? (e.g., japanese, english)"
2. For each language, create localization file:
   - `localisation/japanese/<file>_l_japanese.yml`
   - `localisation/english/<file>_l_english.yml`
3. Ask for translations or use the same name if user doesn't specify

## Working with Existing Files

When files already exist:

1. **Read the file first** to understand structure
2. **Append to existing blocks** - don't duplicate `ideas = {}` or `spriteTypes = {}`
3. **Preserve formatting** - match existing indentation style
4. **Check for duplicates** - warn if idea ID already exists

## Reference Documentation

For detailed information on modifiers and idea structure, consult:
- `references/idea_structure.md` - Complete modifier list and examples
- `references/Idea modding - Hearts of Iron 4 Wiki.html` - Full wiki documentation

When suggesting modifiers, grep for specific sections:
```bash
grep -i "stability" references/idea_structure.md
grep -i "production" references/idea_structure.md
```

## Error Prevention

Common mistakes to avoid:

1. **GFX Prefix Mismatch**
   - ❌ `picture = GFX_idea_my_idea` (in ideas file)
   - ✅ `picture = my_idea`
   - ✅ `name = GFX_idea_my_idea` (in .gfx file)

2. **Wrong Localization Path**
   - Always ask user's language preference
   - Use correct directory: `localisation/<language>/`

3. **Indentation Issues**
   - Use tabs, not spaces (HOI4 convention)
   - Match existing file indentation

4. **UTF-8 BOM Missing**
   - Localization files require UTF-8 BOM
   - Check when creating new files

5. **Duplicate IDs**
   - Check if idea ID already exists before creating
   - Warn user if collision detected
