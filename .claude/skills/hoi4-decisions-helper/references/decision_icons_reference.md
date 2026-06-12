# HOI4 Decision Icons Reference

Common decision icons available in HOI4.

---

## Generic Icons

```
GFX_decision_generic
GFX_decision_generic_nationalism
GFX_decision_generic_political_discourse
GFX_decision_generic_prepare_civil_war
GFX_decision_generic_civil_support
```

---

## Military Icons

### Army
```
GFX_decision_generic_army
GFX_decision_generic_military
GFX_decision_generic_ignite_civil_war
GFX_decision_generic_tank
GFX_decision_generic_army_support
```

### Navy
```
GFX_decision_generic_navy
GFX_decision_generic_naval
```

### Air Force
```
GFX_decision_generic_air_force
GFX_decision_generic_aircraft
```

### General Military
```
GFX_decision_generic_military_mission
GFX_decision_generic_military_deal
GFX_decision_generic_officer
```

---

## Economic Icons

### Industry
```
GFX_decision_generic_industry
GFX_decision_generic_construction
GFX_decision_generic_factory
GFX_decision_generic_production
```

### Resources
```
GFX_decision_generic_oil
GFX_decision_generic_steel
GFX_decision_generic_resources
GFX_decision_generic_fuel
```

### Trade
```
GFX_decision_generic_trade
GFX_decision_generic_agreement
```

---

## Political Icons

### Government
```
GFX_decision_generic_political_discourse
GFX_decision_generic_parliament
GFX_decision_generic_fascism
GFX_decision_generic_communism
GFX_decision_generic_democracy
```

### Diplomacy
```
GFX_decision_generic_form_nation
GFX_decision_generic_nationalism
GFX_decision_generic_flags
GFX_decision_generic_diplomatic_treaty
```

---

## Crisis and Conflict

```
GFX_decision_generic_crisis
GFX_decision_generic_civil_war
GFX_decision_generic_prepare_civil_war
GFX_decision_generic_ignite_civil_war
GFX_decision_generic_oppression
```

---

## Espionage and Intelligence

```
GFX_decision_generic_spy
GFX_decision_generic_intelligence
GFX_decision_generic_infiltrate
```

---

## Research and Technology

```
GFX_decision_generic_research
GFX_decision_generic_rocket
GFX_decision_generic_science
```

---

## Border Conflicts

```
GFX_decision_border_war
GFX_decision_hol_war_on_pacifism
```

---

## Country-Specific Icons

### Germany
```
GFX_decision_ger_reichskommissariat
GFX_decision_ger_mefo_bills
```

### Soviet Union
```
GFX_decision_sov_great_purge
```

### Japan
```
GFX_decision_jap_strike_south
```

---

## How to Use

In your decision definition:

```
decision_name = {
    icon = GFX_decision_generic_industry

    # Rest of decision...
}
```

---

## Creating Custom Icons

1. Create a 150x150 DDS image
2. Place in `gfx/interface/decisions/`
3. Define in a `.gfx` file:

```
spriteTypes = {
    spriteType = {
        name = "GFX_decision_my_custom_icon"
        texturefile = "gfx/interface/decisions/my_custom_icon.dds"
    }
}
```

4. Use in decision:
```
decision_name = {
    icon = GFX_decision_my_custom_icon
}
```

---

## Icon Selection Guide

**Economic decisions:** Use industry/production icons
**Military decisions:** Use army/navy/air force icons
**Diplomatic decisions:** Use flags/treaty icons
**Research decisions:** Use research/science icons
**Crisis decisions:** Use crisis/civil war icons
**Generic decisions:** Use generic icon

**When in doubt:** `GFX_decision_generic` works for everything
