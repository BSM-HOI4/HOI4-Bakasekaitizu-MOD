---
name: hoi4-opinion-modifiers-helper
version: 1.0.0
description: Helper for creating and managing opinion modifiers in Hearts of Iron IV mods - diplomatic relationship modifiers between countries
tags: [hoi4, modding, opinion, diplomacy, relations]
---

# HOI4 Opinion Modifiers Helper

This skill helps you create and manage **opinion modifiers** in Hearts of Iron IV mods. Opinion modifiers define how countries view each other, affecting diplomatic interactions, AI decisions, and trade relations.

## What are Opinion Modifiers?

Opinion modifiers are diplomatic relationship modifiers that:
- Affect opinion values between countries (-200 to +200)
- Control trade permissions (embargoes)
- Influence AI diplomatic decisions
- Can decay over time or be permanent
- Are defined in `common/opinion_modifiers/`

## File Structure

Opinion modifiers are defined in `.txt` files in `common/opinion_modifiers/`:

```
opinion_modifiers = {
    modifier_name = {
        value = X           # Opinion change (-200 to +200)
        trade = yes/no      # Whether this blocks trade (optional)
        decay = X           # How much decays per period (optional)
        months/years/days = X  # Duration before decay starts (optional)
        min_trust = X       # Minimum trust level (optional)
        max_trust = X       # Maximum trust level (optional)
    }
}
```

---

## Using This Skill

### Step 1: Choose Action

Ask the user what they want to do:

1. **Create new opinion modifier** - Design a new diplomatic relationship modifier
2. **Find existing modifiers** - Search for modifiers in your mod
3. **Explain modifier mechanics** - Learn about decay, trade, and trust systems

---

## Action 1: Create New Opinion Modifier

### Step 1.1: Gather Information

Ask the user:

1. **Modifier name**: What should the modifier be called?
   - Example: `SSW_friendly`, `GER_trade_agreement`, `war_aggression`
   - Convention: Use descriptive names, often prefixed with country tag

2. **Opinion value**: How much should this change opinion?
   - Positive values (1-200): Improve relations
   - Negative values (-1 to -200): Worsen relations
   - Common values:
     - Small: ±10-25
     - Medium: ±30-50
     - Large: ±60-100
     - Extreme: ±100-200

3. **Duration type**: Should this modifier be permanent or temporary?
   - **Permanent**: No decay, lasts until removed
   - **Temporary**: Decays over time
   - **Timed**: Lasts for a specific duration then disappears

### Step 1.2: Configure Decay (if temporary)

If the modifier is temporary, ask:

1. **Duration**: How long should it last?
   - `months = X` (most common)
   - `years = X`
   - `days = X`

2. **Decay rate**: How much should it decay per time period?
   - `decay = 1` - Decays by 1 per month (if months specified)
   - `decay = 5` - Decays by 5 per month
   - `decay = 0` - No decay (permanent)

**Example calculation:**
```
value = 50
months = 10
decay = 5

# Result: Starts at +50, decays by 5 each month, gone after 10 months
```

### Step 1.3: Special Properties (Optional)

Ask if the modifier needs any special properties:

1. **Trade restriction**: Should this block trade between countries?
   - `trade = yes` - Blocks trade (embargo)
   - `trade = no` or omit - Allows trade

2. **Trust bounds**: Should this affect trust levels?
   - `min_trust = X` - Minimum trust level
   - `max_trust = X` - Maximum trust level

### Step 1.4: Choose File Location

Ask the user:

**Question:** "Where should this modifier be saved?"

Options:
- **Country-specific file**: `common/opinion_modifiers/[TAG]_opinion_modifiers.txt`
  - Use when modifiers are specific to one country
  - Example: `GER_opinion_modifiers.txt` for German-specific modifiers

- **Feature/system file**: `common/opinion_modifiers/_[system]_opinion_modifiers.txt`
  - Use when modifiers are part of a specific system
  - Example: `_economic_alliance_opinion_modifiers.txt`

- **Generic file**: `common/opinion_modifiers/_generic_opinion_modifiers.txt`
  - Use for shared/reusable modifiers

### Step 1.5: Generate Code

Generate the opinion modifier definition:

```
opinion_modifiers = {
    [modifier_name] = {
        value = [value]
        [trade = yes]  # If trade restriction
        [months = X]   # If temporary
        [decay = X]    # If temporary
        [min_trust = X]  # If specified
        [max_trust = X]  # If specified
    }
}
```

**Real Example from SSW_mod:**
```
SSW_friendly = {
    value = 50
    months = 12
    decay = 1
}

ssw_new_emb = {
    trade = yes
    value = -90
}

GER_returned_north_france = {
    value = 100
}
```

### Step 1.6: Add to File

Use the Edit tool to add the modifier to the chosen file:

1. If file doesn't exist, create it with:
   ```
   opinion_modifiers = {
       [new modifier here]
   }
   ```

2. If file exists, add the new modifier inside the `opinion_modifiers = { }` block

### Step 1.7: Create Localization

Opinion modifiers need localization entries. Ask if the user wants to create them:

**File location:** `localisation/[language]/[filename]_l_[language].yml`

**Format:**
```yaml
l_japanese:
 [modifier_name]:0 "[Display Name]"
 [modifier_name]_desc:0 "[Description of why this opinion modifier was applied]"
```

**Example:**
```yaml
l_japanese:
 SSW_friendly:0 "友好的な関係"
 SSW_friendly_desc:0 "両国の友好的な外交関係を反映しています。"

 ssw_new_emb:0 "禁輸措置"
 ssw_new_emb_desc:0 "貿易を制限する禁輸措置が発動されています。"
```

### Step 1.8: Usage Examples

Explain how to apply this modifier in events, decisions, or focuses:

**In Effects:**
```
# Add opinion modifier
FROM = {
    add_opinion_modifier = {
        target = ROOT
        modifier = [modifier_name]
    }
}

# Remove opinion modifier
FROM = {
    remove_opinion_modifier = {
        target = ROOT
        modifier = [modifier_name]
    }
}

# Reverse (both directions)
add_opinion_modifier = {
    target = GER
    modifier = SSW_friendly
}
reverse_add_opinion_modifier = {
    target = GER
    modifier = SSW_friendly
}
```

**In Triggers (checking if modifier exists):**
```
has_opinion_modifier = {
    target = GER
    modifier = SSW_friendly
}
```

---

## Action 2: Find Existing Modifiers

### Search for Opinion Modifiers

Use Grep to find existing modifiers in your mod:

#### Find All Modifiers in a File

```
Pattern: ^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*\{
Path: common/opinion_modifiers/
Output: files_with_matches
```

#### Search by Value Range

Find modifiers with specific opinion values:

**Positive modifiers (friendly):**
```
Pattern: value\s*=\s*[0-9]+
Path: common/opinion_modifiers/
Output: content
```

**Negative modifiers (hostile):**
```
Pattern: value\s*=\s*-[0-9]+
Path: common/opinion_modifiers/
Output: content
```

#### Find Trade-Blocking Modifiers

```
Pattern: trade\s*=\s*yes
Path: common/opinion_modifiers/
Output: content
-B: 2
```

#### Find Decaying Modifiers

```
Pattern: decay\s*=\s*[0-9]+
Path: common/opinion_modifiers/
Output: content
-B: 3
```

### Read Specific File

Once you've found relevant files, use Read to examine them:

```
Read common/opinion_modifiers/[filename].txt
```

---

## Action 3: Explain Modifier Mechanics

### Decay System

Opinion modifiers can decay over time:

```
protest_action = {
    value = -25      # Starts at -25 opinion
    months = 12      # Lasts for 12 months
    decay = 1        # Decays by 1 per month
}
```

**Behavior:**
- Month 0: -25 opinion
- Month 1: -24 opinion
- Month 2: -23 opinion
- ...
- Month 12: -13 opinion
- After 12 months: Modifier removed

### Permanent Modifiers

Modifiers without decay or duration are permanent:

```
bsm_economic_alliance_relation_boost = {
    value = 15
    decay = 0  # Explicitly permanent
}

# Or simply:
holds_our_cores = {
    value = -30  # No decay/duration = permanent until removed
}
```

### Trade Restrictions

The `trade` property controls whether countries can trade:

```
ssw_new_emb = {
    trade = yes      # This blocks trade
    value = -90
}
```

**Important:**
- `trade = yes` means "block trade" (embargo)
- Used for sanctions, embargoes, economic warfare
- Usually combined with negative opinion value

### Trust System

Trust affects AI behavior in alliances and guarantees:

```
justifying_war_goal = {
    value = -10
    min_trust = -10  # Reduces minimum trust
    days = 10
    decay = 1
}
```

- `min_trust`: Affects how much AI trusts you (lower = less trust)
- `max_trust`: Maximum trust level
- Influences AI acceptance of diplomatic actions

### Opinion Value Guidelines

**Positive Values (Improving Relations):**
- +10-25: Minor positive event (trade deals, minor cooperation)
- +30-50: Significant positive event (alliance, major agreement)
- +60-100: Major positive event (liberation, major territorial return)
- +100-200: Extreme positive event (saving from destruction, vital assistance)

**Negative Values (Worsening Relations):**
- -10-25: Minor negative event (minor disagreement, small claim)
- -30-50: Significant negative event (broken promise, hostile act)
- -60-100: Major negative event (aggression, major betrayal)
- -100-200: Extreme negative event (war crimes, existential threat)

**Real Examples from SSW_mod:**
```
SSW_like = {
    value = 10           # Minor friendship
}

SSW_friendly = {
    value = 50           # Significant friendship
    months = 12
    decay = 1
}

SSW_angry = {
    value = -100         # Major hostility
}

GER_returned_north_france = {
    value = 100          # Honoring a major promise
}

GER_not_returned_north_france = {
    value = -200         # Breaking a major promise
}
```

---

## Common Patterns

### Pattern 1: Simple Permanent Modifier

```
TAG_friendship = {
    value = 50
}
```

### Pattern 2: Decaying Modifier

```
TAG_diplomatic_incident = {
    value = -50
    months = 24
    decay = 2
}
```

### Pattern 3: Embargo/Sanctions

```
TAG_economic_sanctions = {
    trade = yes
    value = -60
    months = 12
}
```

### Pattern 4: Event-Based Trust Impact

```
TAG_broken_promise = {
    value = -100
    min_trust = -50
    months = 36
}
```

### Pattern 5: Tiered Modifiers

Create multiple variants for different intensities:

```
OAS_hostility_25 = {
    value = -25
}

OAS_hostility_30 = {
    value = -30
}

OAS_hostility_50 = {
    value = -50
}
```

### Pattern 6: System-Specific Modifiers

For custom systems like economic alliances:

```
bsm_economic_alliance_relation_boost = {
    value = 15
    decay = 0
}
```

---

## Best Practices

1. **Naming Convention**
   - Use descriptive names
   - Prefix with country tag or system name
   - Use lowercase with underscores

2. **Value Balance**
   - Don't overuse extreme values (±100+)
   - Consider decay for temporary events
   - Match value to event importance

3. **Organization**
   - Group related modifiers in same file
   - Country-specific modifiers in country files
   - System modifiers in system files

4. **Localization**
   - Always provide localization
   - Explain why the modifier exists
   - Use appropriate tone for positive/negative

5. **Testing**
   - Test decay calculations
   - Verify trade restrictions work
   - Check AI behavior with trust modifiers

---

## Common Use Cases

### Diplomatic Events
```
GER_conference_success = {
    value = 30
    months = 12
    decay = 1
}
```

### War and Aggression
```
war_aggression = {
    value = -75
    months = 24
}
```

### Trade Agreements
```
TAG_trade_agreement = {
    value = 20
}
```

### Territory Returns
```
TAG_returned_territory = {
    value = 60
}

TAG_refused_territory = {
    value = -20
}
```

### Alliance Systems
```
alliance_member_bonus = {
    value = 15
    decay = 0
}
```

---

## Reference Files

For detailed information, consult:
- `references/opinion_mechanics.md` - Complete mechanics reference
- `references/usage_patterns.md` - Common usage patterns and examples

---

## Tips

- Opinion affects AI decisions (join faction, accept trade, etc.)
- Values stack - multiple modifiers add together
- Decay happens monthly by default
- Trade restriction is powerful - use sparingly
- Test with different AI personalities
