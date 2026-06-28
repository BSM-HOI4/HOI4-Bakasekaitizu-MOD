---
name: hoi4-data-tokens
description: HOI4 data access tokens and computation pipelines — modifier@, resource@/resource_produced@, party_popularity@/party_popularity_100@, opinion@, distance_to@, num_battalions_with_type@, set_variable_to_random, built-in value reads (state_population_k, num_of_factories...), math-expression variable effects, collection iterators, and MTTH variables as a calculation engine. Use when the user (1) Needs to read modifier values into variables, (2) Wants resource production / unit counts / popularity as numbers, (3) Needs random number generation, (4) Wants multi-step calculation pipelines (scores, budgets, elections, drift), (5) Wants formula-based calculations over collections, or (6) Says phrases like "modifier読み取り", "resource_produced", "計算パイプライン", "math expression", "数式", "random variable", "MTTH計算", "modifier@", "party_popularity". Self-contained reference — all syntax verified against official HOI4 dynamic-variables documentation.
---

# HOI4 Data Access Tokens & Computation Pipelines

## Overview

HOI4 exposes live game state as readable pseudo-variables: `modifier@x` (current modifier values), `resource_produced@x`, `party_popularity@x`, `opinion@TAG`, unit counts, and dozens of built-in country/state values. Reading them into variables and chaining arithmetic effects builds scores, budgets, elections, and feedback controllers. Newer math-expression variable effects let many of those chains collapse into one formula, including formulas that iterate collections.

Companion skills: `hoi4-advanced-arrays` (storing results in arrays), `hoi4-token-system` (dynamic names/`@var:` keys), `hoi4-variable-helper` (math expressions, collections, basics).

## Quick Reference

```
# Modifier values (custom dynamic-modifier channels included)
set_variable = { v = modifier@industrial_capacity_factory }
set_temp_variable = { v = ROOT.modifier@my_custom_channel }       # cross-scope works

# Resources — note the country/state split
set_variable = { surplus_steel = resource@steel }                 # country: SURPLUS
set_variable = { produced_oil = resource_produced@oil }           # country: produced
# state scope: resource@steel = produced in that state

# Party popularity — two scales, variable targets allowed
set_variable = { p = party_popularity@social_democracy }          # 0.00 – 1.00
set_variable = { p = party_popularity_100@social_democracy }      # 0 – 100
set_variable = { p = party_popularity@ruling_party }
set_variable = { p = party_popularity@var:ideology_token_var }

# Other reads
set_temp_variable = { o = opinion@ROOT }                          # -100..100 opinion of ROOT
set_temp_variable = { d = THIS.capital:distance_to@var:target_capital }
set_variable = { n = num_battalions_with_type@artillery }
set_variable = { s = num_ships_with_type@carrier }

# Built-in values (read like variables)
set_variable = { x = state_population_k }     # state scope
set_variable = { x = num_of_factories }       # country scope
set_temp_variable = { r = random }            # [0,1) fresh each read

# Random with range — [min, max) half-open
set_variable_to_random = { var = roll min = -10 max = 10 integer = yes }
set_temp_variable_to_random = { var = roll min = 0 max = total_weight }

# MTTH calculation engine (common/mtth/*.txt)
set_variable = { result = mtth:my_calculation }

# Math-expression pipeline (single variable effect)
set_variable = { score = { value = num_of_factories multiply = modifier@industrial_capacity_factory } }
```

---

## Part 1: modifier@ — Reading Modifier Values

`modifier@<token>` returns the current summed value of that modifier on the scope — including **custom dynamic-modifier channels you define yourself**, which makes it the standard way to let ideas/focuses/laws feed numbers into script systems.

Verified scopes: country (`modifier@x`), state (`123.modifier@local_manpower` or inside state scope), MIO; unit-leader variants exist as `leader_modifier@navy_max_range` / `unit_modifier@army_attack_factor`. Cross-scope prefixes work: `ROOT.modifier@x`, `TAG.modifier@x`, `PREV.modifier@x`.

### The additive + factor channel convention

Define two modifier channels per quantity — `_modifier` (flat) and `_factor` (multiplicative) — then combine:

```
set_variable = { growth = modifier@industrialization_growth_rate_modifier }
set_temp_variable = { factor = modifier@industrialization_growth_rate_factor }
add_to_temp_variable = { factor = 1 }                # delta → multiplier
multiply_variable = { growth = factor }              # growth = flat * (1 + factor)
```

Guard against runaway negatives when stacked debuffs could push the factor below zero:

```
set_temp_variable = { f = 1 }
add_to_temp_variable = { f = modifier@inflation_change_factor }
if = {
    limit = { check_variable = { f < 0 } }
    set_temp_variable = { f = 0 }
}
multiply_temp_variable = { daily_inflation_change = f }
```

### (modifier + 1) × weight scoring

