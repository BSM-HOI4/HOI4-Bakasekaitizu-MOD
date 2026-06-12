# HOI4 Idea Structure Reference

## Basic Idea Definition

Ideas are defined in `common/ideas/<filename>.txt` files:

```
ideas = {
    country = {
        idea_id = {
            name = localization_key           # Optional: defaults to idea_id
            picture = sprite_name_without_prefix  # WITHOUT "GFX_idea_" prefix

            modifier = {
                # Modifiers go here
                stability_factor = 0.10
                political_power_gain = 0.15
            }

            # Optional fields:
            allowed = { trigger }             # Which countries can have this
            allowed_civil_war = { trigger }   # For civil wars
            cancel = { trigger }              # Auto-remove conditions
            available = { trigger }           # When effects are active

            targeted_modifier = {             # Target-specific modifiers
                tag = GER
                attack_bonus_against = 0.10
            }

            equipment_bonus = {               # Equipment bonuses
                infantry_equipment = {
                    build_cost_ic = -0.10
                    instant = yes
                }
            }

            traits = { trait_id }             # For advisors/characters

            cost = 150                        # Political power cost
            removal_cost = -1                 # -1 = cannot be removed manually

            ai_will_do = {                    # AI acceptance weight
                factor = 1
            }
        }
    }
}
```

## Example: Complete Idea Implementation

**common/ideas/JAP.txt:**
```
ideas = {
    country = {
        JAP_industrial_standard = {
            picture = JAP_industrial_standard    # NO "GFX_idea_" prefix here
            modifier = {
                production_speed_industrial_complex_factor = 0.1
                production_speed_arms_factory_factor = 0.1
            }
        }
    }
}
```

**interface/JAP_ideas.gfx:**
```
spriteTypes = {
    SpriteType = {
        name = GFX_idea_JAP_industrial_standard    # WITH "GFX_idea_" prefix
        texturefile = "gfx/interface/ideas/idea_JAP_industrial_standard.png"
    }
}
```

**localisation/japanese/JAP_ideas_l_japanese.yml:**
```yaml
l_japanese:
 JAP_industrial_standard:0 "工業規格統一"
 JAP_industrial_standard_desc:0 "統一された工業規格により生産効率が向上した。"
```

## Idea Categories

- **country**: National spirits (国民精神)
- **political_advisor**: Political advisors
- **theorist**: Military theorists (army, air, naval)
- **army_chief**, **navy_chief**, **air_chief**: Branch chiefs
- **high_command**: High command members
- **tank_manufacturer**, **naval_manufacturer**, etc.: Equipment designers

## Common Modifiers

### Political & Stability
- `stability_factor` - Stability (安定度)
- `war_support_factor` - War support (戦争協力度)
- `political_power_gain` - Daily political power
- `political_power_factor` - Political power gain modifier
- `drift_defence_factor` - Ideology drift defense
- `democratic_drift`, `communism_drift`, `fascism_drift`, `neutrality_drift`

### Economy & Production
- `consumer_goods_factor` - Consumer goods (民需工場)
- `production_speed_buildings_factor` - All construction
- `production_speed_industrial_complex_factor` - Civilian factory construction
- `production_speed_arms_factory_factor` - Military factory construction
- `production_speed_dockyard_factor` - Dockyard construction
- `production_factory_max_efficiency_factor` - Max factory efficiency
- `production_factory_efficiency_gain_factor` - Factory efficiency gain
- `industrial_capacity_factory` - Factory output
- `industrial_capacity_dockyard` - Dockyard output
- `line_change_production_efficiency_factor` - Production line change efficiency

### Military - General
- `army_morale_factor` - Army morale
- `army_org_factor` - Army organization
- `conscription_factor` - Conscription (徴兵)
- `training_time_factor` - Training time
- `experience_gain_factor` - Experience gain
- `land_reinforce_rate` - Reinforcement rate
- `army_attack_factor`, `army_defence_factor` - Combat stats
- `max_planning` - Planning bonus
- `planning_speed` - Planning speed

### Military - Equipment
- `production_speed_<equipment>_factor` - Production speed for equipment
- `build_cost_ic` - IC cost (in equipment_bonus)
- `reliability`, `soft_attack`, `hard_attack` - Equipment stats
- `armor_value`, `ap_attack`, `breakthrough`

### Air Force
- `air_ace_generation_chance_factor` - Ace generation
- `air_attack_factor`, `air_defence_factor` - Air combat
- `air_agility_factor`, `air_range_factor`
- `air_superiority_attack_factor`, `air_superiority_defence_factor`

### Navy
- `navy_max_range_factor` - Naval range
- `navy_org_factor` - Naval organization
- `convoy_escort_efficiency`, `convoy_raiding_efficiency_factor`
- `naval_coordination_factor`, `naval_speed_factor`
- `spotting_chance`, `sub_detection`

### Intelligence & Resistance
- `operative_slot` - Operative slots
- `crypto_strength`, `decryption_factor`
- `resistance_damage_to_garrison` - Resistance damage
- `resistance_growth`, `resistance_decay`
- `compliance_growth`, `compliance_gain`

### Resources & Trade
- `local_resources_factor` - Resource extraction
- `trade_laws_cost_factor` - Trade law cost
- `min_export` - Minimum export

### Other
- `attrition` - Land attrition
- `supply_consumption_factor` - Supply consumption
- `surrender_limit` - Surrender limit (capitulation)
- `ai_focus_aggressive_factor`, `ai_focus_defense_factor` - AI behavior
- `join_faction_tension`, `lend_lease_tension` - World tension for actions

## Targeted Modifiers

Used for country-specific bonuses:

```
targeted_modifier = {
    tag = USA                      # Target country
    attack_bonus_against = 0.10   # +10% attack against USA
    defense_bonus_against = 0.05  # +5% defense against USA
}
```

## Equipment Bonuses

Applied to specific equipment types:

```
equipment_bonus = {
    infantry_equipment = {
        build_cost_ic = -0.10     # -10% IC cost
        reliability = 0.05         # +5% reliability
        instant = yes              # Apply to existing equipment
    }
}
```

## State-Targeted Modifiers

For state-specific effects:

```
state_modifier = {
    state = state_id
    local_resources_factor = 0.15
}
```

## GFX Sprite Naming Convention

**IMPORTANT:** The GFX sprite name and the picture field use different formats:

- **In .gfx file**: Use `GFX_idea_` prefix
  ```
  name = GFX_idea_JAP_industrial_standard
  ```

- **In ideas definition**: Use name WITHOUT `GFX_idea_` prefix
  ```
  picture = JAP_industrial_standard
  ```

The game automatically adds `GFX_idea_` when looking up the sprite.

## Localization Files

Localization path depends on language:
- Japanese: `localisation/japanese/<filename>_l_japanese.yml`
- English: `localisation/english/<filename>_l_english.yml`

Format:
```yaml
l_japanese:
 idea_id:0 "アイデア名"
 idea_id_desc:0 "アイデアの説明文。効果の詳細を記述。"
```

**Note:** File must start with UTF-8 BOM (`﻿`) for proper encoding.
