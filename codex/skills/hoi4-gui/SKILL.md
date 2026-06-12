---
name: hoi4-gui
description: Create Hearts of Iron IV scripted GUIs and interface files for BSM mods. Use when creating custom GUI windows, decision category interfaces, topbar elements, information displays, selection menus, dynamic lists, or any interactive UI elements for HOI4 mods. Provides comprehensive syntax, BSM naming conventions, performance optimization, templates for common patterns (buttons, windows, dynamic lists), and scripted localisation integration.
---

# HOI4 Scripted GUI and Interface Builder

Build custom GUIs for Hearts of Iron IV mods using scripted_gui system.

## Quick Start

### 1. Choose GUI Type
- **Simple button/action**: Use `assets/templates/simple_button.txt`
- **Toggle window**: Use `assets/templates/toggle_window.txt`
- **Dynamic list**: Use `assets/templates/dynamic_list.txt`
- **Decision category GUI**: Use `assets/templates/decision_category_gui.txt`
- **Info display**: Use `assets/templates/info_display.txt`

### 2. Create Files
Two files required:
- **Scripted GUI** (`common/scripted_guis/bsm_SYSTEM_NAME_sgui.txt`) - Logic and triggers
- **Interface** (`interface/bsm_SYSTEM_NAME.gui`) - Visual layout

### 3. Follow Naming Conventions
- **System GUIs**: `_bsm_system_name` (e.g., `_bsm_harvest_system`)
- **Feature GUIs**: `bsm_feature_name` (e.g., `bsm_economic_alliance`)
- **Variables**: `system_variable_name` (e.g., `harvest_system_page`)
- **Buttons**: `action_button` (e.g., `open_button`, `confirm_button`)

## Workflow

### Creating a New GUI

1. **Select template** from `assets/templates/` matching your GUI type

2. **Read syntax reference** for your needs:
   - Scripted GUI syntax: `references/scripted_gui_syntax.md`
   - Interface file syntax: `references/gui_file_syntax.md`
   - BSM patterns: `references/bsm_patterns.md`

3. **Copy template** and replace placeholders:
   - `SYSTEM_NAME` → Your system name
   - `ACTION_NAME` → What buttons do
   - `ARRAY_NAME` → Array variable names
   - `VARIABLE_NAME` → Variable names

4. **Create both files**:
   ```
   common/scripted_guis/bsm_SYSTEM_NAME_sgui.txt
   interface/bsm_SYSTEM_NAME.gui
   ```

5. **Add localisation**:
   ```
   localisation/japanese/bsm_SYSTEM_NAME_l_japanese.yml
   ```

6. **Test in-game** and iterate

### Modifying Existing GUIs

1. **Read the existing files** to understand structure

2. **Consult references** for syntax you need to add:
   - Adding dynamic list? See `references/scripted_gui_syntax.md#dynamic-lists`
   - Need new trigger? See `references/scripted_gui_syntax.md#triggers`
   - Positioning elements? See `references/gui_file_syntax.md#positioning-and-sizing`

3. **Check examples** in `references/examples.md` for proven patterns

4. **Apply BSM patterns** from `references/bsm_patterns.md`

## Reference Guide

### When to Read Each Reference

**`references/scripted_gui_syntax.md`** - Comprehensive scripted_gui documentation
- Read when: Creating/modifying .txt files in `common/scripted_guis/`
- Covers: context types, effects, triggers, properties, dynamic lists, AI config, performance

**`references/gui_file_syntax.md`** - Comprehensive .gui file documentation
- Read when: Creating/modifying .gui files in `interface/`
- Covers: containers, element types, positioning, fonts, tooltips, scrollbars

**`references/bsm_patterns.md`** - BSM-specific patterns and best practices
- Read when: Need proven patterns for toggle, selection, info display, multi-page
- Covers: BSM naming, common patterns, performance optimization, integration

**`references/examples.md`** - Real working examples from BSM/SSW mods
- Read when: Want to see complete working implementations
- Covers: Topbar displays, toggle windows, dynamic lists, country selection

## Key Concepts

### File Relationship
```
Scripted GUI (logic)          GUI File (visual)
┌─────────────────┐          ┌──────────────────┐
│ window_name =   │ ◄─────── │ name = "..."     │
│ effects { }     │          │ buttonType {     │
│ triggers { }    │ ────────►│   name = "..."   │
│ properties { }  │          │ }                │
└─────────────────┘          └──────────────────┘
```

Element names in GUI file match effect/trigger/property names in scripted GUI.

### Context Types
- `player_context` - Player country scope, main window attachment
- `decision_category` - Attached to decision category
- `selected_country_context` - Right-click country
- `selected_state_context` - Left-click state

