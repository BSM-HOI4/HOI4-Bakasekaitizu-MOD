# HOI4 Decision Properties Reference

Complete reference for decision properties and mechanics.

---

## Decision Category Properties

### Basic Structure
```
category_name = {
    icon = GFX_reference
    picture = GFX_reference
    priority = 10
    visible = { }
    allowed = { }
}
```

### icon
**Type:** GFX reference
**Description:** Small icon shown in category tab

**Common values:**
```
GFX_decision_category_generic
GFX_decision_category_border_conflicts
GFX_decision_category_generic_crisis
GFX_decision_category_generic_economy
```

### picture
**Type:** GFX reference
**Description:** Large background picture for category

### priority
**Type:** Number
**Description:** Display order (higher = shown first)
**Default:** 0

**Example:**
```
priority = 100  # Shown first
priority = 1    # Shown last
```

### visible
**Type:** Trigger block
**Description:** Conditions for category to appear

**Example:**
```
visible = {
    always = yes
}

visible = {
    has_war = yes
}

visible = {
    OR = {
        tag = GER
        tag = SOV
    }
}
```

### allowed
**Type:** Trigger block
**Description:** Which countries can access category

**Example:**
```
allowed = {
    original_tag = GER
}

allowed = {
    is_major = yes
}
```

---

## Individual Decision Properties

### Basic Structure
```
decision_name = {
    icon = GFX_reference
    available = { }
    visible = { }
    activation = { }

    cost = 50
    fire_only_once = yes

    days_remove = 30
    days_re_enable = 60
    days_mission_timeout = 180

    modifier = { }
    complete_effect = { }
    remove_effect = { }
    timeout_effect = { }

    ai_will_do = { }
    war_with_target_on_remove = yes
    target_trigger = { }
    target_root_trigger = { }
    target_array = array_name

    state_target = yes
    on_map_mode = map_mode_name
}
```

---

## Core Properties

### icon
**Type:** GFX reference
**Description:** Icon shown for the decision

**Common icons:** See decision_icons_reference.md

### available
**Type:** Trigger block
**Description:** Conditions to execute decision (greyed out if false)

**Example:**
```
available = {
    has_political_power > 100
    has_war = no
    NOT = { has_idea = idea_name }
}
```

**Common checks:**
- Political power amount
- War status
- Ideas/modifiers
- Resource amounts
- Date
- Other decision states

### visible
**Type:** Trigger block
**Description:** Conditions for decision to appear at all

**Example:**
```
visible = {
    has_government = democratic
    NOT = { has_country_flag = decision_taken }
}
```

**Difference from available:**
- `visible = no` → Decision doesn't show
- `available = no` → Decision shows but greyed out

### activation
**Type:** Trigger block
**Description:** Conditions required to activate mission decisions

**Example:**
```
activation = {
    has_war = yes
    has_political_power > 50
}
```

---

## Cost Properties

### cost
**Type:** Number or variable
**Description:** Political power cost

**Examples:**
```
cost = 50              # Fixed cost
cost = 0               # Free
cost = my_cost_var     # Variable cost
```

### command_power
**Type:** Number
**Description:** Command power cost (in addition to PP)

**Example:**
```
cost = 25
command_power = 50
```

### custom_cost_trigger
**Type:** Trigger block
**Description:** Custom resource cost conditions

**Example:**
```
custom_cost_trigger = {
    has_equipment = {
        infantry_equipment > 1000
    }
}

custom_cost_text = equipment_cost_tt
```

### custom_cost_text
**Type:** Localization key
**Description:** Tooltip text for custom costs

---

## Timing Properties

### fire_only_once
**Type:** Boolean
**Description:** Whether decision can only be taken once

**Values:**
```
fire_only_once = yes   # Once per game
fire_only_once = no    # Repeatable
```

### days_remove
**Type:** Number
**Description:** Days until decision completes

**Example:**
```
days_remove = 30       # Completes after 30 days
```

**Use case:** Timed decisions with ongoing effects

### days_re_enable
**Type:** Number
**Description:** Cooldown before decision can be taken again

**Example:**
```
days_re_enable = 90    # 90 day cooldown
```

**Note:** Only works with `fire_only_once = no`

### days_mission_timeout
**Type:** Number
**Description:** Days before mission decision times out

**Example:**
```
days_mission_timeout = 180  # 180 days to complete mission
```

**Use case:** Mission-style decisions with success/failure

### fixed_random_seed
**Type:** Boolean
**Description:** Use fixed seed for random effects

---

## Effect Properties

### complete_effect
**Type:** Effect block
**Description:** Effects when decision completes

**Example:**
```
complete_effect = {
    add_political_power = 50
    add_stability = 0.05
}
```

### remove_effect
**Type:** Effect block
**Description:** Effects when timed decision expires

**Example:**
```
days_remove = 30

remove_effect = {
    # Runs after 30 days
    army_experience = 10
}
```

### timeout_effect
**Type:** Effect block
**Description:** Effects when mission times out (failure)

**Example:**
```
days_mission_timeout = 180

timeout_effect = {
    # Failure effects
    add_stability = -0.05
}

complete_effect = {
    # Success effects (manual completion)
    add_stability = 0.10
}
```

### modifier
**Type:** Modifier block
**Description:** Active modifiers during timed decision

**Example:**
```
days_remove = 60

modifier = {
    army_org_factor = 0.10
    training_time_factor = -0.15
}
```

**Note:** Only active while decision is running

---

## AI Properties

### ai_will_do
**Type:** MTTH block
**Description:** AI likelihood to take decision

**Basic:**
```
ai_will_do = {
    factor = 1
}
```

