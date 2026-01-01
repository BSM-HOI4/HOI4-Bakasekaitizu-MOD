# HOI4 Event Types Reference

## Event Type Overview

| Event Type | Scope | Common Use Cases |
|------------|-------|------------------|
| `country_event` | Country | Most events, political events, decisions outcomes |
| `news_event` | Global/Major Powers | World events, war declarations, major changes |
| `state_event` | State | State-specific events, occupation, resistance |
| `unit_leader_event` | Unit Leader | General/Admiral events, promotions, deaths |

---

## Country Events

**Syntax:**
```
country_event = {
    id = namespace.number
    title = localization_key
    desc = localization_key
    picture = GFX_reference

    # Event properties
    is_triggered_only = yes/no
    fire_only_once = yes/no
    trigger = { }
    mean_time_to_happen = { }
    immediate = { }

    option = { }
}
```

**Scope:**
- ROOT = Country receiving the event
- FROM = Country that triggered the event (if applicable)

**Use Cases:**
- Political events
- Economic decisions
- Diplomatic interactions
- Focus tree outcomes
- Decision outcomes
- National flavor events

**Example:**
```
namespace = german_events

country_event = {
    id = german_events.1
    title = german_events.1.t
    desc = german_events.1.d
    picture = GFX_report_event_german_troops

    is_triggered_only = yes

    option = {
        name = german_events.1.a
        add_political_power = 50
    }

    option = {
        name = german_events.1.b
        add_stability = 0.05
    }
}
```

---

## News Events

**Syntax:**
```
news_event = {
    id = namespace.number
    title = localization_key
    desc = localization_key
    picture = GFX_reference

    # News event specific
    major = yes/no  # Show to all major powers
    is_triggered_only = yes/no
    fire_only_once = yes/no

    # Show to specific countries
    trigger = { }

    option = { }
}
```

**Scope:**
- Each country sees the event individually
- ROOT = Country viewing the event
- Options can be country-specific using triggers

**Properties:**
- `major = yes` - Shows to all major powers
- Can have different options for different countries
- Usually cosmetic (no major gameplay effects)

**Use Cases:**
- World war declarations
- Major victories/defeats
- Country capitulations
- Faction formations
- Historical milestones

**Example:**
```
namespace = world_news

news_event = {
    id = world_news.1
    title = world_news.1.t
    desc = world_news.1.d
    picture = GFX_news_event_war

    major = yes
    is_triggered_only = yes

    option = {
        name = world_news.1.a  # "Concerning..."
        trigger = {
            NOT = { tag = GER }
            NOT = { tag = POL }
        }
    }

    option = {
        name = world_news.1.b  # "For the Fatherland!"
        trigger = { tag = GER }
    }

    option = {
        name = world_news.1.c  # "We will defend!"
        trigger = { tag = POL }
    }
}
```

---

## State Events

**Syntax:**
```
state_event = {
    id = namespace.number
    title = localization_key
    desc = localization_key
    picture = GFX_reference

    is_triggered_only = yes/no
    fire_only_once = yes/no

    option = { }
}
```

**Scope:**
- ROOT = State
- FROM = Country (usually state owner)

**Use Cases:**
- State occupation events
- Resistance activity
- State-specific resources
- Local rebellions
- State development

**Example:**
```
namespace = state_events

state_event = {
    id = state_events.1
    title = state_events.1.t
    desc = state_events.1.d
    picture = GFX_report_event_riot

    is_triggered_only = yes

    option = {
        name = state_events.1.a
        FROM = {
            # Country scope (state owner)
            add_political_power = -25
        }
        ROOT = {
            # State scope
            add_resistance = 10
        }
    }
}
```

---

## Unit Leader Events

**Syntax:**
```
unit_leader_event = {
    id = namespace.number
    title = localization_key
    desc = localization_key
    picture = GFX_reference

    is_triggered_only = yes/no

    option = { }
}
```

**Scope:**
- ROOT = Unit leader (general/admiral)
- FROM = Country owning the leader

