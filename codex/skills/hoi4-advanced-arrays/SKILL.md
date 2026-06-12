---
name: hoi4-advanced-arrays
description: Advanced HOI4 array patterns — parallel arrays (struct-of-arrays), resize_array pre-allocation, sorting algorithms (selection sort, argsort, quicksort), for_each_scope_loop, while_loop_effect, FIFO queues, dedup, seat apportionment, loop control (break, iteration caps), and when to replace manual arrays with live collections. Use when the user (1) Needs multiple properties per entity, (2) Wants to sort or rank arrays, (3) Needs pre-allocated fixed-size arrays, (4) Wants to iterate scope-reference arrays or collections, (5) Needs break/early-exit or bounded loops, (6) Needs formula/reduction logic over arrays or collections, or (7) Says phrases like "配列でソート", "parallel arrays", "多次元配列", "sort array", "resize_array", "for_each_scope_loop", "collection", "コレクション", "議席配分", "ドント式". Self-contained reference — all syntax verified against official HOI4 script documentation.
---

# HOI4 Advanced Array Patterns

## Overview

HOI4 arrays hold one value per index, but disciplined conventions turn them into databases, sorted rankings, queues, and lookup tables. Collections are now the better tool for live, unordered membership derived from game state. This skill covers verified array mechanics (exact effect syntax, loop semantics, the 1000-iteration engine cap), when to switch to collections, and the algorithm library proven in large total-conversion mods.

Companion skills: `hoi4-token-system` (dynamic array *names*, tokens as elements), `hoi4-data-tokens` (reading game values into arrays), `hoi4-variable-helper` (collections, math expressions, basics).

## Quick Reference

```
# Add / remove — verified semantics
add_to_array = { my_array = 42 }                          # short form: append VALUE
add_to_array = { array = my_array value = 42 index = 0 }  # long form: insert at index (shifts)
add_to_array = { array = my_array }                       # no value → adds current SCOPE
remove_from_array = { my_array = 42 }                     # short form: remove BY VALUE (first match)
remove_from_array = { array = my_array index = 3 }        # by index
remove_from_array = { array = my_array }                  # neither → removes LAST element

# Size & indexing
check_variable = { my_array^num > 0 }     # ^num = element count
my_array^0   my_array^i   my_array^idx_var   a^b^c        # literal / variable / nested index

# Pre-allocation — two forms
resize_array = { my_array = 9 }                           # short: size only, new elements = 0
resize_array = { array = my_array value = -1 size = 256 } # long: explicit fill for NEW elements

# Loops
for_each_loop = { array = a value = v index = i break = b ... }   # defaults: v / i / break
for_loop_effect = { start = 0 end = a^num value = v ... }         # end EXCLUSIVE (compare=less_than)
for_each_scope_loop = { array = scope_array ... }                 # scope shifts to each element
while_loop_effect = { limit = { <trigger> } break = b ... }       # trigger tested before each pass

# Break: set the break temp var nonzero (break = yes is INVALID)
set_temp_variable = { b = 1 }

# Search
find_highest_in_array = { array = a value = v index = i }  # outputs are TEMP vars; lowercase names only
find_lowest_in_array  = { array = a value = v index = i }

# Prefer collections when membership is live and unordered:
# collection:non_capitulated_majors, game:all_countries, collections:all_countries where required
```

Use arrays when order, stable indices, sorting, queues, or parallel fields matter. Use collections when the set should auto-update from triggers/operators and does not need stable ordering.

---

## Part 1: Exact Mechanics (the part everyone gets wrong)

### Loop parameters — verified

**for_each_loop**: `array`, `value` (default `v`), `index` (default `i`), `break` (default `break`). The value/index/break names are **temp variables**; defaults apply when omitted — `^i` works inside a loop that never declared `index`.

**for_loop_effect**: `start` (default 0), `end` (default 0), `compare` (default `less_than`), `add` (default 1), `value` (default `v`), `break`. There is **no `index` parameter**. Because the default compare is `less_than`, `end` is **exclusive** — `start = 0 end = my_array^num` visits exactly the valid indices. Use `compare = less_than_or_equals` for inclusive, negative `add` plus `compare = greater_than...` for descending.

