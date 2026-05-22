# Scripted Localisation Patterns Reference

## Pattern Categories

### 1. Variable-Based Selection

#### Single Variable
```
defined_text = {
    name = GetOptionByVar
    text = { trigger = { check_variable = { my_var = 0 } } localization_key = "option_0" }
    text = { trigger = { check_variable = { my_var = 1 } } localization_key = "option_1" }
    text = { trigger = { check_variable = { my_var = 2 } } localization_key = "option_2" }
    text = { trigger = { always = yes } localization_key = "option_default" }
}
```

#### Variable Range
```
defined_text = {
    name = GetProgressLevel
    text = {
        trigger = { check_variable = { progress >= 0.75 } }
        localization_key = "progress_excellent"
    }
    text = {
        trigger = { check_variable = { progress >= 0.50 } }
        localization_key = "progress_good"
    }
    text = {
        trigger = { check_variable = { progress >= 0.25 } }
        localization_key = "progress_fair"
    }
    text = {
        trigger = { always = yes }
        localization_key = "progress_poor"
    }
}
```

#### Array Index
```
defined_text = {
    name = GetArrayElement
    text = { trigger = { check_variable = { my_array^0 = 1 } } localization_key = "element_0_is_1" }
    text = { trigger = { check_variable = { my_array^1 = 1 } } localization_key = "element_1_is_1" }
    text = { trigger = { check_variable = { my_array^2 = 1 } } localization_key = "element_2_is_1" }
}
```

### 2. Idea-Based Selection

#### Direct Idea Check
```
defined_text = {
    name = GetCurrentIdeaName
    text = { trigger = { has_idea = idea_democratic } localization_key = "idea_democratic" }
    text = { trigger = { has_idea = idea_fascist } localization_key = "idea_fascist" }
    text = { trigger = { has_idea = idea_communist } localization_key = "idea_communist" }
    text = { trigger = { always = yes } localization_key = "idea_none" }
}
```

#### Idea Category
```
defined_text = {
    name = GetEconomicPolicy
    text = { trigger = { has_idea = free_market } localization_key = "free_market" }
    text = { trigger = { has_idea = mixed_economy } localization_key = "mixed_economy" }
    text = { trigger = { has_idea = planned_economy } localization_key = "planned_economy" }
}
```

### 3. Flag-Based Selection

#### Country Flags
```
defined_text = {
    name = GetPathChoice
    text = { trigger = { has_country_flag = path_democratic } localization_key = "path_democratic_text" }
    text = { trigger = { has_country_flag = path_monarchist } localization_key = "path_monarchist_text" }
    text = { trigger = { has_country_flag = path_fascist } localization_key = "path_fascist_text" }
}
```

#### Global Flags
```
defined_text = {
    name = GetWorldState
    text = { trigger = { has_global_flag = ww2_started } localization_key = "world_at_war" }
    text = { trigger = { has_global_flag = cold_war } localization_key = "cold_war_era" }
    text = { trigger = { always = yes } localization_key = "interwar_period" }
}
```

### 4. Country-Specific

#### By Tag
```
defined_text = {
    name = GetNationalParty
    text = { trigger = { original_tag = USA } localization_key = "USA_party_name" }
    text = { trigger = { original_tag = GER } localization_key = "GER_party_name" }
    text = { trigger = { original_tag = JAP } localization_key = "JAP_party_name" }
    text = { trigger = { always = yes } localization_key = "generic_party_name" }
}
```

#### By Ideology
```
defined_text = {
    name = GetGovernmentType
    text = { trigger = { has_democratic_government = yes } localization_key = "gov_democratic" }
    text = { trigger = { has_socialist_government = yes } localization_key = "gov_communist" }
    text = { trigger = { has_dictatorship_government = yes } localization_key = "gov_fascist" }
    text = { trigger = { always = yes } localization_key = "gov_neutral" }
}
```

### 5. Game State-Based

