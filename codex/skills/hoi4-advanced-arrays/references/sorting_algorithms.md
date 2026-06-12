# Sorting Algorithms in HOI4 Script

Constraints that shape every sort here: no recursion (emulate stacks with arrays), `MAX_EFFECT_ITERATION = 1000` per loop effect, `find_highest_in_array`/`find_lowest_in_array` output names must be lowercase, and parallel arrays must move together.

## 1. Selection Sort, Paired Arrays (descending) — the workhorse

Use for rankings of ≤ ~60 entities with a value array + an id/tag array:

```
sort_ranking = {
    set_temp_variable = { length_temp = global.score_array^num }

    # Phase 1: extract max repeatedly into temp arrays (source arrays end up empty)
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

    # Phase 2: copy back + assign 1-based ranks onto each country
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

Ascending variant: swap in `find_lowest_in_array`.

## 2. Selection Sort, 3+ Sibling Arrays

Every sibling is read, staged, and removed at the same index inside one iteration:

```
sort_culture_arrays = {
    set_temp_variable = { length_temp = culture_share^num }
    clear_temp_array = culture_share_tmp
    clear_temp_array = culture_pop_tmp
    clear_temp_array = culture_id_tmp

    for_loop_effect = {
        end = length_temp                      # start/add default to 0/+1
        value = n
        find_highest_in_array = {
            array = culture_share
            value = highest_val
            index = highest_idx
        }
        add_to_temp_array = { culture_share_tmp = highest_val }
        set_temp_variable = { pop_tmp = culture_pop^highest_idx }
        set_temp_variable = { id_tmp = culture_id^highest_idx }
        add_to_temp_array = { culture_pop_tmp = pop_tmp }
        add_to_temp_array = { culture_id_tmp = id_tmp }
        remove_from_array = { array = culture_share index = highest_idx }
        remove_from_array = { array = culture_pop index = highest_idx }
        remove_from_array = { array = culture_id index = highest_idx }
    }

    for_loop_effect = {
        end = length_temp
        value = n
        add_to_array = { culture_share = culture_share_tmp^n }
        add_to_array = { culture_pop = culture_pop_tmp^n }
        add_to_array = { culture_id = culture_id_tmp^n }
    }
}
```

## 3. Argsort — non-destructive permutation

Indices stay meaningful (each maps to an entity in other index-aligned tables). Requires strictly positive values; 0 marks "consumed":

```
clear_array = sorted_values
clear_array = sorted_indices
for_loop_effect = {
    start = 0
    end = margins^num
    find_highest_in_array = { array = margins }    # defaults: value → v, index → i
    add_to_array = { sorted_values = v }
    add_to_array = { sorted_indices = i }
    set_variable = { margins^i = 0 }
}
# Optionally restore: for n in 0..^num: margins^(sorted_indices^n) = sorted_values^n
# (restore needs a^b^c nested indexing: set_variable = { margins^sorted_indices^n = sorted_values^n })
```

## 4. Nested Min-Find with Front-Insertion (in-place, descending)

No temp arrays; repeatedly find the minimum of the unsorted tail and move it to the front:

```
for_loop_effect = {
    start = 0
    end = allies^num
    value = base
    set_temp_variable = { lowest = 999999 }
    set_temp_variable = { tgt = -1 }
    for_loop_effect = {
        start = base
        end = allies^num
        value = i
        if = {
            limit = { check_variable = { points^i < lowest } }
            set_temp_variable = { lowest = points^i }
            set_temp_variable = { tgt = i }
        }
    }
    if = {
        limit = { check_variable = { tgt > -1 } }
        set_temp_variable = { tmp_ally = allies^tgt }
        set_temp_variable = { tmp_points = points^tgt }
        remove_from_array = { array = allies index = tgt }
        remove_from_array = { array = points index = tgt }
        add_to_array = { array = allies value = tmp_ally index = 0 }
        add_to_array = { array = points value = tmp_points index = 0 }
    }
}
```

## 5. Find-Middle Trick (max / mid / min of 3+ without sorting)

```
find_highest_in_array = { array = loyalties index = high_i value = high_v }
find_lowest_in_array  = { array = loyalties index = low_i  value = low_v }
set_variable = { loyalties^high_i = 0 }
find_highest_in_array = { array = loyalties index = mid_i value = mid_v }
set_variable = { loyalties^high_i = high_v }
```

## 6. Iterative Quicksort with Explicit Stack (advanced)

O(n log n) for 100+ element sorts. Recursion is emulated with a stack array + `top` pointer; `(low, high)` ranges are pushed as consecutive slots; `while_loop_effect` drains the stack. Wrapping the whole loop in one `meta_effect` makes the **sort key generic** — the per-element variable name `[SORTKEY]` is substituted once for the entire algorithm (see hoi4-token-system, "hoisting"):

```
# params: low / high (temp), items = array of country scopes, sorts by per-country [SORTKEY]
generic_quicksort = {
    set_temp_variable = { stack_size = high }
    subtract_from_temp_variable = { stack_size = low }
    add_to_temp_variable = { stack_size = 1 }
    resize_temp_array = { array = stack value = 0 size = stack_size }

    set_temp_variable = { top = 0 }
    set_temp_variable = { stack^top = low }
    add_to_temp_variable = { top = 1 }
    set_temp_variable = { stack^top = high }

    meta_effect = {
        text = {
            while_loop_effect = {
                limit = {
                    check_variable = { var = top value = 0 compare = greater_than_or_equals }
                }
                # Pop (low, high)
                set_variable = { high = stack^top }
                subtract_from_temp_variable = { top = 1 }
                set_variable = { low = stack^top }
                subtract_from_temp_variable = { top = 1 }

                # --- Lomuto partition with random pivot ---
                set_temp_variable = { span = high }
                subtract_from_temp_variable = { span = low }
                set_temp_variable = { pivot_idx = random }       # built-in [0,1) read
                multiply_temp_variable = { pivot_idx = span }
                add_to_temp_variable = { pivot_idx = low }
                # swap items^pivot_idx ↔ items^high
                set_temp_variable = { swap = items^pivot_idx }
                set_variable = { items^pivot_idx = items^high }
                set_variable = { items^high = swap }

                var:items^high = { set_variable = { PREV.pivot_val = [SORTKEY] } }
                set_temp_variable = { store = low }
                for_loop_effect = {
                    start = low
                    end = high
                    value = scan
                    var:items^scan = { set_variable = { PREV.scan_val = [SORTKEY] } }
                    if = {
                        limit = { check_variable = { scan_val < pivot_val } }
                        set_temp_variable = { swap = items^scan }
                        set_variable = { items^scan = items^store }
                        set_variable = { items^store = swap }
                        add_to_temp_variable = { store = 1 }
                    }
                }
                set_temp_variable = { swap = items^store }
                set_variable = { items^store = items^high }
                set_variable = { items^high = swap }
                # --- end partition; pivot is at 'store' ---

                set_temp_variable = { left_high = store }
                subtract_from_temp_variable = { left_high = 1 }
                if = {
                    limit = { check_variable = { left_high > low } }
                    add_to_temp_variable = { top = 1 }
                    set_temp_variable = { stack^top = low }
                    add_to_temp_variable = { top = 1 }
                    set_temp_variable = { stack^top = left_high }
                }
                set_temp_variable = { right_low = store }
                add_to_temp_variable = { right_low = 1 }
                if = {
                    limit = { check_variable = { right_low < high } }
                    add_to_temp_variable = { top = 1 }
                    set_temp_variable = { stack^top = right_low }
                    add_to_temp_variable = { top = 1 }
                    set_temp_variable = { stack^top = high }
                }
            }
        }
        SORTKEY = "[GetSelectedSortColumn]"    # scripted-loc defined_text returning a variable name
    }
}
```

Notes:

- The `while_loop_effect` obeys the 1000-iteration cap; that bounds total partitions, comfortably enough for a few hundred elements.
- The randomized pivot avoids O(n²) blowup on already-sorted input.
- For a fixed sort key, delete the `meta_effect` wrapper and write the variable name directly.

## Performance Summary

- Selection sort / argsort / nested min-find: O(n²) — fine ≤ ~60, noticeable ≥ 100.
- `find_highest_in_array` scans the whole array each call; `remove_from_array` by index shifts the tail.
- Cache sorted results; re-sort only when inputs change, never per-frame in GUI code.
- Sorting parallel arrays: every structural op hits every sibling, same index, same step.
