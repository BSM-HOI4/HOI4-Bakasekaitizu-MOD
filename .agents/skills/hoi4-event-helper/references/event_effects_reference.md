# HOI4 Event Effects Reference

This document lists common effects used in HOI4 events.

---

## Political Effects

### Political Power
```
add_political_power = 50      # Add political power
add_political_power = -100    # Subtract political power
```

### Stability
```
add_stability = 0.05   # Add 5% stability
add_stability = -0.10  # Subtract 10% stability
```

### War Support
```
add_war_support = 0.05   # Add 5% war support
add_war_support = -0.10  # Subtract 10% war support
```

### National Unity (Old versions)
```
add_national_unity = 0.05
```

---

## Government and Ideology

### Change Government
```
set_politics = {
    ruling_party = fascism
    elections_allowed = no
}
```

### Add Ideology Support
```
add_popularity = {
    ideology = communism
    popularity = 0.15  # Add 15%
}
```

### Start Civil War
```
start_civil_war = {
    ruling_party = fascism
    ideology = democratic
    size = 0.5  # Rebels get 50% of military
}
```

---

## Country Flags

### Set Flag
```
set_country_flag = flag_name
set_country_flag = {
    flag = flag_name
    days = 30  # Flag expires after 30 days
}
```

### Clear Flag
```
clr_country_flag = flag_name
```

### Check Flag (in trigger)
```
has_country_flag = flag_name
```

### Global Flags
```
set_global_flag = flag_name
clr_global_flag = flag_name
has_global_flag = flag_name  # In trigger
```

---

## Military Effects

### Army Experience
```
army_experience = 25    # Add 25 army XP
army_experience = -10   # Subtract 10 army XP
```

### Air Experience
```
air_experience = 25
```

### Navy Experience
```
navy_experience = 25
```

### Add Equipment
```
add_equipment_to_stockpile = {
    type = infantry_equipment
    amount = 1000
}
```

### Add Manpower
```
add_manpower = 10000   # Add 10k manpower
add_manpower = -5000   # Subtract 5k manpower
```

### Create Unit
```
load_oob = "GER_1939"  # Load order of battle file
```

---

## Diplomatic Effects

### Declare War
```
declare_war_on = {
    target = POL
    type = annex_everything
}
```

**War Types:**
- `annex_everything` - Total war
- `take_claimed_state` - Claim war
- `take_core_state` - Core war
- `topple_government` - Regime change

### Create Faction
```
create_faction = faction_name_loc_key
```

### Join Faction
```
GER = {
    add_to_faction = ROOT
}
```

### Leave Faction
```
leave_faction = yes
```

### Puppet
```
puppet = GER  # ROOT becomes GER's puppet

# Or
GER = {
    puppet = ROOT  # GER becomes ROOT's puppet
}
```

### End Puppet
```
end_puppet = TAG
```

### Annex Country
```
annex_country = {
    target = POL
    transfer_troops = yes
}
```

### Release Puppet
```
release_puppet = POL
```

### Independence
```
release = POL  # Release as independent
```

---

## Opinion Modifiers

### Add Opinion Modifier
```
add_opinion_modifier = {
    target = GER
    modifier = positive_relation  # Modifier defined in common/opinion_modifiers/
}
```

### Remove Opinion Modifier
```
remove_opinion_modifier = {
    target = GER
    modifier = positive_relation
}
```

### Reverse Opinion Modifier
```
reverse_add_opinion_modifier = {
    target = GER
    modifier = positive_relation
}
# GER gets opinion of ROOT, not ROOT gets opinion of GER
```

---

## Ideas and National Spirits

### Add Idea
```
add_ideas = idea_name
```

### Remove Idea
```
remove_ideas = idea_name
```

### Swap Idea
```
swap_ideas = {
    remove_idea = old_idea
    add_idea = new_idea
}
```

### Modify Idea
```
modify_timed_idea = {
    idea = timed_idea_name
    days = 60  # Extend/reduce duration
}
```

---

## Resources

### Add Resources
```
add_resource = {
    type = steel
    amount = 10
    state = 123
}
```

---

## States and Buildings

### Transfer State
```
transfer_state = 123  # Transfer state 123 to ROOT
```

### Add State Core
```
add_state_core = 123  # Add state 123 as core
```

### Remove State Core
```
remove_state_core = 123
```

