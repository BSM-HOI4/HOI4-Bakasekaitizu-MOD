---
name: hoi4-decisions-helper
version: 1.0.0
description: Helper for creating and managing decisions in Hearts of Iron IV mods - player-activated choices with costs, conditions, and effects
tags: [hoi4, modding, decisions, decision_categories]
---

# HOI4 Decisions Helper

This skill helps you create and manage **decisions** in Hearts of Iron IV mods. Decisions are player-activated choices that appear in the decisions menu, allowing countries to take specific actions with costs and effects.

## What are Decisions?

Decisions are player-activated actions that:
- Appear in the decisions interface
- Have availability conditions (when they appear)
- Have visible conditions (conditions to execute)
- Require resources/political power to activate
- Execute effects when taken
- Can be one-time or repeatable
- Are organized into categories
- Are defined in `common/decisions/`

## Decision Structure

### Decision Categories
Categories group related decisions and appear as tabs in the decisions menu:

```
category_name = {
    # Category icon
    icon = GFX_decision_category_icon

    # Category properties
    priority = 10

    # Category visibility
    visible = {
        # When category appears
    }

    # Category picture
    picture = GFX_category_picture
}
```

### Individual Decisions
Individual decisions within categories:

```
decision_name = {
    # Icon
    icon = GFX_decision_icon

    # Availability (when decision appears)
    available = {
        # Conditions
    }

    # Visibility (when decision shows)
    visible = {
        # Conditions
    }

    # Activation conditions
    activation = {
        # Conditions to activate
    }

    # Cost
    cost = 50  # Political power cost

    # Days to remove (cooldown)
    days_remove = 30
    days_re_enable = 60

    # Fire only once
    fire_only_once = yes/no

    # Effects
    complete_effect = {
        # Effects when completed
    }

    # Removal effects
    remove_effect = {
        # Effects when removed
    }

    # AI factors
    ai_will_do = {
        factor = 1
    }
}
```

---

## Using This Skill

### Step 1: Choose Action

Ask the user what they want to do:

1. **Create new decision** - Create a new decision with category
2. **Create decision category** - Create a category for organizing decisions
3. **Find existing decisions** - Search for decisions in your mod
4. **Explain decision mechanics** - Learn about decision types and patterns

---

## Action 1: Create New Decision

### Step 1.1: Choose or Create Category

Ask the user:
- Use existing category? (list categories from their mod)
- Create new category?

**If creating new category, ask:**
- Category internal name (e.g., `economic_decisions`)
- Category display name (localization key)
- Category icon
- Category visibility conditions

### Step 1.2: Determine Decision Type

Ask the user which type of decision:

1. **One-time decision** - Can only be taken once
   ```
   fire_only_once = yes
   ```

2. **Repeatable decision** - Can be taken multiple times
   ```
   fire_only_once = no
   ```

3. **Timed decision** - Takes time to complete
   ```
   days_remove = 30
   ```

4. **Mission decision** - Has ongoing effects with progress
   ```
   days_mission_timeout = 180
   ```

5. **Targeted decision** - Targets another country
   ```
   target_trigger = {
       FROM = {
           # Target conditions
       }
   }
   ```

### Step 1.3: Set Decision Properties

Ask the user for:

#### Decision Name
```
Internal name: economic_stimulus
Localization key: economic_stimulus (will create .t and .d keys)
```

#### Availability Conditions
When can the decision be taken?

**Common conditions:**
- Political power amount
- Has specific idea
- At war/peace
- Date requirements
- Resource requirements
- Flag checks

**Example:**
```
available = {
    has_political_power > 100
    has_war = no
    NOT = { has_idea = economic_stimulus_active }
}
```

#### Visibility Conditions
When does the decision appear?

**Example:**
```
visible = {
    has_government = democratic
    date > 1936.1.1
}
```

#### Cost
```
cost = 50  # Political power
```

**Special costs:**
```
# No cost
cost = 0

# Variable cost
cost = political_power_cost_var

# Command power cost
cost = 25
command_power = 25
```

