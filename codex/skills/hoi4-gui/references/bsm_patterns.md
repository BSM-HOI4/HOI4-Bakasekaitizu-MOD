# BSM GUI Patterns and Best Practices

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Common Patterns](#common-patterns)
- [Toggle Patterns](#toggle-patterns)
- [Selection Patterns](#selection-patterns)
- [Dynamic Lists](#dynamic-lists)
- [Info Displays](#info-displays)
- [Multi-Page GUIs](#multi-page-guis)
- [Integration](#integration)

## Naming Conventions

### File Naming
- **System GUIs**: Prefix with `_bsm_` for core systems (e.g., `_bsm_Harvest_System.txt`, `_bsm_mine_dev_GUI.txt`)
- **Feature GUIs**: Prefix with `bsm_` for specific features (e.g., `bsm_economic_alliance_sgui.txt`, `bsm_anomaly.txt`)
- **Country-specific**: Use country tag (e.g., `USA_congress_scripted_gui.txt`)

### GUI Element Naming
- **Containers**: `bsm_system_name` (e.g., `bsm_topbar`, `bsm_Harvest_System_GUI`)
- **Buttons**: `action_description_button` (e.g., `open_button`, `close_button`, `member_select_button`)
- **Icons**: `descriptor_icon` or `descriptor` (e.g., `po`, `cd`, `ec` for topbar resources)
- **Text**: Use uppercase for dynamic values (e.g., `COUNTRY_PO`, `COUNTRY_CD`)

### Variable Naming
- **Page variables**: `system_page` (e.g., `OE_page`, `bsm_anomaly_tab`)
- **Selection variables**: `selected_entity` (e.g., `selected_policy_button_diplomancy`, `ptsd_select_economic_sphere`)
- **State flags**: `system_state_flag` (e.g., `you_are_harvester`, `ptsd_already_opened`)

## Common Patterns

### Basic Button Click
```
scripted_gui = {
    bsm_simple_gui = {
        context_type = player_context
        window_name = "bsm_simple_gui"

        visible = {
            has_country_flag = feature_enabled
        }

        effects = {
            action_button_click = {
                # Perform action
                add_political_power = 50
                set_country_flag = action_taken
            }
        }
    }
}
```

## Toggle Patterns

### Simple Toggle (Variable)
```
effects = {
    toggle_button_click = {
        if = {
            limit = { has_variable = gui_open }
            clear_variable = gui_open
        }
        else = {
            set_variable = { gui_open = 1 }
        }
    }
}
```

### Page Toggle (Multi-Value)
```
effects = {
    page_button_click = {
        if = {
            limit = { has_variable = page_num }
            clear_variable = page_num
        }
        else = {
            set_variable = { page_num = 1 }
        }
    }
}
```

## Selection Patterns

### Select from List with Highlight
```
effects = {
    item_select_button_click = {
        # Clear previous selection if clicking same item
        if = {
            limit = {
                check_variable = { selected_item = FROM.item_id }
            }
            clear_variable = selected_item
        }
        else = {
            # Set new selection
            set_variable = { selected_item = FROM.item_id }

            # Optional: Store reference
            set_temp_variable = { item_ref = FROM.item_id }

            # Optional: Call selection effect
            item_selection_effect = yes
        }
    }
}

triggers = {
    item_select_button_click_enabled = {
        FROM = { has_variable = item_id }
    }
}

properties = {
    item_highlight_icon = {
        # Show highlight when selected
        image = "[?selection_indicator]"
    }
}
```

### Context-Based Selection
```
scripted_gui = {
    bsm_country_selector = {
        context_type = selected_country_context
        parent_window_token = selected_country_view_diplomacy
        window_name = "country_selector_container"

        triggers = {
            select_button_visible = {
                FROM = { is_valid_target = yes }
            }
        }

        effects = {
            select_button_click = {
                ROOT = {
                    set_variable = { selected_country = FROM }
                }
            }
        }

        properties = {
            country_icon = {
                image = "GFX_[?FROM.GetTag]"
            }
        }
    }
}
```

## Dynamic Lists

### Basic Array List
```
dynamic_lists = {
    member_list = {
        array = ROOT.alliance_members
        change_scope = no
        entry_container = "member_entry_container"
    }
}
```

### Country Scope List
```
dynamic_lists = {
    country_list = {
        array = ROOT.member_countries
        change_scope = yes
        country_scope_entry_container = "country_entry"
    }
}
```

### List with Actions
```
# In scripted_gui
dynamic_lists = {
    action_list = {
        array = ROOT.available_actions
        change_scope = no
        entry_container = "action_entry"
    }
}

effects = {
    action_button_click = {
        # Access array index via default 'i' variable
        # Access array value via default 'v' variable
        execute_action_by_index = yes
    }
}
```

## Info Displays

### Resource Display (Topbar Pattern)
```
# In .gui file
containerWindowType = {
    name = "resource_display"
    position = { x = 100 y = 8 }
    size = { width = 56 height = 30 }
    orientation = UPPER_LEFT

    background = {
        position = { x = 2 y = 1 }
        name = "resource_bg"
        quadTextureSprite = "GFX_bg_mini_tooltip"
        pdx_tooltip = "resource_title"
        pdx_tooltip_delayed = "resource_desc"
    }

    iconType = {
        name = "resource_icon"
        spriteType = "GFX_resource_sprite"
        position = { x = 4 y = 2 }
        alwaystransparent = yes
        pdx_tooltip = "resource_title"
        pdx_tooltip_delayed = "resource_desc"
    }

    instantTextBoxType = {
        name = "RESOURCE_VALUE"
        position = { x = 19 y = 5 }
        font = "vanilla_hoi_18mbs"
        text = RESOURCE_VALUE
        format = left
        maxWidth = 50
        maxHeight = 24
        fixedsize = yes
        alwaystransparent = yes
        pdx_tooltip = "resource_title"
        pdx_tooltip_delayed = "resource_desc"
    }
}
```

### Status Indicator
```
# In .gui file
iconType = {
    name = "status_indicator"
    spriteType = "GFX_status_icons"
    position = { x = 10 y = 10 }
    frame = 1  # Controlled by properties
}

# In scripted_gui
properties = {
    status_indicator = {
        frame = status_value  # Variable holding 1, 2, 3, etc.
    }
}
```

## Multi-Page GUIs

### Page System with Variable
```
# Page 1 Container
containerWindowType = {
    name = "page_1_content"
    show_position = { x = 0 y = 50 }
    hide_position = { x = 0 y = -1000 }  # Off-screen when hidden
}

# Page 2 Container
containerWindowType = {
    name = "page_2_content"
    show_position = { x = 0 y = 50 }
    hide_position = { x = 0 y = -1000 }
}

# In scripted_gui
triggers = {
    page_1_content_visible = {
        check_variable = { current_page = 1 }
    }

    page_2_content_visible = {
        check_variable = { current_page = 2 }
    }
}

effects = {
    page_1_button_click = {
        set_variable = { current_page = 1 }
    }

    page_2_button_click = {
        set_variable = { current_page = 2 }
    }
}
```

## Integration

### Attaching to Decision Category
```
# In decision category file (common/decisions/categories/)
bsm_system_decisions = {
    icon = GFX_decision_category_icon

    visible = {
        has_country_flag = system_enabled
    }

    scripted_gui = bsm_system_gui  # Links to scripted_gui name
}
```

### Topbar Integration
```
scripted_gui = {
    bsm_topbar = {
        window_name = "bsm_topbar"
        context_type = player_context
        parent_window_token = top_bar  # Optional, attaches to vanilla topbar

        effects = {
            open_button_click = {
                if = {
                    limit = { has_variable = gui_open }
                    clear_variable = gui_open
                }
                else = {
                    set_variable = { gui_open = 1 }
                }
            }
        }
    }
}
```

### Diplomacy View Integration
```
scripted_gui = {
    bsm_diplomacy_action = {
        context_type = selected_country_context
        parent_window_token = selected_country_view_diplomacy
        window_name = "bsm_diplomacy_container"

        visible = {
            FROM = { is_valid_diplomatic_target = yes }
        }

        effects = {
            diplomatic_action_click = {
                FROM = {
                    # Target country scope
                }
                # ROOT is player
            }
        }
    }
}
```

## Performance Optimization

### Use Dirty Variables for Complex GUIs
```
scripted_gui = {
    bsm_complex_gui = {
        window_name = "bsm_complex_gui"
        context_type = player_context

        # Only update when this variable changes
        dirty = gui_update_trigger

        effects = {
            action_button_click = {
                # Perform action
                do_complex_calculation = yes

                # Force GUI update
                add_to_variable = { gui_update_trigger = 1 }
            }
        }
    }
}
```

### Lightweight Visibility Checks
```
visible = {
    # Check flags first (fast)
    has_country_flag = feature_enabled

    # Then variables (medium)
    has_variable = system_active

    # Avoid heavy checks in visible block
    # Move to triggers for specific elements instead
}
```

### Disable AI for Player-Only GUIs
```
ai_enabled = {
    always = no
}
```

## Common Scripted Localisation Integration

### Variable Display
```
# In localisation file
display_text:0 "Value: [?variable_name]"
member_count:0 "Members: [?member_count_var]"

# In GUI
instantTextBoxType = {
    name = "display_text_element"
    text = "display_text"
}
```

### Conditional Text
```
# In scripted_localisation file
defined_text = {
    name = STATUS_TEXT
    text = {
        localization_key = "status_active"
        trigger = { has_country_flag = active }
    }
    text = {
        localization_key = "status_inactive"
        trigger = { always = yes }
    }
}

# In GUI
instantTextBoxType = {
    text = "STATUS_TEXT"
}
```
