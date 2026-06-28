# HOI4 Dynamic Modifier Guide

## What is Dynamic Modifier?

Dynamic modifiers are special modifiers that:
- Can use **variables** for dynamic values
- Have **enable/remove conditions**
- Update values **daily** (or when forced)
- Can be **scoped** to specific countries/states

## Basic Structure

Defined in `common/dynamic_modifiers/<filename>.txt`:

```
modifier_name = {
    enable = { trigger }           # When this modifier is active
    remove_trigger = { trigger }   # Auto-remove when true
    icon = "GFX_idea_icon"        # Optional icon

    # Modifiers (static or variable-based)
    stability_factor = 0.10
    max_fuel = var_max_fuel        # Uses variable value
}
```

## Key Differences from Regular Modifiers

| Feature | Regular Modifier | Dynamic Modifier |
|---------|-----------------|------------------|
| Values | Static only | Static OR variable-based |
| Conditions | No | enable/remove_trigger |
| Update | Never | Daily or forced |
| Scope | Fixed | Can be scoped dynamically |
| Location | In ideas/focuses | Separate definition + add effect |

## Using Variables

Dynamic modifiers can reference variables:

```
production_boost_modifier = {
    enable = { always = yes }

    # Variable determines the value
    industrial_capacity_factory = var_production_bonus
    stability_factor = var_stability_level
}
```

Setting variables:
```
effect = {
    set_variable = { var_production_bonus = 0.15 }
    set_variable = { var_stability_level = 0.10 }
}
```

## Scopes

### Country Scope
```
country_economic_modifier = {
    enable = { always = yes }
    icon = GFX_idea_generic_production

    industrial_capacity_factory = 0.10
    consumer_goods_factor = -0.05
}
```

Apply to country:
```
add_dynamic_modifier = {
    modifier = country_economic_modifier
}
```

### State Scope
```
state_development_modifier = {
    enable = { always = yes }
    icon = GFX_idea_generic_fortify

    local_building_slots_factor = 0.20
    state_production_speed_buildings_factor = 0.15
}
```

Apply to state:
```
123 = {  # State ID
    add_dynamic_modifier = {
        modifier = state_development_modifier
    }
}
```

### Unit Leader Scope
```
general_bonus_modifier = {
    enable = { always = yes }

    army_attack_factor = 0.10
    army_defence_factor = 0.10
}
```

## Enable and Remove Conditions

### Enable
Modifier only applies when condition is true:

```
war_economy_modifier = {
    enable = {
        has_war = yes
    }

    industrial_capacity_factory = 0.20
    conscription_factor = 0.10
}
```

### Remove Trigger
Auto-removes when condition becomes true:

```
crisis_modifier = {
    enable = { always = yes }
    remove_trigger = {
        has_stability > 0.50
    }

    stability_factor = -0.20
}
```

## Adding Dynamic Modifiers

### Permanent
```
add_dynamic_modifier = {
    modifier = modifier_name
}
```

### Temporary (Days)
```
add_dynamic_modifier = {
    modifier = modifier_name
    days = 365  # Lasts 1 year
}
```

### Scoped to Another Country
```
add_dynamic_modifier = {
    modifier = modifier_name
    scope = GER  # Scoped to Germany
}
```

## Removing Dynamic Modifiers

```
remove_dynamic_modifier = {
    modifier = modifier_name
}
```

## Force Update

Dynamic modifiers update daily by default. Force immediate update:

```
force_update_dynamic_modifier = yes
```

## Common Patterns

### Variable-Based Scaling

```
scaling_industrial_modifier = {
    enable = { always = yes }
    icon = GFX_idea_generic_production

    # Scales with variable
    industrial_capacity_factory = var_industrial_level
}

# In effect:
set_variable = { var_industrial_level = 0.05 }
add_dynamic_modifier = { modifier = scaling_industrial_modifier }

# Later, increase the bonus:
add_to_variable = { var_industrial_level = 0.05 }
force_update_dynamic_modifier = yes
```

### Temporary Resource Penalty

```
sabotaged_resources = {
    enable = { always = yes }
    remove_trigger = { has_resistance = no }
    icon = GFX_modifiers_sabotaged

    temporary_state_resource_oil = var_sabotaged_oil
    temporary_state_resource_steel = var_sabotaged_steel
}
```

### Conditional Military Bonus

```
defensive_stance_modifier = {
    enable = {
        has_defensive_war = yes
    }
    icon = GFX_idea_generic_defend

    army_defence_factor = 0.15
    dig_in_speed_factor = 0.25
}
```

## Complete Example

**Definition** (`common/dynamic_modifiers/economic_modifiers.txt`):
```
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

**Usage** (in event/focus/decision):
```
effect = {
    # Set initial values
    set_variable = { var_recovery_level = 0.10 }
    set_variable = { var_recovery_stability = 0.05 }

    # Add the modifier
    add_dynamic_modifier = {
        modifier = economic_recovery_modifier
    }
}

# Later, improve recovery:
effect = {
    add_to_variable = { var_recovery_level = 0.05 }
    force_update_dynamic_modifier = yes
}
```

## Best Practices

1. **Use for dynamic situations** - Values that change over time
2. **Document scope** - Clearly state Country/State/Leader scope
3. **Name clearly** - Include "modifier" in the name
4. **Set enable conditions** - Prevent modifiers applying inappropriately
5. **Use remove_trigger** - Auto-cleanup when no longer needed
6. **Force updates** - After changing variables
7. **Icon for visibility** - Helps players see active modifiers

## When to Use Dynamic Modifiers

**Use dynamic modifiers when:**
- Values need to change based on variables
- Modifiers need conditional activation
- Building progression systems
- Creating temporary effects

**Use regular modifiers (ideas) when:**
- Values are static
- Simple add/remove pattern
- Traditional national spirit behavior
- No complex conditions needed
