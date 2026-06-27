---
name: hoi4-scripted-triggers-helper
description: Guide for creating reusable conditional logic with HOI4 scripted triggers. Use when the user (1) Needs to reuse complex trigger conditions, (2) Wants to simplify repeated logic, (3) Needs custom tooltips for triggers, or (4) Says phrases like "reusable trigger", "scripted trigger", "trigger template", "conditional helper", etc. Covers trigger definition patterns and best practices.
---

# HOI4 Scripted Triggers Helper

## Overview

Scripted triggers are reusable conditional logic blocks that simplify complex triggers and avoid code duplication. Define once, use everywhere. Essential for maintainable modding and complex conditional systems.

## When This Skill Triggers

This skill activates when:
- User needs to reuse complex trigger conditions
- User wants to avoid duplicating trigger logic
- User needs custom tooltips for specific conditions
- User is building systems with repeated conditional checks
- User says: "reusable trigger", "scripted trigger", "trigger template", "conditional helper"

## Quick Reference

**File Location:** `common/scripted_triggers/<filename>.txt`

**Basic Structure:**
```
trigger_name = {
    # Condition logic
    has_war = yes
    is_major = yes
}
```

**Usage:**
```
# In any trigger block:
trigger = {
    trigger_name = yes
}
```

---

## Part 1: Basic Triggers

### Simple Trigger

**File:** `common/scripted_triggers/my_triggers.txt`

```
is_at_war = {
    has_war = yes
}

is_major_power = {
    is_major = yes
}

is_major_at_war = {
    is_major = yes
    has_war = yes
}
```

**Usage:**
```
# In national focus:
available = {
    is_major_at_war = yes
}

# In event trigger:
trigger = {
    is_at_war = yes
}

# In decision:
visible = {
    is_major_power = yes
}
```

### OR Trigger

```
is_axis_member = {
    OR = {
        tag = GER
        tag = ITA
        tag = JAP
        is_in_faction_with = GER
    }
}
```

### AND with NOT

```
can_get_wargoal_on_THIS = {
    exists = yes
    NOT = { is_in_faction_with = ROOT }
    NOT = { is_subject_of = ROOT }
}
```

---

## Part 2: Custom Tooltip Triggers

### Basic Custom Tooltip

```
is_in_election = {
    custom_trigger_tooltip = {
        tooltip = tt_is_in_election
        has_country_flag = election_active
    }
}
```

**Localization:**
```yaml
l_japanese:
 tt_is_in_election:0 "§R選挙期間中§!"
```

### Multiple Conditions with Tooltip

```
during_parliament_deliberation = {
    custom_trigger_tooltip = {
        tooltip = tt_during_deliberations
        OR = {
            has_variable = lower_house_bill_id
            has_variable = upper_house_bill_id
        }
    }
}
```

### Negated Tooltip

```
not_during_deliberations = {
    custom_trigger_tooltip = {
        tooltip = tt_not_during_deliberations
        NOT = { has_variable = lower_house_bill^0 }
        NOT = { has_variable = upper_house_bill^0 }
    }
}
```

### Complex Tooltip

```
has_dynamic_economic_modifier = {
    custom_trigger_tooltip = {
        tooltip = tt_has_economic_modifier
        OR = {
            has_dynamic_modifier = {
                modifier = leader_modifier
            }
            has_dynamic_modifier = {
                modifier = member_modifier
            }
        }
    }
}
```

---

## Part 3: Variable-Based Triggers

### Simple Variable Check

```
has_high_stability = {
    check_variable = { stability_level > 0.70 }
}

has_low_manpower = {
    check_variable = { manpower_reserve < 100000 }
}
```

### Array Variable Check

```
bill_in_lower_house = {
    has_variable = parliament_bills^0
}

bill_in_upper_house = {
    has_variable = parliament_bills^1
}
```

### Token Comparison

```
is_sphere_leader = {
    has_variable = bsm_ea_sphere
    check_variable = { bsm_ea_is_leader = 1 }
}

in_same_economic_alliance = {
    has_variable = bsm_ea_sphere
    FROM = { has_variable = bsm_ea_sphere }
    check_variable = { bsm_ea_sphere = FROM.bsm_ea_sphere }
}
```

