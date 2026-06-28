# modifier@ Pipeline Reference

## How modifier@ fits into a system

`modifier@<token>` reads the current summed value of a modifier on the scope. Crucially this includes **custom modifier tokens you define** (in `common/modifier_definitions/`) and apply via dynamic modifiers, ideas, focuses, or laws — making `modifier@` the standard input port from "content" (ideas/focuses) into "script" (your calculation systems).

```
Content side:  idea/focus/law → adds my_growth_modifier / my_growth_factor
Script side:   modifier@my_growth_modifier ──▶ pipeline ──▶ stored variables ──▶ GUI / effects
```

## Channel design convention

Define a flat and a factor channel per quantity:

```
# common/modifier_definitions/my_channels.txt
my_growth_modifier = {
    color_type = good
    value_type = number
    precision = 2
    category = country
}
my_growth_factor = {
    color_type = good
    value_type = percentage
    precision = 2
    category = country
}
```

Combine with the canonical read:

```
set_variable = { growth = modifier@my_growth_modifier }       # flat
set_temp_variable = { f = modifier@my_growth_factor }
add_to_temp_variable = { f = 1 }                              # delta → multiplier
multiply_variable = { growth = f }                            # growth = flat × (1 + factor)
```

### Negative-factor guard

```
set_temp_variable = { f = 1 }
add_to_temp_variable = { f = modifier@my_growth_factor }
if = {
    limit = { check_variable = { f < 0 } }
    set_temp_variable = { f = 0 }
}
multiply_variable = { growth = f }
```

## Calculation patterns

```
# Direct read
set_variable = { v = modifier@my_channel }

# Accumulate
add_to_variable = { total = modifier@my_channel }
subtract_from_variable = { total = modifier@my_opposing_channel }

# (modifier + 1) × weight scoring
set_temp_variable = { t = modifier@industrial_capacity_factory }
add_to_temp_variable = { t = 1 }
multiply_temp_variable = { t = 1.5 }
add_to_variable = { score = t }

# Cross-scope
set_temp_variable = { v = ROOT.modifier@country_channel }     # from state/other scope
set_temp_variable = { v = OTH.modifier@their_channel }        # another country
set_temp_variable = { v = 123.modifier@local_manpower }       # a specific state

# Per-member inside dynamic scope
for_each_loop = {
    array = bloc_members
    value = member_tag
    var:member_tag = {
        add_to_variable = { bloc_unity = modifier@monthly_unity_value }
    }
}

# Element write driven by a modifier
set_variable = { farm_dev^0 = ROOT.modifier@my_agriculture_impact }
```

## Where modifier@ reads are legal

- scripted_effects (the normal home)
- scripted_triggers — temp-variable math in trigger context is legal, so a scripted trigger can compute and expose values
- MTTH modifier blocks (`add = modifier@x`, factor temps)
- scripted GUI triggers, ai_will_do blocks, map mode color blocks

## Cost-stacking example (budget model)

Physical counts → coefficients → costs → policy modifier stack → slider remap:

```
# counts × coefficients (see num_battalions_with_type@ / num_ships_with_type@)
set_variable = { manpower_costs = army_fielded_manpower_k }

# policy channels stack multiplicatively
multiply_variable = { manpower_costs = modifier@military_expenditures_factor }
multiply_variable = { manpower_costs = modifier@army_cost_modifier }

# GUI slider 0–100 → 0.2–1.0 multiplier
set_variable = { slider_effect = maintenance_slider_pct }
multiply_variable = { slider_effect = 0.8 }
add_to_variable = { slider_effect = 20 }
divide_variable = { slider_effect = 100 }
multiply_variable = { manpower_costs = slider_effect }
```
