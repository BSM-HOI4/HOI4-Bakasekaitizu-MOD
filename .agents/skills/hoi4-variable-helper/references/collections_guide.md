# HOI4 Collections Complete Guide

## What Are Collections

Collections are live, auto-updating groups of scopable objects (countries, states, characters, etc.). Treat them as unordered arrays whose membership is derived from inputs and operators at evaluation time.

Use collections when membership is dynamic and order does not matter. Use arrays when order, stable indices, sorting, queues, or parallel fields matter.

Always use an explicit prefix. Do not pass bare names like `all_countries`. Definition inputs commonly use `game:`, `collection:`, and `constant:`; some newer call sites/docs use `collections:` for built-in collection namespace references such as `collections:all_countries`.

## Built-In Collections

### Game Scope
```
game:empty                   # Empty collection
game:all_countries           # All existing countries
game:all_possible_countries  # All possible countries (including formables)
game:all_states              # All states in the game
game:scope                   # Current scope as a collection
collections:all_countries    # explicit collection namespace where required by call site/docs
```

### Country Scope
```
country:faction_members      # All members of country's faction
```

## Defining Collections

**File:** `common/collections/my_collections.txt`

### Basic Structure
```
collection_name = {
    input = source_collection

    operators = {
        limit = {
            # Filter conditions
        }
    }

    name = LOCALIZATION_KEY  # Optional
}
```

Collections can also be defined anonymously/inline when no other script needs the collection:

```
every_collection_element = {
    collection = {
        input = game:all_countries
        operators = {
            limit = {
                is_major = yes
                has_capitulated = no
            }
        }
    }
    add_political_power = 25
}
```

### Simple Filter
```
major_powers = {
    input = game:all_countries

    operators = {
        limit = {
            is_major = yes
        }
    }

    name = COLLECTION_MAJOR_POWERS
}
```

### Chained Operators
```
faction_core_states = {
    input = game:scope

    operators = {
        faction_members      # First: get all faction members
        owned_states         # Then: get their owned states
        limit = {
            is_core_of = PREV  # Finally: filter to core states only
        }
    }

    name = COLLECTION_FACTION_CORE_STATES
}
```

### Nested Collections
```
# Define base collection
democratic_countries = {
    input = game:all_countries
    operators = {
        limit = { has_democratic_government = yes }
    }
}

# Build on it
uncapitulated_democracies = {
    input = collection:democratic_countries
    operators = {
        limit = { has_capitulated = no }
    }
}
```

## Available Operators

### Country Operators
- `faction_members` - All members of faction
- `country_and_all_subjects` - Country and its subjects

### State Operators
- `owned_states` - All owned states
- `controlled_states` - All controlled states

### Combined
```
operators = {
    faction_members      # Get faction members
    controlled_states    # Get their controlled states
    limit = {
        is_on_continent = europe  # Filter to Europe
    }
}
```

## Using Collections

### In Effects
```
every_collection_element = {
    collection = collection:major_powers

    # Effects applied to each element
    add_stability = 0.05
}
```

### In Triggers
```
collection_size = {
    collection = collection:democratic_countries
    value > 10
}
```

Undocumented collection-related triggers observed in current builds: `count_in_collection` and `has_resources_in_collection`. Search vanilla usage or test in logs before relying on exact block syntax in production.

### In Math Expressions

```
set_variable = {
    major_factory_total = {
        value = 0
        every_collection = {
            named_collection = non_capitulated_majors
            add = num_of_factories
        }
    }
}
```

## Real-World Examples (SSW Mod)

### Peaceful Countries
```
world_at_peace_countries = {
    input = game:all_countries
    operators = {
        limit = {
            has_war = no
        }
    }
    name = COLLECTION_COUNTRIES_AT_PEACE
}
```

### Faction Filtering
```
democratic_faction_members = {
    input = game:scope
    operators = {
        faction_members
        limit = {
            has_democratic_government = yes
        }
    }
    name = COLLECTION_DEMOCRATIC_FACTION_MEMBERS
}
```

### Regional States
```
states_in_africa = {
    input = game:all_states
    operators = {
        limit = {
            is_on_continent = africa
        }
    }
    name = COLLECTION_STATES_IN_AFRICA
}

faction_states_in_africa = {
    input = game:scope
    operators = {
        faction_members
        controlled_states
        limit = {
            is_on_continent = africa
        }
    }
    name = COLLECTION_FACTION_CONTROLLED_STATES_IN_AFRICA
}
```

