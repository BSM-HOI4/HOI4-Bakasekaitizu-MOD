# Parallel Arrays & Multi-Dimensional Data Reference

## Struct-of-Arrays Convention

One array per field, indices shared across all of them:

```
# Entity 0
add_to_array = { entity_kind = 88 }
add_to_array = { entity_share = 0.68 }
add_to_array = { entity_flags = 1 }
# Entity 1
add_to_array = { entity_kind = 121 }
add_to_array = { entity_share = 0.10 }
add_to_array = { entity_flags = 0 }
# entity_kind^0 / entity_share^0 / entity_flags^0 describe the same record
```

Rules that keep the structure sound:

1. **Append together** — every record write touches all field arrays once, in the same order.
2. **Remove together** — structural ops (remove/insert/sort) hit all siblings at the same index in the same step.
3. **Document the schema** — a comment block (`# kind = culture id, share = pop fraction`) adjacent to the writer; integer "kind" ids are undecipherable without it.
4. Seeding in state `history = { }` blocks executes at game start — fine for static data tables.

## Pre-Allocation Templates

```
# Short form — size only, new elements 0:
resize_array = { seats = 9 }
resize_array = { state_pop_k = 9 }

# Long form — explicit fill for new elements:
resize_array = { array = seats_array value = -1 size = 256 }     # -1 = "unassigned" sentinel
resize_array = { array = area_owner_list value = 17 size = 21 }  # 17 = "no faction" sentinel

# Size from a runtime variable:
resize_array = { array = buckets value = 0 size = length_temp }

# Dynamic name + pre-allocation in a loop (see hoi4-token-system for @var:):
for_loop_effect = {
    start = 0
    end = 11
    value = area_id
    clear_array = area_data_@var:area_id
    resize_array = { array = area_data_@var:area_id value = 0 size = 21 }
}

# Incremental resize → segment-mapped array:
clear_array = group_map
resize_array = { array = group_map value = 1 size = 4 }    # ids 0-3  → group 1
resize_array = { array = group_map value = 2 size = 8 }    # ids 4-7  → group 2
resize_array = { array = group_map value = 3 size = 11 }   # ids 8-10 → group 3
```

Growing fills only the **new** slots; shrinking truncates from the end. Temp variants: `resize_temp_array` (same two forms).

## Filling From Game Data

```
# Per-state harvest into country arrays (scope shifts → prefix the write-back):
for_each_scope_loop = {
    array = global.tracked_states
    set_variable = { slot = my_state_index }       # stored on the state beforehand
    add_to_variable = { ROOT.province_pop^slot = state_population_k }
}

# Alternative: iterate ids, scope in with var::
for_each_loop = {
    array = link_state
    value = state_id
    index = state_idx
    var:state_id = {
        set_variable = { MYC.state_pop_k^state_idx = state_population_k }
    }
}
```

## FIFO Sliding Window (rolling history)

```
graph_monthly_tick = {
    add_to_array = { graph_months = current_month_var }
    add_to_array = { graph_gdp = gdp }
    add_to_array = { graph_inflation = inflation_rate }
    if = {
        limit = { check_variable = { graph_months^num > 17 } }
        remove_from_array = { array = graph_months index = 0 }
        remove_from_array = { array = graph_gdp index = 0 }
        remove_from_array = { array = graph_inflation index = 0 }
    }
}
```

Downstream renderers typically do a min/max scan over the window (`find_highest_in_array` / `find_lowest_in_array`) to auto-scale graph axes.

## Weighted-Random Seat Assignment

Pre-allocate a seat array, then fill each seat by weighted random over a popularity-derived weight array:

```
# 1. Weights from party popularity (see hoi4-data-tokens for party_popularity@):
resize_array = { array = parl_weights value = 1 size = 9 }
set_variable = { parl_weights^0 = party_popularity@social_democracy }
set_variable = { parl_weights^1 = party_popularity@liberal_democracy }
# ... ^2..^8

set_temp_variable = { total_weight = 0 }
for_each_loop = {
    array = parl_weights
    value = w
    add_to_temp_variable = { total_weight = w }
}

# 2. Seat array, -1 = unassigned:
resize_array = { array = seats_array value = -1 size = 256 }

# 3. Weighted random per seat:
for_loop_effect = {
    start = 0
    end = 256
    value = seat
    set_temp_variable_to_random = { var = roll min = 0 max = total_weight }
    set_temp_variable = { cumulative = 0 }
    for_each_loop = {
        array = parl_weights
        value = w
        index = party
        break = assigned
        add_to_temp_variable = { cumulative = w }
        if = {
            limit = { check_variable = { cumulative > roll } }
            set_variable = { seats_array^seat = party }
            set_temp_variable = { assigned = 1 }
        }
    }
}
```

(256 × 9 = 2304 inner iterations total is fine; each individual loop stays far below the 1000-iteration cap.)

## 2D/3D/4D Tables

True multi-dimensional tables are built from dynamic array *names* — `employment_@var:state_id^occupation` etc. That machinery (one `@var:` per name, `meta_effect` for more dimensions) lives in `hoi4-token-system`, `references/dynamic_naming.md`.