```
set_temp_variable = { t = modifier@industrial_capacity_factory }
add_to_temp_variable = { t = 1 }
multiply_temp_variable = { t = 1.5 }
add_to_variable = { industrial_score = t }
```

### Per-member reads inside dynamic scopes

```
for_each_loop = {
    array = bloc_members
    value = member_tag
    var:member_tag = {
        add_to_variable = { bloc_unity = modifier@monthly_bloc_unity_value }
        subtract_from_variable = { bloc_unity = modifier@monthly_separatist_value }
    }
}
```

`modifier@` reads also work inside **scripted triggers** (temp-variable math in trigger context is legal) and inside MTTH modifier blocks (Part 6).

---

## Part 2: Resource Tokens

| Token | Country scope | State scope |
|---|---|---|
| `resource@x` | **surplus** (production − use) | produced in that state |
| `resource_produced@x` | total produced | — |
| `resource_consumed@x` / `resource_exported@x` / `resource_imported@x` | exist, rarely needed | — |

### Weighted resource score pipeline

One temp variable reused per term — read, weight, accumulate:

```
set_variable = { industrial_score = 0 }

set_temp_variable = { t = resource_produced@coal }
multiply_temp_variable = { t = 0.45 }
add_to_variable = { industrial_score = t }

set_temp_variable = { t = resource_produced@steel }
multiply_temp_variable = { t = 0.45 }
add_to_variable = { industrial_score = t }

set_temp_variable = { t = resource_produced@oil }
multiply_temp_variable = { t = 0.70 }
add_to_variable = { industrial_score = t }
# ... one block per resource; weights are balancing choices, tune freely
```

Custom mod resources work identically (`resource_produced@my_custom_resource`).

---

## Part 3: party_popularity@ — Popularity as Numbers

Both variants are **vanilla**, country scope, read-only:

- `party_popularity@<target>` → 0.00 – 1.00
- `party_popularity_100@<target>` → 0 – 100

Targets: an ideology group token (`@democratic`), `@ruling_party`, or **a variable holding an ideology token** (`@var:ideology` / `@my_var_name`). The two scales are the classic bug source — comparing `party_popularity@x > 59` never fires; that needs `> 0.59` or the `_100` variant.

```
# Accumulate a coalition's total support:
set_temp_variable = { support = 0 }
add_to_temp_variable = { support = party_popularity_100@social_democracy }
add_to_temp_variable = { support = party_popularity_100@liberal_democracy }

# Dynamic ideology via a token variable:
for_each_loop = {
    array = coalition_ideologies
    value = temp_ideology
    add_to_variable = { coalition_support = party_popularity@var:temp_ideology }
}

# Cross-scope, e.g. in ai_will_do:
modifier = {
    check_variable = { OTH.party_popularity@national_socialism > 0.59 }
    add = 1000
}

# Weight array for seat allocation:
resize_array = { array = parl_weights value = 1 size = 9 }
set_variable = { parl_weights^0 = party_popularity@social_democracy }
set_variable = { parl_weights^1 = party_popularity@liberal_democracy }
```

---

## Part 4: Other Reads — opinion@, distance_to@, unit counts, built-ins

```
# Diplomatic opinion of another country (symmetric per-pair pipelines):
set_temp_variable = { opinion_t = opinion@PREV }

# Distance between two capitals (var:-parameterized engine query):
set_temp_variable = { target_capital = FROM.capital }
set_temp_variable = { dist = THIS.capital:distance_to@var:target_capital }

# Order-of-battle counts → coefficient cost models:
set_variable = { at_manpower_k = 0.4 }
multiply_variable = { at_manpower_k = num_battalions_with_type@anti_tank }
add_to_variable = { army_manpower_k = at_manpower_k }

set_variable = { cv_manpower_k = 1.2 }
multiply_variable = { cv_manpower_k = num_ships_with_type@carrier }
add_to_variable = { navy_manpower_k = cv_manpower_k }
```

### Built-in values worth knowing

Read like variables on the right-hand side of any variable effect or in `check_variable`:

- **Country**: `num_of_factories`, `num_of_civilian_factories`, `num_of_military_factories`, `num_of_naval_factories`, `max_manpower_k`, `num_divisions`, `num_battalions`, `political_power`, `command_power`, `stability`, `casualties`, `surrender_progress`, `num_owned_states`, `num_core_states`, `amount_research_slots`
- **State**: `state_population`, `state_population_k`, `infrastructure_level`, `industrial_complex_level`, `arms_factory_level`, `dockyard_level`
- **Anywhere**: `random` — a fresh [0,1) sample **each time it is read**; copy it to a temp first if one roll must be reused.

```
var:state_id = {
    set_variable = { MYC.state_pop_k^idx = state_population_k }
}
```

---

## Part 5: Random Numbers

