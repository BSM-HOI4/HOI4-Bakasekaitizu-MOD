---
name: hoi4-modifier-maker
description: Build Hearts of Iron 4 modifier blocks (regular or dynamic) interactively through dialogue. Use when the user (1) Requests "create a modifier block" or "create dynamic modifier", (2) Wants to build effects for an idea/focus/decision, (3) Needs help combining modifiers appropriately, (4) Says phrases like "make modifiers for...", "build a buff for...", "create effects for economic idea", "make dynamic modifier", etc. Supports both static modifiers and variable-based dynamic modifiers.
---

# HOI4 Modifier Maker

## Overview

Build HOI4 modifier blocks (regular or dynamic) interactively by selecting effects, setting values, and combining them appropriately. Supports both static modifier blocks for ideas/focuses and dynamic modifiers that use variables and conditions. Generates ready-to-use code.

## When This Skill Triggers

This skill activates when:
- User requests to create a modifier block
- User wants to build game effects but needs guidance
- User asks for help combining modifiers appropriately
- User says: "make modifiers for production", "create economic buff", "build military modifier block"

## Interactive Workflow

### Step 1: Understand the Goal

Ask the user what type of effect they want:

**Question:** "What type of modifier block do you want to create?"

**Common responses:**
- Economic boost/penalty
- Military buff/debuff
- Naval/air improvements
- Political effects
- Mixed/hybrid effects

### Step 1.5: Choose Static or Dynamic Modifier

Ask the user:

**Question:** "Do you want to create a static modifier block or a dynamic modifier?"

**Static modifiers:**
- Fixed values that never change
- Used in ideas, focuses, decisions
- Simpler to implement
- Example: `stability_factor = 0.10`

**Dynamic modifiers:**
- Values can use variables
- Can have enable/remove conditions
- Update daily or when forced
- More complex but flexible
- Example: `stability_factor = var_stability_bonus`

**When to recommend dynamic:**
- User mentions "scaling", "progressive", "variable"
- Effect should change based on conditions
- Building progression systems
- Temporary effects with auto-removal

**When to recommend static:**
- Simple, permanent effects
- Traditional national spirit behavior
- No complex conditions needed

If **dynamic**, continue with dynamic modifier workflow (see Dynamic Modifier Workflow section).
If **static**, continue with Step 2 below.

### Step 2: Determine Theme and Scope

Based on the user's goal, determine the theme:

**Economic themes:**
- Production boost
- Industrial expansion
- Resource efficiency
- Economic crisis/depression

**Military themes:**
- Offensive power
- Defensive strength
- Training efficiency
- Total mobilization

**Political themes:**
- Stability boost
- Ideology shift
- Political turmoil
- War support

**Hybrid themes:**
- Total war economy
- Peacetime prosperity
- Military-industrial complex

### Step 3: Suggest Template or Custom Build

**Option A: Use Template**

If the user's request matches a template, suggest it:

"I can use the 'Economic Boom' template which includes:
- stability_factor = 0.10
- production_speed_industrial_complex_factor = 0.15
- industrial_capacity_factory = 0.10

Would you like to use this, or customize it?"

See `references/modifier_templates.md` for all templates.

**Option B: Build Custom**

If custom, proceed to gather modifiers:

1. Use `hoi4-modifier-searcher` to find relevant modifiers
2. Ask user which specific effects they want
3. Suggest appropriate values

### Step 4: Select Modifiers

For each desired effect, help user choose appropriate modifiers:

**Example dialogue:**
```
User: "I want to boost production"
Assistant: Let me search for production modifiers...
[Uses modifier-searcher]

Found these options:
1. production_speed_industrial_complex_factor - Civilian factory construction
2. production_speed_arms_factory_factor - Military factory construction
3. production_speed_buildings_factor - All construction
4. industrial_capacity_factory - Factory output

Which would you like to include?
```

### Step 5: Determine Values

For each selected modifier, suggest appropriate values:

**Guideline questions:**
- "Should this be a minor, standard, or major buff?"
- "Is this a temporary or permanent effect?"
- "Should there be any trade-offs (negative effects)?"

**Value suggestions:**
- **Minor:** 0.05 (5%)
- **Standard:** 0.10 (10%)
- **Major:** 0.15-0.20 (15-20%)
- **Extreme:** 0.25+ (use sparingly)

### Step 6: Build and Present the Modifier Block