#### Days to Complete/Remove
```
days_remove = 30        # Takes 30 days to complete
days_re_enable = 60     # 60 day cooldown before can take again
```

#### Effects
```
complete_effect = {
    # Effects when decision completes
}

remove_effect = {
    # Effects when time expires (for timed decisions)
}

modifier = {
    # Active modifiers while decision is active
}
```

### Step 1.4: Generate Decision Code

Based on user input, generate the complete decision code.

**Example 1: Simple One-Time Decision**
```
economic_decisions = {
    economic_stimulus = {
        icon = GFX_decision_generic_industry

        available = {
            has_political_power > 100
            has_war = no
        }

        visible = {
            has_government = democratic
        }

        cost = 100
        fire_only_once = yes

        complete_effect = {
            add_stability = 0.05
            add_political_power = -100
        }

        ai_will_do = {
            factor = 1
            modifier = {
                factor = 2
                has_stability < 0.5
            }
        }
    }
}
```

**Example 2: Timed Decision with Ongoing Effects**
```
military_decisions = {
    military_training_program = {
        icon = GFX_decision_generic_army

        available = {
            has_political_power > 50
        }

        visible = {
            has_war = yes
        }

        cost = 50
        days_remove = 60

        modifier = {
            army_org_factor = 0.05
            training_time_factor = -0.1
        }

        complete_effect = {
            army_experience = 10
        }

        ai_will_do = {
            factor = 1
        }
    }
}
```

**Example 3: Targeted Decision**
```
diplomatic_decisions = {
    demand_territory = {
        icon = GFX_decision_generic_prepare_civil_war

        target_trigger = {
            FROM = {
                is_neighbor_of = ROOT
                is_subject = no
                NOT = { has_war_with = ROOT }
            }
        }

        available = {
            has_political_power > 150
            FROM = {
                is_major = no
            }
        }

        visible = {
            FROM = {
                any_owned_state = {
                    is_core_of = ROOT
                }
            }
        }

        cost = 150
        fire_only_once = no
        days_re_enable = 365

        complete_effect = {
            FROM = {
                country_event = {
                    id = diplomatic_events.1
                }
            }
            custom_effect_tooltip = demand_territory_tt
        }

        ai_will_do = {
            factor = 1
            modifier = {
                factor = 0
                is_historical_focus_on = yes
            }
        }
    }
}
```

**Example 4: Mission Decision**
```
mission_decisions = {
    build_infrastructure_mission = {
        icon = GFX_decision_generic_construction

        available = {
            has_political_power > 25
        }

        activation = {
            # Conditions to activate mission
        }

        days_mission_timeout = 180

        cost = 25
        fire_only_once = no
        days_re_enable = 90

        timeout_effect = {
            # Effect when mission times out (fail)
        }

        complete_effect = {
            # Effect when mission completes (success)
            every_owned_state = {
                limit = {
                    has_state_flag = infrastructure_target
                }
                add_building_construction = {
                    type = infrastructure
                    level = 1
                    instant_build = yes
                }
            }
        }

        ai_will_do = {
            factor = 1
        }
    }
}
```

### Step 1.5: Create Decision Category (if new)

If creating new category:

```
category_name = {
    icon = GFX_decision_category_generic

    priority = 10

    visible = {
        # When category appears
        always = yes
    }

    allowed = {
        # Which countries can see this category
        original_tag = GER
    }
}
```

**Category Properties:**

- `icon` - Category icon (GFX reference)
- `picture` - Large picture for category
- `priority` - Display order (higher = shown first)
- `visible` - When category is visible
- `allowed` - Which countries can access

### Step 1.6: Create Localization

Generate localization entries:

```yml
l_english:
    # Category
    category_name:0 "Category Display Name"
    category_name_desc:0 "Category description"

    # Decision
    decision_name:0 "Decision Title"
    decision_name_desc:0 "Decision description explaining what it does and requirements."

    # Custom tooltips
    decision_name_tt:0 "Custom effect description"
```

### Step 1.7: Choose File Location

