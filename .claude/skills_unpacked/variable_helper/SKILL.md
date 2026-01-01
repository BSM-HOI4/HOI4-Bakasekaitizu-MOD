---
name: hoi4-variable-helper
description: Comprehensive guide for HOI4 variables, arrays, collections, and script constants. Use when the user (1) Needs to manage variables or temporary values, (2) Wants to work with arrays/lists, (3) Asks about collections or filtering objects, (4) Needs to define reusable constants, or (5) Says phrases like "how to use variables", "create array", "define collection", "set up constants", etc. Covers all data management systems in HOI4 scripting.
---

# HOI4 Variable Helper

## Overview

Comprehensive guide for managing data in HOI4 scripting: Variables (single values), Arrays (lists), Collections (filtered object groups), MTTH Variables (dynamic calculated values), and Script Constants (reusable definitions). Provides syntax, examples, and best practices for all data management systems.

## When This Skill Triggers

This skill activates when:
- User needs to store or manipulate values (variables)
- User wants to manage lists of countries/states/etc (arrays)
- User needs to filter and group game objects (collections)
- User wants to define reusable constants across scripts
- User needs dynamic calculated values (MTTH variables)
- User says: "how to use variables", "create array", "loop through countries", "define constants", "mtth variables"

## Quick Reference

### Variables
```
set_variable = { var_name = 10 }
add_to_variable = { var_name = 5 }
check_variable = { var_name > 15 }
```

### Arrays
```
add_to_array = { my_array = GER }
remove_from_array = { my_array = GER }
is_in_array = { my_array = GER }
for_each_loop = { array = my_array ... }
```

### Collections
```
collection:my_collection
game:all_countries
country:faction_members
```

### Script Constants
```
constant:category.key
```

### MTTH Variables
```
mtth:variable_name
```

---

## Part 1: Variables

Variables store single numeric values that can be modified and checked.

### Variable Types

**Country Variables:**
```
set_variable = { industrial_bonus = 0.15 }
```

**Global Variables:**
```
set_variable = { global.world_tension_modifier = 0.10 }
```

**Temporary Variables (not saved):**
```
set_temp_variable = { temp_calc = 100 }
```

### Setting Variables

**Basic assignment:**
```
set_variable = { var_name = 10 }
set_variable = { var_name = 0.15 }  # Decimal
```

**From game values:**
```
set_variable = { my_ic = industrial_capacity }
set_variable = { my_stability = stability }
```

**Copy from another variable:**
```
set_variable = { var_a = var_b }
```

**From scoped variable:**
```
GER = {
    set_variable = { ROOT.german_ic = industrial_capacity }
}
```

### Modifying Variables

**Add:**
```
add_to_variable = { var_name = 5 }
```

**Subtract:**
```
subtract_from_variable = { var_name = 3 }
```

**Multiply:**
```
multiply_variable = { var_name = 2 }
```

**Divide:**
```
divide_variable = { var_name = 2 }
```

**Divide by another variable:**
```
divide_variable = { var_a = var_b }
```

**Temporary variable division:**
```
divide_temp_variable = { my_share = PREV.total_ic }
```

### Clamping Values

**Limit min/max:**
```
clamp_variable = {
    var = var_name
    min = 0
    max = 100
}
```

**Temporary variable:**
```
clamp_temp_variable = {
    var = temp_var
    min = 0
    max = 0.05
}
```

### Checking Variables (Triggers)

**Compare with number:**
```
check_variable = { var_name > 10 }
check_variable = { var_name < 5 }
check_variable = { var_name = 10 }
check_variable = { var_name >= 10 }
check_variable = { var_name <= 10 }
```

**Compare with another variable:**
```
check_variable = { var_a > var_b }
```

**Check if exists:**
```
has_variable = var_name
```

### Clearing Variables

```
clear_variable = var_name
```

### Using Variables in Localization

```yaml
modifier_desc:0 "工業力ボーナス: [?industrial_bonus]%"
```

### Real Example from SSW Mod

