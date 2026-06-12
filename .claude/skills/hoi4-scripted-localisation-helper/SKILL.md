---
name: hoi4-scripted-localisation-helper
description: Guide for creating dynamic text with HOI4 scripted localisation (defined_text). Use when the user (1) Needs dynamic text that changes based on conditions, (2) Wants to display different strings based on variables/flags, (3) Needs conditional tooltips or UI text, or (4) Says phrases like "dynamic text", "conditional localisation", "change text based on variable", "defined_text", etc. Covers trigger-based text selection patterns.
---

# HOI4 Scripted Localisation Helper

## Overview

Scripted localisation allows dynamic text selection based on triggers, variables, and game state. Instead of hardcoding one text, you define multiple options that display conditionally. Essential for GUI systems, dynamic tooltips, and state-dependent text.

## When This Skill Triggers

This skill activates when:
- User needs text that changes based on conditions
- User wants to display different strings based on variables
- User is building GUI systems with dynamic content
- User needs conditional tooltips or descriptions
- User says: "dynamic text", "conditional localisation", "defined_text", "change text based on variable"

## Quick Reference

**File Location:** `common/scripted_localisation/<filename>.txt`

**Basic Structure:**
```
defined_text = {
    name = MyDynamicText

    text = {
        trigger = { <condition> }
        localization_key = "loc_key_1"
    }

    text = {
        trigger = { <condition> }
        localization_key = "loc_key_2"
    }
}
```

**Usage in Localisation:**
```yaml
tooltip:0 "[Root.GetMyDynamicText]"
```

---

## Part 1: Basic Structure

### Defining Scripted Localisation

**File:** `common/scripted_localisation/my_dynamic_text.txt`

```
defined_text = {
    name = GetDynamicText

    text = {
        trigger = {
            has_war = yes
        }
        localization_key = "wartime_text"
    }

    text = {
        trigger = {
            has_war = no
        }
        localization_key = "peacetime_text"
    }
}
```

### Using in Localisation Files

**File:** `localisation/japanese/my_mod_l_japanese.yml`

```yaml
l_japanese:
 my_tooltip:0 "[Root.GetDynamicText]"
 wartime_text:0 "戦時中"
 peacetime_text:0 "平時"
```

### Scope Reference

The scripted localisation evaluates in the scope where it's called:

```
[Root.GetDynamicText]      # Root scope
[This.GetDynamicText]      # This scope
[From.GetDynamicText]      # From scope
[GER.GetDynamicText]       # Specific country
```

---

## Part 2: Variable-Based Selection

### Single Variable Check

```
defined_text = {
    name = GetPageTitle

    text = {
        trigger = { check_variable = { page_id = 0 } }
        localization_key = "page_0_title"
    }

    text = {
        trigger = { check_variable = { page_id = 1 } }
        localization_key = "page_1_title"
    }

    text = {
        trigger = { check_variable = { page_id = 2 } }
        localization_key = "page_2_title"
    }
}
```

### Array Index-Based

```
defined_text = {
    name = GetSelectedObjective

    text = {
        trigger = { check_variable = { objective_array^0 = 1 } }
        localization_key = "objective_industrial_1"
    }

    text = {
        trigger = { check_variable = { objective_array^1 = 1 } }
        localization_key = "objective_research_1"
    }

    text = {
        trigger = { check_variable = { objective_array^2 = 1 } }
        localization_key = "objective_military_1"
    }
}
```

### Multiple Variable Conditions

```
defined_text = {
    name = GetObjectiveProgress

    text = {
        trigger = {
            check_variable = { page_id = 0 }
            check_variable = { objective_type = 1 }
        }
        localization_key = "industrial_objective_1_progress"
    }

    text = {
        trigger = {
            check_variable = { page_id = 0 }
            check_variable = { objective_type = 2 }
        }
        localization_key = "industrial_objective_2_progress"
    }

    text = {
        trigger = {
            check_variable = { page_id = 1 }
        }
        localization_key = "research_objective_progress"
    }
}
```

---

## Part 3: Idea/Flag-Based Selection

### Idea-Based (Economic Alliance Pattern)

