---
name: hoi4-decisions-searcher
version: 1.0.0
description: Helper for searching and analyzing decisions in Hearts of Iron IV mods
tags: [hoi4, modding, decisions, searcher]
---

# HOI4 Decisions Searcher

This skill helps you search and analyze **decisions** in Hearts of Iron IV mods. Quickly find decisions, analyze decision categories, and understand decision mechanics.

## What This Skill Does

- Search for specific decisions by name or ID
- Find decisions by effects or costs
- Analyze decision categories
- Find targeted decisions
- Search by availability conditions
- Locate timed decisions and missions
- Find decision costs and cooldowns

---

## Using This Skill

### Step 1: Ask User What to Search

Ask the user what they want to find:

1. **Search by decision ID/name** - Find specific decision
2. **Search by effect** - Find decisions with specific effects
3. **Search by category** - Find all decisions in a category
4. **Search by type** - Find timed/targeted/mission decisions
5. **Search by cost** - Find decisions by PP cost
6. **Analyze decision file** - Get overview of decision file

---

## Search Patterns

### Search 1: Find Decision by Name

**Ask for:** Decision ID (e.g., `economic_mobilization`)

**Use Grep:**
```
Pattern: economic_mobilization\s*=\s*\{
Path: common/decisions/
Output: content
-B: 2
-A: 40
```

**Explanation:** Shows the entire decision definition

---

### Search 2: Find Decision by Name Pattern

**Ask for:** Search term (e.g., "economic", "military", "diplomatic")

**Use Grep:**
```
Pattern: \w*economic\w*\s*=\s*\{
Path: common/decisions/
Output: content
-B: 2
-A: 40
-i: true
```

**Explanation:** Case-insensitive search for decisions containing the term

---

### Search 3: Find Decisions with Specific Effect

**Ask for:** Effect type (e.g., "add_stability", "declare_war", "add_ideas")

**Use Grep:**
```
Pattern: add_stability
Path: common/decisions/
Output: content
-B: 20
-A: 5
```

**Explanation:** Shows decisions that affect stability (adjust -B to see decision name)

---

### Search 4: Find All Decision Categories

**Use Grep:**
```
Pattern: ^[a-zA-Z_]+\s*=\s*\{
Path: common/decisions/
Output: content
-A: 8
```

**Explanation:** Shows category definitions

---

### Search 5: Find Decisions in Specific Category

**Ask for:** Category name

**Steps:**
1. Find the category in decision files
2. Read the section containing that category
3. List all decisions within

**Use Grep:**
```
Pattern: category_name\s*=\s*\{
Path: common/decisions/
Output: content
-A: 200
```

---

### Search 6: Find Targeted Decisions

**Use Grep:**
```
Pattern: target_trigger\s*=\s*\{
Path: common/decisions/
Output: content
-B: 5
-A: 15
```

**Explanation:** Shows decisions that target other countries

---

### Search 7: Find Timed Decisions

**Use Grep:**
```
Pattern: days_remove\s*=\s*\d+
Path: common/decisions/
Output: content
-B: 5
-A: 10
```

**Explanation:** Shows decisions with completion time

---

### Search 8: Find Mission Decisions

**Use Grep:**
```
Pattern: (days_mission_timeout|is_good\s*=\s*yes)
Path: common/decisions/
Output: content
-B: 10
-A: 10
```

**Explanation:** Shows mission-type decisions

---

### Search 9: Find Decisions by Cost

**Ask for:** Cost value or range

**Use Grep:**
```
Pattern: cost\s*=\s*100
Path: common/decisions/
Output: content
-B: 5
-A: 5
```

---

### Search 10: Find Decisions with Cooldowns

**Use Grep:**
```
Pattern: days_re_enable\s*=\s*\d+
Path: common/decisions/
Output: content
-B: 5
-A: 5
```

**Explanation:** Shows repeatable decisions with cooldowns

---

### Search 11: Find One-Time Decisions

**Use Grep:**
```
Pattern: fire_only_once\s*=\s*yes
Path: common/decisions/
Output: content
-B: 5
-A: 5
```

---

### Search 12: Find State-Targeted Decisions

**Use Grep:**
```
Pattern: state_target\s*=\s*yes
Path: common/decisions/
Output: content
-B: 5
-A: 15
```

---

## Analysis Workflows

### Workflow 1: Analyze Decision Category