**Decision Files:**
- `common/decisions/[category_name].txt`
- Example: `common/decisions/economic_decisions.txt`

**Localization:**
- `localisation/english/[category_name]_l_english.yml`

### Step 1.8: Add to Files

Use Write/Edit tools to:
1. Create/update decision file
2. Create/update localization file

---

## Action 2: Create Decision Category

### Step 2.1: Gather Category Information

Ask user for:
- Internal name
- Display name (localization)
- Icon
- Priority (display order)
- Visibility conditions
- Allowed countries (optional)

### Step 2.2: Generate Category Code

```
category_name = {
    icon = GFX_decision_category_icon
    picture = GFX_category_picture

    priority = 50

    visible = {
        always = yes
    }

    allowed = {
        # Optional: restrict to specific countries
        original_tag = GER
    }
}
```

**Common Category Icons:**
```
GFX_decision_category_generic
GFX_decision_category_border_conflicts
GFX_decision_category_generic_crisis
GFX_decision_category_generic_economy
GFX_decision_category_generic_fascism
GFX_decision_category_generic_communism
GFX_decision_category_generic_democracy
```

---

## Action 3: Find Existing Decisions

### Search for Decisions

Use Grep to find decisions in your mod:

#### Find All Decision Files
```
Pattern: \w+\s*=\s*\{
Path: common/decisions/
Output: files_with_matches
```

#### Find Decision Categories
```
Pattern: ^[a-zA-Z_]+\s*=\s*\{
Path: common/decisions/
Output: content
-A: 5
```

#### Find Specific Decision
```
Pattern: decision_name\s*=\s*\{
Path: common/decisions/
Output: content
-B: 2
-A: 30
```

#### Find Decisions with Specific Effects
```
Pattern: add_political_power
Path: common/decisions/
Output: content
-B: 10
```

#### Find Targeted Decisions
```
Pattern: target_trigger
Path: common/decisions/
Output: content
-B: 5
-A: 10
```

#### Find Timed Decisions
```
Pattern: days_remove
Path: common/decisions/
Output: content
-B: 5
```

---

## Action 4: Explain Decision Mechanics

### Decision Types

#### Standard Decision
```
decision_name = {
    cost = 50
    fire_only_once = yes

    complete_effect = {
        # Immediate effect
    }
}
```

#### Timed Decision
```
decision_name = {
    cost = 50
    days_remove = 30

    modifier = {
        # Active modifiers during the 30 days
    }

    complete_effect = {
        # Effect when 30 days complete
    }
}
```

#### Targeted Decision
```
decision_name = {
    target_trigger = {
        FROM = {
            # Conditions for valid targets
        }
    }

    cost = 50

    complete_effect = {
        # ROOT = country taking decision
        # FROM = target country
    }
}
```

#### Mission Decision
```
decision_name = {
    activation = {
        # Conditions to start mission
    }

    is_good = yes  # Shows in "active missions"
    days_mission_timeout = 180

    timeout_effect = {
        # Failure effect
    }

    complete_effect = {
        # Success effect
    }
}
```

### Decision Properties Explained

#### available
Conditions that must be true to take the decision (greyed out if false)

#### visible
Conditions for decision to appear at all

#### activation
For mission decisions - conditions to activate

#### fire_only_once
`yes` = can only be taken once per game
`no` = can be taken multiple times

#### days_remove
Number of days before decision completes

#### days_re_enable
Cooldown period before decision can be taken again

#### cost
Political power cost (default)

#### command_power
Command power cost

#### modifier
Active modifiers while timed decision is active

#### complete_effect
Effects when decision completes

#### remove_effect
Effects when timed decision expires

#### timeout_effect
Effects when mission decision times out

---

## Common Patterns

