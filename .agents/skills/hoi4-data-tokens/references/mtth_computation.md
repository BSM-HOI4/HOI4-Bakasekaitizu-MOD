# MTTH Computation Engine Reference

## File location & shape

`common/mtth/*.txt`. Each top-level key is a named calculation:

```
variable_name = {
    base = <number>
    modifier = {
        # optional gating conditions
        check_variable = { var = my_var value = 10 compare = greater_than }
        # contribution — add and/or factor
        add = <number | variable | mtth:other>
        factor = <number | variable>
    }
    modifier = { ... }    # applied IN ORDER
}
```

Read anywhere with `mtth:variable_name` — scripted effects, scripted GUI triggers/visible, dynamic modifiers, other MTTH definitions. Values evaluate **on demand**: always current, never cached, recomputed per read.

## Modifier block rules

- Blocks apply in file order: `add` then `factor` ≠ `factor` then `add`.
- `add` accepts literals, plain variables, and `mtth:` references; `factor` accepts literals and variables.
- `check_variable` conditions gate the whole block (multiple conditions AND together).
- Temp-variable computation inside a block is legal — compute, then feed the result to `add`/`factor`.
- **The same temp name must be initialized and consumed.** This bug ships in real mods: a block initializes `x_temp` but adds to / factors by `y_temp` — the contribution silently becomes garbage or never applies. Copy-paste renames are the usual cause; diff temp names when an MTTH "does nothing".
- Compare operators in check_variable: `greater_than`, `less_than`, `greater_than_or_equals`, `less_than_or_equals`, `equals`, `not_equals` (no `!=` shorthand).

## Canonical blocks

```
# Conditional flat bonus
modifier = {
    check_variable = { facilities > 10 }
    add = 2
}

# (1 + factor-channel) multiplier from a modifier@ read
modifier = {
    set_temp_variable = { var = f_temp value = 1 }
    add_to_temp_variable = { var = f_temp value = modifier@my_factor_channel }
    factor = f_temp
}

# Aggregation over owned states — the add line is mandatory:
modifier = {
    set_temp_variable = { var = state_total value = 0 }
    all_owned_state = {
        add_to_temp_variable = { var = state_total value = mtth:per_state_value }
    }
    add = state_total
}

# Tiered factors (each matching tier multiplies in)
modifier = { check_variable = { facilities > 5 }  factor = 1.1 }
modifier = { check_variable = { facilities > 10 } factor = 1.2 }
modifier = { check_variable = { facilities > 20 } factor = 1.5 }
```

## Chaining

```
base_calc = {
    base = 1
    modifier = { add = some_variable }
}
derived_calc = {
    base = 0
    modifier = { add = mtth:base_calc }
    modifier = { factor = 2 }
}
```

Per-state + national chain: a country-level calculation aggregates `mtth:per_state_calc` over `all_owned_state`, then applies national flat/factor channels — formula shape: `result = (base + Σ state values + flat_channel) × (1 + factor_channel)`.

## Drift controller (proportional feedback)

The flagship pattern: a *target* computed live from modifiers, a *stored* variable that chases it.

```
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
        subtract_from_temp_variable = { var = drift_temp value = legitimacy }
        multiply_temp_variable = { var = drift_temp value = 0.2 }
        add = drift_temp
    }
}
```

Driver (on_actions, daily/weekly):

```
add_to_variable = { legitimacy = mtth:legitimacy_drift }
clamp_variable = { var = legitimacy min = 0 max = 100 }
```

Behavior: `drift = (target − current) × 0.2` — exponential approach, 20% of the gap per tick. Raise the coefficient for snappier response; content (ideas/focuses) moves the *target* via the modifier channels and the stored value follows smoothly.

## Usage sites

```
set_variable = { result = mtth:my_calculation }          # effect
visible = { check_variable = { mtth:button_state > 1 } } # scripted GUI
modifier = { factory_output = mtth:production_bonus }    # dynamic modifier
```

## Performance & hygiene

- On-demand evaluation cuts both ways: always fresh, but a complex MTTH read in a per-frame GUI trigger recomputes constantly — cache into a regular variable on a timed tick for hot paths.
- `all_owned_state` aggregation is expensive for wide empires; prefer caching per-state partials.
- No circular references (A → B → A).
- `base` is mandatory in practice — make the no-modifier value explicit (0 for sums, 1 for multipliers).
- Name calculations by what they produce (`legitimacy_target`, `monthly_manpower_total`), not by where they're used.