**With modifiers:**
```
ai_will_do = {
    base = 10

    modifier = {
        factor = 2
        has_war = yes
    }

    modifier = {
        factor = 0
        is_historical_focus_on = yes
    }
}
```

**Important:**
- `factor = 0` → AI never takes
- `factor = 1` → Base likelihood
- `factor = 2` → Twice as likely
- Higher final value = more likely

### ai_hint_pp_cost
**Type:** Number
**Description:** Hint to AI about PP cost (for planning)

---

## Targeted Decision Properties

### target_trigger
**Type:** Trigger block (FROM scope)
**Description:** Conditions for valid targets

**Example:**
```
target_trigger = {
    FROM = {
        is_neighbor_of = ROOT
        NOT = { has_war_with = ROOT }
        is_subject = no
    }
}
```

**Scopes:**
- ROOT = Country taking decision
- FROM = Potential target country

### target_root_trigger
**Type:** Trigger block (ROOT scope)
**Description:** Additional conditions for ROOT

**Example:**
```
target_root_trigger = {
    has_war = no
}
```

### target_array
**Type:** Variable array name
**Description:** Use array for target list

**Example:**
```
target_array = global.my_target_list
```

### war_with_target_on_remove
**Type:** Boolean
**Description:** Whether decision removes if at war with target

**Example:**
```
war_with_target_on_remove = yes
```

### war_with_target_on_complete
**Type:** Boolean
**Description:** Whether decision removes when taken if at war

---

## State Targeted Decisions

### state_target
**Type:** Boolean
**Description:** Decision targets states instead of countries

**Example:**
```
state_target = yes

target_trigger = {
    FROM = {
        # FROM = state
        is_controlled_by = ROOT
        is_core_of = ROOT
    }
}
```

### on_map_mode
**Type:** Map mode name
**Description:** Which map mode to show when selecting

**Example:**
```
on_map_mode = map_mode_state_owner
```

---

## Visibility and Display

### highlighted
**Type:** Boolean
**Description:** Whether to highlight decision

### highlight_state_targets
**Type:** Trigger block
**Description:** Conditions to highlight states

**Example:**
```
highlight_state_targets = {
    # Highlight states matching conditions
}
```

### custom_effect_tooltip
**Type:** Localization key
**Description:** Custom tooltip for effects

**Example:**
```
custom_effect_tooltip = my_decision_tt

hidden_effect = {
    # Actual effects
}
```

---

## Mission Decision Properties

### is_good
**Type:** Boolean
**Description:** Whether mission is "good" (shows in active missions)

**Example:**
```
is_good = yes
```

### selectable_mission
**Type:** Boolean
**Description:** Whether player can manually activate mission

### cancel_trigger
**Type:** Trigger block
**Description:** Conditions that cancel mission

**Example:**
```
cancel_trigger = {
    has_war = no
}
```

---

## Advanced Properties

### allowed
**Type:** Trigger block
**Description:** Which countries can see this specific decision

**Example:**
```
allowed = {
    original_tag = GER
}
```

### cancel_if_not_visible
**Type:** Boolean
**Description:** Cancel decision if visible conditions become false

### available_if_capitulated
**Type:** Boolean
**Description:** Whether decision available when capitulated

**Example:**
```
available_if_capitulated = yes
```

---

## Property Combinations

### Standard One-Time Decision
```
decision_name = {
    cost = 50
    fire_only_once = yes

    available = {
        has_political_power > 50
    }

    complete_effect = {
        # Effects
    }
}
```

### Repeatable with Cooldown
```
decision_name = {
    cost = 75
    fire_only_once = no
    days_re_enable = 90

    complete_effect = {
        # Effects
    }
}
```

### Timed Decision
```
decision_name = {
    cost = 100
    days_remove = 30

    modifier = {
        # Active for 30 days
    }

    remove_effect = {
        # After 30 days
    }
}
```

### Mission Decision
```
decision_name = {
    activation = {
        # Conditions to start
    }

    is_good = yes
    days_mission_timeout = 180

    timeout_effect = {
        # Failure
    }

    complete_effect = {
        # Success
    }
}
```

### Targeted Decision
```
decision_name = {
    target_trigger = {
        FROM = {
            # Target conditions
        }
    }

    cost = 50

    complete_effect = {
        # ROOT = taker
        # FROM = target
    }
}
```

---

## Common Mistakes

### Mistake 1: days_re_enable without fire_only_once
```
# WRONG
decision_name = {
    fire_only_once = yes
    days_re_enable = 90  # Does nothing!
}

# RIGHT
decision_name = {
    fire_only_once = no
    days_re_enable = 90
}
```

### Mistake 2: modifier without days_remove
```
# WRONG
decision_name = {
    modifier = {
        # Modifier never applies!
    }
}

# RIGHT
decision_name = {
    days_remove = 30
    modifier = {
        # Active for 30 days
    }
}
```

### Mistake 3: Confusing visible and available
```
# Less user-friendly
decision_name = {
    visible = {
        has_political_power > 100
    }
}
# Decision disappears when PP < 100

# Better
decision_name = {
    available = {
        has_political_power > 100
    }
}
# Decision shows but greyed out when PP < 100
```

### Mistake 4: Missing target_trigger for targeted decisions
```
# WRONG - no targets!
decision_name = {
    complete_effect = {
        FROM = {
            # FROM is undefined!
        }
    }
}

# RIGHT
decision_name = {
    target_trigger = {
        FROM = {
            # Define valid targets
        }
    }

    complete_effect = {
        FROM = {
            # FROM is now defined
        }
    }
}
```