---

## Part 4: Region and Geography Triggers

### Continent Checks

```
capital_is_europe = {
    any_owned_state = {
        is_capital = yes
        is_on_continent = europe
    }
}

capital_is_asia = {
    any_owned_state = {
        is_capital = yes
        is_on_continent = asia
    }
}
```

### Regional Checks

```
this_is_balkan_state = {
    OR = {
        region = 24  # Western Balkans
        region = 26  # Eastern Balkans
        region = 27  # Northern Balkans
        region = 25  # Greece
    }
}

owns_balkan_state = {
    any_owned_state = {
        this_is_balkan_state = yes
    }
}

this_is_scandinavian_state = {
    OR = {
        region = 11   # Southern Norway
        region = 191  # Northern Norway
        region = 277  # Northern Sweden
        region = 10   # Southern Sweden
        state = 215   # North Karelia
        state = 146   # Karelia
    }
}

owns_scandinavian_state = {
    any_owned_state = {
        this_is_scandinavian_state = yes
    }
}
```

---

## Part 5: Scope-Specific Triggers

### Country Scope

```
is_puppet_and_faction_member = {
    is_puppet_of = ROOT
    is_in_faction_with = ROOT
}

is_ally_of_japan = {
    OR = {
        tag = JAP
        is_in_faction_with = JAP
        is_subject_of = JAP
    }
}
```

### State Scope

```
has_ROOT_divisions_in_state = {
    custom_trigger_tooltip = {
        tooltip = at_least_one_division_in_state
        ROOT = {
            divisions_in_state = {
                state = PREV
                size > 0
            }
        }
    }
}
```

### Border Conflict Triggers

```
is_border_conflict_defender_vs_FROM = {
    has_variable = ROOT.defender_state_vs_@FROM
}

has_not_initiated_border_incident_with_FROM = {
    custom_trigger_tooltip = {
        tooltip = not_initiated_border_incident_with_FROM
        NOT = {
            any_state = {
                check_variable = { FROM.defender_state_vs_@PREV = id }
            }
        }
    }
}
```

---

## Part 6: AI Logic Triggers

### AI Acceptance Logic

```
ai_will_accept_alliance = {
    # Minimum opinion
    has_opinion = {
        target = FROM
        value > 30
    }

    # Ideology check
    NOT = {
        AND = {
            has_government = democratic
            FROM = { has_government = fascism }
        }
    }

    # Tension check
    FROM = {
        check_variable = { generated_world_tension < 10 }
    }
}
```

### DLC/Focus Tree Checks

```
has_unique_focus_tree = {
    NOT = { tag = GER }
    NOT = { tag = USA }
    NOT = { tag = JAP }
    NOT = {
        AND = {
            tag = FRA
            has_dlc = "La Resistance"
        }
    }
}
```

---

## Part 7: Complex Helper Triggers

### Economic Alliance Helper

```
is_in_economic_alliance_with = {
    has_variable = bsm_ea_sphere
    FROM = { has_variable = bsm_ea_sphere }
    check_variable = { bsm_ea_sphere = FROM.bsm_ea_sphere }
}

is_economic_alliance_leader = {
    has_variable = bsm_ea_sphere
    check_variable = { bsm_ea_is_leader = 1 }
}

is_member_of_ROOT_economic_alliance = {
    # ROOT = Leader
    # FROM/THIS = Member check
    ROOT = { is_economic_alliance_leader = yes }
    is_in_economic_alliance_with = yes
}
```

### Visibility Helpers

```
can_form_alliance_visible = {
    is_subject = no
    NOT = { has_country_flag = alliance_cooldown }
}

can_form_alliance_allowed = {
    is_major = yes
    NOT = { has_war = yes }
    has_political_power > 100
}

can_join_alliance_visible = {
    is_subject = no
    FROM = { is_economic_alliance_leader = yes }
}

can_join_alliance_allowed = {
    has_opinion = {
        target = FROM
        value > 50
    }
}
```

---

## Real-World Examples

### SSW Mod: Capital Region Checks

