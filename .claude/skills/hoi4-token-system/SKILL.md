---
name: hoi4-token-system
description: HOI4 token system and dynamic variable naming (token:, @var:, @ROOT/@PREV/@FROM, meta_effect, meta_trigger, GetTokenKey, var: dynamic scoping), with guidance for combining tokens with collections and math-expression variable effects. Use when the user (1) Needs to store game object references (parties, ideas, decisions, ideologies) in variables, (2) Wants dynamically-named variables/arrays, (3) Needs multi-dimensional data access beyond simple arrays, (4) Wants meta_effect/meta_trigger for runtime script construction, (5) Needs GetTokenKey/GetTokenLocalizedKey to display tokens in GUI/localisation, (6) Needs token-keyed collections or formula-driven token pipelines, or (7) Says phrases like "token使いたい", "動的変数名", "dynamic variable name", "meta_effect", "meta_trigger", "@var:", "GetTokenKey". Self-contained reference — all syntax verified against official HOI4 script documentation.
---

# HOI4 Token System & Dynamic Variable Naming

## Overview

HOI4 script can store references to game objects (ideologies, ideas, decisions, custom tokens) in variables, and can build variable/array/effect/trigger names at runtime. Combining the two gives you dictionaries, records, dispatch tables, and multi-dimensional data — the foundation of every large GUI-driven mod system (elections, economies, dynamic timelines, custom decision UIs).

This skill is self-contained: every pattern below is complete and uses verified syntax. For array algorithms see `hoi4-advanced-arrays`; for value-reading tokens (`modifier@`, `party_popularity@`...) see `hoi4-data-tokens`; for collections and math-expression variable effects see `hoi4-variable-helper`.

## Quick Reference

```
# Store a game reference
set_variable = { my_party = token:social_democracy }

# Compare (NOTE: != does not exist — use compare = not_equals)
check_variable = { my_party = token:social_democracy }
check_variable = { var = my_party value = token:fascism compare = not_equals }
check_variable = { my_party = 0 }          # unset (token vars read as 0 when unset)

# ONE dynamic component in a name → @var:
set_variable = { employment_@var:state_id = 0.5 }
clear_array = global.member_list_@var:group_token

# Scope-id suffixes
set_variable = { trade_oil@PREV = amount }     # per-partner variable
set_variable = { FROM.raid_state_vs_@ROOT = THIS }

# TWO+ dynamic components, or splicing into identifiers → meta_effect
meta_effect = {
    text = { add_to_variable = { support_[st]_[occ]^party_id = amount } }
    st  = "[?state_var]"
    occ = "[?occupation_var]"
}

# Dynamic trigger text → meta_trigger (same shape as meta_effect)
meta_trigger = {
    text = { check_variable = { [ARR]^idx > 0 } }
    ARR = "[?array_name_token.GetTokenKey]"
}

# Token → text (scripted_localisation)
defined_text = {
    name = GetEconomyTypeName
    text = { localization_key = "[?economy_type.GetTokenLocalizedKey]" }
}

# Dynamic scope from a variable
var:target_country = { add_political_power = 50 }
var:state_list^idx = { set_state_flag = my_flag }

# Token systems can now hand off to collections/math expressions:
# use collections for live membership, arrays for ordered/token-keyed records.
set_variable = { weighted_value = { value = base_score multiply = modifier@my_factor } }
```

## Decision Tree

- **Store a game reference (party, decision, idea)?** → `token:identifier`
- **ONE dynamic component in a variable/array name?** → `@var:variable_name`
- **Per-scope (per-country-pair) variable names?** → `@PREV`, `@ROOT`, `@FROM`, `@THIS`
- **TWO+ dynamic components, or dynamic effect/decision/event names?** → `meta_effect`
- **Dynamic trigger text?** → `meta_trigger`
- **Display a token in GUI/text?** → `.GetTokenLocalizedKey` (localized) / `.GetTokenKey` (raw key)
- **Scope into a country/state stored in a variable?** → `var:variable_name = { ... }`
- **Need live, auto-updating membership instead of token arrays?** → define/use a collection (`collection:name`, `game:all_countries`, `collections:all_countries` where required)
- **Need formula math while reading token-keyed values?** → use math-expression variable effects from `hoi4-variable-helper`

