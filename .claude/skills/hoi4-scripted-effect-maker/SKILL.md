---
name: hoi4-scripted-effect-maker
description: Create Hearts of Iron 4 scripted effects through interactive dialogue. Use when the user (1) Requests "create a scripted effect", (2) Wants to make reusable effect blocks, (3) Needs to avoid duplicating effect code, or (4) Says phrases like "make scripted effect", "create effect", "define reusable effect", etc. Handles implementation in common/scripted_effects/ with proper structure and tooltips.
---

# HOI4 Scripted Effect Maker

## Overview

Create HOI4 scripted effects through interactive dialogue. Build reusable effect blocks that can be called from events, focuses, decisions, and other game mechanics.

## When This Skill Triggers

This skill activates when:
- User requests creating a scripted effect
- User wants to make reusable effect code
- User needs to avoid duplicating complex effects
- User says: "create scripted effect", "make reusable effect", "define effect block"

## Interactive Workflow

### Step 1: Gather Basic Information

Ask the user:

1. **Effect Identity**
   - "What should the effect name be?" (e.g., `enact_new_deal`, `grant_industrial_bonus`)

2. **Mod Context**
   - "Which mod?" (to determine file paths)
   - "Which file should this go in?" (or suggest based on purpose)

3. **Scope**
   - "What scope does this effect work in?" (Country, State, Character, etc.)

### Step 2: Define Effect Contents

Ask:
- "What should this effect do?"

**Common effect types:**
- Grant political power/stability/war support
- Add/remove ideas
- Grant buildings/factories
- Modify variables
- Trigger events
- Grant research bonuses

Use `hoi4-modifier-searcher` to find appropriate modifiers if needed.

### Step 3: Determine Tooltip Needs

Ask:
- "Should this have a custom tooltip for players?"
- "What should the tooltip say?"

If yes, create with `custom_effect_tooltip`.

### Step 4: Check for Existing Effects

Use `hoi4-scripted-effect-searcher` to check if similar effect exists:
- Search for effects with similar actions
- Avoid duplicate effect names
- Consider reusing existing effects

### Step 5: Confirm Implementation Plan

Present summary:
```
I will create the following scripted effect:

Name: enact_new_deal
Scope: Country
File: common/scripted_effects/economic_effects.txt

Effect:
- Remove great depression idea
- Add economic recovery idea
- Grant 2 civilian factories
- Add +5% stability
- Add +50 political power

Custom Tooltip: "Implement New Deal economic reforms"

Proceed? (yes/no)
```

### Step 6: Implement Effect

Add to `common/scripted_effects/<file>.txt`:

```
# Country scope
enact_new_deal = {
    custom_effect_tooltip = enact_new_deal_tt
    hidden_effect = {
        if = {
            limit = { has_idea = great_depression }
            remove_ideas = great_depression
        }
        add_ideas = economic_recovery
        random_owned_controlled_state = {
            add_building_construction = {
                type = industrial_complex
                level = 2
                instant_build = yes
            }
        }
        add_stability = 0.05
        add_political_power = 50
    }
}
```

### Step 7: Add Localization (if custom tooltip)

If custom tooltip is used, add to localization:

```yaml
l_japanese:
 enact_new_deal_tt:0 "ニューディール経済改革を実施"
```

### Step 8: Verify Implementation

Confirm:
- ✅ Effect defined in `common/scripted_effects/`
- ✅ Scope documented in comment
- ✅ Custom tooltip localized (if applicable)
- ✅ Effect name is unique

## Common Patterns

### Simple Effect

```
grant_pp_bonus = {
    add_political_power = 100
}
```

### Effect with Tooltip

```
implement_reforms = {
    custom_effect_tooltip = implement_reforms_tt
    hidden_effect = {
        add_stability = 0.05
        add_ideas = reform_spirit
    }
}
```

### Conditional Effect

```
war_or_peace_bonus = {
    if = {
        limit = { has_war = yes }
        add_war_support = 0.10
    }
    else = {
        add_stability = 0.10
    }
}
```

### Cleanup Effect

```
remove_crisis_modifiers = {
    remove_ideas = economic_crisis
    remove_ideas = political_instability
    remove_ideas = military_weakness
}
```

## Integration with Other Skills

### With hoi4-scripted-effect-searcher

Before creating:
1. Search for similar existing effects
2. Reuse if possible
3. Avoid duplicate names

### With hoi4-modifier-searcher

When defining effect contents:
1. Search for appropriate modifiers
2. Use correct modifier syntax
3. Balance effect strength

### With hoi4-nf-creator / hoi4-idea-creator

When completion rewards need complex effects:
1. Create scripted effect first
2. Call it from focus/idea/event:
   ```
   completion_reward = {
       enact_new_deal = yes
   }
   ```

## File Organization

Organize effects by purpose:

- `economic_effects.txt` - Economic bonuses, trade, resources
- `political_effects.txt` - Stability, support, ideology
- `military_effects.txt` - Army, combat, equipment
- `<country>_effects.txt` - Country-specific effects
- `generic_effects.txt` - General-purpose effects

## Calling Scripted Effects

Once created, call effects from:

**National Focuses:**
```
completion_reward = {
    enact_new_deal = yes
}
```

**Events:**
```
option = {
    name = event.1.a
    enact_new_deal = yes
}
```

**Decisions:**
```
complete_effect = {
    enact_new_deal
}
```

## Reference Documentation

For complete syntax and examples:
- `references/scripted_effect_structure.md` - Full structure guide

## Notes

- **Scope is critical** - Always document required scope
- **Unique names** - Effect names must be unique across all files
- **Tooltips** - Use for player-facing effects
- **Reusability** - Create effects for code reuse, not one-time use
- **Testing** - Test effects in different scenarios