```
# Version tracking
set_temp_variable = { update_num = 3 }
set_temp_variable = { update_date = 61509.275 }
set_temp_variable = { update_ver_o1 = 1 }   # Major version
set_temp_variable = { update_ver_o2 = 2 }   # Minor version
set_temp_variable = { update_ver_o3 = 0 }   # Patch version

# Page selection
every_country = {
    set_variable = { bol_select_page = 0 }
    set_variable = { update_detail = global.update_log_list^0 }
}
```

---

## Part 2: Arrays

Arrays store lists of values (countries, states, numbers, tokens).

### Creating Arrays

**Initialize empty:**
```
clear_array = my_array
```

**Add elements:**
```
add_to_array = { my_array = GER }
add_to_array = { my_array = USA }
add_to_array = { my_array = 10 }
```

### Array Operations

**Add element:**
```
add_to_array = { array = my_array value = GER }
# Or shorthand:
add_to_array = { my_array = GER }
```

**Add at specific index:**
```
add_to_array = { array = my_array value = GER index = 0 }
```

**Remove element:**
```
remove_from_array = { array = my_array value = GER }
# Or shorthand:
remove_from_array = { my_array = GER }
```

**Check if element exists:**
```
is_in_array = { array = my_array value = GER }
# Or shorthand:
is_in_array = { my_array = GER }
```

**Clear all:**
```
clear_array = my_array
```

**Get size:**
```
# In trigger or effect:
check_variable = { my_array^num > 0 }
# ^num gives array size
```

**Access specific index:**
```
# Access first element:
my_array^0
# Access second element:
my_array^1
```

### Special Array Operations

**Find highest value:**
```
find_highest_in_array = {
    array = global.update_log_list
    value = first_page
}
```

**Find lowest value:**
```
find_lowest_in_array = {
    array = score_array
    value = lowest_score
}
```

### Looping Through Arrays

**Basic loop (for_each_loop):**
```
for_each_loop = {
    array = my_array
    value = v_current

    # Use var:v_current to reference element
    var:v_current = {
        # Effects on the element
        add_stability = 0.05
    }
}
```

**Index-based loop (for_loop_effect):**
```
for_loop_effect = {
    start = 0
    end = global.function_amount
    value = function_id

    add_to_array = { global.function_list = function_id }
}
```

**Loop with index tracking:**
```
for_each_loop = {
    array = my_array
    value = v_element
    index = v_index

    # var:v_index contains current index (0-based)
    # var:v_element contains current element
}
```

**Break from loop:**
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

### Global Arrays

**Define:**
```
add_to_array = { global.sphere_list = USA_SPHERE }
```

**Access:**
```
for_each_loop = {
    array = global.sphere_list
    value = v_sphere
    # ...
}
```

### Dynamic Array Names

Using tokens/variables in array names:

```
# Create array with dynamic name
clear_array = global.member_list_@var:sphere_token
add_to_array = {
    global.member_list_@var:sphere_token = THIS
}

# Access later
for_each_loop = {
    array = global.member_list_@var:sphere_token
    value = v_member
    # ...
}
```

### Real Example from SSW Mod

```
# Initialize page list
clear_array = global.sde_page_list
for_loop_effect = {
    start = 0
    end = 6
    value = page_id
    add_to_array = { global.sde_page_list = page_id }
}

# Create path guide list
clear_array = global.path_guide_list
add_to_array = { global.path_guide_list = BUL }
add_to_array = { global.path_guide_list = GRE }
add_to_array = { global.path_guide_list = JAP }
add_to_array = { global.path_guide_list = GER }
add_to_array = { global.path_guide_list = ENG }
# ... more countries

# Find latest update
find_highest_in_array = {
    array = global.update_log_list
    value = first_page
}

# Store in variable
every_country = {
    set_variable = { update_detail = global.update_log_list^0 }
    clear_array = bol_select_subpage_5
    add_to_array = { bol_select_subpage_5 = first_page }
}

# Create function list using loop
clear_array = global.function_list
for_loop_effect = {
    start = 0
    end = global.function_amount
    value = function_id
    add_to_array = { global.function_list = function_id }
}
```

---

## Part 3: Collections

Collections are filtered groups of game objects (countries, states, etc).

### Built-In Collections