---

## Part 1: token: — Storing Game Object References

### What a token is

`token:identifier` resolves a database token — an ideology, idea, decision, equipment type, character, or any custom localisation-keyed token — to an **opaque numeric id** at evaluation time. Stored token values behave like plain numbers: they go into variables and arrays, can be removed from arrays by value, and compare with `check_variable`. Do **not** do arithmetic on them (the one exception is the sentinel-range trick below, which is deliberately fragile).

```
set_variable = { ruling_ideology = token:social_democracy }
set_variable = { active_law = token:MYMOD_draft_budget_1950 }
add_to_array = { law_list = token:MYMOD_press_freedom_act }
remove_from_array = { law_list = token:MYMOD_press_freedom_act }   # short form removes BY VALUE
```

**Comparison and the unset check.** An unset variable reads as 0 and token ids are nonzero, so `= 0` is the canonical "no token stored" test:

```
check_variable = { active_law = token:MYMOD_draft_budget_1950 }            # equality
check_variable = { var = active_law value = token:MYMOD_x compare = not_equals }
check_variable = { active_law = 0 }                                        # unset
NOT = { check_variable = { active_law = 0 } }                              # set
```

> `!=` is **not** a valid check_variable shorthand. Only `=`, `>`, `<` exist as shorthands; everything else needs `compare = not_equals / greater_than_or_equals / less_than_or_equals`.

### Pattern A: Token registry (membership set + function-call convention)

A clean architecture for "which X are currently active" systems. One generic add/remove pair, thin wrappers that set a parameter temp variable, and `is_in_array` gating everywhere else:

```
# Generic effects — 'conflict_id' is the parameter (a temp variable)
add_active_conflict = {
    if = {
        limit = { NOT = { is_in_array = { active_conflicts = conflict_id } } }
        add_to_array = { active_conflicts = conflict_id }
    }
}
remove_active_conflict = {
    if = {
        limit = { is_in_array = { active_conflicts = conflict_id } }
        remove_from_array = { array = active_conflicts value = conflict_id }
    }
}

# Thin wrappers = the public API
start_border_conflict = {
    set_temp_variable = { conflict_id = token:conflict_border_war }
    add_active_conflict = yes
}

# Any decision / focus / GUI then gates on membership:
visible = { is_in_array = { active_conflicts = token:conflict_border_war } }
```

Document the parameter contract as header comments above each generic effect (`# params: conflict_id = token of the conflict`); temp variables are invisible arguments, comments are your only signature.

### Pattern B: Token-keyed variable namespaces (completion flags & friends)

A token can act as a composite key for a whole family of variables. Write with `@token:NAME` (literal token), read back with `@var:loop_var` inside loops:

```
# Write: on decision completion (e.g. from a hidden event)
set_variable = { finished@token:MYMOD_decision_land_reform = 1 }
set_variable = { cost@token:MYMOD_decision_land_reform = 50 }
set_variable = { progress@token:MYMOD_decision_land_reform = 10 }

# Read back in a loop over a token array (v holds a token):
for_each_loop = {
    array = reform_decision_list
    value = v
    if = {
        limit = { check_variable = { finished@var:v > 0 } }
        add_to_temp_variable = { completed_reforms = 1 }
    }
}
```

This also works in scripted_localisation triggers (`check_variable = { finished@var:v > 0 }`) — GUI loops can read the same namespace.

### Pattern C: Tokens as enum fields in records

Stored tokens give array slots typed "enum" values that read naturally at the consumer side:

```
# Record slots: 0 = date, 1 = event token, 2 = scale, 3 = type token
add_to_array = { global.timeline_entry_@var:entry_id = event_date }
add_to_array = { global.timeline_entry_@var:entry_id = event_token }
add_to_array = { global.timeline_entry_@var:entry_id = scale }
add_to_array = { global.timeline_entry_@var:entry_id = token:entry_type_war_start }

# Consumer (scripted_localisation): match slot 3 against the enum
defined_text = {
    name = GetTimelineIcon
    text = {
        trigger = { check_variable = { global.timeline_entry_@var:entry_id^3 = token:entry_type_war_start } }
        localization_key = "GFX_timeline_war_start"
    }
    text = { localization_key = "GFX_timeline_generic" }
}
```

See `references/dynamic_naming.md` for the full record-store template (auto-increment ids, optional parameters, duplicate guard).

### Pattern D (advanced, fragile): Token-range iteration with sentinels

Token ids are assigned contiguously per database in load order, so two sentinel ideas defined at the alphabetical start/end of `common/ideas/` bracket every idea id. Iterating the numeric range and converting each id back to its key with `GetTokenKey` gives "remove every national spirit" with zero bookkeeping:

```
remove_all_national_spirits = {
    set_temp_variable = { first_spirit = token:AAA_first_natspirit }   # sentinel ideas you define
    set_temp_variable = { last_spirit  = token:ZZZ_last_natspirit }
    for_loop_effect = {
        start = first_spirit
        end = last_spirit
        value = spirit
        meta_effect = {
            text = { if = { limit = { has_idea = [TOKEN] } remove_ideas = [TOKEN] } }
            TOKEN = "[?spirit.GetTokenKey]"
        }
    }
}
```

This is the only sanctioned arithmetic on token ids, and it breaks if files load in an unexpected order — always bracket with sentinels you control, never hard-code ids.

---

## Part 2: @var: — Single Dynamic Name Component

`@var:name` dereferences `name` and splices its value into the variable/array name at runtime. If `state_id = 3`, then `data_@var:state_id` resolves to `data_3`.

### The complexity ladder

```
# Level 1 — dynamic suffix
set_variable = { data_@var:id = 10 }

# Level 2 — dynamic name + element index (a 2D table)
add_to_variable = { employment_@var:state_id^occupation = amount }
clamp_variable = { var = settle_rate_@var:state_id^occupation min = 0 max = 100 }

# Level 3 — dynamically-named global arrays (a dict of arrays)
clear_array = global.member_list_@var:group_token
add_to_array = { global.member_list_@var:group_token = THIS }
for_each_scope_loop = {
    array = global.member_list_@var:group_token
    # scope = each member country
}

# Level 4 — full variable-path grammar INSIDE the key
# select_state holds a state id; select_state^union_id reads variable union_id ON that state;
# the result keys a country-level lookup table:
check_variable = { union_party_table_@var:select_state^union_id = 5 }
```

Level 4 is the composability rule worth remembering: the text after `@var:` accepts the full variable-path grammar including `^` scope traversal — "variable of (the state selected in a variable)" can key a dictionary with no intermediate temp.

`has_variable` fully supports dynamic names: `has_variable = data_@var:id`, `has_variable = coup_party@ROOT`.

### Parameterizing engine queries

`@var:` is not limited to your own variable names — it parameterizes the engine's built-in query tokens too. Dynamic two-endpoint distance:

```
set_temp_variable = { target_capital = FROM.capital }
set_temp_variable = { capital_distance = THIS.capital:distance_to@var:target_capital }
```

(`THIS.capital` opens the capital state scope, `:distance_to@var:X` queries distance to the state whose id is in `X`.)

### var:-held tokens in native effect/trigger slots

A variable holding an ideology token can be passed via `var:` straight into hardcoded triggers and effects that normally take a literal token:

```
set_variable = { saved_party@ROOT = PREV.ROOT.current_party_ideology_group }

has_government = var:saved_party@ROOT                      # trigger slot

set_temp_variable = { ideology = saved_party@ROOT }
set_temp_variable = { war_size = party_popularity@var:ideology }   # engine pseudo-array, keyed by var
clamp_temp_variable = { var = war_size min = 0.1 }

start_civil_war = {
    ideology = var:saved_party@ROOT                        # effect slot
    size = war_size
}
clear_variable = saved_party@ROOT
```

