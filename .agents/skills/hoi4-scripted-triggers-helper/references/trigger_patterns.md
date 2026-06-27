## HOI4 Scripted Trigger Patterns Reference

## Category 1: Basic Condition Patterns

### Single Condition
```
is_at_war = {
    has_war = yes
}

is_ai = {
    is_ai = yes
}

is_major = {
    is_major = yes
}
```

### AND Conditions
```
is_major_at_war = {
    is_major = yes
    has_war = yes
}

is_independent_democracy = {
    is_subject = no
    has_government = democratic
}
```

### OR Conditions
```
is_axis_member = {
    OR = {
        tag = GER
        tag = ITA
        tag = JAP
    }
}

has_economic_crisis = {
    OR = {
        has_idea = great_depression
        check_variable = { stability < 0.30 }
        has_country_flag = economic_collapse
    }
}
```

### NOT Conditions
```
is_not_at_war = {
    NOT = { has_war = yes }
}

is_independent = {
    NOT = { is_subject = yes }
}

can_declare_war = {
    NOT = { has_war_with = FROM }
    NOT = { is_in_faction_with = FROM }
}
```

---

## Category 2: Custom Tooltip Patterns

### Simple Tooltip
```
has_election_active = {
    custom_trigger_tooltip = {
        tooltip = tt_election_active
        has_country_flag = election_in_progress
    }
}
```

### Multiple Conditions with Tooltip
```
can_pass_bill = {
    custom_trigger_tooltip = {
        tooltip = tt_can_pass_bill
        OR = {
            check_variable = { lower_house_support > 0.50 }
            check_variable = { upper_house_support > 0.50 }
        }
    }
}
```

### Tooltip with Variable Display
```
has_enough_resources = {
    custom_trigger_tooltip = {
        tooltip = tt_has_enough_resources
        check_variable = { resource_stockpile > 100 }
    }
}

# Localisation:
# tt_has_enough_resources:0 "必要な資源: §Y[?resource_stockpile]§!/100"
```

---

## Category 3: Variable-Based Patterns

### Simple Variable Check
```
has_high_stability = {
    check_variable = { stability > 0.70 }
}

has_sufficient_manpower = {
    check_variable = { available_manpower > 50000 }
}
```

### Comparing Two Variables
```
factories_exceed_goal = {
    check_variable = { current_factories > factory_goal }
}

progress_complete = {
    check_variable = { progress >= 1.0 }
}
```

### Array Variable Check
```
has_bill_in_lower_house = {
    has_variable = lower_house_bills^0
}

has_three_objectives = {
    check_variable = { objectives^num = 3 }
}
```

### Token Comparison
```
sphere_matches = {
    check_variable = { my_sphere = FROM.my_sphere }
}

is_leader_of_sphere = {
    check_variable = { sphere_role = token:leader }
}
```

---

## Category 4: Geographic Patterns

### Continent Check
```
is_in_europe = {
    capital_scope = {
        is_on_continent = europe
    }
}

owns_asian_territory = {
    any_owned_state = {
        is_on_continent = asia
    }
}
```

### Region Check
```
is_balkan_state = {
    OR = {
        region = 24
        region = 25
        region = 26
        region = 27
    }
}

owns_balkan_territory = {
    any_owned_state = {
        is_balkan_state = yes
    }
}
```

### Specific State Check
```
owns_berlin = {
    owns_state = 64
}

controls_suez = {
    controls_state = 447
}

has_core_in_region = {
    any_state = {
        is_balkan_state = yes
        is_core_of = ROOT
    }
}
```

### Capital Check
```
capital_is_coastal = {
    capital_scope = {
        is_coastal = yes
    }
}

capital_in_balkans = {
    capital_scope = {
        is_balkan_state = yes
    }
}
```

---

## Category 5: Faction/Alliance Patterns

### Faction Membership
```
is_in_faction = {
    has_any_faction_member = yes
}

is_faction_leader = {
    is_faction_leader = yes
}

same_faction_as_FROM = {
    is_in_faction_with = FROM
}
```

