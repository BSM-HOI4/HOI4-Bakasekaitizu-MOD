# Token System Reference — Storage Catalog & Templates

## What can be a token

`token:` resolves entries of script databases to opaque numeric ids. Verified-working sources:

| Source | Example | Typical use |
|---|---|---|
| Ideology groups | `token:social_democracy` | party/government systems |
| Ideas / national spirits | `token:MYMOD_war_economy` | idea bookkeeping, range iteration |
| Decisions | `token:MYMOD_decision_land_reform` | completion flags, parameter passing |
| Equipment types | `token:artillery_equipment` | production scripting |
| Characters | `token:MYMOD_leader_name` | leader display in custom GUIs |
| Custom loc-keyed tokens | `token:MYMOD_alert_low_funds` | pure symbolic ids — any identifier with a localisation entry works as a cross-subsystem symbol |

The last row is the most powerful: you can mint tokens that exist *only* as symbols (alert categories, GUI page ids, conflict ids, record-type enums). Give each a localisation entry and it gains a display name for free via `GetTokenLocalizedKey`.

## Equality semantics

```
check_variable = { x = token:some_token }                                  # equal
check_variable = { var = x value = token:some_token compare = not_equals } # not equal (NO != shorthand)
check_variable = { x = 0 }                                                 # unset
NOT = { check_variable = { x = 0 } }                                       # set
is_in_array = { my_tokens = token:some_token }                             # membership
is_in_array = { my_tokens = x }                                            # membership of a stored token
remove_from_array = { my_tokens = token:some_token }                       # remove by value (short form)
```

## Template 1: Registry (membership-set model)

Supports enumeration, count (`^num`), and removal — prefer it over flag spam.

```
# --- common/scripted_effects/mymod_registry.txt ---
# params: entry_id = token to add/remove
registry_add = {
    if = {
        limit = { NOT = { is_in_array = { my_registry = entry_id } } }
        add_to_array = { my_registry = entry_id }
    }
}
registry_remove = {
    if = {
        limit = { is_in_array = { my_registry = entry_id } }
        remove_from_array = { array = my_registry value = entry_id }
    }
}

# Wrappers (public API):
activate_border_conflict = {
    set_temp_variable = { entry_id = token:conflict_border_war }
    registry_add = yes
}

# Consumers anywhere:
#   visible = { is_in_array = { my_registry = token:conflict_border_war } }
#   check_variable = { my_registry^num > 2 }
# Enumeration:
for_each_loop = {
    array = my_registry
    value = entry_token
    # display: [?entry_token.GetTokenLocalizedKey]
}
```

## Template 2: Token-keyed variable namespace (flags + attributes)

The token is a composite key into several parallel variable families. Write with `@token:` (literal), read with `@var:` (loop variable):

```
# Writes — typically one hidden event / effect per milestone:
set_variable = { finished@token:MYMOD_decision_land_reform = 1 }
set_variable = { cost@token:MYMOD_decision_land_reform = 50 }
set_variable = { progress@token:MYMOD_decision_land_reform = 10 }
set_variable = { icon@token:MYMOD_decision_land_reform = 4 }

# Reads — loops and scripted_localisation share the namespace:
for_each_loop = {
    array = reform_list           # array of decision tokens
    value = v
    if = {
        limit = { check_variable = { finished@var:v > 0 } }
        add_to_temp_variable = { done_count = 1 }
    }
}

# scripted_localisation (GUI grid rows; v set by the GUI loop):
defined_text = {
    name = GetReformCostLabel
    text = {
        trigger = { check_variable = { finished@var:v > 0 } }
        localization_key = reform_cost_finished
    }
    text = { localization_key = reform_cost_normal }
}
```

## Template 3: Parameter passing (effects as functions)

Temp variables are the arguments; a header comment is the signature. Multiple "calls" in one option just repeat the full block:

```
# params: pr_token (token), pr_cost (int), pr_category (int), pr_progress (int)
propose_reform = {
    set_variable = { cost@var:pr_token = pr_cost }
    set_variable = { progress@var:pr_token = pr_progress }
    if = {
        limit = { check_variable = { pr_category = 1 } }
        add_to_array = { reform_list_political = pr_token }
    }
    else_if = {
        limit = { check_variable = { pr_category = 2 } }
        add_to_array = { reform_list_economic = pr_token }
    }
}

# Call site (event option) — repeat per proposal:
option = {
    name = my_event.1.a
    set_temp_variable = { pr_token = token:MYMOD_decision_statistics_bureau }
    set_temp_variable = { pr_cost = 50 }
    set_temp_variable = { pr_category = 1 }
    set_temp_variable = { pr_progress = 10 }
    propose_reform = yes
}
```

## Template 4: Tokens as enum fields

```
# Writer — record slots: 0=date 1=event 2=scale 3=type(enum token)
add_to_array = { global.entry_@var:id = token:entry_type_war_start }

# Reader — branch per enum value:
defined_text = {
    name = GetEntryIcon
    text = {
        trigger = { check_variable = { global.entry_@var:id^3 = token:entry_type_war_start } }
        localization_key = "GFX_icon_war_start"
    }
    text = {
        trigger = { check_variable = { global.entry_@var:id^3 = token:entry_type_war_end } }
        localization_key = "GFX_icon_war_end"
    }
    text = { localization_key = "GFX_icon_generic" }
}
```

## Template 5: Sentinel-range iteration (advanced, fragile)

Token ids within one database are contiguous in load order. Bracket the range with two sentinel entries **you define** at the alphabetical extremes, then iterate numerically and re-materialize each key via meta_effect:

```
# common/ideas/AAA_sentinels.txt defines AAA_first_natspirit;
# common/ideas/ZZZ_sentinels.txt defines ZZZ_last_natspirit.
remove_all_national_spirits = {
    set_temp_variable = { first = token:AAA_first_natspirit }
    set_temp_variable = { last  = token:ZZZ_last_natspirit }
    for_loop_effect = {
        start = first
        end = last
        value = t
        meta_effect = {
            text = { if = { limit = { has_idea = [TOKEN] } remove_ideas = [TOKEN] } }
            TOKEN = "[?t.GetTokenKey]"
        }
    }
}
```

Risks: per-iteration meta_effect cost (acceptable for occasional cleanup, not for ticks), and dependence on file-load order — never use without owning both sentinels.

## Display quick table

```
[?token_var.GetTokenLocalizedKey]        # player-facing localized name
[?token_var.GetTokenKey]                 # raw key string
"GFX_[?token_var.GetTokenKey]"           # sprite key composition
"[?token_var.GetTokenKey]_desc"          # description key composition
[?array^idx_var.GetTokenLocalizedKey]    # array element display
```
