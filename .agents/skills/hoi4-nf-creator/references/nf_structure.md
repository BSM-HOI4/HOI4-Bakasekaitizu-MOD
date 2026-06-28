# HOI4 National Focus Structure Reference

## Focus Tree Structure

National Focuses are defined in `common/national_focus/<filename>.txt` files:

```
focus_tree = {
    id = country_focus_tree_name

    country = {
        factor = 0
        modifier = {
            add = 20
            tag = JAP
        }
    }

    default = no  # or yes

    continuous_focus_position = { x = 20 y = 1600 }

    focus = {
        # Focus definition
    }

    focus = {
        # Another focus
    }
}
```

## Focus Definition

```
focus = {
    id = focus_unique_id                    # Unique identifier
    icon = "GFX_goal_icon_name"            # Icon sprite name
    cost = 10                               # Political power cost (usually 5 or 10)

    # Position
    x = 10                                  # X coordinate in tree
    y = 8                                   # Y coordinate in tree

    # OR use relative positioning
    relative_position_id = parent_focus_id # Position relative to another focus

    # Prerequisites
    prerequisite = { focus = required_focus_1 }
    prerequisite = { focus = required_focus_2 }

    # Mutually exclusive (choose one path)
    mutually_exclusive = { focus = alternative_focus }

    # Availability conditions
    available = {
        has_completed_focus = some_focus
        has_war = yes
        # Any trigger
    }

    # Bypass conditions
    bypass = {
        has_war_with = GER
        # Any trigger
    }

    # Cancel conditions
    cancel_if_invalid = yes  # or no

    # Rewards
    completion_reward = {
        add_ideas = national_spirit_id
        add_political_power = 150
        # Any effect
    }

    # AI behavior
    ai_will_do = {
        factor = 50
        modifier = {
            factor = 2
            has_war = yes
        }
    }

    # Search filters
    search_filters = { FOCUS_FILTER_POLITICAL }

    # Allow branching
    allow_branch = {
        # Conditions for entire branch
    }
}
```

## Position System

### Absolute Positioning

```
focus = {
    id = focus_1
    x = 5       # Column (0-based from left)
    y = 0       # Row (0-based from top)
}
```

### Relative Positioning

```
focus = {
    id = focus_child
    relative_position_id = focus_parent
    x = 0       # Offset from parent
    y = 1       # 1 row below parent
}
```

## Prerequisites

### Single Prerequisite

```
prerequisite = { focus = parent_focus }
```

### Multiple Prerequisites (OR logic)

```
prerequisite = { focus = option_a }
prerequisite = { focus = option_b }
# Requires EITHER option_a OR option_b
```

### Multiple Prerequisites (AND logic)

```
prerequisite = {
    focus = required_1
    focus = required_2
}
# Requires BOTH required_1 AND required_2
```

## Mutually Exclusive

For branching paths where player must choose one:

```
focus = {
    id = democratic_path
    mutually_exclusive = { focus = fascist_path }
}

focus = {
    id = fascist_path
    mutually_exclusive = { focus = democratic_path }
}
```

## Common Completion Rewards

### Add National Spirit

```
completion_reward = {
    add_ideas = idea_id
}
```

### Swap Ideas

```
completion_reward = {
    swap_ideas = {
        remove_idea = old_idea
        add_idea = new_idea
    }
}
```

### Add Political Power

```
completion_reward = {
    add_political_power = 150
}
```

### Grant Research Bonus

```
completion_reward = {
    add_tech_bonus = {
        bonus = 0.5
        uses = 2
        category = infantry_weapons
    }
}
```

### Unlock Decisions

```
completion_reward = {
    unlock_decision_category_tooltip = decision_category_id
}
```

### Country Effects

```
completion_reward = {
    add_stability = 0.05
    add_war_support = 0.10
    add_manpower = 10000
}
```

### Factories

```
completion_reward = {
    random_owned_controlled_state = {
        add_building_construction = {
            type = industrial_complex
            level = 1
            instant_build = yes
        }
    }
}
```

## Common Icons

- `GFX_goal_generic_political_pressure` - Political
- `GFX_goal_generic_demand_territory` - Territorial
- `GFX_goal_generic_military_sphere` - Military alliance
- `GFX_goal_generic_army_doctrines` - Military doctrine
- `GFX_goal_generic_construct_military` - Military construction
- `GFX_goal_generic_production` - Industrial production
- `GFX_goal_generic_construction2` - Construction
- `GFX_goal_support_democracy` - Democratic
- `GFX_goal_support_fascism` - Fascist
- `GFX_goal_support_communism` - Communist
- `GFX_goal_generic_propaganda` - Propaganda
- `GFX_goal_generic_major_alliance` - Major alliance
- `GFX_goal_generic_attack` - Attack
- `GFX_goal_generic_defend` - Defend

## Search Filters

```
FOCUS_FILTER_POLITICAL      # Political focuses
FOCUS_FILTER_RESEARCH       # Research bonuses
FOCUS_FILTER_INDUSTRY       # Industrial focuses
FOCUS_FILTER_STABILITY      # Stability-related
FOCUS_FILTER_WAR_SUPPORT    # War support
FOCUS_FILTER_MANPOWER       # Manpower
FOCUS_FILTER_ANNEXATION     # Annexation/territory
```

## Localization Required

For each focus, create entries in `localisation/<language>/`:

```yaml
l_japanese:
 focus_id:0 "国家方針名"
 focus_id_desc:0 "国家方針の説明。効果と背景を記述。"
```

For English:
```yaml
l_english:
 focus_id:0 "Focus Name"
 focus_id_desc:0 "Description of the focus and its effects."
```

## AI Behavior

### Basic AI Weight

```
ai_will_do = {
    factor = 10  # Base weight
}
```

### Conditional AI

```
ai_will_do = {
    factor = 10
    modifier = {
        factor = 0      # Never take
        is_historical_focus_on = yes
    }
    modifier = {
        factor = 5      # Much more likely
        has_war = yes
    }
}
```

## Continuous Focuses

Special focuses that can be taken repeatedly:

```
continuous_focus_position = { x = 20 y = 1600 }

focus = {
    id = continuous_focus_id
    icon = "GFX_goal_generic_political_pressure"
    cost = 1

    x = 20
    y = 1600

    # No prerequisites for continuous focuses

    completion_reward = {
        # Effects
    }
}
```

## Tips

1. **Cost**: Standard focuses cost 10, quick focuses cost 5
2. **Position**: Plan tree layout before implementing
3. **Prerequisites**: Use for logical progression
4. **Mutually Exclusive**: For branching storylines
5. **Icons**: Choose thematically appropriate icons
6. **AI**: Give reasonable AI weights (usually 1-100)
7. **Localization**: Always provide name and description