```
defined_text = {
    name = GetEconomicAllianceName

    text = {
        trigger = { has_idea = bsm_ea_idea_european_union }
        localization_key = bsm_ea_idea_european_union
    }

    text = {
        trigger = { has_idea = bsm_ea_idea_commonwealth }
        localization_key = bsm_ea_idea_commonwealth
    }

    text = {
        trigger = { has_idea = bsm_ea_idea_east_asia_league }
        localization_key = bsm_ea_idea_east_asia_league
    }

    text = {
        trigger = { has_idea = bsm_ea_idea_nafta }
        localization_key = bsm_ea_idea_nafta
    }
}
```

### Country Tag-Based

```
defined_text = {
    name = GetPartyName

    text = {
        trigger = { original_tag = JAP }
        localization_key = "JAP_party_name"
    }

    text = {
        trigger = { original_tag = GER }
        localization_key = "GER_party_name"
    }

    text = {
        trigger = { original_tag = USA }
        localization_key = "USA_party_name"
    }
}
```

### Flag-Based

```
defined_text = {
    name = GetRegimeType

    text = {
        trigger = { has_country_flag = democratic_regime }
        localization_key = "regime_democratic"
    }

    text = {
        trigger = { has_country_flag = authoritarian_regime }
        localization_key = "regime_authoritarian"
    }

    text = {
        trigger = { has_country_flag = totalitarian_regime }
        localization_key = "regime_totalitarian"
    }
}
```

---

## Part 4: Token-Based Selection

### Dynamic Token Comparison

```
defined_text = {
    name = GetTimelineIcon

    text = {
        trigger = {
            check_variable = {
                global.timeline_id_@var:timeline_id^3 = token:dts_type_start_of_war
            }
        }
        localization_key = "GFX_dts_type_start_of_war"
    }

    text = {
        trigger = {
            check_variable = {
                global.timeline_id_@var:timeline_id^3 = token:dts_type_end_of_war
            }
        }
        localization_key = "GFX_dts_type_end_of_war"
    }

    text = {
        trigger = {
            check_variable = {
                global.timeline_id_@var:timeline_id^3 = token:dts_type_progress_of_war
            }
        }
        localization_key = "GFX_dts_type_progress_of_war"
    }
}
```

---

## Part 5: Complex Patterns

### Nested Conditions

```
defined_text = {
    name = GetComplexStatus

    text = {
        trigger = {
            check_variable = { page_id = 0 }
            OR = {
                has_war = yes
                has_stability < 0.50
            }
        }
        localization_key = "status_crisis_page_0"
    }

    text = {
        trigger = {
            check_variable = { page_id = 0 }
            has_war = no
            has_stability > 0.50
        }
        localization_key = "status_stable_page_0"
    }

    text = {
        trigger = {
            check_variable = { page_id = 1 }
        }
        localization_key = "status_page_1"
    }
}
```

### Fallback Pattern

```
defined_text = {
    name = GetAllianceName

    # Specific alliances first
    text = {
        trigger = { has_idea = european_union }
        localization_key = "alliance_eu"
    }

    text = {
        trigger = { has_idea = nato }
        localization_key = "alliance_nato"
    }

    # Generic fallback (always true)
    text = {
        trigger = { always = yes }
        localization_key = "alliance_generic"
    }
}
```

### Priority Order

**IMPORTANT:** Triggers are evaluated **in order**. First matching trigger wins.

```
defined_text = {
    name = GetPriorityText

    # More specific conditions first
    text = {
        trigger = {
            has_war = yes
            is_major = yes
        }
        localization_key = "major_at_war"
    }

    # Less specific conditions later
    text = {
        trigger = { has_war = yes }
        localization_key = "at_war"
    }

    # Fallback
    text = {
        trigger = { always = yes }
        localization_key = "at_peace"
    }
}
```

---

## Real-World Examples (SSW Mod)

### Page Navigation System

