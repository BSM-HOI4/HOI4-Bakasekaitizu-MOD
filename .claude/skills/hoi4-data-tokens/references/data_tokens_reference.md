# Data Access Token Catalog

## Value-reading tokens

| Token | Scope | Returns |
|---|---|---|
| `modifier@<token>` | country, state, MIO | current summed value of the modifier (custom dynamic-modifier channels included) |
| `leader_modifier@<token>` | unit leader | leader-scope modifier value (e.g. `leader_modifier@navy_max_range`) |
| `unit_modifier@<token>` | unit leader | unit-scope modifier value (e.g. `unit_modifier@army_attack_factor`) |
| `resource@<resource>` | country | **surplus** of that resource |
| `resource@<resource>` | state | resources **produced** in the state |
| `resource_produced@<resource>` | country | total produced by the country |
| `resource_consumed@` / `resource_exported@` / `resource_imported@` | country | as named (rarely needed) |
| `party_popularity@<target>` | country | popularity 0.00–1.00; target = ideology group, `ruling_party`, or a token variable (`@var:x` / `@my_var`) |
| `party_popularity_100@<target>` | country | popularity 0–100, same targets |
| `opinion@<TAG/scope>` | country | diplomatic opinion of the target |
| `distance_to@<state>` | state | distance to the given state; parameterizable: `:distance_to@var:x` |
| `num_battalions_with_type@<sub_unit>` | country | fielded battalion count of that type |
| `num_ships_with_type@<hull>` | country | fielded ship count of that hull type |
| `days_mission_timeout@<mission>` | country | days until the mission times out (loc/display use) |

Cross-scope prefixes work on all of them: `ROOT.modifier@x`, `PREV.modifier@x`, `GER.party_popularity@democratic`, `123.modifier@local_manpower`.

## Built-in values readable as variables

Country scope: `num_of_factories`, `num_of_civilian_factories`, `num_of_military_factories`, `num_of_naval_factories`, `num_of_available_civilian_factories`, `num_of_available_military_factories`, `max_manpower_k`, `max_available_manpower_k`, `manpower_k`, `num_divisions`, `num_battalions`, `political_power`, `command_power`, `stability`, `war_support`, `casualties`, `surrender_progress`, `num_owned_states`, `num_owned_controlled_states`, `num_occupied_states`, `num_core_states`, `amount_research_slots`, `legitimacy` (government-in-exile), `capital` (state id — feeds `var:` scoping).

State scope: `state_population`, `state_population_k`, `infrastructure_level`, `industrial_complex_level`, `arms_factory_level`, `dockyard_level`, `state_strategic_value`.

Anywhere: `random` — fresh [0,1) sample per read; snapshot to a temp to reuse one roll.

```
set_variable = { x = num_of_factories }
check_variable = { state_population_k > 500 }
set_temp_variable = { r = random }
```

## set_variable_to_random — full forms

```
set_variable_to_random = num_dogs                                  # [0, 1)
set_variable_to_random = { var = x min = 5 max = 10 }              # [min, max), floats
set_variable_to_random = { var = x min = -10 max = 10 integer = yes }
set_temp_variable_to_random = { var = x min = 0 max = var:cap }    # temp variant, variable bounds
```

Defaults: min 0, max 1, integer no. Range is half-open — `max` never occurs.

## Computation chain cheat sheet

```
# Read–weight–accumulate
set_temp_variable = { t = DATA_SOURCE }
multiply_temp_variable = { t = WEIGHT }
add_to_variable = { accumulator = t }

# Factor application (delta → multiplier, clamped)
set_temp_variable = { f = 1 }
add_to_temp_variable = { f = modifier@my_factor_channel }
if = {
    limit = { check_variable = { f < 0 } }
    set_temp_variable = { f = 0 }
}
multiply_variable = { result = f }

# Percentage share
set_variable = { share = part }
divide_variable = { share = whole }
multiply_variable = { share = 100 }
round_variable = share

# Drift toward a target
set_temp_variable = { drift = mtth:target_value }
subtract_from_temp_variable = { drift = current_value }
multiply_temp_variable = { drift = 0.2 }
add_to_variable = { current_value = drift }
clamp_variable = { var = current_value min = 0 max = 100 }
```

Rounding/modulo effects: `round_variable = x`, `round_temp_variable = x`, `modulo_variable = { var = x value = n }`, `modulo_temp_variable = { var = x value = n }`. `divide_variable` never rounds. `clamp_variable = { var = x min = a max = b }` — min or max may be omitted; order is `Max(Min(var, max), min)`.