**Use Cases:**
- General promotion events
- Trait acquisition
- Leader death/retirement
- Combat experiences
- Personal storylines

**Example:**
```
namespace = leader_events

unit_leader_event = {
    id = leader_events.1
    title = leader_events.1.t
    desc = leader_events.1.d
    picture = GFX_report_event_military_planning

    is_triggered_only = yes

    option = {
        name = leader_events.1.a
        ROOT = {
            # Unit leader scope
            add_unit_leader_trait = brilliant_strategist
        }
    }
}
```

---

## Event Properties

### is_triggered_only

**Values:** `yes` or `no`

**Description:**
- `yes` = Event can only be triggered by effects, on_actions, or console
- `no` = Event uses MTTH (mean time to happen) system

**Usage:**
```
is_triggered_only = yes  # Most events
is_triggered_only = no   # MTTH events
```

### fire_only_once

**Values:** `yes` or `no`

**Description:**
- `yes` = Event fires only once per game
- `no` = Event can fire multiple times

**Usage:**
```
fire_only_once = yes  # Unique historical events
fire_only_once = no   # Recurring events
```

### major (News Events Only)

**Values:** `yes` or `no`

**Description:**
- `yes` = Show to all major powers
- `no` = Show based on trigger conditions

**Usage:**
```
major = yes  # World war declaration
major = no   # Regional event
```

### hidden

**Values:** `yes` or `no`

**Description:**
- `yes` = Event fires but doesn't show popup
- `no` = Normal visible event

**Usage:**
```
hidden = yes  # Scripting event
hidden = no   # Normal event
```

### timeout_days

**Type:** Number

**Description:** Number of days before event auto-closes

**Usage:**
```
timeout_days = 30

option = {
    name = event.1.a
    # Player choice
}

option = {
    name = event.1.b
    default = yes  # Auto-selected on timeout
}
```

---

## Trigger Conditions

Events can have triggers that determine when they can fire:

```
trigger = {
    # Date conditions
    date > 1939.1.1
    date < 1945.1.1

    # Country conditions
    tag = GER
    has_government = fascism
    has_war = yes
    is_major = yes

    # Resource conditions
    has_political_power > 100
    has_manpower > 10000

    # Flag conditions
    has_country_flag = flag_name
    NOT = { has_global_flag = event_fired }

    # State conditions (for state events)
    is_coastal = yes
    is_controlled_by = GER

    # Complex conditions
    OR = {
        tag = GER
        tag = ITA
        tag = JAP
    }

    AND = {
        has_war = yes
        surrender_progress > 0.5
    }
}
```

---

## Mean Time To Happen (MTTH)

For events with `is_triggered_only = no`:

```
mean_time_to_happen = {
    days = 30  # Base: event fires on average every 30 days

    # Modifiers change the frequency
    modifier = {
        factor = 0.5  # Half the time (fires more often)
        has_war = yes
    }

    modifier = {
        factor = 2  # Double the time (fires less often)
        has_stability > 0.7
    }

    modifier = {
        factor = 0  # Never fires
        has_country_flag = event_disabled
    }
}
```

**Understanding Factors:**
- `factor = 0.5` = Event fires TWICE as often
- `factor = 2` = Event fires HALF as often
- `factor = 0` = Event NEVER fires
- Factors are multiplicative

**Example:**
```
mean_time_to_happen = {
    days = 60  # Base 60 days

    modifier = {
        factor = 0.5  # 30 days
        has_war = yes
    }

    modifier = {
        factor = 0.5  # 15 days total
        has_government = fascism
    }
}
# If both conditions are true: 60 * 0.5 * 0.5 = 15 days average
```

---

## Immediate Effects

Effects that execute before the event shows:

```
immediate = {
    # Logging
    log = "[GetDateText]: Event fired for [Root.GetName]"

    # Set flags
    set_country_flag = event_in_progress

    # Save scopes
    save_event_target_as = original_target

    # Variable calculations
    set_variable = { temp_value = political_power }
}
```

**Common Uses:**
- Logging for debugging
- Saving scope targets
- Setting flags
- Variable calculations
- One-time setup