**Game scope:**
```
game:empty                   # Empty collection
game:all_countries           # All existing countries
game:all_possible_countries  # All possible countries
game:all_states              # All states
game:scope                   # Current scope as collection
```

**Country scope:**
```
country:faction_members      # All faction members
```

### Using Collections

**In effects:**
```
every_collection_element = {
    collection = game:all_countries
    # Effects on each country
    add_stability = 0.05
}
```

**Check size:**
```
collection_size = {
    collection = game:all_countries
    value > 10
}
```

### Defining Custom Collections

**File:** `common/collections/my_collections.txt`

**Basic structure:**
```
my_collection_name = {
    input = game:all_countries  # Source collection

    operators = {
        limit = {
            # Filter criteria
            # SCOPE = element from input
            # PREV = previous scope
            # ROOT = PREV.ROOT
            # FROM = PREV.FROM

            is_major = yes
        }
    }

    name = COLLECTION_MY_COLLECTION  # Localization key (optional)
}
```

### Collection Operators

**Filtering:**
```
operators = {
    limit = {
        # Filter condition
    }
}
```

**Chaining operators:**
```
operators = {
    faction_members      # Get faction members
    controlled_states    # Then get their controlled states
    limit = {
        is_core_of = PREV
    }
}
```

### Real Examples from SSW Mod

**Simple filter:**
```
world_at_peace_countries = {
    input = game:all_countries
    operators = {
        limit = {
            has_war = no
        }
    }
    name = COLLECTION_COUNTRIES_AT_PEACE
}
```

**Chained operators:**
```
faction_owned_core_states = {
    input = game:scope
    operators = {
        faction_members     # Get all faction members
        owned_states        # Get their owned states
        limit = {
            is_core_of = PREV  # Only core states
        }
    }
    name = COLLECTION_FACTION_OWNED_CORE_STATES
}
```

**Nested collections:**
```
world_uncapitulated_democratic_countries = {
    input = collection:world_democratic_countries
    operators = {
        limit = {
            has_capitulated = no
        }
    }
    name = COLLECTION_UNCAPITULATED_DEMOCRATIC_COUNTRIES
}
```

**Regional filtering:**
```
states_in_africa = {
    input = game:all_states
    operators = {
        limit = {
            is_on_continent = africa
        }
    }
    name = COLLECTION_STATES_IN_AFRICA
}

faction_states_in_africa = {
    input = game:scope
    operators = {
        faction_members
        controlled_states
        limit = {
            is_on_continent = africa
        }
    }
    name = COLLECTION_FACTION_CONTROLLED_STATES_IN_AFRICA
}
```

**Using script constants:**
```
controllable_balkan_states = {
    input = constant:state_groups.balkans
    name = COLLECTION_FACTION_BALKAN_STATES
}

faction_controlled_balkan_states = {
    input = constant:state_groups.balkans
    operators = {
        limit = {
            is_controlled_by_ROOT_or_ally = yes
        }
    }
    name = COLLECTION_FACTION_CONTROLLED_BALKAN_STATES
}
```

**Complex faction logic:**
```
democratic_faction_members = {
    input = game:scope
    operators = {
        faction_members
        limit = {
            has_democratic_government = yes
        }
    }
    name = COLLECTION_DEMOCRATIC_FACTION_MEMBERS
}

islamic_faction_members = {
    input = constant:country_groups.islamic_world
    operators = {
        limit = {
            OR = {
                tag = ROOT
                is_in_faction_with = ROOT
            }
        }
    }
    name = COLLECTION_ISLAMIC_FACTION_MEMBERS
}
```

**Continental checks:**
```
states_on_my_continent = {
    input = game:all_states
    operators = {
        limit = {
            is_on_same_continent_as = ROOT
        }
    }
    name = COLLECTION_STATES_MY_CONTINENT
}

non_fascist_controlled_states_on_my_continent = {
    input = collection:states_on_my_continent
    operators = {
        limit = {
            controller = { NOT = { has_dictatorship_government = yes } }
        }
    }
    name = COLLECTION_NON_FASCIST_STATES_MY_CONTINENT
}
```

### Usage Examples

