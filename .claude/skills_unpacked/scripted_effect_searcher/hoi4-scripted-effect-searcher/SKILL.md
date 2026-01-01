---
name: hoi4-scripted-effect-searcher
description: Search for Hearts of Iron 4 scripted effects in mod files. Use when the user (1) Asks "what scripted effects are available?", (2) Wants to find a specific scripted effect, (3) Needs to know what effects exist in the codebase, or (4) Says phrases like "search for scripted effect", "find effect", "list available effects", etc. Searches through common/scripted_effects/ directory using Grep tool.
---

# HOI4 Scripted Effect Searcher

## Overview

Search for scripted effects defined in `common/scripted_effects/` files. Quickly find reusable effect blocks by name or keyword using Grep searches.

## When This Skill Triggers

This skill activates when:
- User asks about available scripted effects
- User wants to find a specific effect by name
- User needs to know what effects are defined in the mod
- User says: "search scripted effects", "find effect X", "what effects exist?"

## Search Methods

### Method 1: Grep Search by Name

Use Grep tool to search for scripted effect definitions:

```
Pattern: ^[a-zA-Z_][a-zA-Z0-9_]*\s*=
Path: common/scripted_effects/
Type: txt
```

This finds all effect definitions in the format `effect_name = { ... }`.

### Method 2: Search by Keyword

Search for effects containing specific keywords:

```
Pattern: keyword
Path: common/scripted_effects/
-A: 5  (show 5 lines after match)
```

### Method 3: Find Specific Effect

Search for a specific effect name:

```
Pattern: ^effect_name\s*=
Path: common/scripted_effects/
```

## Common Search Patterns

### Find Effects with Certain Actions

**Add ideas:**
```
Pattern: add_ideas
Path: common/scripted_effects/
-B: 2  (show effect name context)
```

**Grant factories:**
```
Pattern: add_building_construction
Path: common/scripted_effects/
-B: 2
```

**Custom tooltips:**
```
Pattern: custom_effect_tooltip
Path: common/scripted_effects/
-B: 2
```

## Example Workflows

### "Does an effect for X exist?"

User asks: "Is there a scripted effect for removing ministers?"

Use Grep tool:
```
Pattern: remove.*minister
Path: common/scripted_effects/
-i: true (case insensitive)
```

### "What effects grant political power?"

```
Pattern: add_political_power
Path: common/scripted_effects/
-B: 3  (show effect name)
```

### "List all effects in a file"

Use Read tool to read the file, then search for lines starting with effect names.

## Integration with Other Skills

### With hoi4-scripted-effect-maker

1. Search for similar existing effects before creating new ones
2. Use found effects as templates
3. Avoid duplicate effect names

### With hoi4-nf-creator / hoi4-idea-creator

When defining effects:
1. Search for existing scripted effects first
2. Reuse common patterns
3. Call scripted effects to avoid code duplication

## Understanding Results

When an effect is found, note:

1. **Effect Name** - The identifier (e.g., `remove_all_ministers`)
2. **File Location** - Which file it's defined in
3. **Scope** - Country scope, State scope, etc. (usually in comments)
4. **Contents** - What the effect does

## Notes

- Scripted effects are in `common/scripted_effects/`
- Each file can contain multiple effects
- Effect names must be unique across all files
- Effects are called with: `effect_name = yes` or just `effect_name`
- Always use Grep tool, not Bash grep commands
