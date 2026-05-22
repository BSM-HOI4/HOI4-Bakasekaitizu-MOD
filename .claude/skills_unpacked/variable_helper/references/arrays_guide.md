# HOI4 Arrays Complete Guide

## Array Basics

Arrays store lists of values: countries, states, numbers, or tokens.

## Creating and Initializing

### Clear Array
```
clear_array = my_array
clear_array = global.my_array
```

### Add Elements
```
add_to_array = { my_array = GER }
add_to_array = { my_array = 100 }
add_to_array = { my_array = var:my_token }
```

### Add at Specific Index
```
add_to_array = { array = my_array value = GER index = 0 }  # Add at beginning
add_to_array = { array = my_array value = USA index = 2 }  # Add at index 2
```

## Array Operations

### Add Element
```
add_to_array = { array = my_array value = GER }
# Shorthand:
add_to_array = { my_array = GER }
```

### Remove Element
```
remove_from_array = { array = my_array value = GER }
# Shorthand:
remove_from_array = { my_array = GER }
```

### Check Membership
```
is_in_array = { array = my_array value = GER }
# Shorthand:
is_in_array = { my_array = GER }
```

### Get Size
```
check_variable = { my_array^num > 0 }
# ^num returns the number of elements
```

### Access by Index
```
my_array^0  # First element
my_array^1  # Second element
my_array^2  # Third element
```

## Special Operations

### Find Highest Value
```
find_highest_in_array = {
    array = score_array
    value = highest_score
}
# Sets highest_score to the maximum value in array
```

### Find Lowest Value
```
find_lowest_in_array = {
    array = score_array
    value = lowest_score
}
# Sets lowest_score to the minimum value in array
```

## Looping

### for_each_loop (Iterate Existing Array)
```
for_each_loop = {
    array = my_array
    value = v_current

    var:v_current = {
        # v_current is the current element
        add_stability = 0.05
    }
}
```

### With Index
```
for_each_loop = {
    array = my_array
    value = v_element
    index = v_index

    # v_index = current index (0, 1, 2, ...)
    # v_element = current element
}
```

### for_loop_effect (Generate Range)
```
for_loop_effect = {
    start = 0
    end = 10
    value = loop_var

    # loop_var goes from 0 to 9
    add_to_array = { my_array = loop_var }
}
```

### Break from Loop
```
for_each_loop = {
    array = my_array
    value = v_current

    if = {
        limit = { var:v_current = { is_ai = yes } }
        break = yes
    }
}
```

## Global Arrays

### Define
```
clear_array = global.world_factions
add_to_array = { global.world_factions = ALLIES }
add_to_array = { global.world_factions = AXIS }
```

### Access
```
for_each_loop = {
    array = global.world_factions
    value = v_faction
    # Process each faction
}
```

## Dynamic Array Names

### Using Tokens
```
# Create array with dynamic name
set_temp_variable = { sphere_id = USA_SPHERE }
clear_array = global.members_@var:sphere_id

# Add to it
add_to_array = {
    global.members_@var:sphere_id = ENG
}

# Access later
for_each_loop = {
    array = global.members_@var:sphere_id
    value = v_member
    # ...
}
```

## Real-World Examples (SSW Mod)

### Creating Numbered List
```
clear_array = global.sde_page_list
for_loop_effect = {
    start = 0
    end = 6
    value = page_id
    add_to_array = { global.sde_page_list = page_id }
}
# Creates array: [0, 1, 2, 3, 4, 5]
```

### Building Country List
```
clear_array = global.path_guide_list
add_to_array = { global.path_guide_list = BUL }
add_to_array = { global.path_guide_list = GRE }
add_to_array = { global.path_guide_list = JAP }
add_to_array = { global.path_guide_list = GER }
add_to_array = { global.path_guide_list = ENG }
```

### Function List Generation
```
clear_array = global.function_list
for_loop_effect = {
    start = 0
    end = global.function_amount
    value = function_id
    add_to_array = { global.function_list = function_id }
}
```

### Finding Latest Version
```
find_highest_in_array = {
    array = global.update_log_list
    value = first_page
}

every_country = {
    set_variable = { update_detail = global.update_log_list^0 }
    clear_array = bol_select_subpage_5
    add_to_array = { bol_select_subpage_5 = first_page }
}
```

## Best Practices

1. **Clear before use** - Always initialize with clear_array
2. **Check membership** - Use is_in_array instead of looping
3. **Use find_highest/lowest** - More efficient than manual loops
4. **Limit array size** - Keep under 100 elements when possible
5. **Use global for shared data** - Cross-country lists
6. **Access by index** - Use ^0, ^1, ^2 for specific elements
7. **Break early** - Exit loops when condition is met

## Common Patterns

### Membership Tracking
```
# Add member
add_to_array = { faction_members = THIS }

# Check member
if = {
    limit = { is_in_array = { faction_members = THIS } }
    # Is member
}

# Remove member
remove_from_array = { faction_members = THIS }
```

### Ranking System
```
# Store scores
add_to_array = { score_array = 100 }
add_to_array = { score_array = 85 }
add_to_array = { score_array = 120 }

# Find winner
find_highest_in_array = {
    array = score_array
    value = winning_score
}
```

### Index-Based Processing
```
for_loop_effect = {
    start = 0
    end = my_array^num
    value = idx

    # Process my_array^idx
}
```