```
# Count states in collection
if = {
    limit = {
        collection_size = {
            collection = collection:faction_states_in_africa
            value > 20
        }
    }
    # Unlock achievement
}

# Process all elements
every_collection_element = {
    collection = collection:world_at_peace_countries
    add_stability = 0.05
}

# Use in triggers
if = {
    limit = {
        collection_size = {
            collection = collection:democratic_faction_members
            value > 5
        }
    }
    # Large democratic faction
}
```

---

## Part 4: MTTH Variables

MTTH (Mean Time To Happen) variables are dynamic calculated values that can reference other variables and use modifiers. They are defined in `common/mtth/` and can be used in scripted effects, scripted GUIs, and other contexts.

### What Are MTTH Variables

MTTH variables are calculated values with a base and modifiers that can:
- Reference other variables dynamically
- Use check_variable conditions
- Chain calculations (reference other MTTH variables)
- Update dynamically based on game state

### File Structure

**File:** `common/mtth/my_mtth_variables.txt`

**Basic structure:**
```
variable_name = {
    base = <number>

    modifier = {
        # Conditions (optional)
        check_variable = { ... }

        # Effect on value
        add = <number or variable>
        factor = <number>
    }
}
```

### Defining MTTH Variables

#### Simple MTTH Variable

```
iron_int_var = {
    base = 0
    modifier = {
        add = noOfConversion^i
        check_variable = {
            var = noOfConversion^i
            value = resource@iron
            compare = less_than
        }
    }
    modifier = {
        add = this.resource@iron
        check_variable = {
            var = this.noOfConversion^i
            value = this.resource@iron
            compare = greater_than_or_equals
        }
    }
}
```

**Behavior:**
- `base = 0` - Starting value
- First modifier: Add `noOfConversion^i` if it's less than `resource@iron`
- Second modifier: Add `this.resource@iron` if `noOfConversion^i` >= `resource@iron`

#### Chaining MTTH Variables

```
steel_int_var = {
    base = 0
    modifier = {
        add = mtth:iron_int_var
    }
    modifier = {
        factor = 2
    }
}
```

**Behavior:**
- Starts at 0
- Adds the calculated value of `iron_int_var`
- Multiplies by 2
- Result: `steel_int_var = (iron_int_var) × 2`

#### Conditional Factors

```
button_onoff1 = {
    base = 1
    modifier = {
        check_variable = {
            var = noOfConversion^i
            compare = greater_than_or_equals
            value = 1
        }
        check_variable = {
            var = conversion_x5_array^i
            compare = not_equals
            value = 2
        }
        check_variable = {
            var = conversion_x10_array^i
            compare = not_equals
            value = 2
        }
        factor = 2
    }
    modifier = {
        check_variable = {
            var = noOfConversion^i
            compare = greater_than_or_equals
            value = 1
        }
        check_variable = {
            var = conversion_x5_array^i
            compare = equals
            value = 2
        }
        factor = 3
    }
}
```

**Behavior:**
- Base value: 1
- If conditions 1 match: multiply by 2 (result = 2)
- If conditions 2 match: multiply by 3 (result = 3)
- Multiple modifiers with `factor` multiply the result

### MTTH Modifier Properties

#### add

Adds a value to the result:
```
modifier = {
    add = 10
}

modifier = {
    add = my_variable
}

modifier = {
    add = mtth:other_mtth_var
}
```

#### factor

Multiplies the result:
```
modifier = {
    factor = 2
}

modifier = {
    factor = 0.5  # Divides by 2
}
```

#### check_variable (condition)

Conditions for when the modifier applies:
```
modifier = {
    check_variable = {
        var = my_var
        value = 10
        compare = greater_than
    }
    add = 5
}
```

**Compare operators:**
- `greater_than` or `>`
- `less_than` or `<`
- `greater_than_or_equals` or `>=`
- `less_than_or_equals` or `<=`
- `equals` or `=`
- `not_equals` or `!=`

### Using MTTH Variables

**Reference syntax:**
```
mtth:variable_name
```

**In scripted effects:**
```
set_variable = {
    calculated_value = mtth:iron_int_var
}
```