**while_loop_effect**: `limit = { <trigger> }` tested before each iteration, plus `break`.

**Break semantics**: `break = name` *names* a temp variable; setting it nonzero exits **before the next iteration** — the remaining effects of the current iteration still run. Guard trailing statements with `if` if they must not execute after the break condition. `break = yes` is invalid (it would read a variable literally named `yes`).

**Engine cap**: `MAX_EFFECT_ITERATION = 1000` (defines) — no loop effect exceeds 1000 iterations. For bigger jobs, time-slice (Part 6).

### find_highest_in_array / find_lowest_in_array

Params: `array` (required), `value` (default `v`), `index` (default `i`). Outputs are temp variables. Two caveats:

- **Output names must be all-lowercase** — uppercase characters in `value`/`index` names break these effects.
- On an **empty array** the outputs are never written (read as 0) — guard with `check_variable = { arr^num > 0 }`.

### resize_array — two forms, different fill behavior

```
resize_array = { my_array = 58 }                            # short: grow/shrink, new slots = 0
resize_array = { array = my_array value = 17 size = 21 }    # long: new slots = 17
```

Growing fills only the **newly added** slots with `value`; shrinking truncates from the end. Incremental resizing builds segment-mapped arrays:

```
clear_array = faction_group_map
resize_array = { array = faction_group_map value = 1 size = 4 }   # factions 0-3  → group 1
resize_array = { array = faction_group_map value = 2 size = 8 }   # factions 4-7  → group 2
resize_array = { array = faction_group_map value = 3 size = 11 }  # factions 8-10 → group 3
# faction_group_map = [1,1,1,1,2,2,2,2,3,3,3]
```

Size can come from a runtime variable: `resize_array = { array = buckets value = 0 size = length_temp }`. Temp variants exist for everything: `add_to_temp_array`, `remove_from_temp_array`, `clear_temp_array = name`, `resize_temp_array`.

---

## Part 2: Parallel Arrays — Struct of Arrays

Multiple arrays sharing indices simulate records. Convention: name them `<entity>_<field>`.

```
# Per-state demographics seeded in state history blocks (runs at game start):
add_to_array = { state_culture_array = 88 }       # culture id
add_to_array = { state_culture_array_num = 0.68 } # population share
add_to_array = { state_culture_array = 121 }
add_to_array = { state_culture_array_num = 0.10 }
# state_culture_array^0 and state_culture_array_num^0 describe the same group
```

### Loop one array, index the siblings

```
for_each_loop = {
    array = council_member_id
    value = v
    index = i
    if = {
        limit = { check_variable = { council_member_alignment^i = 0 } }
        add_to_temp_variable = { hardliner_count = 1 }
    }
    if = {
        limit = { check_variable = { council_member_alignment^i = 1 } }
        add_to_temp_variable = { moderate_count = 1 }
    }
}
```

### Fill from game data with for_each_scope_loop

`for_each_scope_loop` shifts scope to each element, so writes back to the calling country need an explicit prefix (`ROOT.` or a tag):

```
clear_array = province_pop
clear_array = province_gdp
resize_array = { province_pop = 58 }
resize_array = { province_gdp = 58 }

for_each_scope_loop = {
    array = global.tracked_states            # state scopes stored with add_to_array = { ... = THIS }
    set_variable = { slot = my_state_index } # variable stored on the state
    set_variable = { pop_m = state_population_k }
    divide_variable = { pop_m = 1000 }
    add_to_variable = { ROOT.province_pop^slot = pop_m }
    add_to_variable = { ROOT.province_gdp^slot = state_value_estimate }
}
```

### FIFO sliding window (rolling graph data)

Bounded queue over parallel arrays — append at tail, drop index 0 when over capacity, **always dequeue every sibling together**:

```
graph_monthly_tick = {
    add_to_array = { graph_months = current_month_var }
    add_to_array = { graph_gdp = gdp }
    add_to_array = { graph_inflation = inflation_rate }
    if = {
        limit = { check_variable = { graph_months^num > 17 } }    # keep last 18
        remove_from_array = { array = graph_months index = 0 }
        remove_from_array = { array = graph_gdp index = 0 }
        remove_from_array = { array = graph_inflation index = 0 }
    }
}
```

`remove_from_array` by index shifts the remainder down, so the window stays aligned and ordered.

### Sorting parallel arrays

Whatever sort you use, **remove/copy all sibling arrays at the same index in the same step** (Part 4) — desync between siblings corrupts every record after the first mismatch.

---

## Part 3: Scope Arrays — Storing Countries & States

`add_to_array = { list = THIS }` stores the current scope's id (country id in country scope, state id in state scope); `THIS.id` does the same explicitly from country scope. Scope back in with `var:` or iterate with `for_each_scope_loop`:

```
add_to_array = { global.major_powers = THIS }
var:global.major_powers^0 = { add_political_power = 50 }
for_each_scope_loop = {
    array = global.major_powers
    # scope = each stored country
}
```

### Collections as array replacements

Do not maintain an array by periodic add/remove effects when the membership is just "all countries/states matching conditions right now". Define a collection in `common/collections/` and iterate/count it directly; it auto-updates and can be chained with constants or other collections.

```
non_capitulated_majors = {
    input = game:all_countries
    operators = {
        limit = {
            is_major = yes
            has_capitulated = no
        }
    }
    name = COLLECTION_NON_CAPITULATED_MAJORS
}

set_variable = {
    major_factory_total = {
        value = 0
        every_collection = {
            named_collection = non_capitulated_majors
            add = num_of_factories
        }
    }
}
```

Keep arrays for ordered leaderboards, queue windows, stable index tables, and token-keyed records. Use collections for dynamic target sets such as non-capitulated majors, faction-controlled core states, or constant-defined regional state groups.

### Leader-at-index-0 idiom

```
remove_from_array = { global.group_members = THIS }                       # remove by value
add_to_array = { array = global.group_members value = THIS index = 0 }    # re-insert at front
```

### Arrays as decision-target sources

A curated scope array can drive targeted decisions directly — cheaper than `target_trigger` scans and exactly tracks a dynamic set:

```
my_state_decision = {
    state_target = yes
    target_array = MYC.managed_states          # one decision instance per element
    target_trigger = { FROM = { is_core_of = MYC } }   # cheap secondary filter
    complete_effect = { add_to_variable = { FROM.local_control = 1.5 } }
}

# Curate the array at runtime:
every_owned_state = {
    limit = { NOT = { state = 123 } }
    MYC = { add_to_array = { managed_states = PREV } }
}
```

---

## Part 4: Sorting Algorithms

Full annotated templates in `references/sorting_algorithms.md`. Summary of when to use which:

| Algorithm | Use when | Cost |
|---|---|---|
| Selection sort (find_highest + remove) | ≤ ~60 elements, paired arrays | O(n²), destructive w/ copy-back |
| Argsort (sentinel zeroing) | indices must stay meaningful (id → name lookups) | O(n²), non-destructive |
| Nested min-find + front-insert | small arrays, in-place | O(n²) |
| Find-middle trick | just need max / mid / min | O(n) |
| Iterative quicksort (explicit stack) | 100+ elements, generic sort key | O(n log n), advanced |

### Selection sort with paired arrays (canonical template)

```
sort_ranking = {
    set_temp_variable = { length_temp = global.score_array^num }

    # Phase 1: repeatedly extract the max into temp arrays
    for_loop_effect = {
        start = 0
        end = length_temp
        value = n
        find_highest_in_array = {
            array = global.score_array
            value = best_value
            index = best_index
        }
        set_temp_variable = { tag_temp = global.score_tag_array^best_index }
        remove_from_array = { array = global.score_array index = best_index }
        remove_from_array = { array = global.score_tag_array index = best_index }
        add_to_temp_array = { array = global.score_array_temp value = best_value }
        add_to_temp_array = { array = global.score_tag_array_temp value = tag_temp }
    }

    # Phase 2: copy back sorted; assign 1-based rank to each country
    for_loop_effect = {
        start = 0
        end = length_temp
        value = n
        add_to_array = { array = global.score_array value = global.score_array_temp^n }
        add_to_array = { array = global.score_tag_array value = global.score_tag_array_temp^n }
        set_temp_variable = { rank_tag = global.score_tag_array_temp^n }
        var:rank_tag = {
            set_variable = { score_rank = n }
            add_to_variable = { score_rank = 1 }
        }
    }
}
```