```
set_variable_to_random = num_dogs                                   # direct form: [0, 1)
set_variable_to_random = { var = roll min = 5 max = 10 }            # block form: [min, max)
set_variable_to_random = { var = roll min = -10 max = 10 integer = yes }
set_temp_variable_to_random = { var = roll min = 0 max = var:cap }  # temp variant; var bounds OK
```

Range is **half-open** `[min, max)`; `integer = yes` yields whole numbers; defaults min 0, max 1.

### Pattern: jitter

```
set_variable_to_random = { var = jitter min = -10 max = 10 integer = yes }
add_to_variable = { region_data^2 = jitter }
subtract_from_variable = { region_data^0 = jitter }      # conserve the total
```

### Pattern: random partition summing exactly to 100

Roll each share from what remains; assign the **last share deterministically** — no normalization pass needed:

```
set_temp_variable = { pct_left = 100 }
set_variable_to_random = { var = share_state@var:v min = 0 max = 100 integer = yes }
subtract_from_temp_variable = { pct_left = share_state@var:v }
set_variable_to_random = { var = share_corporate@var:v min = 0 max = var:pct_left integer = yes }
subtract_from_temp_variable = { pct_left = share_corporate@var:v }
set_variable = { share_private@var:v = pct_left }
```

Caveat: earlier rolls statistically dominate later ones (stick-breaking bias) — acceptable for flavor seeding, not for fair distributions.

### Pattern: random factor

```
set_variable_to_random = { var = f min = 0.8 max = 1.2 }
multiply_variable = { base_growth = f }
```

---

## Part 6: MTTH Variables as a Computation Engine

Files in `common/mtth/*.txt` define named calculations with a `base` and ordered `modifier` blocks; read anywhere with `mtth:name`. They evaluate **on demand** (always current, never cached).

```
my_calculation = {
    base = 5
    modifier = {                                  # conditional flat add
        check_variable = { facilities > 10 }
        add = 2
    }
    modifier = { add = modifier@my_flat_channel } # data tokens work here
    modifier = {                                  # (1 + factor-channel) multiplier
        set_temp_variable = { var = f_temp value = 1 }
        add_to_temp_variable = { var = f_temp value = modifier@my_factor_channel }
        factor = f_temp
    }
}
```

Rules: modifiers apply **in order** (`add` then `factor` ≠ `factor` then `add`); `add`/`factor` accept literals, variables, and `mtth:` references; `check_variable` conditions gate each block; temp-variable math inside a block is legal. **Initialize and consume the *same* temp name** — a mismatched temp name silently contributes nothing (this exact bug ships in real mods).

### Aggregation over states

```
state_total_calc = {
    base = 0
    modifier = {
        set_temp_variable = { var = state_total value = 0 }
        all_owned_state = {
            add_to_temp_variable = { var = state_total value = mtth:per_state_value }
        }
        add = state_total          # ← without this line the loop computes and discards
    }
}
```

### Drift controller (proportional feedback)

Target computed from modifiers; stored value chases it at 20%/tick:

```
# common/mtth/legitimacy.txt
legitimacy_target = {
    base = 50
    modifier = { add = modifier@legitimacy_modifier }
    modifier = {
        set_temp_variable = { var = lf_temp value = 1 }
        add_to_temp_variable = { var = lf_temp value = modifier@legitimacy_factor }
        factor = lf_temp
    }
}
legitimacy_drift = {
    base = 0
    modifier = {
        set_temp_variable = { var = drift_temp value = mtth:legitimacy_target }
        subtract_from_temp_variable = { var = drift_temp value = legitimacy }   # stored variable
        multiply_temp_variable = { var = drift_temp value = 0.2 }
        add = drift_temp
    }
}

# on_actions (daily/weekly):
add_to_variable = { legitimacy = mtth:legitimacy_drift }
clamp_variable = { var = legitimacy min = 0 max = 100 }
```

MTTH values also work in scripted GUI `visible`/triggers and dynamic modifiers. Avoid circular references; cache hot values into regular variables when read repeatedly per tick; `all_owned_state` aggregation is expensive for wide empires.

---

## Part 7: Pipeline Idioms

### Math-expression pipeline

For one-shot calculations, prefer a math expression in the variable effect over a long temp-variable chain. Expressions start with `value = ...`, then apply operations in order. They support data tokens, variables, constants, conditionals, comparisons, `round`, `clamp`, and `every_collection`.

```
set_variable = {
    industrial_score = {
        value = resource_produced@steel
        multiply = 0.45
        add = { value = resource_produced@oil multiply = 0.70 }
        add = { value = modifier@industrial_capacity_factory add = 1 multiply = num_of_factories }
        clamp = { min = 0 max = 9999 }
    }
}
```

Boolean expression results use `0.0` as false and nonzero as true; comparison operators return `1.0` or `0.0`.