### Add State Claim
```
add_state_claim = 123
```

### Add Building
```
123 = {
    add_building_construction = {
        type = industrial_complex
        level = 2
        instant_build = yes
    }
}
```

### Damage Building
```
123 = {
    damage_building = {
        type = industrial_complex
        damage = 1
    }
}
```

### Add Extra State Slots
```
123 = {
    add_extra_state_shared_building_slots = 2
}
```

---

## Technology and Research

### Add Research Slot
```
add_research_slot = 1
```

### Add Tech Bonus
```
add_tech_bonus = {
    name = infantry_tech_bonus
    bonus = 1.0  # 100% bonus
    uses = 2
    category = infantry_weapons
}
```

### Set Technology
```
set_technology = {
    tech_name = 1
}
```

---

## Leaders and Advisors

### Create Country Leader
```
create_country_leader = {
    name = "Leader Name"
    picture = "gfx_portrait.dds"
    ideology = nazism
    traits = {
        trait_name
    }
}
```

### Create Field Marshal
```
create_field_marshal = {
    name = "Marshal Name"
    picture = "portrait.dds"
    traits = {
        trait_name
    }
    skill = 4
    attack_skill = 3
    defense_skill = 4
    planning_skill = 3
    logistics_skill = 2
}
```

### Create Corps Commander
```
create_corps_commander = {
    name = "General Name"
    picture = "portrait.dds"
    traits = {
        trait_name
    }
    skill = 3
    attack_skill = 2
    defense_skill = 3
    planning_skill = 2
    logistics_skill = 3
}
```

### Create Navy Leader
```
create_navy_leader = {
    name = "Admiral Name"
    picture = "portrait.dds"
    traits = {
        trait_name
    }
    skill = 3
}
```

### Add Unit Leader Trait
```
# In unit_leader scope
add_unit_leader_trait = trait_name
```

### Remove Unit Leader Trait
```
remove_unit_leader_trait = trait_name
```

### Retire Leader
```
retire_country_leader = yes
```

### Kill Leader
```
kill_country_leader = yes
```

---

## Variables

### Set Variable
```
set_variable = { var_name = 10 }
set_variable = { var_name = 10.5 }
```

### Add to Variable
```
add_to_variable = { var_name = 5 }
```

### Subtract from Variable
```
subtract_from_variable = { var_name = 3 }
```

### Multiply Variable
```
multiply_variable = { var_name = 2 }
```

### Divide Variable
```
divide_variable = { var_name = 2 }
```

### Clear Variable
```
clear_variable = var_name
```

### Check Variable (in trigger)
```
check_variable = { var_name > 10 }
check_variable = { var_name < 5 }
check_variable = { var_name = 10 }
```

---

## Arrays

### Add to Array
```
add_to_array = {
    array_name = value
}
```

### Remove from Array
```
remove_from_array = {
    array_name = value
}
```

### Clear Array
```
clear_array = array_name
```

### Resize Array
```
resize_array = {
    array = array_name
    size = 10
}
```

---

## Event Triggering

### Trigger Country Event
```
country_event = {
    id = event.1
    days = 7
    random_days = 3
}
```

### Trigger for Another Country
```
GER = {
    country_event = {
        id = event.1
    }
}
```

### Trigger for Every Country
```
every_country = {
    limit = { is_major = yes }
    country_event = {
        id = event.1
    }
}
```

### Trigger News Event
```
news_event = {
    id = news.1
    days = 1
}
```

### Hidden Event
```
country_event = {
    id = event.1
    hidden = yes
}
```

---

## Focus and Decision Effects

### Unlock Decision
```
unlock_decision_tooltip = decision_name
unlock_decision_category_tooltip = category_name
```

### Activate Targeted Decision
```
activate_targeted_decision = {
    decision = decision_name
    target = GER
}
```

### Complete National Focus
```
complete_national_focus = focus_name
```

### Unlock National Focus
```
unlock_national_focus = focus_name
```

---

## Custom Effects

### Trigger Effect Tooltip
```
effect_tooltip = {
    add_political_power = 50
}
# Shows tooltip without executing
```

### Hidden Effect
```
hidden_effect = {
    add_political_power = 50
}
# Executes without showing tooltip
```

### Custom Effect Tooltip
```
custom_effect_tooltip = my_tooltip_loc_key
hidden_effect = {
    # Actual effects
}
```