---

## Conditional Descriptions

Events can have multiple descriptions based on conditions:

```
country_event = {
    id = event.1
    title = event.1.t

    # Multiple descriptions - first matching trigger is used
    desc = {
        text = event.1.d_winning
        trigger = {
            has_war = yes
            surrender_progress < 0.2
        }
    }

    desc = {
        text = event.1.d_losing
        trigger = {
            has_war = yes
            surrender_progress > 0.5
        }
    }

    desc = {
        text = event.1.d_default
        # No trigger = default, always shows if no other matches
    }

    picture = GFX_report_event_generic
    is_triggered_only = yes

    option = {
        name = event.1.a
    }
}
```

---

## Event Options

Every event must have at least one option:

### Basic Option
```
option = {
    name = localization_key
}
```

### Option with Effects
```
option = {
    name = event.1.a
    add_political_power = 50
    add_stability = 0.05
}
```

### Conditional Option
```
option = {
    name = event.1.a
    trigger = {
        has_political_power > 100
    }
    add_political_power = -100
    army_experience = 25
}
```

### Option with AI Chance
```
option = {
    name = event.1.a
    ai_chance = {
        factor = 70
        modifier = {
            factor = 2
            has_government = fascism
        }
    }
}
```

### Default Option (for timeouts)
```
option = {
    name = event.1.a
    default = yes  # Selected on timeout
}
```

---

## Scope Switching in Events

### Country Events

```
country_event = {
    id = event.1

    option = {
        name = event.1.a

        # Current country (ROOT)
        add_political_power = 50

        # Explicit ROOT
        ROOT = {
            add_stability = 0.05
        }

        # Triggering country (FROM)
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = positive_relations
            }
        }

        # Other countries
        GER = {
            country_event = { id = event.2 }
        }

        every_country = {
            limit = { is_major = yes }
            country_event = { id = event.3 }
        }
    }
}
```

### State Events

```
state_event = {
    id = state_event.1

    option = {
        name = state_event.1.a

        # Current state (ROOT)
        add_building_construction = {
            type = industrial_complex
            level = 1
            instant_build = yes
        }

        # State owner (FROM)
        FROM = {
            add_political_power = -25
        }

        # Other states
        123 = {
            # State ID 123
        }
    }
}
```

---

## Best Practices by Event Type

### Country Events
- Use for most gameplay events
- Always consider AI behavior
- Provide meaningful choices
- Use flags to track player decisions

### News Events
- Keep effects minimal or cosmetic
- Use `major = yes` for important world events
- Provide different options for involved countries
- Use appropriate dramatic descriptions

### State Events
- Use sparingly (performance)
- Focus on state-specific situations
- Remember ROOT = state, FROM = country

### Unit Leader Events
- Use for character development
- Trait acquisition
- Personal storylines
- Rare compared to country events

---

## Common Mistakes

### Mistake 1: Wrong Scope
```
# WRONG - trying to add PP to a state
state_event = {
    option = {
        add_political_power = 50  # States don't have PP!
    }
}

# RIGHT
state_event = {
    option = {
        FROM = {
            # Country scope
            add_political_power = 50
        }
    }
}
```

### Mistake 2: Missing is_triggered_only
```
# WRONG - MTTH event without mean_time_to_happen
country_event = {
    id = event.1
    # No is_triggered_only and no mean_time_to_happen
}

# RIGHT
country_event = {
    id = event.1
    is_triggered_only = yes
}
```

### Mistake 3: No Options
```
# WRONG - events need at least one option
country_event = {
    id = event.1
    title = event.1.t
    desc = event.1.d
    # No options!
}

# RIGHT
country_event = {
    id = event.1
    title = event.1.t
    desc = event.1.d

    option = {
        name = event.1.a
    }
}
```

### Mistake 4: Hardcoded Text
```
# WRONG - hardcoded text
country_event = {
    title = "My Event"
    desc = "This is my event description"
}

# RIGHT - localization keys
country_event = {
    title = my_mod.1.t
    desc = my_mod.1.d
}
```
