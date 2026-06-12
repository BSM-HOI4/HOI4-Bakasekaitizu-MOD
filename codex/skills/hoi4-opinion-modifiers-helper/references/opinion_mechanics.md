# Opinion Modifiers - Complete Mechanics Reference

## Core Properties

### value

The core opinion change applied to diplomatic relations.

**Range:** -200 to +200

**Behavior:**
- Positive values improve relations
- Negative values worsen relations
- Values stack if multiple modifiers are active
- Affects AI diplomatic decisions

**Examples:**
```
cheat_opinion_modifier_good = {
    value = 200  # Maximum positive opinion
}

cheat_opinion_modifier_bad = {
    value = -200  # Maximum negative opinion
}

holds_our_cores = {
    value = -30  # Moderate negative opinion
}
```

---

## Duration and Decay

### months / years / days

Defines how long the modifier lasts before decay starts or completes.

**Syntax:**
- `months = X` - Most common, lasts X months
- `years = X` - Lasts X years
- `days = X` - Lasts X days

**Examples:**
```
short_term = {
    value = -25
    months = 6  # Lasts 6 months
}

long_term = {
    value = 50
    years = 2  # Lasts 2 years (24 months)
}

very_short = {
    value = -10
    days = 30  # Lasts 30 days
}
```

### decay

How much the opinion value decreases per time period (usually monthly).

**Behavior:**
- `decay = 0` - Permanent modifier (no decay)
- `decay = 1` - Decreases by 1 per period
- `decay = X` - Decreases by X per period
- Decay removes modifier when value reaches 0

**Examples:**
```
# Gradual decay
protest_action = {
    value = -25
    months = 12
    decay = 1
    # Month 0: -25, Month 1: -24, ..., Month 12: -13
    # After 12 months: Removed
}

# Fast decay
quick_forgiveness = {
    value = -50
    months = 10
    decay = 5
    # Month 0: -50, Month 1: -45, Month 2: -40, ...
    # Reaches 0 at month 10
}

# No decay (permanent)
permanent_hostility = {
    value = -100
    decay = 0
}
```

### Decay Calculation

**Formula:**
```
Current Value = Initial Value - (decay × elapsed_periods)
```

**Example:**
```
GER_bought_fighter = {
    value = 10
    months = 2
}

# No decay specified, so modifier is removed after 2 months
# Month 0: +10
# Month 1: +10
# Month 2: Removed
```

**With decay:**
```
our_liberators = {
    value = 40
    months = 18
    decay = 1
}

# Month 0: +40
# Month 1: +39
# Month 2: +38
# ...
# Month 18: +22
# After 18 months: Continues to decay until 0
```

---

## Trade Restrictions

### trade

Controls whether countries can trade with each other.

**Values:**
- `trade = yes` - **Blocks trade** (embargo/sanctions)
- `trade = no` or omitted - Allows trade

**Important:** `trade = yes` means "restrict trade" (counter-intuitive!)

**Examples:**
```
# Embargo
ssw_new_emb = {
    trade = yes      # Blocks trade
    value = -90      # Also hurts opinion
}

# Severe embargo with faction implications
faction_traitor_trade = {
    trade = yes
    value = -40
}

# Normal hostile modifier (trade still allowed)
faction_traitor = {
    value = -75
    # No trade restriction
}
```

**Usage Context:**
- Economic warfare
- Sanctions systems
- Punishment for betrayal
- Isolation mechanics

---

## Trust System

### min_trust

Sets the minimum trust level in diplomatic relations.

**Behavior:**
- Affects AI willingness to form alliances
- Influences guarantee acceptance
- Impacts faction joining decisions
- Lower values = less trust

**Example:**
```
justifying_war_goal = {
    value = -10
    min_trust = -10  # Also reduces trust
    days = 10
    decay = 1
}
```

### max_trust

Sets the maximum trust level in diplomatic relations.

**Behavior:**
- Caps how much AI trusts you
- Rare in vanilla HOI4
- Used for special diplomatic situations

**Example:**
```
suspicious_ally = {
    value = 20
    max_trust = 50  # Can't trust fully despite good opinion
}
```

### Trust vs Opinion

- **Opinion**: How much a country likes/dislikes you (-200 to +200)
- **Trust**: How reliable AI considers you (affects diplomatic actions)
- **Relationship**: Both opinion and trust affect AI behavior

---

## Modifier Stacking

Multiple opinion modifiers stack together.

**Example:**
```
# Country A has these modifiers toward Country B:
SSW_friendly = {
    value = 50
}

SSW_thanks = {
    value = 30
}

TAG_friend_country = {
    value = 50
}

# Total opinion: +130
```

**Decay with Stacking:**
```
# Turn 0:
SSW_friendly (50, decays 1/month) = +50
GER_trade_agreement (20, permanent) = +20
Total: +70

# Turn 1 (1 month later):
SSW_friendly = +49
GER_trade_agreement = +20
Total: +69

# Eventually:
SSW_friendly = removed (decayed to 0)
GER_trade_agreement = +20
Total: +20
```

---

## Special Modifiers

### Permanent Until Removed

Modifiers with no `decay` or duration last forever until explicitly removed.

**Examples:**
```
holds_our_cores = {
    value = -30
    # No decay/duration = permanent
}

anti_comintern_pact_opinion = {
    value = 25
    # Lasts until pact ends or modifier removed
}
```

**Removal:**
```
remove_opinion_modifier = {
    target = GER
    modifier = holds_our_cores
}
```

### Civil War Special

```
hostile_status = {
    value = -100
    # Special: Blocks faction mechanics during civil wars
}
```

### Time-Limited No Decay