```
set_variable = {
    pressure_bonus = {
        value = surrender_progress
        greater_than = 0.5
        multiply = 25
    }
}
```

Aggregation over a live collection:

```
set_variable = {
    non_capitulated_major_factories = {
        value = 0
        every_collection = {
            named_collection = non_capitulated_majors
            add = num_of_factories
        }
    }
}
```

Expressions are supported by normal and temp variable effects except `modulo_variable` and `clamp_variable`, which keep their native syntax.

### Read–weight–accumulate (temp reuse)

One temp per pipeline, reset by each `set_temp_variable` — see the resource score in Part 2.

### Factor application

`factor_channel` is a delta; convert before multiplying: `+1`, clamp at 0 if debuffs can stack, multiply.

### Share / percentage normalization

```
set_variable = { ratio^idx = part^idx }
divide_variable = { ratio^idx = whole^idx }
multiply_variable = { ratio^idx = 100 }
round_variable = ratio^idx                       # round_variable / round_temp_variable exist
```

`divide_variable` does **not** round — apply `round_variable` explicitly. `modulo_variable = { var = x value = n }` exists for cyclic math. For making rounded shares sum to exactly 100, see the largest-remainder repair in `hoi4-advanced-arrays`.

### Quota apportionment with floor

```
set_variable = { seats^idx = pop_k^idx }
divide_variable = { seats^idx = 4 }              # 1 seat per 4k population
round_variable = seats^idx
if = {
    limit = { check_variable = { seats^idx = 0 } }
    set_variable = { seats^idx = 1 }             # small-region protection
}
```

### Sign-splitting for display (map mode RGB)

Map a signed value onto a red↔green gradient with zero branching — divide by opposite-signed ranges and clamp:

```
set_temp_variable = { red = opinion@ROOT }
divide_temp_variable = { red = -75 }             # negative opinions → positive red
clamp_temp_variable = { var = red min = 0 max = 1 }
set_temp_variable = { green = opinion@ROOT }
divide_temp_variable = { green = 75 }            # positive opinions → positive green
clamp_temp_variable = { var = green min = 0 max = 1 }
```

### Slider remap

Map a 0–100 GUI slider onto a 0.2–1.0 multiplier:

```
set_variable = { slider_effect = my_slider_pct }
multiply_variable = { slider_effect = 0.8 }
add_to_variable = { slider_effect = 20 }
divide_variable = { slider_effect = 100 }
multiply_variable = { upkeep_costs = slider_effect }
```

### Demographic multiply-chain (election model)

votes = roll × bloc share × turnout × affiliation, fanned out per party and accumulated — then normalized to popularity:

```
set_temp_variable = { bloc_voters = voter_roll }
multiply_temp_variable = { bloc_voters = bloc_pop_share }
multiply_temp_variable = { bloc_voters = bloc_turnout }

set_temp_variable = { votes_a = bloc_voters }
multiply_temp_variable = { votes_a = MYC.bloc_party_a_affiliation }
add_to_temp_variable = { party_a_votes = votes_a }
# ... per bloc × per party; finally:
set_variable = { party_a_pop = party_a_votes }
divide_variable = { party_a_pop = total_votes }
multiply_variable = { party_a_pop = 100 }
round_variable = party_a_pop
```

### Effects as functions

Temp variables are arguments; document the contract in a header comment:

```
# params: prestige_change = amount to add
change_prestige = {
    custom_effect_tooltip = change_prestige_tt
    add_to_variable = { prestige_score = prestige_change }
}

# call:
set_temp_variable = { prestige_change = 5 }
change_prestige = yes
```

---

## Pitfalls

1. **Scale traps**: `party_popularity@` is 0–1, `party_popularity_100@` is 0–100; `state_population_k` is thousands. Convert explicitly.
2. **`resource@` means surplus** in country scope but production in state scope.
3. **`random` re-rolls on every read** — snapshot to a temp when one roll feeds several places.
4. **`set_variable_to_random` is half-open** `[min, max)` — `max` itself never occurs; for integer dice over 1..6 use `min = 1 max = 7 integer = yes`.
5. **MTTH temp-name mismatches fail silently** — initialize and consume identical names; ensure aggregation blocks actually `add`/`factor` their accumulator.
6. **`divide_variable` doesn't round**; `!=` doesn't exist in `check_variable` (use `compare = not_equals`).
7. **Factor channels can go negative** under stacked debuffs — clamp before multiplying if that would flip signs.

## Reference Files

- `references/data_tokens_reference.md` — full token & built-in value catalog, cross-scope forms
- `references/modifier_pipeline.md` — custom modifier channel design, calculation patterns
- `references/mtth_computation.md` — MTTH engine details, chaining, drift controllers
- `../hoi4-variable-helper/references/math_expressions.md` — inline formulas and collection iterators for variable effects