### Custom Alliance System
```
in_economic_alliance = {
    has_variable = alliance_id
}

in_same_alliance_as_FROM = {
    has_variable = alliance_id
    FROM = { has_variable = alliance_id }
    check_variable = { alliance_id = FROM.alliance_id }
}

is_alliance_leader = {
    has_variable = alliance_id
    check_variable = { alliance_role = token:leader }
}
```

---

## Category 6: AI Logic Patterns

### AI Acceptance Logic
```
ai_will_accept = {
    has_opinion = {
        target = FROM
        value > 50
    }

    OR = {
        is_in_faction_with = FROM
        has_government = FROM
    }

    NOT = { has_war_with = FROM }
}
```

### AI Strategy
```
ai_wants_alliance = {
    is_ai = yes
    is_major = yes
    has_opinion = {
        target = FROM
        value > 30
    }
    FROM = {
        is_major = yes
        strength_ratio = { tag = ROOT ratio > 0.8 }
    }
}
```

### AI Modifier
```
ai_will_do_decision = {
    factor = 10

    modifier = {
        factor = 2
        is_major = yes
    }

    modifier = {
        factor = 0
        has_war = yes
    }
}
```

---

## Category 7: Scope-Specific Patterns

### Country Scope
```
is_valid_target = {
    exists = yes
    NOT = { is_in_faction_with = ROOT }
    NOT = { is_subject_of = ROOT }
    NOT = { tag = ROOT }
}

is_puppet_of_ROOT = {
    is_puppet_of = ROOT
}
```

### State Scope
```
is_valuable_state = {
    industrial_capacity > 5
    is_coastal = yes
    NOT = { is_core_of = ROOT }
}

ROOT_has_divisions_here = {
    ROOT = {
        divisions_in_state = {
            state = PREV
            size > 0
        }
    }
}
```

### Character Scope
```
is_fascist_leader = {
    has_ideology = fascism_ideology
}

has_high_popularity = {
    check_variable = { popularity > 0.50 }
}
```

---

## Category 8: System State Patterns

### GUI State
```
gui_is_open = {
    has_country_flag = gui_window_open
}

page_is_selected = {
    check_variable = { current_page = 2 }
}

menu_option_unlocked = {
    has_country_flag = option_unlocked
    check_variable = { option_requirements_met = 1 }
}
```

### System Status
```
system_is_active = {
    has_country_flag = system_enabled
    NOT = { has_country_flag = system_paused }
}

system_has_cooldown = {
    has_country_flag = system_cooldown
}
```

### Process State
```
bill_in_deliberation = {
    has_variable = current_bill_id
}

election_active = {
    has_country_flag = election_in_progress
}

war_plan_executing = {
    has_variable = plan_stage
    check_variable = { plan_stage > 0 }
}
```

---

## Category 9: DLC/Content Check Patterns

### DLC Check
```
has_required_dlc = {
    has_dlc = "My DLC Name"
}

can_use_mechanic = {
    OR = {
        has_dlc = "DLC A"
        has_dlc = "DLC B"
    }
}
```

### Focus Tree Check
```
has_unique_tree = {
    NOT = { has_country_flag = generic_focus_tree }
    OR = {
        tag = GER
        tag = USA
        tag = JAP
    }
}

can_switch_ideology = {
    NOT = { tag = GER }
    NOT = {
        AND = {
            tag = USA
            has_dlc = "Man the Guns"
        }
    }
}
```

---

## Category 10: Complex Helper Patterns

### Nested Trigger Chain
```
# Base
is_system_participant = {
    has_variable = participant_id
}

# Level 1
is_system_leader = {
    is_system_participant = yes
    check_variable = { is_leader = 1 }
}

# Level 2
can_invite_to_system = {
    is_system_leader = yes
    FROM = {
        is_system_participant = no
        ai_will_accept_invite = yes
    }
}
```

### Composite Trigger
```
is_eligible_for_event = {
    is_major = yes
    is_at_war = no
    has_completed_prerequisites = yes
    NOT = { has_cooldown_flag = yes }
}

has_completed_prerequisites = {
    has_completed_focus = prerequisite_1
    has_completed_focus = prerequisite_2
    check_variable = { research_progress > 0.50 }
}

has_cooldown_flag = {
    has_country_flag = event_cooldown
}
```

