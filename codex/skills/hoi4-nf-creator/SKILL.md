---
name: hoi4-nf-creator
description: Create Hearts of Iron 4 national focuses through interactive dialogue. Use when the user (1) Requests "create a national focus/NF", (2) Wants to add focuses to a focus tree, (3) Implements focus effects mentioned in mod planning, or (4) Says phrases like "NFを作る", "create national focus", "add focus", "make focus tree", etc. Handles complete implementation including focus definition, icon, localization, and proper tree positioning.
---

# HOI4 National Focus Creator

## Overview

Create complete HOI4 national focuses (国家方針/NF) through interactive dialogue. Guides through defining position, prerequisites, icons, rewards, and automatically implements all required files: focus definition and localization.

## When This Skill Triggers

This skill activates when:
- User explicitly requests creating a national focus
- User wants to add focuses to an existing tree
- While planning mods, user specifies adding national focuses
- User says: "NFを作る", "create national focus", "add focus to tree", "make a new focus"

## Interactive Workflow

### Step 1: Gather Basic Information

Ask the user:

1. **Mod/Country Context**
   - "Which mod?" (to determine file paths)
   - "Which country/focus tree?" (e.g., JAP, GER, generic)

2. **Focus Identity**
   - "What should the focus ID be?" (e.g., `JAP_industrial_expansion`)
   - "What category?" (political, industrial, military, etc.)

3. **Localization Language**
   - "What language(s)?" (japanese, english, etc.)

4. **Focus Name & Description**
   - "What is the display name?"
   - "What is the description?"

### Step 2: Determine Position

Ask about tree position:

**Option A: Absolute Position**
- "What are the X and Y coordinates?" (e.g., x=5, y=2)

**Option B: Relative Position**
- "Which focus should this be relative to?"
- "What offset?" (e.g., x=0, y=1 for directly below)

### Step 3: Define Prerequisites

Ask:
- "Does this focus require any prerequisites?"
- "Which focuses must be completed first?"

**Options:**
- No prerequisites (starting focus)
- Single prerequisite
- Multiple prerequisites (OR logic - need any one)
- Multiple prerequisites (AND logic - need all)

### Step 4: Check for Mutual Exclusivity

Ask:
- "Is this focus mutually exclusive with another focus?" (branching paths)
- "Which focus is the alternative?"

### Step 5: Select Icon

Ask:
- "Which icon should be used?"
- Suggest common icons based on category:
  - Political: `GFX_goal_generic_political_pressure`
  - Industrial: `GFX_goal_generic_production`
  - Military: `GFX_goal_generic_construct_military`
  - Research: `GFX_goal_generic_army_doctrines`

Or use `hoi4-nf-icon-searcher` to find icons.

### Step 6: Define Cost

Ask:
- "What political power cost?" (usually 5 or 10)

Default: 10 for standard focus, 5 for quick focus.

### Step 7: Define Completion Rewards

Ask:
- "What should happen when this focus completes?"

**Common reward types:**
- Add national spirit (use `hoi4-idea-creator` if needed)
- Grant political power
- Add factories/infrastructure
- Research bonus
- Stability/war support
- Unlock decisions

Example dialogue:
```
User: "Grant +10% stability and add an industrial idea"
Assistant: I'll create:
  completion_reward = {
      add_stability = 0.10
      add_ideas = JAP_industrial_expansion
  }
```

Use `hoi4-modifier-searcher` to find appropriate effects.

### Step 8: AI Behavior (Optional)

Ask:
- "What AI weight?" (default: 10)
- "Any conditional AI modifiers?"

### Step 9: Confirm Implementation Plan

Present summary:
```
I will create the following focus:

ID: JAP_industrial_expansion
Name: 産業拡張 (Industrial Expansion)
Description: 工業生産能力を拡大する計画

Position: x=5, y=2 (or relative to JAP_economic_reforms, x=0, y=1)
Icon: GFX_goal_generic_production
Cost: 10

Prerequisites:
  - JAP_economic_reforms

Completion Reward:
  - add_stability = 0.10
  - add_ideas = JAP_industrial_expansion

Files to create/modify:
  1. common/national_focus/<country>.txt (add focus definition)
  2. localisation/japanese/<country>_focus_l_japanese.yml (add localization)

Proceed? (yes/no)
```

### Step 10: Implement Focus Definition

Add to `common/national_focus/<file>.txt`:

```
focus = {
    id = JAP_industrial_expansion
    icon = "GFX_goal_generic_production"
    cost = 10

    x = 5
    y = 2

    prerequisite = { focus = JAP_economic_reforms }

    completion_reward = {
        add_stability = 0.10
        add_ideas = JAP_industrial_expansion
    }

    ai_will_do = {
        factor = 10
    }
}
```

**Important:**
- If file exists and has `focus_tree = { ... }`, append inside the tree
- Preserve existing formatting
- Use tabs for indentation

### Step 11: Implement Localization

Add to `localisation/<language>/<file>_l_<language>.yml`:

```yaml
l_japanese:
 JAP_industrial_expansion:0 "産業拡張"
 JAP_industrial_expansion_desc:0 "工業生産能力を拡大する計画を実行する。"
```

### Step 12: Verify Implementation

Confirm:
- ✅ Focus definition in `common/national_focus/`
- ✅ Localization in `localisation/<language>/`
- ✅ Icon referenced correctly
- ✅ Prerequisites are valid focus IDs

## Common Patterns

### Starting Focus (No Prerequisites)

```
focus = {
    id = JAP_start
    icon = "GFX_goal_generic_political_pressure"
    cost = 10
    x = 5
    y = 0

    completion_reward = {
        add_political_power = 120
    }
}
```

### Branching Path (Mutually Exclusive)

```
focus = {
    id = JAP_democratic_path
    mutually_exclusive = { focus = JAP_fascist_path }
    prerequisite = { focus = JAP_political_crisis }
    # ...
}

focus = {
    id = JAP_fascist_path
    mutually_exclusive = { focus = JAP_democratic_path }
    prerequisite = { focus = JAP_political_crisis }
    # ...
}
```

### Multiple Prerequisites (AND)

```
focus = {
    id = JAP_advanced_focus
    prerequisite = {
        focus = JAP_required_1
        focus = JAP_required_2
    }
    # Requires BOTH focuses
}
```

### Multiple Prerequisites (OR)

```
focus = {
    id = JAP_flexible_focus
    prerequisite = { focus = JAP_option_a }
    prerequisite = { focus = JAP_option_b }
    # Requires EITHER focus
}
```

### Relative Positioning

```
focus = {
    id = JAP_child_focus
    relative_position_id = JAP_parent_focus
    x = 0    # Same column as parent
    y = 1    # One row below parent
    # ...
}
```

## Common Completion Rewards

See `references/nf_structure.md` for complete list.

**Examples:**

```
# Add idea
completion_reward = {
    add_ideas = idea_id
}

# Swap ideas
completion_reward = {
    swap_ideas = {
        remove_idea = old_idea
        add_idea = new_idea
    }
}

# Grant factories
completion_reward = {
    random_owned_controlled_state = {
        add_building_construction = {
            type = industrial_complex
            level = 2
            instant_build = yes
        }
    }
}

# Research bonus
completion_reward = {
    add_tech_bonus = {
        bonus = 0.5
        uses = 2
        category = infantry_weapons
    }
}
```

## Integration with Other Skills

### With hoi4-idea-creator

If completion reward includes adding an idea:
1. Check if idea exists
2. If not, offer to create it using `hoi4-idea-creator`
3. Implement both focus and idea together

### With hoi4-modifier-searcher

When defining completion rewards:
1. Use modifier-searcher to find appropriate effects
2. Suggest modifiers based on focus category
3. Build reward block with selected modifiers

### With hoi4-nf-icon-searcher

When selecting icon:
1. Use nf-icon-searcher to browse available icons
2. Filter by category or keyword
3. Show preview if possible

## Working with Existing Focus Trees

When adding to existing tree:

1. **Read the file first** to understand structure
2. **Check for duplicate IDs** - warn if ID exists
3. **Validate prerequisites** - ensure referenced focuses exist
4. **Check positioning** - avoid coordinate conflicts
5. **Preserve formatting** - match existing indentation

## Reference Documentation

For detailed focus structure and options:
- `references/nf_structure.md` - Complete NF syntax reference

## Notes

- **Cost**: 10 for standard, 5 for quick focuses
- **Position**: Plan tree layout to avoid overlaps
- **Icons**: Use thematically appropriate icons
- **Prerequisites**: Ensure logical progression
- **Localization**: Always provide name and description
- **AI Weight**: Usually 1-100, with 10 as standard
