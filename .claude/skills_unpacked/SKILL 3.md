---
name: hoi4-focus-searcher
version: 1.0.0
description: Helper for searching and analyzing national focus trees in Hearts of Iron IV mods
tags: [hoi4, modding, focus, national_focus, searcher]
---

# HOI4 Focus Searcher

This skill helps you search and analyze **national focus trees** in Hearts of Iron IV mods. Quickly find focuses, analyze focus trees, and understand focus relationships.

## What This Skill Does

- Search for specific focuses by name or ID
- Find focuses by effects or completion rewards
- Analyze focus tree structure
- Find focus prerequisites and dependencies
- Search by country/tag
- Find bypass conditions
- Locate AI factors

---

## Using This Skill

### Step 1: Ask User What to Search

Ask the user what they want to find:

1. **Search by focus ID/name** - Find specific focus
2. **Search by effect** - Find focuses with specific effects
3. **Search by country** - Find all focuses for a country
4. **Search by prerequisite** - Find focus dependencies
5. **Analyze focus tree** - Get overview of a focus tree file

---

## Search Patterns

### Search 1: Find Focus by ID

**Ask for:** Focus ID (e.g., `GER_anschluss`)

**Use Grep:**
```
Pattern: id\s*=\s*GER_anschluss
Path: common/national_focus/
Output: content
-B: 2
-A: 50
```

**Explanation:** Shows the entire focus definition

---

### Search 2: Find Focus by Name Pattern

**Ask for:** Search term (e.g., "anschluss", "military", "industry")

**Use Grep:**
```
Pattern: id\s*=\s*\w*anschluss
Path: common/national_focus/
Output: content
-B: 2
-A: 50
-i: true
```

**Explanation:** Case-insensitive search for focuses containing the term

---

### Search 3: Find Focuses with Specific Effect

**Ask for:** Effect type (e.g., "add_political_power", "declare_war", "add_ideas")

**Use Grep:**
```
Pattern: add_political_power
Path: common/national_focus/
Output: content
-B: 15
-A: 5
```

**Explanation:** Shows focuses that grant political power (adjust -B to see focus ID)

---

### Search 4: Find All Focuses for Country

**Ask for:** Country tag (e.g., GER, SOV, USA)

**Method 1 - By prefix:**
```
Pattern: id\s*=\s*GER_
Path: common/national_focus/
Output: content
-A: 3
```

**Method 2 - By focus tree definition:**
```
Pattern: focus_tree\s*=\s*\{
Path: common/national_focus/
Output: content
-A: 10
```

Then look for country scope or tag restrictions.

---

### Search 5: Find Focus Prerequisites

**Ask for:** Focus ID to find prerequisites FOR

**Use Grep:**
```
Pattern: prerequisite.*=.*\{[^}]*GER_anschluss
Path: common/national_focus/
Output: content
-B: 5
-A: 10
```

**Explanation:** Finds focuses that require GER_anschluss

---

### Search 6: Find Focus Bypass Conditions

**Use Grep:**
```
Pattern: bypass\s*=\s*\{
Path: common/national_focus/
Output: content
-B: 5
-A: 10
```

**Explanation:** Shows all bypass conditions in focus trees

---

### Search 7: Find Mutually Exclusive Focuses

**Use Grep:**
```
Pattern: mutually_exclusive\s*=\s*\{
Path: common/national_focus/
Output: content
-B: 3
-A: 5
```

---

### Search 8: Find Focuses by Cost

**Ask for:** Cost value or range

**Use Grep:**
```
Pattern: cost\s*=\s*10
Path: common/national_focus/
Output: content
-B: 5
-A: 5
```

---

### Search 9: Find Focuses with Available Conditions

**Use Grep:**
```
Pattern: available\s*=\s*\{
Path: common/national_focus/
Output: content
-B: 5
-A: 15
```

**Explanation:** Shows conditional focuses

---

### Search 10: Find All Focus Tree Files

**Use Glob:**
```
Pattern: *.txt
Path: common/national_focus/
```

**Then read specific files for analysis**

---

## Analysis Workflows

### Workflow 1: Analyze Entire Focus Tree