```
this_is_capital_and_europe = {
    AND = {
        is_on_continent = europe
        is_capital = yes
    }
}

capital_is_europe = {
    any_owned_state = {
        this_is_capital_and_europe = yes
    }
}

capital_is_south_america = {
    any_owned_state = {
        AND = {
            is_on_continent = south_america
            is_capital = yes
        }
    }
}
```

### SSW Mod: Parliament System

```
during_deliberations_on_parliament = {
    OR = {
        during_deliberations_on_lower_house = yes
        during_deliberations_on_upper_house = yes
    }
}

not_during_deliberations_on_parliament = {
    custom_trigger_tooltip = {
        tooltip = tt_not_during_deliberations_on_parliament
        NOT = { has_variable = lower_house_current_law^0 }
        NOT = { has_variable = upper_house_current_law^0 }
    }
}

during_deliberations_on_lower_house = {
    custom_trigger_tooltip = {
        tooltip = tt_during_deliberations_on_lower_house
        has_variable = lower_house_current_law^0
    }
}

is_in_election = {
    custom_trigger_tooltip = {
        tooltip = tt_is_in_election
        has_country_flag = election_active
    }
}
```

### BSM Mod: Economic Alliance System

```
is_in_economic_alliance_with = {
    has_variable = bsm_ea_sphere
    FROM = { has_variable = bsm_ea_sphere }
    check_variable = { bsm_ea_sphere = FROM.bsm_ea_sphere }
}

ai_will_accept_economic_alliance = {
    has_opinion = {
        target = FROM
        value > 30
    }

    NOT = {
        OR = {
            AND = {
                has_government = kyonulism
                FROM = { has_government = hinnulism }
            }
            AND = {
                has_government = longitudinalism
                FROM = { has_government = horizontalism }
            }
        }
    }

    FROM = {
        check_variable = { generated_world_tension < 10 }
    }
}

is_economic_alliance_member_of_root = {
    ROOT = { is_bsm_ea_leader = yes }
    is_in_economic_alliance_with = yes
}
```

---

## Common Patterns

### Pattern 1: Reusable Faction Check

```
is_axis = {
    OR = {
        tag = GER
        tag = ITA
        tag = JAP
        is_in_faction_with = GER
    }
}

is_allies = {
    OR = {
        tag = ENG
        tag = FRA
        tag = USA
        is_in_faction_with = ENG
    }
}
```

### Pattern 2: State Validation

```
is_valid_target_state = {
    NOT = { is_owned_by = ROOT }
    NOT = { is_core_of = ROOT }
    is_controlled_by = FROM
    is_coastal = yes
}
```

### Pattern 3: GUI Availability

```
can_open_gui = {
    is_ai = no
    NOT = { has_country_flag = gui_cooldown }
    has_completed_focus = unlock_gui_focus
}
```

### Pattern 4: Resource Check

```
has_sufficient_resources = {
    has_political_power > 50
    has_manpower > 10000
    check_variable = { resource_stockpile > 100 }
}
```

### Pattern 5: Nested Trigger Chain

```
is_eligible_for_system = {
    can_participate_visible = yes
    can_participate_allowed = yes
    NOT = { has_system_penalty = yes }
}

can_participate_visible = {
    is_subject = no
    has_dlc = "My DLC"
}

can_participate_allowed = {
    is_major = yes
    has_completed_focus = system_unlock
}

has_system_penalty = {
    OR = {
        has_country_flag = system_banned
        has_idea = system_penalty_idea
    }
}
```

---

## Best Practices

### 1. Name Clearly

```
# GOOD
is_major_at_war
can_form_alliance
has_completed_economic_tree

# BAD
check_1
trigger_a
test
```

### 2. Document Scope

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

### 3. Use Custom Tooltips When Needed

```
# Without tooltip (confusing)
has_bill = {
    has_variable = bill_id^0
}

# With tooltip (clear)
has_bill = {
    custom_trigger_tooltip = {
        tooltip = tt_has_bill_in_parliament
        has_variable = bill_id^0
    }
}
```

### 4. Chain Triggers

```
# Base trigger
is_economic_member = {
    has_variable = economic_alliance_id
}

# Build on base
is_economic_leader = {
    is_economic_member = yes
    check_variable = { is_leader = 1 }
}

# Further chain
can_invite_to_alliance = {
    is_economic_leader = yes
    FROM = { is_economic_member = no }
}
```

