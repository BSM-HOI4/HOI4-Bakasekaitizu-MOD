# HOI4 Modifier Categories Reference

## Category Overview

Modifiers are organized into the following categories:

### political
Political and internal stability modifiers
- Stability, war support, political power
- Ideology drift and conversion
- Internal politics

### economy
Economic and production modifiers
- Factory construction and output
- Consumer goods
- Production efficiency
- Resource extraction

### military
General land warfare modifiers
- Organization, morale, attack, defense
- Training, experience, reinforcement
- Planning and execution

### air
Air force modifiers
- Aircraft stats (attack, defense, agility, range)
- Air ace generation
- Air combat effectiveness

### navy
Naval modifiers
- Ship stats and organization
- Convoy operations
- Naval combat and coordination

### intelligence
Intelligence and espionage modifiers
- Operative slots
- Encryption/decryption
- Intelligence operations

### resources
Resource and trade modifiers
- Resource extraction
- Trade efficiency
- Resource availability

### other
Miscellaneous modifiers
- Supply and attrition
- AI behavior
- Special mechanics

## Common Search Patterns

### By Effect Type

**Boost stability:**
```bash
python3 scripts/search_modifiers.py --search stability
```

**Increase production:**
```bash
python3 scripts/search_modifiers.py --search production
python3 scripts/search_modifiers.py --category economy
```

**Military buffs:**
```bash
python3 scripts/search_modifiers.py --category military
python3 scripts/search_modifiers.py --search attack
```

**Naval improvements:**
```bash
python3 scripts/search_modifiers.py --category navy
python3 scripts/search_modifiers.py --search convoy
```

### By Game Mechanic

**Factory-related:**
```bash
python3 scripts/search_modifiers.py --search factory
```

**Experience and training:**
```bash
python3 scripts/search_modifiers.py --search experience
python3 scripts/search_modifiers.py --search training
```

**Supply and logistics:**
```bash
python3 scripts/search_modifiers.py --search supply
python3 scripts/search_modifiers.py --search attrition
```

## Typical Modifier Values

### Percentage Modifiers
Most modifiers use decimal values representing percentages:
- `0.10` = +10%
- `-0.10` = -10%
- `0.05` = +5%

### Absolute Values
Some modifiers use absolute numbers:
- `operative_slot = 1` (adds 1 operative slot)
- `crypto_strength = 1` (adds 1 encryption level)

### Common Ranges

**Small bonuses (minor buffs):**
- `0.05` to `0.10` (5% to 10%)

**Medium bonuses (standard national spirits):**
- `0.10` to `0.20` (10% to 20%)

**Large bonuses (major effects):**
- `0.25` to `0.50` (25% to 50%)

**Debuffs (negative effects):**
- `-0.05` to `-0.20` (typically)
- Economic crisis: `-0.30` or more

## Combining Modifiers

Ideas can have multiple modifiers in the same block:

```
modifier = {
    stability_factor = 0.10
    war_support_factor = 0.05
    political_power_gain = 0.15
}
```

### Thematic Combinations

**Economic Boom:**
```
modifier = {
    stability_factor = 0.10
    production_speed_industrial_complex_factor = 0.15
    industrial_capacity_factory = 0.10
}
```

**Military Focus:**
```
modifier = {
    conscription_factor = 0.10
    training_time_factor = -0.10
    army_org_factor = 0.05
}
```

**Naval Supremacy:**
```
modifier = {
    navy_org_factor = 0.10
    naval_coordination_factor = 0.15
    convoy_escort_efficiency = 0.10
}
```

**Total War:**
```
modifier = {
    war_support_factor = 0.15
    conscription_factor = 0.15
    consumer_goods_factor = -0.05
}
```