**Steps:**
1. Use Glob to find focus tree file
2. Read the entire file
3. Identify:
   - Focus tree ID
   - Country restrictions
   - Number of focuses
   - Branch structure
   - Shared focuses

**Example:**
```
1. Glob: common/national_focus/*.txt
2. Read: common/national_focus/german_focus.txt
3. Analyze structure and report to user
```

---

### Workflow 2: Find Focus Chain

**Ask for:** Starting focus ID

**Steps:**
1. Find the focus with Grep
2. Note `relative_position_id` values
3. Find focuses that list this focus in prerequisites
4. Build chain forward

---

### Workflow 3: Compare Focus Trees

**Ask for:** Two country tags

**Steps:**
1. Find both focus tree files
2. Read both files
3. Compare:
   - Tree size
   - Focus costs
   - Effect types
   - Shared focuses

---

## Common Search Patterns

### Pattern: Find War-Related Focuses

```
Pattern: (declare_war|create_wargoal|add_war_support)
Path: common/national_focus/
Output: content
-B: 15
```

### Pattern: Find Economic Focuses

```
Pattern: (add_stability|consumer_goods_factor|industrial_capacity)
Path: common/national_focus/
Output: content
-B: 15
```

### Pattern: Find Diplomatic Focuses

```
Pattern: (add_opinion_modifier|create_faction|puppet)
Path: common/national_focus/
Output: content
-B: 15
```

### Pattern: Find Research Focuses

```
Pattern: add_tech_bonus
Path: common/national_focus/
Output: content
-B: 15
```

---

## Understanding Focus Structure

When you find a focus, explain this structure to the user:

```
focus = {
    id = GER_anschluss              # Focus ID
    icon = GFX_goal_anschluss       # Icon
    text = GER_anschluss            # Localization key

    cost = 10                       # Political power cost (days)

    # Position
    x = 0
    y = 1
    relative_position_id = GER_rhineland

    # Prerequisites
    prerequisite = {
        focus = GER_rhineland
    }

    # Mutually exclusive
    mutually_exclusive = {
        focus = GER_oppose_hitler
    }

    # Bypass conditions
    bypass = {
        AUS = { is_in_faction_with = GER }
    }

    # Availability
    available = {
        date > 1938.1.1
    }

    # Effects
    completion_reward = {
        add_political_power = 50
        # More effects...
    }

    # AI behavior
    ai_will_do = {
        factor = 10
    }
}
```

---

## Response Format

When providing search results, format like this:

**Focus Found:** `GER_anschluss`
**File:** `common/national_focus/german_focus.txt:142`
**Cost:** 10 days
**Prerequisites:** GER_rhineland
**Effects:**
- Annex Austria (if they accept)
- Add 50 political power
- Gain cores on Austrian states

**AI Factor:** 10 (high priority)

---

## Tips for Users

- Focus IDs usually follow pattern: `TAG_focus_name`
- Generic focuses shared across countries have `generic_` prefix
- Cost is in days (10 cost = 70 days with 7-day weeks)
- Position (x, y) determines visual location in tree
- `relative_position_id` anchors position to another focus
- Bypass allows skipping focus if conditions met
- `available` makes focus grey until conditions met
- `completion_reward` contains all effects

---

## Common Use Cases

**Use Case 1:** "Find the focus that gives Germany war goals on Poland"
```
Search for: declare_war.*POL or create_wargoal.*POL in german_focus.txt
```

**Use Case 2:** "What focuses does Germany have for industry?"
```
Search for: industrial_complex or factory in german_focus.txt
```

**Use Case 3:** "Which focuses require Rhineland to be completed?"
```
Search for: prerequisite.*GER_rhineland
```

**Use Case 4:** "Show me all shared focuses"
```
Search for: shared_focus in all focus files
```

---

## Reference Files

For detailed information, consult:
- `references/focus_properties_reference.md` - All focus properties explained
- `references/focus_search_examples.md` - Common search examples

---

## Limitations

- This skill searches existing focuses, it does not create them
- For creating new focuses, use a dedicated focus creator skill
- Complex tree analysis may require reading entire files

---

## Tips

- Start with broad searches, narrow down
- Use -B (before) flag to see focus IDs
- Use -A (after) flag to see effects
- Read entire file for full tree analysis
- Check both `completion_reward` and `available` for full picture