See `references/scripted_gui_syntax.md#context-types` for all types.

### Dynamic Lists
Arrays in HOI4 can populate GUI lists:
1. Define array in scripted effects: `add_to_array = { members = GER }`
2. Reference in scripted_gui: `array = ROOT.members`
3. Create entry template in .gui file
4. Access via `v` (value) and `i` (index) in effects

See `references/scripted_gui_syntax.md#dynamic-lists` and `assets/templates/dynamic_list.txt`.

### Properties
Modify visuals dynamically:
- **Images**: `image = "GFX_[?variable.GetTokenKey]"`
- **Frames**: `frame = variable_holding_number`
- **Position**: `x = variable`, `y = variable`

See `references/scripted_gui_syntax.md#properties`.

## BSM Conventions

### Performance Optimization
1. **Use dirty variables** for complex GUIs that don't need per-tick updates:
   ```
   dirty = gui_update_trigger
   ```

2. **Disable AI** for player-only GUIs:
   ```
   ai_enabled = { always = no }
   ```

3. **Lightweight visibility checks** - put expensive checks in element triggers, not main visible block

4. **Cache with flags** - store computation results in flags rather than recalculating

See `references/bsm_patterns.md#performance-optimization`.

### File Organization
- System files: `_bsm_system_name.*`
- Feature files: `bsm_feature_name.*`
- Match .txt and .gui filenames for clarity

### Variable Patterns
- Toggle variables: `system_window_open`
- Page variables: `system_page`
- Selection variables: `selected_item_id`
- State flags: `system_feature_enabled`

## Common Patterns

### Toggle Button
```
effects = {
    toggle_button_click = {
        if = {
            limit = { has_variable = window_open }
            clear_variable = window_open
        }
        else = {
            set_variable = { window_open = 1 }
        }
    }
}
```

### Selection with Highlight
```
effects = {
    item_button_click = {
        if = {
            limit = { check_variable = { selected_item = v } }
            clear_variable = selected_item
        }
        else = {
            set_variable = { selected_item = v }
        }
    }
}

triggers = {
    highlight_visible = {
        check_variable = { selected_item = v }
    }
}
```

### Multi-Page GUI
```
effects = {
    page_1_button_click = { set_variable = { page = 1 } }
    page_2_button_click = { set_variable = { page = 2 } }
}

triggers = {
    page_1_content_visible = { check_variable = { page = 1 } }
    page_2_content_visible = { check_variable = { page = 2 } }
}
```

More patterns in `references/bsm_patterns.md#common-patterns`.

## Integration

### Decision Category
```
# common/decisions/categories/
bsm_system_category = {
    icon = GFX_category_icon
    visible = { has_country_flag = enabled }
    scripted_gui = bsm_system_gui
}
```

### Topbar
```
scripted_gui = {
    bsm_topbar_element = {
        window_name = "bsm_topbar_element"
        context_type = player_context
        parent_window_token = top_bar  # Optional
    }
}
```

### Diplomacy View
```
scripted_gui = {
    bsm_diplo_action = {
        context_type = selected_country_context
        parent_window_token = selected_country_view_diplomacy
        window_name = "bsm_diplo_container"
    }
}
```

## Troubleshooting

### GUI Not Appearing
1. Check `visible = { }` block in scripted_gui
2. Verify window_name matches between .txt and .gui
3. Check parent_window_token is valid
4. Ensure country has required flags/variables

### Buttons Not Working
1. Verify button name matches effect name + `_click`
2. Check trigger `button_name_click_enabled` isn't false
3. Test with `always = yes` trigger to isolate issue

### Dynamic List Empty
1. Verify array is populated (check with `log` command)
2. Check array name matches exactly
3. Verify entry_container name matches container in .gui
4. Check change_scope setting

### Elements Misaligned
1. Check position { x y } values
2. Verify orientation setting
3. Check parent container size
4. Test with absolute positioning first

## Best Practices

1. **Read existing code first** - Check BSM/SSW examples before creating new patterns
2. **Follow naming conventions** - Consistency makes debugging easier
3. **Test incrementally** - Build GUI in stages, test each addition
4. **Use templates** - Start with proven template, modify as needed
5. **Comment complex logic** - Future you will thank present you
6. **Performance matters** - Use dirty variables, disable AI, cache computations
7. **Localise everything** - Even debug text should have loc keys

## Additional Resources

- HOI4 Wiki: https://hoi4.paradoxwikis.com/Scripted_GUI_modding
- BSM codebase examples in `/bakasekai/common/scripted_guis/` and `/interface/`
- SSW mod examples in `/SSW_mod/common/scripted_guis/`