**In scripted GUIs:**
```
visible = {
    check_variable = {
        var = mtth:button_onoff1
        value = 2
        compare = greater_than_or_equals
    }
}
```

**In dynamic modifiers:**
```
modifier = {
    factory_output = mtth:production_bonus
}
```

### Real Example from Day-of-Wrath Mod

**Resource calculation:**
```
iron_int_var = {
    base = 0
    modifier = {
        add = noOfConversion^i
        check_variable = {
            var = noOfConversion^i
            value = resource@iron
            compare = less_than
        }
    }
    modifier = {
        add = this.resource@iron
        check_variable = {
            var = this.noOfConversion^i
            value = this.resource@iron
            compare = greater_than_or_equals
        }
    }
}
```

**Chained calculation:**
```
steel_int_var = {
    base = 0
    modifier = {
        add = mtth:iron_int_var
    }
    modifier = {
        factor = 2
    }
}
```

**UI button state:**
```
button_onoff1 = {
    base = 1
    modifier = {
        check_variable = {
            var = noOfConversion^i
            compare = greater_than_or_equals
            value = 1
        }
        check_variable = {
            var = conversion_x5_array^i
            compare = not_equals
            value = 2
        }
        factor = 2
    }
    modifier = {
        check_variable = {
            var = noOfConversion^i
            compare = greater_than_or_equals
            value = 1
        }
        check_variable = {
            var = conversion_x5_array^i
            compare = equals
            value = 2
        }
        factor = 3
    }
}
```

### Use Cases

**1. Dynamic Calculations:**
```
production_efficiency = {
    base = 1.0
    modifier = {
        check_variable = { stability > 0.5 }
        add = 0.1
    }
    modifier = {
        check_variable = { war_support > 0.7 }
        factor = 1.2
    }
}
```

**2. Conditional UI States:**
```
button_enabled = {
    base = 0
    modifier = {
        check_variable = { political_power >= 50 }
        add = 1
    }
}
```

**3. Resource Conversion:**
```
converted_resources = {
    base = 0
    modifier = {
        add = input_resources
        check_variable = { conversion_active = 1 }
    }
    modifier = {
        factor = conversion_rate
    }
}
```

**4. Tiered Bonuses:**
```
research_bonus = {
    base = 1.0
    modifier = {
        check_variable = { research_facilities > 5 }
        factor = 1.1
    }
    modifier = {
        check_variable = { research_facilities > 10 }
        factor = 1.2
    }
    modifier = {
        check_variable = { research_facilities > 20 }
        factor = 1.5
    }
}
```

### Best Practices

1. **Clear Naming:** Use descriptive names that indicate what is calculated
   ```
   production_efficiency_bonus = { ... }
   ```

2. **Base Value:** Always define a base value
   ```
   base = 0  # or 1.0 for multiplicative bonuses
   ```

3. **Order Matters:** Modifiers apply in order
   ```
   # First adds, then multiplies
   modifier = { add = 10 }
   modifier = { factor = 2 }
   # Result: (base + 10) × 2
   ```

4. **Use for Complex Calculations:** MTTH variables are ideal for calculations that depend on multiple conditions
   ```
   complex_bonus = {
       base = 1.0
       modifier = { ... }
       modifier = { ... }
       modifier = { ... }
   }
   ```

5. **Chain When Needed:** Reference other MTTH variables for modular calculations
   ```
   total_bonus = {
       base = 0
       modifier = { add = mtth:bonus_a }
       modifier = { add = mtth:bonus_b }
   }
   ```

### Performance Considerations

- ✅ MTTH variables are calculated on-demand
- ⚠️ Complex MTTH variables with many modifiers can be expensive
- ⚠️ Avoid circular references (A references B, B references A)
- ✅ Use in scripted GUIs for dynamic UI updates
- ✅ Cache results in regular variables if value doesn't change often

---

## Part 5: Script Constants

Reusable constant definitions for scripts.

### What Are Script Constants

Script constants define reusable values (numbers, complex structures, arrays) that can be referenced across all scripts. Defined in `common/script_constants/`.

### Defining Script Constants

**File:** `common/script_constants/my_constants.txt`