```
defined_text = {
    name = bol_page_name

    text = {
        trigger = { check_variable = { bol_select_page = 0 } }
        localization_key = "bol_page_0"
    }

    text = {
        trigger = { check_variable = { bol_select_page = 1 } }
        localization_key = "bol_countrydesc_title"
    }

    text = {
        trigger = { check_variable = { bol_select_page = 2 } }
        localization_key = "bol_page_2"
    }

    text = {
        trigger = { check_variable = { bol_select_page = 3 } }
        localization_key = "bol_page_3"
    }
}
```

### Objective System

```
defined_text = {
    name = fypg_objective

    text = {
        trigger = {
            check_variable = { fypg_select_page^0 = 2 }
            check_variable = { fypg_objective_type^0 = 1 }
        }
        localization_key = "fypg_industrial_objective_1_title"
    }

    text = {
        trigger = {
            check_variable = { fypg_select_page^0 = 2 }
            check_variable = { fypg_objective_type^0 = 2 }
        }
        localization_key = "fypg_industrial_objective_2_title"
    }

    text = {
        trigger = { check_variable = { fypg_select_page^1 = 2 } }
        localization_key = "fypg_research_objective_title"
    }
}
```

### Progress Display

```
defined_text = {
    name = fypg_progress

    text = {
        trigger = { check_variable = { fypg_select_page^0 = 2 } }
        localization_key = "fypg_progress_key_0"
    }

    text = {
        trigger = { check_variable = { fypg_select_page^1 = 2 } }
        localization_key = "fypg_progress_key_1"
    }

    text = {
        trigger = { check_variable = { fypg_select_page^2 = 2 } }
        localization_key = "fypg_progress_key_2"
    }
}
```

---

## Common Patterns

### Pattern 1: Menu System

```
defined_text = {
    name = GetMenuOption

    text = {
        trigger = { check_variable = { menu_index = 0 } }
        localization_key = "menu_option_0"
    }

    text = {
        trigger = { check_variable = { menu_index = 1 } }
        localization_key = "menu_option_1"
    }

    text = {
        trigger = { check_variable = { menu_index = 2 } }
        localization_key = "menu_option_2"
    }
}
```

### Pattern 2: State-Based Text

```
defined_text = {
    name = GetSystemStatus

    text = {
        trigger = { has_country_flag = system_active }
        localization_key = "system_status_active"
    }

    text = {
        trigger = { has_country_flag = system_paused }
        localization_key = "system_status_paused"
    }

    text = {
        trigger = { always = yes }
        localization_key = "system_status_inactive"
    }
}
```

### Pattern 3: Leader Names

```
defined_text = {
    name = GetCurrentLeaderName

    text = {
        trigger = {
            has_country_leader = {
                character = GER_adolf_hitler
            }
        }
        localization_key = "GER_adolf_hitler"
    }

    text = {
        trigger = {
            has_country_leader = {
                character = GER_wilhelm_pieck
            }
        }
        localization_key = "GER_wilhelm_pieck"
    }
}
```

### Pattern 4: Tooltip Variants

```
defined_text = {
    name = GetActionTooltip

    text = {
        trigger = {
            check_variable = { action_cost > political_power }
        }
        localization_key = "action_tooltip_cannot_afford"
    }

    text = {
        trigger = {
            check_variable = { action_available = 0 }
        }
        localization_key = "action_tooltip_locked"
    }

    text = {
        trigger = { always = yes }
        localization_key = "action_tooltip_available"
    }
}
```

### Pattern 5: Icon Selection

```
defined_text = {
    name = GetCategoryIcon

    text = {
        trigger = { check_variable = { category = 1 } }
        localization_key = "GFX_icon_military"
    }

    text = {
        trigger = { check_variable = { category = 2 } }
        localization_key = "GFX_icon_economic"
    }

    text = {
        trigger = { check_variable = { category = 3 } }
        localization_key = "GFX_icon_political"
    }

    text = {
        trigger = { always = yes }
        localization_key = "GFX_icon_generic"
    }
}
```

---

## Usage in GUI

### Scripted GUI Text

```
# In scripted GUI:
dynamic_text = {
    text = "[Root.GetDynamicText]"
}

# In localisation:
l_japanese:
 tooltip:0 "[Root.GetDynamicText]を選択"
```

### Button Text

