# GUI Integration Guide for Scripted Localisation

## Using in Scripted GUIs

### Basic Text Display

```
# In scripted GUI:
window_name = {
    dynamic_text = {
        text = "[Root.GetDynamicText]"
    }
}

# In scripted localisation:
defined_text = {
    name = GetDynamicText
    text = { trigger = { has_war = yes } localization_key = "text_war" }
    text = { trigger = { always = yes } localization_key = "text_peace" }
}

# In localisation file:
l_japanese:
 text_war:0 "戦時中"
 text_peace:0 "平時"
```

### Button Text

```
# In scripted GUI:
buttonType = {
    name = "my_button"
    text = "[Root.GetButtonText]"
}

# In scripted localisation:
defined_text = {
    name = GetButtonText
    text = {
        trigger = { check_variable = { button_enabled = 1 } }
        localization_key = "button_enabled"
    }
    text = {
        trigger = { always = yes }
        localization_key = "button_disabled"
    }
}
```

### Icon Selection

```
# In scripted GUI:
iconType = {
    name = "status_icon"
    spriteType = "[Root.GetStatusIcon]"
}

# In scripted localisation:
defined_text = {
    name = GetStatusIcon
    text = { trigger = { has_war = yes } localization_key = "GFX_icon_war" }
    text = { trigger = { has_stability < 0.50 } localization_key = "GFX_icon_crisis" }
    text = { trigger = { always = yes } localization_key = "GFX_icon_peace" }
}
```

## Tooltip Integration

### Dynamic Tooltips

```
# In scripted GUI:
buttonType = {
    name = "action_button"
    tooltipText = "[Root.GetActionTooltip]"
}

# In scripted localisation:
defined_text = {
    name = GetActionTooltip
    text = {
        trigger = {
            NOT = { has_political_power > 50 }
        }
        localization_key = "tooltip_need_pp"
    }
    text = {
        trigger = { has_war = yes }
        localization_key = "tooltip_cannot_war"
    }
    text = {
        trigger = { always = yes }
        localization_key = "tooltip_available"
    }
}

# In localisation:
l_japanese:
 tooltip_need_pp:0 "§R政治力が不足しています§!"
 tooltip_cannot_war:0 "§Y戦時中は実行できません§!"
 tooltip_available:0 "§G実行可能§!"
```

### Multi-Line Tooltips

```
# In localisation:
l_japanese:
 complex_tooltip:0 "[Root.GetStatusText]\n\n[Root.GetRequirementsText]\n\n[Root.GetEffectsText]"

# Multiple scripted localisations for each section
defined_text = {
    name = GetStatusText
    # ...
}

defined_text = {
    name = GetRequirementsText
    # ...
}

defined_text = {
    name = GetEffectsText
    # ...
}
```

## Container Integration

### Dynamic List Items

```
# In scripted GUI:
container = {
    dynamic_list = {
        name = "item_list"

        containerWindowType = {
            name = "list_item"

            dynamic_text = {
                text = "[Root.GetListItemText]"
            }

            iconType = {
                spriteType = "[Root.GetListItemIcon]"
            }
        }
    }
}

# With index variable in localisation:
defined_text = {
    name = GetListItemText
    text = { trigger = { check_variable = { list_index = 0 } } localization_key = "item_0" }
    text = { trigger = { check_variable = { list_index = 1 } } localization_key = "item_1" }
    text = { trigger = { check_variable = { list_index = 2 } } localization_key = "item_2" }
}
```

### Grid Items

```
# In scripted GUI gridbox:
gridBoxType = {
    name = "option_grid"

    containerWindowType = {
        name = "grid_cell"

        dynamic_text = {
            text = "[Root.GetCellText]"
        }
    }
}

# Variable-based cell text:
defined_text = {
    name = GetCellText
    text = { trigger = { check_variable = { cell_type = 1 } } localization_key = "cell_military" }
    text = { trigger = { check_variable = { cell_type = 2 } } localization_key = "cell_economy" }
    text = { trigger = { check_variable = { cell_type = 3 } } localization_key = "cell_political" }
}
```

## Visibility Conditions

### Conditional Display

```
# In scripted GUI:
window_name = {
    dynamic_text = {
        text = "[Root.GetConditionalText]"
        visible = "[Root.ShouldShowText]"
    }
}

# Visibility trigger:
scripted_trigger = {
    name = ShouldShowText
    check_variable = { show_text = 1 }
}

# Text content:
defined_text = {
    name = GetConditionalText
    text = { trigger = { check_variable = { text_type = 1 } } localization_key = "text_1" }
    text = { trigger = { check_variable = { text_type = 2 } } localization_key = "text_2" }
}
```

## Progress Bar Integration

### Dynamic Progress Text