**Ask for:** Category name

**Steps:**
1. Find category definition
2. Count decisions in category
3. Identify decision types (timed, targeted, etc.)
4. List all decision IDs

**Report:**
```
Category: economic_decisions
Icon: GFX_decision_category_generic_economy
Decisions found: 5
- economic_mobilization (timed, 30 days)
- war_bonds (repeatable, 90 day cooldown)
- rationing (one-time)
- industrial_expansion (timed, 60 days)
- trade_agreement (targeted)
```

---

### Workflow 2: Find Decision Chain

**Ask for:** Related keyword

**Steps:**
1. Search for all decisions with keyword
2. Check for flag connections
3. Identify chain sequence

---

### Workflow 3: Compare Decision Costs

**Steps:**
1. Search all decisions with cost values
2. Sort by cost
3. Report cost distribution

---

## Common Search Patterns

### Pattern: Find Economic Decisions

```
Pattern: (add_stability|consumer_goods|industrial_capacity|add_offsite_building)
Path: common/decisions/
Output: content
-B: 20
```

### Pattern: Find Military Decisions

```
Pattern: (army_experience|navy_experience|air_experience|add_equipment)
Path: common/decisions/
Output: content
-B: 20
```

### Pattern: Find Diplomatic Decisions

```
Pattern: (add_opinion_modifier|create_faction|diplomatic_relation)
Path: common/decisions/
Output: content
-B: 20
```

### Pattern: Find Research Decisions

```
Pattern: add_tech_bonus
Path: common/decisions/
Output: content
-B: 20
```

---

## Understanding Decision Structure

When you find a decision, explain this structure to the user:

```
category_name = {
    decision_name = {
        icon = GFX_decision_icon       # Icon

        # When decision appears
        visible = {
            has_government = democratic
        }

        # When decision can be taken
        available = {
            has_political_power > 100
        }

        # Cost
        cost = 100

        # Type properties
        fire_only_once = yes           # One-time
        days_remove = 30               # Timed
        days_re_enable = 90            # Cooldown

        # Active modifiers (timed only)
        modifier = {
            stability_factor = 0.05
        }

        # Effects
        complete_effect = {
            add_stability = 0.10
        }

        # AI
        ai_will_do = {
            factor = 1
        }
    }
}
```

---

## Response Format

When providing search results, format like this:

**Decision Found:** `economic_mobilization`
**Category:** `economic_decisions`
**File:** `common/decisions/economic_decisions.txt:45`
**Type:** Timed decision (30 days)
**Cost:** 100 political power
**Cooldown:** 180 days

**Requirements:**
- Has democratic government
- Political power > 100
- Not at war

**Effects:**
- +5% stability (active during 30 days)
- +10% industrial capacity (permanent after completion)

**AI Factor:** 2 (moderate priority, higher when stability low)

---

## Tips for Users

- Decision categories organize decisions into tabs
- `visible` controls when decision appears in menu
- `available` controls when decision can be taken (greyed out if false)
- `cost` is in political power (default) or command power
- `fire_only_once = yes` means one-time decision
- `days_remove` means decision takes time to complete
- `days_re_enable` is cooldown for repeatable decisions
- `modifier` block only works with timed decisions
- Targeted decisions use `target_trigger` for valid targets

---

## Common Use Cases

**Use Case 1:** "Find decisions that give stability"
```
Search for: add_stability in decisions/
```

**Use Case 2:** "What decisions does the economic category have?"
```
Find category definition, read that section
```

**Use Case 3:** "Find all targeted diplomatic decisions"
```
Search for: target_trigger in decisions/
Filter for diplomatic effects
```

**Use Case 4:** "Which decisions have the longest cooldowns?"
```
Search for: days_re_enable
Compare values
```

---

## Reference Files

For detailed information, consult:
- `references/decision_search_examples.md` - Common search examples
- `references/decision_types_guide.md` - Decision type explanations

---

## Limitations

- This skill searches existing decisions, it does not create them
- For creating new decisions, use hoi4-decisions-helper skill
- Complex category analysis may require reading entire files

---

## Tips

- Start with category search to understand organization
- Use -B (before) flag to see decision names
- Use -A (after) flag to see complete effects
- Targeted decisions are more complex, read full definition
- Mission decisions have both success and failure effects
- Check both `complete_effect` and `modifier` blocks