```
# In GUI button:
buttonText = "[Root.GetButtonText]"

# In scripted localisation:
defined_text = {
    name = GetButtonText

    text = {
        trigger = { has_country_flag = button_enabled }
        localization_key = "button_text_enabled"
    }

    text = {
        trigger = { always = yes }
        localization_key = "button_text_disabled"
    }
}
```

### Conditional Icons

```
# In GUI:
icon = "[Root.GetStatusIcon]"

# In scripted localisation:
defined_text = {
    name = GetStatusIcon

    text = {
        trigger = { has_war = yes }
        localization_key = "GFX_icon_war"
    }

    text = {
        trigger = { always = yes }
        localization_key = "GFX_icon_peace"
    }
}
```

---

## Best Practices

### 1. Order Matters

Place most specific conditions first:

```
# GOOD
text = {
    trigger = {
        has_war = yes
        is_major = yes
        has_stability < 0.30
    }
    localization_key = "crisis_major_war"
}

text = {
    trigger = { has_war = yes }
    localization_key = "at_war"
}

# BAD (generic trigger first)
text = {
    trigger = { always = yes }  # This will always match!
    localization_key = "generic"
}

text = {
    trigger = { has_war = yes }  # Never reached
    localization_key = "at_war"
}
```

### 2. Always Provide Fallback

```
defined_text = {
    name = GetText

    # Specific cases
    text = { trigger = { condition_1 } localization_key = "text_1" }
    text = { trigger = { condition_2 } localization_key = "text_2" }

    # Fallback (always at end)
    text = {
        trigger = { always = yes }
        localization_key = "text_default"
    }
}
```

### 3. Name Clearly

Use descriptive names:

```
# GOOD
GetEconomicAllianceName
GetCurrentPageTitle
GetObjectiveProgress

# BAD
GetText
GetName
GetData
```

### 4. Group Related Texts

Organize by system/feature:

```
# File: _ssw_page_navigation.txt
defined_text = { name = bol_page_name ... }
defined_text = { name = bol_pagelist_name ... }
defined_text = { name = tt_bol_page_name ... }

# File: _ssw_objectives.txt
defined_text = { name = fypg_objective ... }
defined_text = { name = fypg_progress ... }
```

### 5. Consistent Prefixing

Use prefixes for organization:

```
# System prefix
tt_bol_page_name      # Tooltip
bol_page_name         # Button text
icon_bol_page         # Icon

# Feature prefix
fypg_objective        # Four Year Plan GUI
ea_alliance_name      # Economic Alliance
```

---

## Performance Considerations

- ✅ Scripted localisation is efficient (evaluated on display)
- ✅ Triggers run only when text is shown
- ⚠️ Avoid expensive triggers (every_country loops)
- ✅ Use simple variable checks when possible
- ✅ Cache results in variables if displayed frequently

---

## Debugging Tips

### Test in Localisation

```yaml
test_tooltip:0 "Current value: [Root.GetDynamicText]"
```

### Log Values

```
# In effect:
log = "Dynamic text result: [Root.GetDynamicText]"
```

### Check Trigger Order

If wrong text shows, check trigger order - earlier triggers take priority.

---

## Reference Documentation

For detailed examples:
- `references/scripted_loc_patterns.md` - Common patterns and templates
- `references/gui_integration.md` - Using in scripted GUIs

For real-world examples:
- SSW mod: `/Users/eightman/Desktop/HOI4_modding/SSW_mod/common/scripted_localisation/`
- BSM mod: `/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai/common/scripted_localisation/`

---

## Integration with Other Skills

### With hoi4-variable-helper
Use variables for dynamic text selection based on state.

### With hoi4-scripted-effect-maker
Change variables in effects, display results via scripted localisation.

---

## Quick Decision Tree

**Need different text based on game state?** → Use **defined_text**

**Need to show variable values?** → Use **[?variable_name]** in localisation

**Need conditional tooltips?** → Use **defined_text** with tooltip localization keys

**Need icons to change?** → Use **defined_text** with GFX_ localization keys

**Building GUI system?** → Use **defined_text** extensively for dynamic content
