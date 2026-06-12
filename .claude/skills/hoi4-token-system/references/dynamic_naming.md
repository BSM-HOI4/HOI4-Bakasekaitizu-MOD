# Dynamic Variable Naming Reference

## @var: Complexity Ladder

```
# Level 1 — simple dynamic suffix
set_variable = { data_@var:id = 10 }                    # id=3 → data_3

# Level 2 — dynamic name + element index (2D table)
set_variable = { data_@var:id^idx = 10 }                # id=3, idx=2 → data_3^2
add_to_variable = { data_@var:id^idx = 5 }
clamp_variable = { var = data_@var:id^idx min = 0 max = 100 }

# Level 3 — dynamically-named (global) arrays = dict of arrays
clear_array = global.list_@var:key_token
add_to_array = { global.list_@var:key_token = THIS }
resize_array = { array = data_@var:area_id value = 0 size = 21 }
find_highest_in_array = { array = data_@var:area_id value = best_v index = best_i }

# Level 4 — full path grammar inside the key (scope traversal with ^)
# select_state holds a state id; union_id is a variable ON that state:
check_variable = { party_table_@var:select_state^union_id = 5 }

# Cross-scope suffixes (per-scope families):
set_variable = { trade_oil@PREV = amount }
check_variable = { 1857.strength_var_@ROOT > 29 }
has_variable = coup_party@ROOT
```

`has_variable`, `clear_variable`, `check_variable`, all arithmetic effects, `resize_array`, `clear_array`, `find_highest_in_array` — every variable/array operation accepts dynamic names.

## meta_effect Dimensionality Templates

One `@var:` per name; every additional dynamic component must be baked by meta_effect:

```
# 2D — two baked components
meta_effect = {
    text = { clear_array = prefix_[a]_[b]_list }
    a = "[?var_a]"
    b = "[?var_b]"
}

# 3D — one baked + one @var: + one ^index
meta_effect = {
    text = { add_to_variable = { values_[st]_@var:occupation^value_type = amount } }
    st = "[?state_var]"
}

# 4D — two baked + one @var: + one ^index
meta_effect = {
    text = { add_to_variable = { support_[st]_[occ]_@var:sub_type^party_id = amount } }
    st  = "[?state_var]"
    occ = "[?occupation_var]"
}
```

Cost model: baked components are paid at meta_effect parse time (every execution), `@var:` and `^` are resolved natively. Prefer pushing components into `@var:`/`^` and keep the meta-baked count minimal.

## Worked Example 1: Group membership system (dict-of-arrays)

A complete "spheres/blocs/alliances" subsystem: each group is a token, members are country scopes in a dynamically-named global array, the leader is pinned to index 0.

```
# params: group_token = token of the group to create (caller scope = leader)
group_create = {
    add_to_array = { global.group_list = group_token }
    clear_array = global.group_members_@var:group_token

    every_country = {
        limit = {
            OR = {
                tag = PREV
                is_subject_of = PREV
                is_in_faction_with = PREV
            }
        }
        add_to_array = { global.group_members_@var:group_token = THIS }
        set_variable = { my_group = group_token }
    }

    # Pin the leader to index 0: remove by value, re-insert at front
    remove_from_array = { global.group_members_@var:group_token = THIS }
    add_to_array = { array = global.group_members_@var:group_token value = THIS index = 0 }
}

# Iterate all groups and their members:
group_process_all = {
    for_each_loop = {
        array = global.group_list
        value = group_token
        for_each_scope_loop = {
            array = global.group_members_@var:group_token
            # scope = member country
            clear_variable = my_group
        }
        clear_array = global.group_members_@var:group_token
    }
    clear_array = global.group_list
}

# Move every member to another group:
# params: group_token (source), new_group_token (destination)
group_merge_into = {
    clear_array = global.group_members_@var:new_group_token
    for_each_scope_loop = {
        array = global.group_members_@var:group_token
        add_to_array = { global.group_members_@var:new_group_token = THIS }
        set_variable = { my_group = new_group_token }
    }
    clear_array = global.group_members_@var:group_token
}
```

## Worked Example 2: Record store (hashmap of records)

A growable object store: an index array of allocated ids, one dynamically-named array per record, positional fields, auto-increment id allocation, optional-parameter defaults, duplicate guard.

```
# params: entry_event (token, required — pass via set_temp_variable & has_variable guard)
#         entry_date (default global.date), entry_scale (default 1), entry_type (token, default none)
record_add = {
    if = {
        limit = { has_variable = entry_event }

        # Allocate id = max existing id + 1
        find_highest_in_array = {
            array = global.record_list
            value = new_id
        }
        if = {
            # Duplicate guard: skip if newest record already holds this event
            limit = { NOT = { check_variable = { global.record_@var:new_id^1 = entry_event } } }
            add_to_temp_variable = { new_id = 1 }
            add_to_array = { array = global.record_list value = new_id index = 0 }   # newest-first index

            clear_array = global.record_@var:new_id

            # Slot 0: date (optional)
            if = {
                limit = { check_variable = { entry_date = 0 } }
                set_temp_variable = { entry_date = global.date }
            }
            add_to_array = { global.record_@var:new_id = entry_date }

            # Slot 1: event token (required)
            add_to_array = { global.record_@var:new_id = entry_event }

            # Slot 2: scale (optional)
            if = {
                limit = { check_variable = { entry_scale = 0 } }
                set_temp_variable = { entry_scale = 1 }
            }
            add_to_array = { global.record_@var:new_id = entry_scale }

            # Slot 3: type enum token (optional)
            if = {
                limit = { check_variable = { entry_type = 0 } }
                set_temp_variable = { entry_type = token:record_type_none }
            }
            add_to_array = { global.record_@var:new_id = entry_type }

            # Slots 4+: variable-length related-country list
            for_each_loop = {
                array = related_countries
                value = rel_tag
                add_to_array = { global.record_@var:new_id = rel_tag }
            }
        }
    }
}

# Reader (GUI / scripted_localisation): record_id comes from iterating global.record_list
#   date:  global.record_@var:record_id^0
#   event: [?global.record_@var:record_id^1.GetTokenLocalizedKey]
#   type:  check_variable = { global.record_@var:record_id^3 = token:record_type_war_start }
```

Design notes:

- Inserting new ids at `index = 0` makes the index array double as newest-first display order.
- Field meaning lives in a schema comment (`# 0=date 1=event 2=scale 3=type`) — keep it adjacent to the writer.
- "Optional parameter" = temp variable that reads 0 when the caller didn't set it; fill defaults before writing.
- Deleting a record: `remove_from_array = { array = global.record_list value = dead_id }` + `clear_array = global.record_@var:dead_id`.

## var: Dynamic Scope Patterns

```
# Country from variable:
set_temp_variable = { target = global.tag_array^v }
var:target = { set_variable = { rank = v } }

# State from array element, write-back to country arrays via explicit prefix:
for_each_loop = {
    array = state_list
    index = idx
    value = state_ref
    var:state_ref = {
        set_variable = { MYC.state_data^idx = industrial_complex_level }
    }
}

# Direct element scoping (cursor state machine across events):
var:ranked_list^cursor_var = { country_event = my_mod.209 }

# In triggers:
limit = { var:global.tag_array^i = { is_subject_of = ROOT } }
limit = { NOT = { has_government = var:saved_party_token } }
```

What `add_to_array = { list = THIS }` stores: the scope's internal id (country id from country scope, state id from state scope). `THIS.id` from country scope stores the same id explicitly. Either feeds `var:` scope-opens and `for_each_scope_loop`.