---

## Template: Decision Visibility/Availability

```
# Visible condition
can_see_decision = {
    is_subject = no
    has_dlc = "My DLC"
    has_completed_focus = unlock_focus
}

# Available condition
can_take_decision = {
    is_at_war = no
    has_political_power > 100
    has_stability > 0.50
}

# AI will do
ai_will_take_decision = {
    is_ai = yes
    is_major = yes
    has_opinion = {
        target = FROM
        value > 50
    }
}
```

---

## Template: GUI System

```
# Can open GUI
can_open_gui = {
    is_ai = no
    has_completed_focus = gui_unlock
    NOT = { has_country_flag = gui_disabled }
}

# Can interact with element
can_interact = {
    can_open_gui = yes
    check_variable = { element_unlocked = 1 }
    NOT = { has_country_flag = element_cooldown }
}

# Element is selected
is_selected = {
    check_variable = { selected_id = element_id }
}

# Can confirm action
can_confirm = {
    can_interact = yes
    has_sufficient_resources = yes
    passes_requirements = yes
}
```

---

## Template: Alliance/Sphere System

```
# Formation
can_form_sphere_visible = {
    is_subject = no
    is_major = yes
}

can_form_sphere_allowed = {
    has_political_power > 100
    NOT = { has_country_flag = sphere_cooldown }
    NOT = { has_variable = my_sphere }
}

# Joining
can_join_sphere_visible = {
    is_subject = no
    FROM = { is_sphere_leader = yes }
}

can_join_sphere_allowed = {
    NOT = { has_variable = my_sphere }
    has_opinion = {
        target = FROM
        value > 30
    }
}

# Membership check
is_sphere_leader = {
    has_variable = my_sphere
    check_variable = { is_leader = 1 }
}

in_same_sphere_as_FROM = {
    has_variable = my_sphere
    FROM = { has_variable = my_sphere }
    check_variable = { my_sphere = FROM.my_sphere }
}

is_member_of_ROOT_sphere = {
    ROOT = { is_sphere_leader = yes }
    in_same_sphere_as_FROM = yes
}
```

---

## Template: Parliament/Legislative System

```
# Deliberation status
bill_in_deliberation = {
    OR = {
        bill_in_lower_house = yes
        bill_in_upper_house = yes
    }
}

bill_in_lower_house = {
    custom_trigger_tooltip = {
        tooltip = tt_bill_in_lower_house
        has_variable = lower_house_bill_id
    }
}

bill_in_upper_house = {
    custom_trigger_tooltip = {
        tooltip = tt_bill_in_upper_house
        has_variable = upper_house_bill_id
    }
}

not_in_deliberation = {
    custom_trigger_tooltip = {
        tooltip = tt_not_in_deliberation
        NOT = { has_variable = lower_house_bill_id }
        NOT = { has_variable = upper_house_bill_id }
    }
}

# Support check
has_majority_support = {
    check_variable = { support_percentage > 0.50 }
}

can_pass_bill = {
    bill_in_deliberation = yes
    has_majority_support = yes
}

# Election
is_in_election = {
    custom_trigger_tooltip = {
        tooltip = tt_is_in_election
        has_country_flag = election_active
    }
}

can_call_election = {
    NOT = { is_in_election = yes }
    check_variable = { months_since_election > 12 }
}
```

---

## Common Mistakes

### ❌ Missing Scope
```
# BAD - will error if FROM doesn't exist
is_ally = {
    is_in_faction_with = FROM
}

# GOOD - check FROM exists
is_ally = {
    FROM = { exists = yes }
    is_in_faction_with = FROM
}
```

### ❌ Expensive Operation Without Guard
```
# BAD - always expensive
owns_many_states = {
    any_owned_state = {
        # Complex check
    }
}

# GOOD - early exit
owns_many_states = {
    num_of_owned_states > 10
    any_owned_state = {
        # Complex check
    }
}
```

### ❌ Unclear Trigger Name
```
# BAD
check_1 = {
    is_major = yes
    has_war = yes
}

# GOOD
is_major_at_war = {
    is_major = yes
    has_war = yes
}
```