---

## Scopes

### Every Country
```
every_country = {
    limit = {
        is_major = yes
    }
    add_political_power = 10
}
```

### Random Country
```
random_country = {
    limit = {
        is_major = yes
    }
    country_event = { id = event.1 }
}
```

### Every Neighbor Country
```
every_neighbor_country = {
    add_opinion_modifier = {
        target = ROOT
        modifier = negative_relation
    }
}
```

### Every Owned State
```
every_owned_state = {
    add_extra_state_shared_building_slots = 1
}
```

### Every State
```
every_state = {
    limit = {
        is_coastal = yes
    }
    # Effects
}
```

### Random Owned State
```
random_owned_state = {
    limit = {
        is_coastal = yes
    }
    # Effects
}
```

---

## Conditional Effects

### If-Else
```
if = {
    limit = {
        has_war = yes
    }
    add_war_support = 0.05
}
else_if = {
    limit = {
        has_stability > 0.5
    }
    add_stability = 0.02
}
else = {
    add_political_power = 25
}
```

---

## Meta Effects

### Log to Console
```
log = "Text message [Root.GetName]"
```

### Save Event Target
```
save_event_target_as = target_name
```

### Clear Event Target
```
clear_event_target = target_name
```

### Save Global Event Target
```
save_global_event_target_as = target_name
```

---

## Common Effect Combinations

### Grant War Goal
```
create_wargoal = {
    type = annex_everything
    target = POL
}
```

### White Peace
```
white_peace = GER
```

### Transfer Technology
```
GER = {
    set_technology = {
        advanced_infantry = 1
    }
}
```

### Boost Party Popularity
```
add_popularity = {
    ideology = fascism
    popularity = 0.1
}
```

### Remove Cores
```
every_owned_state = {
    limit = {
        is_core_of = POL
    }
    remove_core_of = POL
}
```

---

## Event Chain Patterns

### Start Chain with Flag
```
option = {
    name = event.1.a
    set_country_flag = event_chain_active
    country_event = {
        id = event.2
        days = 7
    }
}
```

### Continue Chain
```
country_event = {
    id = event.2
    trigger = {
        has_country_flag = event_chain_active
    }

    option = {
        name = event.2.a
        country_event = {
            id = event.3
            days = 7
        }
    }
}
```

### End Chain
```
country_event = {
    id = event.3

    immediate = {
        clr_country_flag = event_chain_active
    }

    option = {
        name = event.3.a
        # Final effects
    }
}
```

---

## Performance Tips

1. **Use Limits**: Always use limits in every_country/every_state loops
```
every_country = {
    limit = { is_major = yes }  # Only majors, not all countries
    # Effects
}
```

2. **Hidden Effects**: Use hidden_effect for multiple effects
```
hidden_effect = {
    add_political_power = 50
    add_stability = 0.05
    set_country_flag = flag
}
```

3. **Avoid Nested Loops**: Don't nest every_country inside every_country
```
# BAD
every_country = {
    every_country = {
        # Very slow!
    }
}

# GOOD
every_country = {
    limit = { is_major = yes }
    save_event_target_as = major_country
}
```

---

## Common Patterns

### Give Player Choice of Bonuses
```
option = {
    name = event.1.a  # Military
    army_experience = 25
}

option = {
    name = event.1.b  # Economic
    add_stability = 0.05
}

option = {
    name = event.1.c  # Political
    add_political_power = 100
}
```

### Random Outcome
```
random_list = {
    50 = {
        # 50% chance
        add_political_power = 100
    }
    30 = {
        # 30% chance
        add_stability = 0.05
    }
    20 = {
        # 20% chance
        # Nothing happens
    }
}
```

### Bilateral Diplomacy
```
# Event for ROOT (sender)
option = {
    name = event.1.a
    GER = {
        country_event = {
            id = event.2  # Proposal for GER
        }
    }
}

# Event for GER (receiver)
country_event = {
    id = event.2

    option = {
        name = event.2.a  # Accept
        FROM = {  # Sender (ROOT of event.1)
            country_event = {
                id = event.3  # Acceptance notification
            }
        }
    }

    option = {
        name = event.2.b  # Reject
        FROM = {
            country_event = {
                id = event.4  # Rejection notification
            }
        }
    }
}
```