### Continental Filtering
```
states_on_my_continent = {
    input = game:all_states
    operators = {
        limit = {
            is_on_same_continent_as = ROOT
        }
    }
    name = COLLECTION_STATES_MY_CONTINENT
}

non_fascist_controlled_states_on_my_continent = {
    input = collection:states_on_my_continent
    operators = {
        limit = {
            controller = {
                NOT = { has_dictatorship_government = yes }
            }
        }
    }
    name = COLLECTION_NON_FASCIST_STATES_MY_CONTINENT
}
```

### Using Script Constants
```
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
    name = COLLECTION_FACTION_CONTROLLED_BALKAN_STATES
}
```

### Complex Faction Logic
```
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
    name = COLLECTION_ISLAMIC_FACTION_MEMBERS
}
```

### Multi-Level Chaining
```
faction_owned_core_states = {
    input = game:scope
    operators = {
        faction_members          # 1. Get faction members
        owned_states             # 2. Get their owned states
        limit = {
            is_core_of = PREV    # 3. Filter to cores
        }
    }
    name = COLLECTION_FACTION_OWNED_CORE_STATES
}

faction_controlled_non_core_states = {
    input = game:scope
    operators = {
        faction_members
        controlled_states
        limit = {
            NOT = { is_core_of = PREV }
        }
    }
    name = COLLECTION_FACTION_CONTROLLED_NON_CORE_STATES
}
```

### Complex State Filtering
```
china_potential_core_states = {
    input = game:all_states
    operators = {
        limit = {
            OR = {
                is_core_of = CHI
            }
        }
    }
}

china_potential_core_mainland_states = {
    input = collection:china_potential_core_states
    operators = {
        limit = {
            NOT = { state = 524 }  # Taiwan
            is_one_state_island = no
        }
    }
}
```

### Ideology-Based State Control
```
communist_controlled_states_my_continent = {
    input = game:all_states
    operators = {
        limit = {
            is_on_same_continent_as = ROOT
            controller = {
                has_socialist_government = yes
            }
        }
    }
    name = COLLECTION_COMMUNIST_CONTROLLED_STATES_SAME_CONTINENT
}
```

## Anonymous Collections

Define collections inline without naming them:

```
every_collection_element = {
    collection = {
        input = game:all_countries
        operators = {
            limit = {
                is_ai = yes
                is_major = yes
            }
        }
    }

    # Effects on AI majors
}
```

## Scope Context

### ROOT, PREV, FROM in Collections

```
neighboring_states_to_leader = {
    input = game:all_states
    operators = {
        limit = {
            any_neighbor_state = {
                is_owned_by = ROOT  # ROOT is the scope using this collection
            }
        }
    }
    name = COLLECTION_NEIGHBORING_STATES
}
```

### PREV in Chained Operators

```
states_controlled_by_faction_member_and_core_holder = {
    input = game:scope
    operators = {
        faction_members      # PREV becomes each faction member
        controlled_states    # Process their states
        limit = {
            is_core_of = controller  # Check core status
        }
    }
    name = COLLECTION_STATES_CONTROLLED_BY_FACTION_MEMBER_AND_CORE_HOLDER
}
```

## Usage Patterns

### Count Elements
```
if = {
    limit = {
        collection_size = {
            collection = collection:faction_states_in_africa
            value > 20
        }
    }
    # Achievement unlocked
}
```

### Process All
```
every_collection_element = {
    collection = collection:world_at_peace_countries
    add_stability = 0.05
}
```

### Combine with Triggers
```
if = {
    limit = {
        collection_size = {
            collection = collection:democratic_faction_members
            value > 5
        }
    }
    # Large democratic alliance
}
```

## Best Practices

1. **Name collections clearly** - Describe what they filter
2. **Reuse base collections** - Build chains for efficiency
3. **Use script constants** - For state/country groups
4. **Add localization names** - For tooltip display
5. **Optimize filters** - Put cheap checks first
6. **Chain wisely** - Each operator adds processing
7. **Document complex logic** - Add comments explaining filters

## Performance Tips

- ✅ Collections are lazy - only evaluated when used
- ✅ Reuse named collections instead of duplicating filters
- ✅ Put simple checks before complex ones
- ⚠️ Avoid deeply nested limit blocks
- ✅ Use operators like `faction_members` instead of manual loops
- ✅ Build on existing collections with filters