Assemble the modifier block and show it to the user:

```
Here's your modifier block:

modifier = {
    stability_factor = 0.10
    production_speed_industrial_complex_factor = 0.15
    industrial_capacity_factory = 0.10
}

This provides:
- +10% stability
- +15% civilian factory construction speed
- +10% factory output

Would you like to adjust any values or add/remove modifiers?
```

### Step 7: Offer Refinement

Ask if the user wants to:
- Adjust values
- Add more modifiers
- Remove modifiers
- Add negative effects for balance

Iterate until satisfied.

### Step 8: Provide Final Code

Present the final modifier block in proper format:

```
modifier = {
    stability_factor = 0.10
    production_speed_industrial_complex_factor = 0.15
    industrial_capacity_factory = 0.10
}
```

## Dynamic Modifier Workflow

When user chooses **dynamic modifier** in Step 1.5, follow this workflow:

### D1: Define Modifier Identity

Ask:
- "What should the modifier name be?" (e.g., `economic_recovery_modifier`)
- "What scope?" (Country, State, Unit Leader)

### D2: Determine Enable Conditions

Ask: "When should this modifier be active?"

**Common conditions:**
- `always = yes` - Always active
- `has_war = yes` - Only during war
- `has_idea = X` - When specific idea exists
- `check_variable = { var > 0.5 }` - When variable meets condition

Example:
```
enable = {
    has_war = yes
    NOT = { has_idea = pacifism }
}
```

### D3: Determine Remove Trigger (Optional)

Ask: "Should this auto-remove under certain conditions?"

**Common remove conditions:**
- `has_stability > 0.50` - When stability is high
- `has_war = no` - When war ends
- `check_variable = { var < 0.01 }` - When variable is too low

Example:
```
remove_trigger = {
    has_stability > 0.50
}
```

### D4: Select Modifiers and Values

Ask: "Should modifier values be static or variable-based?"

**Static values:**
```
industrial_capacity_factory = 0.10
```

**Variable-based values:**
```
industrial_capacity_factory = var_production_bonus
stability_factor = var_stability_level
```

Use `hoi4-modifier-searcher` to find appropriate modifiers.

### D5: Icon Selection

Ask: "What icon should represent this modifier?"

Suggest: `GFX_idea_generic_production`, `GFX_idea_generic_fortify`, etc.

### D6: Build and Present Dynamic Modifier

Show complete definition:

```
Here's your dynamic modifier definition:

File: common/dynamic_modifiers/economic_modifiers.txt

economic_recovery_modifier = {
    enable = {
        NOT = { has_idea = great_depression }
    }
    remove_trigger = {
        check_variable = { var_recovery_level < 0.01 }
    }
    icon = GFX_idea_generic_production

    # Variable-based modifiers
    industrial_capacity_factory = var_recovery_level
    stability_factor = var_recovery_stability

    # Static modifiers
    consumer_goods_factor = -0.05
}
```

### D7: Show Usage Code

Present how to use the dynamic modifier:

```
To use this modifier:

1. Set variables first:
effect = {
    set_variable = { var_recovery_level = 0.10 }
    set_variable = { var_recovery_stability = 0.05 }
}

2. Add the modifier:
add_dynamic_modifier = {
    modifier = economic_recovery_modifier
}

3. Update variables later:
effect = {
    add_to_variable = { var_recovery_level = 0.05 }
    force_update_dynamic_modifier = yes
}

4. Remove when done:
remove_dynamic_modifier = {
    modifier = economic_recovery_modifier
}
```

### D8: Offer Refinement

Ask if user wants to:
- Adjust enable/remove conditions
- Change static/variable values
- Add more modifiers
- Change scope

See `references/dynamic_modifier_guide.md` for complete syntax and examples.

## Using Templates

For common use cases, suggest templates from `references/modifier_templates.md`:

### Template Categories

**Economic:**
- Economic Boom
- Industrial Focus
- Resource Efficiency
- Economic Depression

**Military:**
- Military Readiness
- Offensive Doctrine
- Defensive Posture
- Total Mobilization

**Naval:**
- Naval Supremacy
- Submarine Warfare
- Fleet Expansion

**Political:**
- Internal Stability
- Political Turmoil
- Ideological Shift

**Hybrid:**
- Total War Economy
- Peacetime Prosperity
- Military-Industrial Complex

### When to Use Templates

Use templates when user requests match common patterns:

**User says:** "Create an economic boom modifier"
**Response:** "I'll use the Economic Boom template..."

**User says:** "Make military buffs"
**Response:** "Let me suggest the Military Readiness template..."

### Customizing Templates

Templates can be customized:

1. Start with template
2. Ask user if they want to adjust values
3. Ask if they want to add/remove specific modifiers
4. Present customized version

## Integration with Other Skills

### With hoi4-modifier-searcher

Use searcher to find appropriate modifiers:

```
User: "I want factory bonuses"
1. Run: python3 scripts/search_modifiers.py --search factory
2. Present options to user
3. Build modifier block with selected options
```

### With hoi4-idea-creator

Modifier-maker output integrates directly into idea-creator:

```
1. User requests idea creation
2. Use modifier-maker to build modifier block
3. Pass modifier block to idea-creator
4. Complete idea implementation
```

## Value Balancing Guidelines

### Standard Ranges

**Political:**
- Stability: 0.05 to 0.15
- War support: 0.05 to 0.20
- Political power: 0.10 to 0.25

**Economy:**
- Construction speed: 0.10 to 0.20
- Factory output: 0.05 to 0.15
- Efficiency: 0.10 to 0.20

**Military:**
- Combat stats: 0.10 to 0.20
- Organization: 0.05 to 0.15
- Training time: -0.10 to -0.20 (negative = faster)

### Combining Multiple Effects

When combining modifiers:

**Good balance (3-5 modifiers):**
```
modifier = {
    stability_factor = 0.10
    production_speed_industrial_complex_factor = 0.15
    industrial_capacity_factory = 0.10
}
```

**Too many (avoid):**
```
modifier = {
    # 10+ modifiers - overwhelming
}
```

**Add trade-offs for realism:**
```
modifier = {
    production_speed_arms_factory_factor = 0.20  # benefit
    consumer_goods_factor = 0.05                 # cost
}
```

## Common Request Patterns

### "Make an economic modifier"

1. Suggest Economic Boom template or ask for specifics
2. If custom, search for production/factory/stability modifiers
3. Combine 3-4 appropriate modifiers
4. Use values around 0.10-0.15

### "Create military buffs"

1. Ask: offensive, defensive, or general?
2. Search military category modifiers
3. Suggest attack/defense/org/training modifiers
4. Use values around 0.10-0.15

### "Build a debuff/penalty"

1. Ask what area should be weakened
2. Find relevant modifiers
3. Use negative values or positive for consumer_goods_factor
4. Suggest values: -0.10 to -0.20

### "Mixed economic and military"

1. Suggest Total War Economy or Military-Industrial Complex template
2. Or build custom with both categories
3. Balance between economic and military effects
4. Use moderate values: 0.05-0.10 each

### "Create a scaling/progressive modifier"

1. Recommend dynamic modifier with variables
2. Ask what should trigger scaling (time, victories, economic milestones)
3. Define variable-based modifiers
4. Show how to increment variables over time
5. Example: Industrial growth that increases with each factory built

### "Make a temporary wartime bonus"

1. Recommend dynamic modifier with enable condition
2. Set enable: `has_war = yes`
3. Set remove_trigger: `has_war = no`
4. Use higher values since it's temporary
5. Example: War economy that auto-removes at peace

### "Build a conditional modifier"

1. Use dynamic modifier with specific enable conditions
2. Ask what conditions should activate it
3. Define enable trigger precisely
4. Consider remove_trigger for cleanup
5. Example: Defensive bonus only when under attack

## Error Prevention

### Common Mistakes to Avoid

**Too many modifiers:**
- Limit to 3-5 for clarity
- More modifiers = harder to balance

**Extreme values:**
- Avoid >0.30 unless intentional
- Game can become unbalanced

**Unthemed combinations:**
- Keep modifiers thematically related
- Don't mix unrelated effects randomly

**Missing trade-offs:**
- Pure buffs are less interesting
- Consider small penalties for balance

## Reference Documentation

For static modifiers:
- `references/modifier_templates.md` - Pre-built modifier combinations for common use cases

For dynamic modifiers:
- `references/dynamic_modifier_guide.md` - Complete guide to dynamic modifiers with variables, conditions, and examples

For finding specific modifiers:
- Use `hoi4-modifier-searcher` skill to search available modifiers

## Example Workflows

### Workflow 1: Template-Based

```
User: "Create economic growth modifiers"