#### War Status
```
defined_text = {
    name = GetWarStatus
    text = {
        trigger = {
            has_war = yes
            has_defensive_war = yes
        }
        localization_key = "status_defensive_war"
    }
    text = {
        trigger = { has_war = yes }
        localization_key = "status_offensive_war"
    }
    text = {
        trigger = { always = yes }
        localization_key = "status_peace"
    }
}
```

#### Territory Control
```
defined_text = {
    name = GetTerritoryStatus
    text = {
        trigger = { controls_state = 125 }
        localization_key = "controls_berlin"
    }
    text = {
        trigger = { owns_state = 125 }
        localization_key = "owns_berlin"
    }
    text = {
        trigger = { always = yes }
        localization_key = "no_berlin"
    }
}
```

### 6. Character/Leader-Based

#### Current Leader
```
defined_text = {
    name = GetLeaderName
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

### 7. Token-Based

#### Dynamic Token Check
```
defined_text = {
    name = GetTokenText
    text = {
        trigger = {
            check_variable = {
                token_var = token:value_a
            }
        }
        localization_key = "text_for_a"
    }
    text = {
        trigger = {
            check_variable = {
                token_var = token:value_b
            }
        }
        localization_key = "text_for_b"
    }
}
```

#### Dynamic Array Token
```
defined_text = {
    name = GetTimelineType
    text = {
        trigger = {
            check_variable = {
                global.timeline_data_@var:id^0 = token:type_military
            }
        }
        localization_key = "timeline_military"
    }
    text = {
        trigger = {
            check_variable = {
                global.timeline_data_@var:id^0 = token:type_political
            }
        }
        localization_key = "timeline_political"
    }
}
```

### 8. Multiple Condition Patterns

#### AND Conditions
```
defined_text = {
    name = GetComplexState
    text = {
        trigger = {
            check_variable = { page_id = 1 }
            check_variable = { subpage_id = 2 }
            has_country_flag = feature_unlocked
        }
        localization_key = "complex_state_1_2_unlocked"
    }
    text = {
        trigger = {
            check_variable = { page_id = 1 }
            check_variable = { subpage_id = 2 }
        }
        localization_key = "complex_state_1_2_locked"
    }
}
```

#### OR Conditions
```
defined_text = {
    name = GetAllianceStatus
    text = {
        trigger = {
            OR = {
                is_in_faction_with = GER
                is_in_faction_with = ITA
                is_in_faction_with = JAP
            }
        }
        localization_key = "alliance_axis"
    }
    text = {
        trigger = { always = yes }
        localization_key = "alliance_none"
    }
}
```

### 9. GUI-Specific Patterns

#### Button State
```
defined_text = {
    name = GetButtonText
    text = {
        trigger = {
            check_variable = { button_enabled = 1 }
            check_variable = { cost <= political_power }
        }
        localization_key = "button_available"
    }
    text = {
        trigger = { check_variable = { button_enabled = 1 } }
        localization_key = "button_cannot_afford"
    }
    text = {
        trigger = { always = yes }
        localization_key = "button_locked"
    }
}
```

#### Icon Selection
```
defined_text = {
    name = GetCategoryIcon
    text = { trigger = { check_variable = { category = 1 } } localization_key = "GFX_cat_military" }
    text = { trigger = { check_variable = { category = 2 } } localization_key = "GFX_cat_economy" }
    text = { trigger = { check_variable = { category = 3 } } localization_key = "GFX_cat_political" }
    text = { trigger = { always = yes } localization_key = "GFX_cat_generic" }
}
```

#### Progress Bar Text
```
defined_text = {
    name = GetProgressText
    text = {
        trigger = { check_variable = { progress >= 1.0 } }
        localization_key = "progress_complete"
    }
    text = {
        trigger = { check_variable = { progress > 0.0 } }
        localization_key = "progress_in_progress"
    }
    text = {
        trigger = { always = yes }
        localization_key = "progress_not_started"
    }
}
```

### 10. Tooltip Patterns

#### Conditional Tooltip
```
defined_text = {
    name = GetActionTooltip
    text = {
        trigger = {
            NOT = { has_political_power > 50 }
        }
        localization_key = "tooltip_need_more_pp"
    }
    text = {
        trigger = { has_war = yes }
        localization_key = "tooltip_cannot_during_war"
    }
    text = {
        trigger = { always = yes }
        localization_key = "tooltip_available"
    }
}
```

#### Dynamic Warning
```
defined_text = {
    name = GetWarningText
    text = {
        trigger = {
            check_variable = { stability < 0.30 }
        }
        localization_key = "warning_low_stability"
    }
    text = {
        trigger = {
            check_variable = { manpower < 100000 }
        }
        localization_key = "warning_low_manpower"
    }
    text = {
        trigger = { always = yes }
        localization_key = "warning_none"
    }
}
```

## Template: Menu System

```
# Page titles
defined_text = {
    name = GetMenuPageTitle
    text = { trigger = { check_variable = { menu_page = 0 } } localization_key = "menu_page_0_title" }
    text = { trigger = { check_variable = { menu_page = 1 } } localization_key = "menu_page_1_title" }
    text = { trigger = { check_variable = { menu_page = 2 } } localization_key = "menu_page_2_title" }
}