**Basic structure:**
```
category_name = {
    # Schema defines the structure
    schema = {
        any_key = yes        # Accept any key name
        data = int           # Data type: int, fixed_point, array, or complex
    }

    # Constant definitions
    key1 = value1
    key2 = value2
}
```

### Simple Constants

**Integer constants:**
```
research_times = {
    schema = {
        any_key = yes
        data = int
    }

    short = 15
    medium = 30
    long = 60
    very_long = 90
}
```

**Decimal constants:**
```
modifier_values = {
    schema = {
        any_key = yes
        data = fixed_point
    }

    small = 0.05
    medium = 0.10
    large = 0.15
}
```

### Array Constants

**Country groups:**
```
country_groups = {
    schema = {
        any_key = yes
        array = country
    }

    nordics = {
        SWE
        NOR
        FIN
        DEN
        ICE
    }

    axis_core = {
        GER
        ITA
        JAP
    }
}
```

**State groups:**
```
state_groups = {
    schema = {
        any_key = yes
        array = state
    }

    balkans = {
        106  # Macedonia
        107  # Thrace
        184  # Albania
        # ... more states
    }
}
```

### Complex Constants

**Structured data:**
```
special_project_complexity = {
    schema = {
        any_key = yes
        data = {
            {
                key = min
                data = int
            }
            {
                key = max
                data = int
            }
        }
    }

    small = {
        min = 20
        max = 30
    }

    medium = {
        min = 15
        max = 20
    }
}
```

### Real Example from SSW Mod

```
sde_page = {
    schema = {
        any_key = yes
        data = int
    }
}
```

### Using Script Constants

**Reference syntax:**
```
constant:category.key
```

**In collections:**
```
controllable_balkan_states = {
    input = constant:state_groups.balkans
    name = COLLECTION_FACTION_BALKAN_STATES
}

all_islamic_countries = {
    input = constant:country_groups.islamic_world
    name = COLLECTION_FACTION_ISLAMIC_COUNTRIES
}
```

**In effects:**
```
# Use research time constant
add_timed_idea = {
    idea = economic_boom
    days = constant:research_times.medium  # 30 days
}

# Use modifier value constant
modifier = {
    stability_factor = constant:modifier_values.medium  # 0.10
}
```

**In triggers:**
```
# Check against constant
if = {
    limit = {
        num_of_factories > constant:production_thresholds.major_power
    }
    # Is major industrial power
}
```

---

## Common Patterns and Best Practices

### Pattern 1: Counter System

```
# Initialize counter
set_variable = { kill_count = 0 }

# Increment on event
on_enemy_unit_destroyed = {
    add_to_variable = { kill_count = 1 }
}

# Check milestone
if = {
    limit = { check_variable = { kill_count > 100 } }
    # Unlock achievement
}
```

### Pattern 2: Dynamic List Management

```
# Create country list
clear_array = global.path_guide_list
add_to_array = { global.path_guide_list = BUL }
add_to_array = { global.path_guide_list = GRE }
add_to_array = { global.path_guide_list = JAP }

# Check if country has guide
if = {
    limit = {
        is_in_array = { global.path_guide_list = THIS }
    }
    # Show path guide
}

# Loop through all
for_each_loop = {
    array = global.path_guide_list
    value = v_country
    var:v_country = {
        # Process each country
    }
}
```

### Pattern 3: Index-Based Generation

```
# Create numbered list
clear_array = global.function_list
for_loop_effect = {
    start = 0
    end = global.function_amount
    value = function_id
    add_to_array = { global.function_list = function_id }
}
```

### Pattern 4: Version Tracking

```
set_temp_variable = { update_num = 3 }
set_temp_variable = { update_date = 61509.275 }
set_temp_variable = { update_ver_o1 = 1 }   # Major
set_temp_variable = { update_ver_o2 = 2 }   # Minor
set_temp_variable = { update_ver_o3 = 0 }   # Patch
```

### Pattern 5: Collection Chaining

```
# Start with all countries
input = game:all_countries

# Filter to continent
operators = {
    limit = { is_on_same_continent_as = ROOT }
}

# Then use in another collection
non_fascist_my_continent = {
    input = collection:countries_my_continent
    operators = {
        limit = { NOT = { has_dictatorship_government = yes } }
    }
}
```

