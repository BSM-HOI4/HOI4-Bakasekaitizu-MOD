# Scope Reference for Scripted Triggers

## Understanding Scopes

Scripted triggers execute in a specific scope context. Understanding scope is critical for writing correct triggers.

## Scope Types

### Country Scope
Most common scope. Represents a nation.

```
is_major_power = {
    # THIS/ROOT = country
    is_major = yes
}
```

### State Scope
Represents a province/state.

```
is_core_state = {
    # THIS/ROOT = state
    is_core_of = ROOT
}
```

### Character Scope
Represents a character (leader, advisor, general).

```
is_popular_leader = {
    # THIS/ROOT = character
    has_ideology = fascism_ideology
}
```

### Unit Leader Scope
Represents a field marshal or general.

```
is_skilled_general = {
    # THIS/ROOT = unit leader
    skill > 3
}
```

---

## Scope Keywords

### THIS
Current scope being evaluated.

```
is_at_war = {
    # THIS implicitly = the country this trigger is evaluated for
    has_war = yes
}
```

### ROOT
The scope that initiated the event/focus/decision.

```
is_ally_of_ROOT = {
    # THIS = country being checked
    # ROOT = country that triggered the event
    is_in_faction_with = ROOT
}
```

### FROM
The scope passed as context (varies by situation).

```
can_get_wargoal_on_FROM = {
    # THIS = country checking
    # FROM = target country
    NOT = { is_in_faction_with = FROM }
    NOT = { is_subject_of = FROM }
}
```

### PREV
Previous scope in a nested structure.

```
ROOT_has_divisions_in_state = {
    # THIS = state scope
    # ROOT = country scope
    ROOT = {
        # THIS = country (ROOT)
        # PREV = state (original THIS)
        divisions_in_state = {
            state = PREV
            size > 0
        }
    }
}
```

---

## Scope Navigation

### From Country to State

```
owns_coastal_state = {
    # Start: country scope
    any_owned_state = {
        # Now: state scope
        is_coastal = yes
    }
}
```

### From State to Country

```
owned_by_major = {
    # Start: state scope
    owner = {
        # Now: country scope (state owner)
        is_major = yes
    }
}

controller_at_war = {
    # Start: state scope
    controller = {
        # Now: country scope (state controller)
        has_war = yes
    }
}
```

### From Country to Country

```
is_ally_of_FROM = {
    # Start: country scope (THIS)
    # Check: country scope (FROM)
    is_in_faction_with = FROM
}

has_puppet = {
    # Start: country scope
    any_subject_country = {
        # Now: country scope (each subject)
        is_puppet_of = ROOT
    }
}
```

---

## Common Scope Patterns

### Pattern 1: Check Own States

```
owns_industrial_state = {
    # Country scope
    any_owned_state = {
        # State scope
        industrial_capacity > 10
    }
}
```

### Pattern 2: Check Controller vs Owner

```
this_state_is_occupied = {
    # State scope
    NOT = {
        owner = {
            # Owner country
            tag = PREV.controller
        }
    }
}

# Or simpler:
this_state_is_occupied = {
    is_controlled_by = owner
}
```

### Pattern 3: Cross-Country Checks

```
FROM_is_stronger_than_ROOT = {
    # Evaluated in any scope
    FROM = {
        # FROM country
        strength_ratio = {
            tag = ROOT
            ratio > 1.2
        }
    }
}
```

### Pattern 4: State Owner Checks

```
state_owner_is_major = {
    # State scope
    owner = {
        # Country scope
        is_major = yes
    }
}

state_controlled_by_ROOT = {
    # State scope
    controller = {
        # Country scope
        tag = ROOT
    }
}

# Or simpler:
state_controlled_by_ROOT = {
    is_controlled_by = ROOT
}
```

### Pattern 5: Nested State Checks

```
capital_is_coastal = {
    # Country scope
    capital_scope = {
        # State scope (capital state)
        is_coastal = yes
    }
}

capital_in_europe = {
    # Country scope
    capital_scope = {
        # State scope
        is_on_continent = europe
    }
}
```

---

## PREV Chain

### Single PREV

```
owner_controls_state = {
    # State scope
    owner = {
        # Country scope (owner)
        # PREV = state scope
        controls_state = PREV
    }
}
```

### Double PREV

```
complex_check = {
    # Country scope (A)
    any_owned_state = {
        # State scope (B)
        owner = {
            # Country scope (C) - owner
            # PREV = B (state)
            # PREV.PREV = A (original country)
            is_in_faction_with = PREV.PREV
        }
    }
}
```

