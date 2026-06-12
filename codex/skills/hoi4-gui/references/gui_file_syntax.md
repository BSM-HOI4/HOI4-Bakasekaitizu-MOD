# GUI File (.gui) Syntax Reference

## Table of Contents
- [File Structure](#file-structure)
- [Container Types](#container-types)
- [Element Types](#element-types)
- [Positioning and Sizing](#positioning-and-sizing)
- [Common Properties](#common-properties)
- [Scripted Localisation](#scripted-localisation)
- [Tooltips](#tooltips)

## File Structure

All GUI elements must be wrapped in `guiTypes`:

```
guiTypes = {
    containerWindowType = {
        name = "window_name"
        # ... properties
    }
}
```

## Container Types

### containerWindowType
Main container for organizing elements:

```
containerWindowType = {
    name = "container_name"
    position = { x = 0 y = 0 }
    size = { width = 400 height = 300 }
    orientation = UPPER_LEFT

    # Nested containers and elements
    containerWindowType = { }
    buttonType = { }
    iconType = { }
    instantTextBoxType = { }
}
```

### gridBoxType
Grid layout for dynamic lists:

```
gridBoxType = {
    name = "grid_name"
    position = { x = 10 y = 10 }
    size = { width = 400 height = 600 }
    slotsize = { width = 100 height = 50 }
    max_slots_horizontal = 4
    format = "UPPER_LEFT"
}
```

### windowType
Alternative container (less common):

```
windowType = {
    name = "window_name"
    position = { x = 0 y = 0 }
    size = { width = 100%% height = 100%% }
}
```

## Element Types

### buttonType
Clickable button:

```
buttonType = {
    name = "button_name"
    position = { x = 10 y = 10 }
    quadTextureSprite = "GFX_button_sprite"
    orientation = UPPER_LEFT

    shortcut = "a"              # Keyboard shortcut
    clicksound = click_default
    oversound = ui_menu_over

    pdx_tooltip = "tooltip_key"
    pdx_tooltip_delayed = "detailed_tooltip_key"
}
```

### iconType
Static or dynamic image:

```
iconType = {
    name = "icon_name"
    position = { x = 5 y = 5 }
    spriteType = "GFX_icon_sprite"
    orientation = UPPER_LEFT

    frame = 1                   # For animated sprites
    scale = 1.0
    alwaystransparent = yes     # Click-through

    pdx_tooltip = "tooltip_key"
}
```

### instantTextBoxType
Text display:

```
instantTextBoxType = {
    name = "text_name"
    position = { x = 10 y = 10 }
    font = "hoi_18mbs"
    text = "LOCALISATION_KEY"
    format = left               # left, center, right

    maxWidth = 200
    maxHeight = 24
    fixedsize = yes

    alwaystransparent = yes
    pdx_tooltip = "tooltip_key"
}
```

### background
Background element for containers:

```
background = {
    name = "bg_name"
    position = { x = 0 y = 0 }
    quadTextureSprite = "GFX_background_sprite"

    pdx_tooltip = "tooltip_key"
}
```

### scrollbarType
Scrollbar for scrollable areas:

```
scrollbarType = {
    name = "scrollbar_name"
    position = { x = -16 y = 0 }
    size = { width = 16 height = 100%% }
    orientation = "UPPER_RIGHT"

    slider = {
        name = "slider"
        quadTextureSprite = "GFX_scrollbar_slider"
        position = { x = 0 y = 0 }
        alwaystransparent = yes
    }

    track = {
        name = "track"
        quadTextureSprite = "GFX_scrollbar_track"
        position = { x = 0 y = 0 }
        alwaystransparent = yes
    }

    increaseButton = {
        name = "increase"
        quadTextureSprite = "GFX_scrollbar_down"
        position = { x = 0 y = -16 }
        orientation = "LOWER_LEFT"
    }

    decreaseButton = {
        name = "decrease"
        quadTextureSprite = "GFX_scrollbar_up"
        position = { x = 0 y = 16 }
    }
}
```

## Positioning and Sizing

### Absolute Positioning
```
position = { x = 100 y = 50 }
```

### Percentage-Based Sizing
```
size = { width = 100%% height = 50%% }  # Note: Double %% for escaping
```

### Orientation
```
orientation = UPPER_LEFT    # Anchor point
```

Available orientations:
- `UPPER_LEFT`, `UPPER_RIGHT`
- `LOWER_LEFT`, `LOWER_RIGHT`
- `CENTER`, `CENTER_UP`, `CENTER_DOWN`

### Negative Positioning
Negative values position from right/bottom edge:
```
position = { x = -200 y = -100 }  # 200px from right, 100px from bottom
orientation = UPPER_RIGHT
```

## Common Properties

### Visibility
```
show_position = { x = 0 y = 0 }
hide_position = { x = -1000 y = 0 }  # Off-screen when hidden
```

### Animation
```
animation = {
    animationtype = decelerated
    animationduration = 0.3
}

show_animation_type = decelerated
hide_animation_type = accelerated
```

### Click-Through
```
alwaystransparent = yes  # Element doesn't intercept clicks
```

### Clipping
```
clipping = yes  # Clip content to container bounds
```

### Vertical Scrolling
```
verticalScrollbar = "scrollbar_name"
smooth_scrolling = yes
```

## Scripted Localisation

Embed dynamic values in text using scripted localisation:

### In GUI Files
```
instantTextBoxType = {
    name = "dynamic_text"
    text = "DYNAMIC_LOC_KEY"
}
```

### In Scripted Localisation File
```
defined_text = {
    name = DYNAMIC_LOC_KEY
    text = {
        localization_key = "value_display"
        trigger = { always = yes }
    }
}
```

### In Localisation File
```
value_display:0 "Value: [?variable_name]"
```

### Common Patterns
- `[?variable_name]` - Display variable value
- `[This.GetName]` - Country/state name
- `[This.GetTag]` - Country tag
- `[Root.GetName]` - Root scope name

## Tooltips

### Basic Tooltip
```
pdx_tooltip = "tooltip_localisation_key"
```

### Delayed Tooltip
```
pdx_tooltip = "short_tooltip"
pdx_tooltip_delayed = "detailed_tooltip"
```

### Conditional Tooltips
Handled via scripted effects and flags:
```
buttonType = {
    name = "conditional_button"
    pdx_tooltip = "button_tooltip"  # Defined in scripted localisation
}
```

## Font Names

Common HOI4 fonts:
- `hoi_18mbs` - Standard 18pt
- `hoi_24header` - 24pt headers
- `hoi_36header` - Large headers
- `hoi_16mbs` - Small text
- `vanilla_hoi_18mbs` - Vanilla-style 18pt
- `aldrich_24_outline` - Outlined text

## Sound Effects

Common click sounds:
- `click_default`
- `click_close`
- `click_ok`
- `click_checkbox`

Common over sounds:
- `ui_menu_over`
- `ui_menu_over_small`

## Special Cases

### Percentage in Text
Use double percentage for literal %:
```
text = "Efficiency: 100%%"
```

### Escaping Quotes
Use backslash to escape:
```
text = "He said \"Hello\""
```

### Multi-Line Containers
Containers can be nested indefinitely:
```
containerWindowType = {
    name = "outer"
    containerWindowType = {
        name = "middle"
        containerWindowType = {
            name = "inner"
        }
    }
}
```