### Pattern 6: Constant-Based Collections

```
# Define state group constant
state_groups = {
    schema = { any_key = yes array = state }
    mare_nostrum_states = { 117 118 162 ... }
}

# Use in collection
controllable_mare_nostrum_states = {
    input = constant:state_groups.mare_nostrum_states
    name = COLLECTION_FACTION_MARE_NOSTRUM_STATES
}

# Filter controlled ones
faction_controlled_mare_nostrum_states = {
    input = constant:state_groups.mare_nostrum_states
    operators = {
        limit = { is_controlled_by_ROOT_or_ally = yes }
    }
}
```

---

## Performance Considerations

### Variables
- ✅ Variables are fast and efficient
- ✅ Use temp variables for calculations that don't need saving
- ⚠️ Global variables persist across saves
- ⚠️ Clear unused variables to save memory

### Arrays
- ✅ Arrays are efficient for moderate sizes (<100 elements)
- ⚠️ Avoid massive arrays (>1000 elements)
- ⚠️ for_each_loop on large arrays can be slow
- ✅ Use is_in_array for membership checks instead of looping
- ✅ find_highest_in_array / find_lowest_in_array are optimized

### Collections
- ✅ Collections are evaluated on-demand (lazy)
- ✅ Use collections instead of every_country when filtering
- ⚠️ Complex limit triggers can be expensive
- ✅ Reuse named collections instead of anonymous ones
- ✅ Chain collections to build on previous filters

### MTTH Variables
- ✅ MTTH variables are calculated on-demand
- ⚠️ Complex MTTH variables with many modifiers can be expensive
- ⚠️ Avoid circular references
- ✅ Use in scripted GUIs for dynamic UI updates
- ✅ Cache results in regular variables if value doesn't change often

### Script Constants
- ✅ Constants have zero runtime cost
- ✅ Use constants for magic numbers
- ✅ Makes balancing easier (central values)
- ✅ Great for state/country groups

---

## Debugging Tips

### Print Variable Values

```
log = "Variable value: [This.var_name]"
```

### Check Array Contents

```
log = "Array size: [This.my_array^num]"
log = "First element: [This.my_array^0]"
```

### Test Collection Filters

```
# Log collection size
if = {
    limit = {
        collection_size = {
            collection = collection:my_collection
            value > 0
        }
    }
    log = "Collection has elements"
}
```

### Verify Constants

```
# Constants are compile-time, check in collection definitions
controllable_states = {
    input = constant:state_groups.my_states
    # Will error if constant doesn't exist
}
```

---

## Reference Documentation

For detailed syntax and examples:
- `references/variables_guide.md` - Complete variable operations
- `references/arrays_guide.md` - Array manipulation and loops
- `references/collections_guide.md` - Collection creation and usage
- `references/constants_guide.md` - Script constants schema

For real-world examples:
- SSW mod: `/Users/eightman/Desktop/HOI4_modding/SSW_mod/common/`
- Vanilla collections: `/Users/eightman/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/common/collections/`
- Vanilla constants: `/Users/eightman/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/common/script_constants/`

---

## Integration with Other Skills

### With hoi4-scripted-effect-maker
Use variables and arrays in scripted effects for complex state management.

### With hoi4-modifier-maker
Use script constants for modifier values to maintain consistent balance.

### With hoi4-idea-creator
Store idea state in variables, manage idea lists in arrays.

### With hoi4-nf-creator
Use collections to check faction/alliance requirements dynamically.

---

## Quick Decision Tree

**Need to store a single number?** → Use **Variable**

**Need to store a list of items?** → Use **Array**

**Need to filter game objects?** → Use **Collection**

**Need reusable predefined values?** → Use **Script Constants**

**Need dynamic calculated values with conditions?** → Use **MTTH Variables**

**Need to loop with indices?** → Use **for_loop_effect**

**Need to loop through existing array?** → Use **for_each_loop**

**Need to find max/min in array?** → Use **find_highest_in_array** / **find_lowest_in_array**