### Dictionary-as-variables (color lookup example)

Parallel `@var:`-keyed variables form an id→RGB dictionary; a scripted map mode does the inverse lookup per state:

```
# Setup once:
set_temp_variable = { culture_id = global.my_culture_a }
set_variable = { global.culture_red@var:culture_id = 0.25 }
set_variable = { global.culture_green@var:culture_id = 0.25 }
set_variable = { global.culture_blue@var:culture_id = 0.25 }

# Consumer — common/map_modes/*.txt, color block:
set_temp_variable = { culture_id = FROM.state_culture_array^0 }
set_temp_variable = { red   = global.culture_red@var:culture_id }
set_temp_variable = { green = global.culture_green@var:culture_id }
set_temp_variable = { blue  = global.culture_blue@var:culture_id }
set_temp_variable = { alpha = FROM.state_culture_array_num^0 }
```

---

## Part 3: Scope-Suffix Names — @PREV / @ROOT / @FROM / @THIS

These suffixes resolve to the id of the named scope, creating **per-scope variable families** ("how do I feel about / relate to that specific country") without arrays. All four are live in production code; `@token:NAME` (splice a literal token's id) also exists but is rare.

### Bilateral relationship variables

```
# Called from country A with PREV = country B
set_temp_variable = { opinion_t = opinion@PREV }            # data token, see hoi4-data-tokens
set_variable = { trade_opinion@PREV = trade_opinion_t }     # A's variable about B

# Symmetric pair — set both directions:
set_variable = { trade_oil@PREV = trade_amount }            # on A, about B
PREV = { set_variable = { trade_oil@PREV = trade_amount } } # on B, about A (inside B, PREV = A)
```

### Per-pair state targeting (raid/conflict systems)

Store state ids on the *target* country, keyed by the *acting* country (`@ROOT`), so many countries can run the same mechanic against the same target without collision:

```
# In a decision targeting FROM:
random_owned_controlled_state = {
    limit = { ... }
    set_variable = { FROM.attacker_state_vs_@ROOT = THIS }   # state scope: THIS = state id
}

# Later, scope into the stored state:
var:FROM.attacker_state_vs_@ROOT = { is_fully_controlled_by = ROOT }

# Or check from a literal state id prefix:
check_variable = { 1857.strength_var_@ROOT > 29 }

# ALWAYS clean up in every exit path (timeout/cancel/complete):
FROM = {
    clear_variable = attacker_state_vs_@ROOT
    clear_variable = defender_state_vs_@ROOT
}
```

**Cleanup discipline:** per-scope variables created in paired interactions must be cleared symmetrically in *every* exit path, or stale pairs leak into later interactions.

---

## Part 4: var: — Dynamic Scoping

`var:x` used as a scope opener jumps into the country/state whose id is stored in `x`. Sources of valid ids: `THIS` stored from a state scope, `THIS.id` stored from a country scope, array elements, capital references.

```
# Scope into a country from an array element, assign a rank:
set_temp_variable = { rank_tag = global.score_tag_array_temp^v }
var:rank_tag = {
    set_variable = { score_rank = v }
    add_to_variable = { score_rank = 1 }       # 1-based rank
}

# Scope into a state and write back to a country array (note the country prefix):
for_each_loop = {
    array = link_state
    index = state_idx
    value = state_value
    var:state_value = {
        set_variable = { MYC.state_ic^state_idx = industrial_complex_level }
        add_to_variable = { MYC.state_ic^state_idx = arms_factory_level }
    }
}

# Direct element scoping — array^cursor as event target:
set_variable = { switch_cursor = 0 }
var:ranked_subject_list^switch_cursor = { country_event = my_mod.209 }
```

In triggers, `var:` array elements work the same way: `var:global.score_tag_array^i = { is_subject_of = ROOT }`.

---

## Part 5: meta_effect & meta_trigger — Runtime Script Construction

### Verified syntax

```
meta_effect = {
    text = {
        # script with [NAME] placeholders — placeholders may appear ANYWHERE in the raw
        # text: identifier names, numbers, event ids, even inside quoted strings
        add_to_variable = { values_[st]_@var:occupation^value_type = amount }
    }
    st = "[?state_var]"      # substitutions are quoted localisation strings, evaluated at run time
    debug = yes              # optional: logs the generated script (remove when done)
}

meta_trigger = {             # identical shape, builds TRIGGER text; usable in trigger blocks,
    text = { check_variable = { [ARR]^n = 32 } }      # scripted GUI triggers, and loc triggers
    ARR = "[?array_token.GetTokenKey]"
}
```

Substitution values you will actually use: `"[?numeric_var]"` (number), `"[?token_var.GetTokenKey]"` (raw token key), `"[THIS.GetTag]"` / `"[?country_var.GetTag]"` (country tag), `"[MyDefinedText]"` (output of a scripted-loc function — full indirection).

**When you need it:** `@var:` handles exactly one dynamic component inside a *variable name*. Reach for `meta_effect` when you need (a) two+ dynamic components, (b) dynamic *identifier* names (effects, decisions, ideas, event ids), or (c) splicing into places variables can't go (quoted strings, tag-literal slots).

### Pattern A: Multi-dimensional names (3D/4D tables)

```
# 3D: one baked component + one @var: + one ^index
meta_effect = {
    text = { add_to_variable = { values_[st]_@var:occupation^value_type = amount } }
    st = "[?state_var]"
}
# → e.g. values_3_1^0

# 4D: two baked + one @var: + one ^index
meta_effect = {
    text = { add_to_variable = { support_[st]_[occ]_@var:sub_type^party_id = amount } }
    st  = "[?state_var]"
    occ = "[?occupation_var]"
}
# → e.g. support_3_1_0^2
```

### Pattern B: Token-keyed dispatch table (custom decision systems)

Each pseudo-decision is a token; by convention every token has companion scripted effects/triggers named `<token>_select`, `<token>_remove`, `<token>_allowed`. The GUI dispatches by splicing the token key:

```
# Availability (in a scripted GUI triggers block):
meta_trigger = {
    text = { [dec]_allowed = yes }
    dec = "[?dec_token.GetTokenKey]"
}

# Click effect — wrap the same dispatch in effect_tooltip to PREVIEW it to the player:
effect_tooltip = {
    meta_effect = {
        text = { [dec]_select = yes }
        dec = "[?dec_token.GetTokenKey]"
    }
}
```

### Pattern C: Dynamic names for things that demand literals

```
# Tag-literal-only effects (opinion modifiers, set_cosmetic_tag, puppet...):
meta_effect = {
    text = { add_opinion_modifier = { target = [RIVAL] modifier = my_rival_modifier } }
    RIVAL = "[?rival_country.GetTag]"
}

# Numbered decision families:
meta_effect = {
    text = { activate_decision = MYMOD_election_actions_[faction_id] }
    faction_id = "[?faction_id]"
}

# Splice INSIDE a quoted string (create_unit division names) and into event ids:
meta_effect = {
    text = {
        create_unit = {
            division = "name = \"[n]. Marine-Infanterie-Division\" division_template = \"Marine-Division\" start_experience_factor = 0.75"
            owner = TAG
        }
    }
    n = "[?counter_var]"
}
```

### Pattern D: Hoisting — wrap the algorithm, not the iteration

`meta_effect` re-parses text every execution. If a loop body needs a substituted name, put the **whole loop inside one meta_effect** so substitution happens once:

```
meta_effect = {
    text = {
        while_loop_effect = {
            limit = { check_variable = { top > -1 } }
            # ... entire algorithm body using [SORTKEY] ...
            var:items^cursor = { set_variable = { PREV.tmp_sort = [SORTKEY] } }
        }
    }
    SORTKEY = "[GetSelectedSortColumn]"     # scripted loc picks the variable name at runtime
}
```

**Performance:** never call `meta_effect` per-iteration in hot loops (daily ticks, 100+ element arrays). Hoist it, or cache results in regular arrays.

---

## Part 6: Displaying Tokens — GetTokenKey vs GetTokenLocalizedKey

Both are localisation functions on token-holding variables:

| Function | Returns | Use for |
|---|---|---|
| `GetTokenKey` | the **raw key string** (`social_democracy`) | composing loc/GFX keys, splicing into meta_effect/meta_trigger text |
| `GetTokenLocalizedKey` | the **localized text** of that key | player-facing names in tooltips/GUI |

### Composition patterns (scripted_localisation)

```
defined_text = {
    name = GetEconomyTypeName
    text = { localization_key = "[?economy_type.GetTokenLocalizedKey]" }     # display name
}

defined_text = {
    name = GetEconomyTypeIcon
    text = {
        trigger = { check_variable = { economy_subtype = 0 } }               # unset → fall back to type
        localization_key = "GFX_[?economy_type.GetTokenKey]"
    }
    text = { localization_key = "GFX_[?economy_subtype.GetTokenKey]" }       # last text = no trigger = default
}

defined_text = {
    name = GetEconomyTypeDesc
    text = { localization_key = "[?economy_type.GetTokenKey]_desc" }         # key suffix composition
}
```

defined_text rules worth knowing: branches are evaluated top-down, the **last, trigger-less text is the fallback**; `localization_key = ""` is a legal explicit blank.

### Advanced loc patterns

```
# Array element + dynamic index inside [?...]:
localization_key = "[?law_amendments^selected_slot.GetTokenLocalizedKey]"

# Variable on a scope stored in another variable:
localization_key = "[?selected_state_var:StateTitle.GetTokenKey]"

# Constructing a NEW token from a key at loc time (meta_trigger side effect):
text = {
    trigger = {
        meta_trigger = {
            text = { set_temp_variable = { desc_token = token:[LAW]_desc } }
            LAW = "[?active_law.GetTokenKey]"
        }
    }
    localization_key = "[?desc_token.GetTokenLocalizedKey]"
}
```

### Number formatting and debug display

Format codes combine freely after `|` in `[?var|fmt]`: digits `0/1/2/3` = decimal places (`|.0` dot form also valid), `%` = percentage (×100, % appended), `+` = explicit sign with green/red coloring, `G/R/Y/H` = color overrides. Common combos: `[?x|%0]`, `[?x|+0]`, `[?x|.1%]`.

Debug logging from effects: `log = "value: [?my_var] owner: [THIS.GetName]"` — and `[?token_var.GetTokenLocalizedKey]` works in log strings too.

---

## Pitfalls

1. **`!=` does not exist** in check_variable — use `compare = not_equals`.
2. **Token ids are opaque** — no arithmetic, no persistence assumptions across mod versions (ids shift when databases change). Compare, store, display; nothing else (sentinel-range iteration being the one guarded exception).
3. **Unset reads as 0** — `check_variable = { x = 0 }` is the unset test; guard `var:x` scope-opens with it to avoid error-log spam.
4. **meta_effect cost** — re-parses text each run; hoist around algorithms, never per-iteration in hot paths. Tooltips of meta-dispatched effects need explicit `effect_tooltip` wrapping.
5. **Per-scope variable leaks** — `@ROOT`/`@PREV` pair variables must be cleared in every exit path.
6. **Quoting** — meta substitutions are always quoted strings: `st = "[?state_var]"`, never `st = state_var`.
7. **Working examples in your own mod may contain load-bearing typos** (misspelled but consistently-used variable names). When extending an existing system, match its existing names exactly — never "fix" spellings in place.

## Reference Files

- `references/token_guide.md` — token storage catalog, registry/flag/enum templates, equality semantics
- `references/dynamic_naming.md` — @var: complexity ladder, full record-store + group-membership worked examples, meta_effect dimensionality templates