Modifiers that last for a duration but don't decay:

```
GER_bought_fighter = {
    value = 10
    months = 2
    # No decay specified
    # Stays at +10 for 2 months, then removed
}
```

---

## AI Behavior Impact

Opinion modifiers affect AI decisions:

### Diplomatic Actions

**High Positive Opinion (+50+):**
- More likely to accept alliances
- More likely to join factions
- More likely to accept trade deals
- Less likely to justify war goals

**High Negative Opinion (-50+):**
- More likely to refuse diplomatic offers
- More likely to justify war goals
- Less likely to trade
- May leave factions

### Threshold Examples

**Faction Joining:**
```
# AI more likely to join if opinion > +25
# AI unlikely to join if opinion < 0

faction_invite_bonus = {
    value = 30  # Helps AI accept
}
```

**Trade Deals:**
```
# AI considers opinion for trade
# Negative opinion reduces trade willingness

trade_partner_bonus = {
    value = 20
}
```

**War Goals:**
```
# Negative opinion makes AI more aggressive

territorial_dispute = {
    value = -50
    # AI more likely to justify war goals
}
```

---

## Real-World Mechanics

### SSW Mod: Embargo System

```
ssw_new_emb = {
    trade = yes      # Trade restriction
    value = -90      # Severe opinion penalty
}

ssw_new_emb_opinion = {
    value = -75      # Opinion-only component
}

ssw_emb_lifted = {
    value = 20       # Bonus for lifting embargo
    decay = 10       # Decays quickly
}
```

**Workflow:**
1. Apply `ssw_new_emb` (blocks trade, -90 opinion)
2. Apply `ssw_new_emb_opinion` (additional -75 opinion)
3. Total: -165 opinion, no trade
4. When lifted: Remove embargoes, add `ssw_emb_lifted`

### SSW Mod: Friendship Decay

```
SSW_friendly = {
    value = 50
    months = 12
    decay = 1
}
```

**Use Case:**
- Diplomatic event creates temporary friendship
- Decays by 1 per month for 12 months
- After 12 months, still +38 opinion
- Continues to decay until 0

### BSM Mod: Economic Alliance

```
bsm_economic_alliance_relation_boost = {
    value = 15
    decay = 0
}
```

**Use Case:**
- Permanent bonus for alliance members
- No decay - lasts until alliance ends
- Applied when joining alliance
- Removed when leaving alliance

### Vanilla: Justifying War Goal

```
justifying_war_goal = {
    value = -10
    min_trust = -10
    days = 10
    decay = 1
}
```

**Behavior:**
- Applied when country justifies war goal
- Lasts 10 days
- Decays by 1 per day
- Also reduces trust

### Vanilla: Liberation Gratitude

```
our_liberators = {
    value = 40
    months = 18
    decay = 1
}
```

**Behavior:**
- Applied when country liberates your territory
- Starts at +40 opinion
- Decays by 1 per month
- After 18 months: +22 opinion
- Continues to decay to 0

---

## Edge Cases and Special Behavior

### Zero Decay

```
permanent_modifier = {
    value = 50
    decay = 0
}
```

Explicitly permanent. Never decays.

### Duration Without Decay

```
temporary_boost = {
    value = 30
    months = 6
}
```

Lasts 6 months at +30, then removed instantly.

### Decay Faster Than Duration

```
quick_decay = {
    value = 50
    months = 20
    decay = 5
}
```

- Decays to 0 after 10 months (50 ÷ 5)
- Duration 20 months never reached
- Removed when value reaches 0

### Negative Decay (Invalid)

```
# DON'T DO THIS
invalid_modifier = {
    value = 10
    decay = -1  # Invalid! Decay must be positive or 0
}
```

---

## Performance Considerations

Opinion modifiers are checked frequently by AI:

**Lightweight:**
- Simple value checks
- Permanent modifiers (no decay calculation)

**Moderate:**
- Decaying modifiers (monthly calculation)
- Duration tracking

**Heavy:**
- Trust calculations
- Trade restriction checks

**Best Practices:**
- Use permanent modifiers when possible
- Avoid too many decaying modifiers per country pair
- Clean up expired modifiers in events

---

## Debugging Opinion

### In-Game Console

```
# Check current opinion
tag GER
observe
# Hover over country relations to see active modifiers
```

### Log Modifier Application

```
# In effect:
add_opinion_modifier = {
    target = GER
    modifier = test_modifier
}
log = "Applied test_modifier to GER: [This.GetOpinionOfCountry:GER]"
```

---

## Compatibility Notes

### With Other Mods

- Opinion modifiers are additive
- Mods can add new modifiers without conflicts
- Name collisions are critical (use unique prefixes)

### DLC Considerations

- Base game: All features work
- DLC: Some opinion modifiers tied to DLC features
- Trust system: Enhanced in certain DLCs

---

## Quick Reference Table

| Property | Values | Purpose |
|----------|--------|---------|
| `value` | -200 to +200 | Opinion change |
| `trade` | yes/no | Block trade if yes |
| `decay` | 0+ | Decay rate per period |
| `months` | 1+ | Duration in months |
| `years` | 1+ | Duration in years |
| `days` | 1+ | Duration in days |
| `min_trust` | Any | Minimum trust level |
| `max_trust` | Any | Maximum trust level |

## Common Value Ranges

| Range | Type | Example Use |
|-------|------|-------------|
| ±10-25 | Minor | Small diplomatic events |
| ±30-50 | Medium | Significant agreements/disputes |
| ±60-100 | Major | Alliance formation/major betrayal |
| ±100-200 | Extreme | War crimes/vital assistance |
