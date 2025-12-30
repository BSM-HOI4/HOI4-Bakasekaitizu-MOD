# HOI4 Variables Complete Guide

## Variable Types

### Country Variables
```
set_variable = { my_var = 10 }
```
Stored in country scope, saved with the game.

### Global Variables
```
set_variable = { global.my_var = 10 }
```
Accessible from any scope, saved globally.

### Temporary Variables
```
set_temp_variable = { temp_var = 10 }
```
Not saved, only exists during current execution.

## Setting Variables

### Direct Assignment
```
set_variable = { var_name = 100 }
set_variable = { var_name = 0.15 }
```

### From Game Values
```
set_variable = { my_ic = industrial_capacity }
set_variable = { my_stability = stability }
set_variable = { my_manpower = manpower }
```

### From Other Variables
```
set_variable = { var_a = var_b }
set_variable = { var_a = PREV.var_b }
```

### Scoped Assignment
```
GER = {
    set_variable = { ROOT.german_ic = industrial_capacity }
}
```

## Modifying Variables

### Arithmetic Operations
```
add_to_variable = { var_name = 5 }
subtract_from_variable = { var_name = 3 }
multiply_variable = { var_name = 2 }
divide_variable = { var_name = 2 }
```

### Variable-to-Variable Operations
```
add_to_variable = { var_a = var_b }
subtract_from_variable = { var_a = var_b }
multiply_variable = { var_a = var_b }
divide_variable = { var_a = var_b }
```

### Temporary Variable Operations
```
set_temp_variable = { temp_a = 100 }
set_temp_variable = { temp_b = 50 }
divide_temp_variable = { temp_a = temp_b }  # temp_a = 2
```

## Clamping

### Basic Clamping
```
clamp_variable = {
    var = var_name
    min = 0
    max = 100
}
```

### Temporary Variable Clamping
```
clamp_temp_variable = {
    var = temp_var
    min = 0
    max = 1
}
```

## Checking Variables (Triggers)

### Comparisons
```
check_variable = { var_name > 10 }
check_variable = { var_name < 5 }
check_variable = { var_name = 10 }
check_variable = { var_name >= 10 }
check_variable = { var_name <= 10 }
check_variable = { var_name != 10 }
```

### Variable Comparisons
```
check_variable = { var_a > var_b }
check_variable = { var_a = var_b }
```

### Existence Check
```
has_variable = var_name
```

## Clearing Variables

```
clear_variable = var_name
```

## Localization

### Display in Tooltips
```yaml
my_tooltip:0 "Current value: [?var_name]"
percentage_tooltip:0 "Bonus: [?var_name|%]%"
```

### Format as Percentage
```yaml
modifier_desc:0 "工業力ボーナス: [?industrial_bonus|%]%"
```

## Real-World Example (SSW Mod)

```
# Version tracking system
set_temp_variable = { update_num = 3 }
set_temp_variable = { update_date = 61509.275 }
set_temp_variable = { update_ver_o1 = 1 }   # Major version
set_temp_variable = { update_ver_o2 = 2 }   # Minor version
set_temp_variable = { update_ver_o3 = 0 }   # Patch version

# UI state management
every_country = {
    limit = { is_ai = no }
    set_country_flag = { flag = sde_window value = 2 }
    set_variable = { bol_select_page = 0 }
    set_variable = { update_detail = global.update_log_list^0 }
}
```

## Best Practices

1. **Use temp variables for calculations** - Don't save unnecessary data
2. **Use global variables for cross-country data** - Faction systems, world events
3. **Name variables clearly** - `industrial_bonus` not `ib`
4. **Clamp when necessary** - Prevent values from going out of range
5. **Clear when done** - Free up memory for unused variables