```
# In scripted GUI:
progressType = {
    name = "progress_bar"

    dynamic_text = {
        text = "[Root.GetProgressText]"
    }
}

# Progress-based text:
defined_text = {
    name = GetProgressText
    text = {
        trigger = { check_variable = { progress >= 1.0 } }
        localization_key = "progress_100"
    }
    text = {
        trigger = { check_variable = { progress >= 0.75 } }
        localization_key = "progress_75"
    }
    text = {
        trigger = { check_variable = { progress >= 0.50 } }
        localization_key = "progress_50"
    }
    text = {
        trigger = { check_variable = { progress >= 0.25 } }
        localization_key = "progress_25"
    }
    text = {
        trigger = { always = yes }
        localization_key = "progress_0"
    }
}

# In localisation:
l_japanese:
 progress_100:0 "§G完了§!"
 progress_75:0 "§G75%§!"
 progress_50:0 "§Y50%§!"
 progress_25:0 "§Y25%§!"
 progress_0:0 "§R未開始§!"
```

## Click Effect Integration

### Button State After Click

```
# In scripted GUI effect:
on_click = {
    set_variable = { button_clicked = 1 }
}

# Button text changes after click:
buttonType = {
    name = "toggle_button"
    text = "[Root.GetToggleText]"
}

# Scripted localisation:
defined_text = {
    name = GetToggleText
    text = {
        trigger = { check_variable = { button_clicked = 1 } }
        localization_key = "button_clicked"
    }
    text = {
        trigger = { always = yes }
        localization_key = "button_unclicked"
    }
}
```

## Real-World Example: Page Navigation

```
# In scripted GUI:
containerWindowType = {
    name = "page_navigation"

    # Page title
    dynamic_text = {
        name = "page_title"
        text = "[Root.GetPageTitle]"
        position = { x = 10 y = 10 }
    }

    # Page description
    dynamic_text = {
        name = "page_desc"
        text = "[Root.GetPageDescription]"
        position = { x = 10 y = 40 }
    }

    # Navigation buttons
    buttonType = {
        name = "prev_button"
        text = "[Root.GetPrevButtonText]"
        on_click = {
            subtract_from_variable = { page_id = 1 }
            clamp_variable = { var = page_id min = 0 }
        }
    }

    buttonType = {
        name = "next_button"
        text = "[Root.GetNextButtonText]"
        on_click = {
            add_to_variable = { page_id = 1 }
            clamp_variable = { var = page_id max = 5 }
        }
    }
}

# Scripted localisation:
defined_text = {
    name = GetPageTitle
    text = { trigger = { check_variable = { page_id = 0 } } localization_key = "page_0_title" }
    text = { trigger = { check_variable = { page_id = 1 } } localization_key = "page_1_title" }
    text = { trigger = { check_variable = { page_id = 2 } } localization_key = "page_2_title" }
    text = { trigger = { check_variable = { page_id = 3 } } localization_key = "page_3_title" }
    text = { trigger = { check_variable = { page_id = 4 } } localization_key = "page_4_title" }
    text = { trigger = { check_variable = { page_id = 5 } } localization_key = "page_5_title" }
}

defined_text = {
    name = GetPageDescription
    text = { trigger = { check_variable = { page_id = 0 } } localization_key = "page_0_desc" }
    text = { trigger = { check_variable = { page_id = 1 } } localization_key = "page_1_desc" }
    text = { trigger = { check_variable = { page_id = 2 } } localization_key = "page_2_desc" }
    text = { trigger = { check_variable = { page_id = 3 } } localization_key = "page_3_desc" }
    text = { trigger = { check_variable = { page_id = 4 } } localization_key = "page_4_desc" }
    text = { trigger = { check_variable = { page_id = 5 } } localization_key = "page_5_desc" }
}

defined_text = {
    name = GetPrevButtonText
    text = {
        trigger = { check_variable = { page_id = 0 } }
        localization_key = "button_prev_disabled"
    }
    text = {
        trigger = { always = yes }
        localization_key = "button_prev_enabled"
    }
}

defined_text = {
    name = GetNextButtonText
    text = {
        trigger = { check_variable = { page_id = 5 } }
        localization_key = "button_next_disabled"
    }
    text = {
        trigger = { always = yes }
        localization_key = "button_next_enabled"
    }
}
```

## Best Practices for GUI

1. **Separate concerns** - One scripted localisation per UI element
2. **Use clear names** - `GetPageTitle` not `GetText`
3. **Provide fallbacks** - Always have a default case
4. **Test all states** - Check every variable value
5. **Color code** - Use §G, §Y, §R for status indication
6. **Cache when possible** - Store frequently-used results in variables

## Color Codes in Localisation

```
§G - Green (success/available)
§Y - Yellow (warning/in progress)
§R - Red (error/unavailable)
§! - Reset to default color
§H - Highlight
```

Example:
```yaml
status_good:0 "§G実行可能§!"
status_warning:0 "§Y注意が必要§!"
status_bad:0 "§R実行不可§!"
```