After Phase 1 the source arrays are empty (every element was removed), so Phase 2 plain-appends — no clear needed. With 3+ sibling arrays, extract and remove **all** siblings at `best_index` in Phase 1.

### Argsort — non-destructive rank order

When indices map to entities (state id → name/color tables), produce a sorted *permutation* instead of moving data. Requires strictly positive values (0 is the "consumed" sentinel):

```
clear_array = sorted_values
clear_array = sorted_indices
for_loop_effect = {
    start = 0
    end = margins^num
    find_highest_in_array = { array = margins }   # defaults: value → v, index → i
    add_to_array = { sorted_values = v }
    add_to_array = { sorted_indices = i }
    set_variable = { margins^i = 0 }              # consume
}
# Restore margins from sorted_values/sorted_indices afterwards if needed.
```

### Find-middle trick

```
find_highest_in_array = { array = loyalties index = high_i value = high_v }
find_lowest_in_array  = { array = loyalties index = low_i  value = low_v }
set_variable = { loyalties^high_i = 0 }
find_highest_in_array = { array = loyalties index = mid_i value = mid_v }
set_variable = { loyalties^high_i = high_v }      # restore
```

---

## Part 5: Algorithm Toolbox

### D'Hondt seat apportionment (proportional representation)

Award seats one at a time: quotient = support / divisor; winner's divisor increments, shrinking its next quotient:

```
award_one_seat = {
    clear_temp_array = quotient_list
    for_each_loop = {
        array = party_support
        index = party_id
        set_temp_variable = { q = party_support^party_id }
        divide_temp_variable = { q = divisor_list^party_id }
        add_to_temp_array = { quotient_list = q }
    }
    find_highest_in_array = { array = quotient_list index = winner }
    add_to_variable = { seats_list^winner = 1 }
    add_to_variable = { divisor_list^winner = 1 }       # D'Hondt: divisor starts at 1
}
# Initialize divisor_list to all 1s (resize_array long form), call once per seat.
```

### Sum-to-100 normalization (largest-remainder repair)

Independently rounded percentages drift off 100; dump the residual on the largest element:

```
set_temp_variable = { ratio_sum = 0 }
for_each_loop = {
    array = ratio_list
    value = r
    add_to_temp_variable = { ratio_sum = r }
}
find_highest_in_array = { array = ratio_list value = big_v index = big_i }
while_loop_effect = {
    limit = { check_variable = { ratio_sum < 100 } }
    add_to_variable = { ratio_list^big_i = 1 }
    add_to_temp_variable = { ratio_sum = 1 }
}
while_loop_effect = {
    limit = { check_variable = { ratio_sum > 100 } }
    subtract_from_variable = { ratio_list^big_i = 1 }
    subtract_from_temp_variable = { ratio_sum = 1 }
}
```

### In-place dedup (nested occurrence scan)

```
for_each_loop = {
    array = sample_array
    index = outer_i
    value = outer_v
    set_temp_variable = { seen = 0 }
    for_each_loop = {
        array = sample_array                  # inner loop uses default v / i
        if = {
            limit = { check_variable = { outer_v = v } }
            add_to_temp_variable = { seen = 1 }
        }
        if = {
            limit = { check_variable = { seen = 2 } }
            remove_from_array = { array = sample_array index = i }
            set_temp_variable = { seen = 1 }   # keep stripping further copies
        }
    }
}
```

Works because the outer loop's renamed `outer_v`/`outer_i` don't collide with the inner defaults. O(n²) — fine for small sets (e.g. 8 random picks).

### Lookup-table function evaluation