# Page descriptions
defined_text = {
    name = GetMenuPageDesc
    text = { trigger = { check_variable = { menu_page = 0 } } localization_key = "menu_page_0_desc" }
    text = { trigger = { check_variable = { menu_page = 1 } } localization_key = "menu_page_1_desc" }
    text = { trigger = { check_variable = { menu_page = 2 } } localization_key = "menu_page_2_desc" }
}

# Page icons
defined_text = {
    name = GetMenuPageIcon
    text = { trigger = { check_variable = { menu_page = 0 } } localization_key = "GFX_menu_page_0" }
    text = { trigger = { check_variable = { menu_page = 1 } } localization_key = "GFX_menu_page_1" }
    text = { trigger = { check_variable = { menu_page = 2 } } localization_key = "GFX_menu_page_2" }
}
```

## Template: Objective System

```
# Objective title
defined_text = {
    name = GetObjectiveTitle
    text = {
        trigger = {
            check_variable = { objective_type = 1 }
        }
        localization_key = "objective_industrial_title"
    }
    text = {
        trigger = {
            check_variable = { objective_type = 2 }
        }
        localization_key = "objective_military_title"
    }
    text = {
        trigger = {
            check_variable = { objective_type = 3 }
        }
        localization_key = "objective_research_title"
    }
}

# Objective progress
defined_text = {
    name = GetObjectiveProgress
    text = {
        trigger = {
            check_variable = { objective_progress >= 1.0 }
        }
        localization_key = "objective_completed"
    }
    text = {
        trigger = {
            check_variable = { objective_progress >= 0.5 }
        }
        localization_key = "objective_halfway"
    }
    text = {
        trigger = { always = yes }
        localization_key = "objective_in_progress"
    }
}

# Objective status icon
defined_text = {
    name = GetObjectiveStatusIcon
    text = {
        trigger = { check_variable = { objective_progress >= 1.0 } }
        localization_key = "GFX_objective_complete"
    }
    text = {
        trigger = { check_variable = { objective_progress > 0.0 } }
        localization_key = "GFX_objective_progress"
    }
    text = {
        trigger = { always = yes }
        localization_key = "GFX_objective_locked"
    }
}
```

## Common Mistakes

### ❌ Wrong Order
```
# BAD - Generic always matches first
text = { trigger = { always = yes } localization_key = "generic" }
text = { trigger = { has_war = yes } localization_key = "war" }  # Never reached!
```

### ✅ Correct Order
```
# GOOD - Specific first, generic last
text = { trigger = { has_war = yes } localization_key = "war" }
text = { trigger = { always = yes } localization_key = "generic" }
```

### ❌ Missing Fallback
```
# BAD - No fallback if neither condition is true
text = { trigger = { has_war = yes } localization_key = "war" }
text = { trigger = { has_war = no } localization_key = "peace" }
# What if has_war is undefined?
```

### ✅ With Fallback
```
# GOOD - Always have a fallback
text = { trigger = { has_war = yes } localization_key = "war" }
text = { trigger = { always = yes } localization_key = "peace" }
```