---

## Scope-Specific Triggers

### Country Scope Only

```
is_major_country = {
    # Must be in country scope
    is_major = yes
    has_war = yes
    is_in_faction_with = FROM
}
```

### State Scope Only

```
is_valuable_state = {
    # Must be in state scope
    is_coastal = yes
    industrial_capacity > 5
    is_core_of = ROOT
}
```

### Mixed Scope Navigation

```
country_owns_valuable_states = {
    # Country scope
    any_owned_state = {
        # State scope
        is_valuable_state = yes
    }
}
```

---

## Real-World Examples

### SSW Mod: Capital Checks

```
this_is_capital_and_europe = {
    # State scope
    AND = {
        is_on_continent = europe
        is_capital = yes
    }
}

capital_is_europe = {
    # Country scope
    any_owned_state = {
        # State scope
        this_is_capital_and_europe = yes
    }
}
```

### BSM Mod: Alliance Scope

```
in_same_alliance_as_FROM = {
    # Country scope (THIS)
    has_variable = alliance_id
    FROM = {
        # Country scope (FROM)
        has_variable = alliance_id
    }
    # Back to THIS
    check_variable = { alliance_id = FROM.alliance_id }
}
```

### Border Conflict Example

```
is_border_conflict_defender_vs_FROM = {
    # Country scope (THIS = defender)
    # FROM = attacker
    has_variable = ROOT.defender_state_vs_@FROM
}

has_not_initiated_with_FROM = {
    # Country scope
    NOT = {
        any_state = {
            # State scope
            # Check if FROM is defender against PREV (state owner)
            check_variable = { FROM.defender_state_vs_@PREV = id }
        }
    }
}
```

---

## Scope Documentation Best Practice

### Document Expected Scope

```
# Country scope
is_major_power = {
    is_major = yes
}

# State scope
is_core_state = {
    is_core_of = ROOT
}

# Character scope
is_fascist_leader = {
    has_ideology = fascism_ideology
}
```

### Note Scope Changes

```
# Country scope -> State scope
owns_coastal_territory = {
    any_owned_state = {  # Enters state scope
        is_coastal = yes
    }
}

# State scope -> Country scope -> State scope
owner_controls_this_state = {
    owner = {  # Enters country scope (owner)
        controls_state = PREV  # PREV = original state
    }
}
```

---

## Common Scope Errors

### ❌ Wrong Scope

```
# BAD - is_major only works in country scope
is_major_state = {
    # State scope
    is_major = yes  # ERROR!
}

# GOOD
state_owned_by_major = {
    # State scope
    owner = {
        # Country scope
        is_major = yes
    }
}
```

### ❌ Lost Scope Reference

```
# BAD - loses reference to original state
check_state_owner = {
    owner = {
        # What state? Lost reference!
        is_major = yes
    }
}

# GOOD - use PREV
check_state_owner = {
    owner = {
        # PREV = original state
        owns_state = PREV
    }
}
```

### ❌ Scope Mismatch

```
# BAD - FROM might not be a country
is_ally = {
    is_in_faction_with = FROM
}

# GOOD - verify FROM exists and is valid
is_ally = {
    FROM = { exists = yes }
    is_in_faction_with = FROM
}
```

---

## Scope Debugging

### Log Current Scope

```
debug_scope = {
    log = "Checking in scope: [This.GetName]"
    is_major = yes
    log = "Is major: yes"
}
```

### Verify Scope Type

```
# If unsure of scope, test with scope-specific commands
test_if_country_scope = {
    is_major = yes  # Works in country scope
}

test_if_state_scope = {
    is_coastal = yes  # Works in state scope
}
```

---

## Quick Reference

| Keyword | Meaning |
|---------|---------|
| `THIS` | Current scope |
| `ROOT` | Initiating scope (event/focus origin) |
| `FROM` | Context scope (target/parameter) |
| `PREV` | Previous scope (in nested blocks) |
| `owner` | Owner of state (state → country) |
| `controller` | Controller of state (state → country) |
| `capital_scope` | Capital state (country → state) |

| Navigation | From | To |
|------------|------|-----|
| `any_owned_state` | Country | State |
| `any_subject_country` | Country | Country (subjects) |
| `owner` | State | Country |
| `controller` | State | Country |
| `capital_scope` | Country | State |
| `overlord` | Country | Country (overlord) |
