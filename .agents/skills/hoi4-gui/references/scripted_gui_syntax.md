# Scripted GUI Syntax Reference

## Table of Contents
- [Basic Structure](#basic-structure)
- [Context Types](#context-types)
- [Parent Windows](#parent-windows)
- [Visibility](#visibility)
- [Effects](#effects)
- [Triggers](#triggers)
- [Properties](#properties)
- [Dynamic Lists](#dynamic-lists)
- [AI Configuration](#ai-configuration)
- [Performance](#performance)

## Basic Structure

```
scripted_gui = {
    gui_name = {
        context_type = player_context
        window_name = "container_name"

        visible = { }
        effects = { }
        triggers = { }
        properties = { }
        dynamic_lists = { }
    }
}
```

## Context Types

Determines the scope and attachment point:

- **`player_context`** - Scope: player country. GUI attached to main window.
- **`selected_country_context`** - Scope: target country (right-click on country).
- **`selected_state_context`** - Scope: target state (left-click on state).
- **`diplomacy_target_context`** - Attached to diplomacy window, targets selected country.
- **`decision_category`** - Attached to specific decision category (add `scripted_gui = gui_name` to category). Scope: player.
- **`diplomatic_action`** - Attached to diplomatic action (see scripted diplomatic actions).
- **`country_mapicon`** - Map icon for each country. Scope: the country.
- **`state_mapicon`** - Map icon for each state. Scope: the state.

## Parent Windows

Override default attachment location:

### Using Tokens
```
parent_window_token = top_bar
```

Available tokens:
- `top_bar`, `decision_tab`, `technology_tab`, `trade_tab`, `construction_tab`, `production_tab`, `deployment_tab`, `logistics_tab`, `diplomacy_tab`
- `national_focus`, `politics_tab`
- `selected_country_view`, `selected_state_view`, `selected_country_view_info`, `selected_country_view_diplomacy`
- `army_ledger`, `navy_ledger`, `civilian_ledger`, `air_ledger`
- Tech folder tokens: `tech_infantry_folder`, `tech_support_folder`, `tech_armor_folder`, `tech_artillery_folder`, `tech_land_doctrine_folder`, `tech_naval_folder`, `tech_naval_doctrine_folder`, `tech_air_techs_folder`, `tech_air_doctrine_folder`, `tech_electronics_folder`, `tech_industry_folder`

### Using Container Names
```
parent_window_window = "container_name"
```
Searches all UIs for matching container. May not always work.

### Using Other Scripted GUIs
```
parent_scripted_gui = "other_gui_name"
```

## Visibility

Controls when GUI appears:

```
visible = {
    has_country_flag = system_active
    NOT = { has_variable = gui_closed }
}
```

## Effects

Button click handlers. Supports modifiers: `_click`, `_right_click`, `_alt_click`, `_shift_click`, `_control_click` and combinations like `_alt_right_click`.

```
effects = {
    button_name_click = {
        set_variable = { var_name = 1 }
    }

    button_name_shift_click = {
        clear_variable = var_name
    }

    button_name_alt_right_click = {
        add_to_variable = { var_name = 1 }
    }
}
```

## Triggers

Control element visibility and enabled state:

```
triggers = {
    button_name_click_enabled = {
        has_political_power > 50
    }

    icon_name_visible = {
        has_country_flag = feature_unlocked
    }

    text_element_visible = {
        check_variable = { display_mode = 1 }
    }
}
```

Suffix patterns:
- `_click_enabled` - Button is enabled
- `_visible` - Element is visible

## Properties

Modify visual properties dynamically:

### Image Properties
```
properties = {
    icon_name = {
        image = "[?variable_name.GetTokenKey]"  # Dynamic image from variable
        frame = 1  # Or variable for frame number
    }

    flag_icon = {
        image = "GFX_[?country_var]"
    }
}
```

### Position Properties
```
properties = {
    element_name = {
        x = 100  # Or variable
        y = 200  # Or variable
    }
}
```

## Dynamic Lists

Populate lists from arrays:

```
dynamic_lists = {
    list_name = {
        array = array_name                    # Required: source array
        value = val_name                      # Optional: store current value (default: v)
        index = index_name                    # Optional: store current index (default: i)
        change_scope = yes                    # Optional: change scope to array element

        # Container selection (uses scripted loc)
        entry_container = "container_name"
        country_scope_entry_container = "country_container"
        state_scope_entry_container = "state_container"
    }
}
```

Example:
```
dynamic_lists = {
    member_list = {
        array = ROOT.alliance_members
        change_scope = yes
        entry_container = "member_entry"
    }
}
```

## AI Configuration

Control AI interaction with GUI:

```
# Checked once at game start
ai_enabled = {
    tag = GER  # Only enable for specific tags
}

# Test frequency
ai_test_interval = 24      # Hours between tests
ai_test_variance = 24      # Random variance in hours

# Per-test check
ai_check = {
    has_political_power > 100
}

# For targeted GUIs, which countries/states to test
ai_test_scopes = test_ally_countries

# Per-target check
ai_check_scope = {
    is_neighbor_of = ROOT
}

# AI weights for button clicks
ai_weights = {
    button_name_click = {
        ai_will_do = {
            base = 10
            modifier = {
                factor = 2
                tag = GER
            }
        }
        ignore_lower_weights = yes  # Don't click lower-weighted buttons
    }
}

ai_max_weight_taken_per_test = 100  # Max total weight per test cycle
```

Available `ai_test_scopes`:
- `test_self_country`, `test_enemy_countries`, `test_ally_countries`, `test_neighbouring_countries`
- `test_neighbouring_ally_countries`, `test_neighbouring_enemy_countries`
- `test_self_owned_states`, `test_enemy_owned_states`, `test_ally_owned_states`
- `test_self_controlled_states`, `test_enemy_controlled_states`, `test_ally_controlled_states`
- `test_neighbouring_states`, `test_neighbouring_enemy_states`, `test_neighbouring_ally_states`
- `test_our_neighbouring_states`, `test_our_neighbouring_states_against_allies`, `test_our_neighbouring_states_against_enemies`
- `test_contesded_states`, `test_if_only_major`, `test_if_only_coastal`

## Performance

### Dirty Variable (Update Optimization)
```
dirty = var_name
```
GUI only updates when this variable changes. Use `add_to_variable = { var_name = 1 }` in effects to force update.

### Map Mode Filtering
```
map_mode = map_mode_name
```
Only show GUI in specific map mode.

### Performance Tips
1. Use `dirty` variable for complex GUIs that don't need tick updates
2. Keep `visible` triggers lightweight - they run every frame
3. Use `ai_enabled = { always = no }` for player-only GUIs
4. Avoid expensive triggers in frequently-checked elements
5. Cache results in country flags when possible