### 5. Avoid Expensive Operations

```
# EXPENSIVE (avoid if possible)
has_many_factories = {
    num_of_factories > 50  # Counts all factories
}

# BETTER (if you can cache)
has_many_factories = {
    check_variable = { factory_count > 50 }
}
```

---

## File Organization

### By System

```
# economic_alliance_triggers.txt
is_in_alliance = { ... }
can_form_alliance = { ... }
can_join_alliance = { ... }

# parliament_triggers.txt
during_deliberations = { ... }
has_majority = { ... }
can_pass_bill = { ... }

# gui_triggers.txt
can_open_menu = { ... }
is_page_unlocked = { ...}
has_selected_option = { ... }
```

### By Country

```
# JAP_triggers.txt
JAP_is_militarist = { ... }
JAP_has_zaibatsu = { ... }
JAP_can_form_co_prosperity = { ... }

# GER_triggers.txt
GER_is_nazi = { ... }
GER_has_four_year_plan = { ... }
```

### By Feature

```
# region_triggers.txt
is_balkan_state = { ... }
is_scandinavian = { ... }
is_mediterranean = { ... }

# ideology_triggers.txt
has_democratic_government = { ... }
has_fascist_government = { ... }
```

---

## Usage Patterns

### In National Focuses

```
focus = {
    id = my_focus

    available = {
        is_major_power = yes
        not_at_war = yes
    }

    visible = {
        can_see_focus_tree = yes
    }
}
```

### In Decisions

```
decision = {
    visible = {
        can_form_alliance_visible = yes
    }

    available = {
        can_form_alliance_allowed = yes
    }

    ai_will_do = {
        factor = 10
        modifier = {
            factor = 0
            NOT = { ai_will_form_alliance = yes }
        }
    }
}
```

### In Events

```
country_event = {
    trigger = {
        is_major_at_war = yes
        has_low_stability = yes
    }

    option = {
        trigger = {
            can_choose_peaceful_option = yes
        }
    }
}
```

### In Scripted GUI

```
scripted_gui = {
    my_gui = {
        visible = {
            can_open_gui = yes
        }

        trigger = {
            enabled = {
                can_interact_with_gui = yes
            }
        }
    }
}
```

---

## Performance Tips

- ✅ Scripted triggers are efficient (evaluated once per check)
- ⚠️ Avoid expensive operations (any_country, any_state loops)
- ✅ Cache results in variables when checked frequently
- ✅ Put cheap checks first in AND blocks
- ✅ Use NOT = { ... } sparingly in expensive triggers

---

## Debugging

### Test Trigger

```
# In console:
add_country_flag = test_flag

# Or via event:
country_event = {
    trigger = {
        my_trigger = yes
    }
    immediate = {
        log = "Trigger worked!"
    }
}
```

### Log Trigger Results

```
my_trigger = {
    is_major = yes
    log = "[This.GetName] is major"
    has_war = yes
    log = "[This.GetName] has war"
}
```

---

## Reference Documentation

For detailed patterns:
- `references/trigger_patterns.md` - Common trigger patterns
- `references/scope_reference.md` - Scope usage guide

For real-world examples:
- SSW mod: `/Users/eightman/Desktop/HOI4_modding/SSW_mod/common/scripted_triggers/`
- BSM mod: `/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai/common/scripted_triggers/`

---

## Integration with Other Skills

### With hoi4-variable-helper
Use variables in triggers for dynamic conditions.

### With hoi4-scripted-localisation-helper
Custom tooltips reference localisation keys.

### With hoi4-scripted-effect-maker
Triggers determine when effects execute.

---

## Quick Decision Tree

**Repeating same trigger logic?** → Use **scripted trigger**

**Need custom tooltip?** → Use **custom_trigger_tooltip**

**Complex AND/OR conditions?** → Create **helper trigger**

**Checking variables?** → Use **check_variable** in trigger

**Geographic checks?** → Create **region helper triggers**

**System availability?** → Create **_visible** and **_allowed** triggers