Math functions via pre-built tables: scale the input to an integer index (array subscripts truncate), look up, and optionally discard the table afterwards to avoid savegame bloat:

```
# arctan via 0.001-resolution table over [-pi/2, pi/2]:
add_to_temp_variable = { input = 1.571 }          # shift to non-negative
multiply_temp_variable = { input = 1000 }          # scale to index
build_atan_table = yes                             # add_to_array x N entries
set_temp_variable = { result = atan_values^input }
clear_array = atan_values                          # build-use-discard
```

### Accumulation / reduction

```
clear_variable = total
for_each_loop = {
    array = per_state_values
    value = x
    add_to_variable = { total = x }
}
```

### Index-list generation

```
clear_array = global.page_list
for_loop_effect = {
    start = 0
    end = global.page_count
    value = page_id
    add_to_array = { global.page_list = page_id }
}
```

---

## Part 6: Loop Control Patterns

### Nested matching with break

```
every_owned_state = {
    for_each_loop = {
        array = state_culture_array
        index = i
        value = v
        for_each_loop = {
            array = PREV.national_culture_array        # PREV = the country
            index = ii
            value = vv
            break = bb
            if = {
                limit = { check_variable = { v = vv } }
                add_to_variable = { PREV.national_culture_population^ii = state_culture_pop^i }
                set_temp_variable = { bb = 1 }
            }
        }
    }
}
```

Remember: the break takes effect before the *next* iteration — statements after `set_temp_variable = { bb = 1 }` in the same pass still run.

### Time-slicing (beating the 1000-iteration cap & frame hitches)

Process a bounded chunk per tick/GUI-update, tracking progress in persistent variables — e.g. an election counting one seat per state per update:

```
count_votes_tick = {
    for_each_loop = {
        array = constituency_list
        index = c_id
        if = {
            limit = { check_variable = { counted_seats^c_id < total_seats^c_id } }
            # ... award exactly one seat (D'Hondt step above) ...
            add_to_variable = { counted_seats^c_id = 1 }
        }
    }
}
# Re-invoked by on_actions / GUI updates until counted == total — animates results live.
```

### Cursor state machine across events

Iterate an array where each step is a player-facing event: store a cursor, fire `var:array^cursor`, increment on the event's answer, re-check `cursor < array^num`:

```
set_variable = { cursor = 0 }
var:negotiation_targets^cursor = { country_event = my_mod.209 }
# In my_mod.209's options: add_to_variable = { PREV.cursor = 1 } then re-fire if in bounds.
```

### Manufactured bounded loop (recursion substitute)

Script effects can't recurse (beyond one self-reference level). To "loop until N collected", iterate a dummy array of size N with a break:

```
resize_temp_array = { temp_loop = 8 }
for_each_loop = {
    array = temp_loop
    break = done
    # ... attempt to generate/collect one item ...
    if = {
        limit = { check_variable = { collected^num > 7 } }
        set_temp_variable = { done = 1 }
    }
}
```

---

## Pitfalls & Performance

1. **`break = yes` is invalid**; `end` of for_loop_effect is exclusive; for_loop_effect has no `index`.
2. **find_highest/lowest output names: lowercase only**; unwritten on empty arrays.
3. **Sibling desync** — any structural change (remove/insert/sort) must hit every parallel array identically, in the same step.
4. **remove_from_array short form removes by value** — `remove_from_array = { arr = 3 }` removes the first element *equal to 3*, not index 3.
5. **1000-iteration engine cap** on loop effects — time-slice anything bigger.
6. **Selection sort is O(n²)** — fine ≤ ~60 elements; use the quicksort template beyond that.
7. **^num is a pseudo-element** (the size), not an index; valid loop indices are `0 .. ^num-1`.
8. Prefer `is_in_array` to a manual scan; prefer `find_highest_in_array` to a manual max loop — they're native single effects.

## Reference Files

- `references/parallel_arrays.md` — struct-of-arrays conventions, pre-allocation templates, FIFO window, weighted-random seat assignment
- `references/sorting_algorithms.md` — full sort templates incl. iterative quicksort with meta_effect-parameterized sort key