### Pattern 1: Economic Boost Decision
```
economic_boost = {
    icon = GFX_decision_generic_industry

    available = {
        has_political_power > 100
    }

    cost = 100
    fire_only_once = no
    days_re_enable = 180

    complete_effect = {
        add_stability = 0.03
        random_owned_controlled_state = {
            limit = {
                is_core_of = ROOT
                free_building_slots = {
                    building = industrial_complex
                    size > 0
                }
            }
            add_extra_state_shared_building_slots = 1
        }
    }

    ai_will_do = {
        factor = 1
        modifier = {
            factor = 2
            has_stability < 0.5
        }
    }
}
```

### Pattern 2: Diplomatic Influence Decision
```
influence_neighbor = {
    icon = GFX_decision_generic_political_discourse

    target_trigger = {
        FROM = {
            is_neighbor_of = ROOT
            NOT = { is_in_faction_with = ROOT }
        }
    }

    available = {
        has_political_power > 75
        FROM = {
            NOT = { has_opinion = { target = ROOT value > 50 } }
        }
    }

    cost = 75
    fire_only_once = no
    days_re_enable = 90

    complete_effect = {
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = diplomatic_pressure
            }
        }
    }

    ai_will_do = {
        factor = 1
    }
}
```

### Pattern 3: Military Preparation Decision
```
prepare_for_war = {
    icon = GFX_decision_generic_prepare_civil_war

    available = {
        has_political_power > 150
        has_war = no
    }

    visible = {
        has_war = no
    }

    cost = 150
    days_remove = 90
    fire_only_once = yes

    modifier = {
        army_org_factor = 0.05
        training_time_factor = -0.15
        industrial_capacity_factory = 0.05
    }

    complete_effect = {
        army_experience = 25
        air_experience = 15
        add_war_support = 0.05
    }

    ai_will_do = {
        factor = 1
        modifier = {
            factor = 0
            has_war_support < 0.3
        }
    }
}
```

### Pattern 4: Research Boost Decision
```
research_initiative = {
    icon = GFX_decision_generic_research

    available = {
        has_political_power > 100
        num_of_factories > 20
    }

    cost = 100
    fire_only_once = no
    days_re_enable = 365

    complete_effect = {
        add_tech_bonus = {
            name = research_initiative_bonus
            bonus = 1.0
            uses = 2
            category = industry
        }
    }

    ai_will_do = {
        factor = 1
    }
}
```

### Pattern 5: Crisis Response Decision
```
respond_to_crisis = {
    icon = GFX_decision_generic_crisis

    available = {
        has_country_flag = crisis_active
        has_political_power > 50
    }

    visible = {
        has_country_flag = crisis_active
    }

    cost = 50
    fire_only_once = yes

    complete_effect = {
        clr_country_flag = crisis_active

        if = {
            limit = { has_stability < 0.5 }
            add_stability = 0.10
        }
        else = {
            add_political_power = 50
        }
    }

    ai_will_do = {
        factor = 100  # AI takes immediately
    }
}
```

---

## Best Practices

1. **Clear Conditions**
   - Make `available` conditions clear to player
   - Use tooltips to explain complex requirements

2. **Balanced Costs**
   - Don't make decisions too cheap (trivializes choices)
   - Don't make decisions too expensive (never used)
   - Consider cooldowns for repeatable decisions

3. **AI Behavior**
   - Always set `ai_will_do` factors
   - Consider historical AI behavior
   - Test AI decision-making

4. **Localization**
   - Write clear, descriptive titles
   - Explain effects in description
   - Use custom tooltips for complex effects

5. **Performance**
   - Avoid expensive checks in `visible`
   - Use flags to track decision states
   - Limit targeted decision target pools

6. **Player Experience**
   - Group related decisions in categories
   - Use appropriate icons
   - Provide meaningful choices

---

## Reference Files

For detailed information, consult:
- `references/decision_properties_reference.md` - Complete property documentation
- `references/decision_icons_reference.md` - Available decision icons
- `references/decision_patterns_reference.md` - Common decision patterns

---

## Tips

- Decisions are player-initiated, events are system-triggered
- Use targeted decisions for interactive diplomacy
- Timed decisions create strategic timing choices
- Mission decisions create long-term goals
- Always test AI behavior with decisions
- Use custom tooltips for clarity
- Consider decision category organization carefully
