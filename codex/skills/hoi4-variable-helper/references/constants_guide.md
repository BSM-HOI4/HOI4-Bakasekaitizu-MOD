# HOI4 Script Constants Complete Guide

## What Are Script Constants

Script constants are reusable, compile-time values defined once and referenced everywhere. They have **zero runtime cost** and make balancing easier.

**Location:** `common/script_constants/<filename>.txt`

## Basic Structure

```
category_name = {
    schema = {
        # Schema definition
    }

    # Constant entries
}
```

## Schema Types

### Integer Constants
```
category_name = {
    schema = {
        any_key = yes
        data = int
    }

    key1 = 10
    key2 = 20
}
```

### Decimal Constants
```
category_name = {
    schema = {
        any_key = yes
        data = fixed_point
    }

    small = 0.05
    large = 0.15
}
```

### Array Constants
```
category_name = {
    schema = {
        any_key = yes
        array = country  # or state, character, etc.
    }

    group1 = {
        GER
        ITA
        JAP
    }
}
```

### Complex Constants
```
category_name = {
    schema = {
        any_key = yes
        data = {
            {
                key = field1
                data = int
            }
            {
                key = field2
                data = fixed_point
            }
        }
    }

    entry1 = {
        field1 = 10
        field2 = 0.5
    }
}
```

## Using Constants

### Reference Syntax
```
constant:category.key
```

### In Effects
```
add_timed_idea = {
    idea = my_idea
    days = constant:durations.medium
}
```

### In Modifiers
```
modifier = {
    stability_factor = constant:bonuses.standard
}
```

### In Collections
```
my_collection = {
    input = constant:country_groups.axis
    operators = {
        limit = { has_war = yes }
    }
}
```

## Real-World Examples

### Simple Integer Constants (SSW Mod)
```
sde_page = {
    schema = {
        any_key = yes
        data = int
    }
}
```

### Country Groups (Vanilla)
```
country_groups = {
    schema = {
        any_key = yes
        array = country
    }

    nordics = {
        SWE
        NOR
        FIN
        DEN
        ICE
    }

    literally_china = {
        CHI
        PRC
        GXC
        YUN
        SHX
        XSM
        SIK
    }

    chinese_warlords = {
        GXC
        YUN
        SHX
        XSM
        SIK
        GDC
        SND
        SIC
    }

    islamic_world = {
        SAU
        IRQ
        PER
        AFG
        # ... more countries
    }
}
```

### State Groups (Vanilla)
```
state_groups = {
    schema = {
        any_key = yes
        array = state
    }

    balkans = {
        106  # Macedonia
        107  # Thrace
        184  # Albania
        # ... more states
    }

    mare_nostrum_states = {
        117  # Sicily
        118  # Sardinia
        162  # Crete
        # ... more states
    }

    comintern_starting_border = {
        11   # Leningrad
        195  # Bessarabia
        # ... more states
    }
}
```

### Complex Constants (Vanilla)
```
special_project_complexity = {
    schema = {
        any_key = yes
        data = {
            {
                key = min
                data = int
            }
            {
                key = max
                data = int
            }
        }
    }

    small = {
        min = 20
        max = 30
    }

    medium = {
        min = 15
        max = 20
    }

    large = {
        min = 10
        max = 15
    }

    insane = {
        min = 5
        max = 10
    }
}

basic_research_time = {
    schema = {
        any_key = yes
        data = int
    }

    short = 15
    medium = 30
    long = 60
    very_long = 90
}
```

## Usage Examples

### Using Country Groups
```
# In collection
all_islamic_countries = {
    input = constant:country_groups.islamic_world
    name = COLLECTION_FACTION_ISLAMIC_COUNTRIES
}

islamic_faction_members = {
    input = constant:country_groups.islamic_world
    operators = {
        limit = {
            OR = {
                tag = ROOT
                is_in_faction_with = ROOT
            }
        }
    }
}
```

### Using State Groups
```
# In collection
controllable_balkan_states = {
    input = constant:state_groups.balkans
    name = COLLECTION_FACTION_BALKAN_STATES
}

faction_controlled_balkan_states = {
    input = constant:state_groups.balkans
    operators = {
        limit = {
            is_controlled_by_ROOT_or_ally = yes
        }
    }
}

# In trigger
if = {
    limit = {
        any_of = {
            array = constant:state_groups.mare_nostrum_states
            owns_state = var:v
        }
    }
    # Owns a Mare Nostrum state
}
```

### Using Complex Constants
```
# In effect
random = {
    chance = 50
    add_days_mission_timeout = {
        mission = current_mission
        days = random_days = {
            min = constant:special_project_complexity.medium.min
            max = constant:special_project_complexity.medium.max
        }
    }
}
```

## Common Patterns

### Modifier Values
```
modifier_values = {
    schema = {
        any_key = yes
        data = fixed_point
    }

    tiny = 0.01
    small = 0.05
    medium = 0.10
    large = 0.15
    huge = 0.25
}

# Use in ideas:
modifier = {
    stability_factor = constant:modifier_values.medium
    war_support_factor = constant:modifier_values.small
}
```

### Duration Constants
```
durations = {
    schema = {
        any_key = yes
        data = int
    }

    very_short = 30
    short = 60
    medium = 120
    long = 365
    very_long = 730
}

# Use in effects:
add_timed_idea = {
    idea = wartime_economy
    days = constant:durations.long
}
```

### Cost Constants
```
costs = {
    schema = {
        any_key = yes
        data = int
    }

    cheap = 25
    standard = 50
    expensive = 100
    very_expensive = 200
}

# Use in decisions:
cost = constant:costs.standard
```

### Regional Groups
```
regional_groups = {
    schema = {
        any_key = yes
        array = state
    }

    western_europe = {
        16   # Paris
        17   # Normandy
        # ... more
    }

    eastern_europe = {
        10   # Poland
        91   # Lithuania
        # ... more
    }
}
```

## Best Practices

1. **Use descriptive names** - `modifier_values.medium` not `mod_val.m`
2. **Group related constants** - All durations in one category
3. **Document units** - Days, percentage, absolute value?
4. **Use for balance** - Central place for tuning values
5. **Array constants for groups** - Country/state collections
6. **Complex for structured data** - Min/max ranges, multi-field data
7. **Zero runtime cost** - Use liberally

## Schema Reference

### Simple Data Types
- `data = int` - Integer values
- `data = fixed_point` - Decimal values

### Array Types
- `array = country` - List of country tags
- `array = state` - List of state IDs
- `array = character` - List of character tokens

### Complex Structures
```
data = {
    {
        key = field_name
        data = type
    }
    # More fields...
}
```

### Key Specification
- `any_key = yes` - Accept any key name
- `key = specific_name` - Only accept this exact key

## Advantages

✅ **Zero runtime cost** - Resolved at compile time
✅ **Central balancing** - Change values in one place
✅ **Readability** - `constant:costs.expensive` vs magic number `100`
✅ **Type safety** - Schema validation
✅ **Easy tuning** - Modify balance without touching logic
✅ **Reusability** - Use in collections, effects, triggers

## When to Use

**Use script constants for:**
- Modifier values for balance
- Duration/cost values
- Country/state groupings
- Configuration values
- Threshold values

**Don't use for:**
- Runtime-changing values (use variables)
- Player-specific data (use variables)
- Dynamic lists (use arrays)
- Conditional logic (use triggers)
