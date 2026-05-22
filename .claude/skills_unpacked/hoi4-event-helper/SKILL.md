---
name: hoi4-event-helper
version: 1.0.0
description: Helper for creating and managing events in Hearts of Iron IV mods - country events, news events, state events with options, triggers, and effects
tags: [hoi4, modding, events, country_event, news_event, state_event]
---

# HOI4 Event Helper

This skill helps you create and manage **events** in Hearts of Iron IV mods. Events are interactive pop-ups that appear during gameplay, allowing players to make choices that affect the game state.

## What are Events?

Events are interactive game elements that:
- Display narrative text and images to the player
- Offer choices (options) that trigger effects
- Can be triggered by various conditions (triggers)
- Can be country-specific, state-specific, or news events
- Are defined in `events/` directory
- Use localization files for text content

## Event Types

### Country Events (`country_event`)
- Trigger for a specific country
- Player sees the event if they control that country
- ROOT scope = country receiving the event
- FROM scope = country that triggered the event (if applicable)

### News Events (`news_event`)
- Global events shown to all or selected countries
- Used for major world events
- Can be shown to all major powers or custom sets

### State Events (`state_event`)
- Trigger for a specific state
- ROOT scope = state
- FROM scope = country owning the state (if applicable)

### Unit Leader Events (`unit_leader_event`)
- Trigger for specific unit leaders/generals
- ROOT scope = unit leader
- FROM scope = country owning the leader

---

## Using This Skill

### Step 1: Choose Action

Ask the user what they want to do:

1. **Create new event** - Generate a new event with options
2. **Find existing events** - Search for events in your mod
3. **Explain event mechanics** - Learn about event structure and mechanics

---

## Action 1: Create New Event

### Step 1.1: Choose Event Type

Ask the user which type of event they want to create:

- **country_event** - Event for a specific country
- **news_event** - Global news event
- **state_event** - Event for a specific state
- **unit_leader_event** - Event for a unit leader

### Step 1.2: Determine Event Properties

Ask the user for the following information:

#### Event ID
```
namespace.number
Example: my_mod.1
```

**Convention**:
- Use namespace matching your mod name
- Number events sequentially
- Related events should be grouped (e.g., `japanese_events.1`, `japanese_events.2`)

#### Event Title
```
Displayed as the event header
Example: "The Great War Begins"
```

#### Event Description
```
Main text describing the situation
Can have multiple versions based on triggers
Example: "Germany has declared war on Poland..."
```

#### Event Picture (Optional)
```
GFX reference for event image
Example: GFX_report_event_german_troops
```

### Step 1.3: Create Event Options

Events must have at least one option. Ask the user for:

**For each option:**

1. **Option Name** - Display text (e.g., "Accept", "Reject", "Declare War")
2. **Effects** - What happens when this option is chosen
3. **AI Factors** (optional) - How likely AI is to choose this option
4. **Trigger** (optional) - Conditions for this option to appear

**Common Option Patterns:**

**Simple Acknowledgment:**
```
option = {
    name = my_mod.1.a  # Localization key
}
```

**Option with Effects:**
```
option = {
    name = my_mod.1.a
    add_political_power = 50
    add_stability = 0.05
}
```

**Option with AI Factor:**
```
option = {
    name = my_mod.1.a
    add_war_support = 0.1
    ai_chance = {
        factor = 80
        modifier = {
            factor = 2
            has_government = fascism
        }
    }
}
```

**Conditional Option:**
```
option = {
    name = my_mod.1.a
    trigger = {
        has_political_power > 100
    }
    add_political_power = -100
    add_ideas = prepared_for_war
}
```

### Step 1.4: Add Event Triggers (Optional)

Ask if the event should only fire under certain conditions:

```
trigger = {
    # Conditions for event to fire
    has_war = yes
    has_government = democratic
    date > 1939.1.1
}
```

**Common Triggers:**
- `tag = GER` - Specific country
- `has_war = yes` - At war
- `has_government = ideology` - Government type
- `date > 1939.1.1` - After specific date
- `has_country_flag = flag_name` - Has flag set

### Step 1.5: Set Event Properties

Ask for additional properties:

#### Is Triggered Only?
```
is_triggered_only = yes  # Event can only be triggered by effects/on_actions
is_triggered_only = no   # Event can fire from MTTH
```

#### Mean Time To Happen (MTTH) - If not triggered only
```
mean_time_to_happen = {
    days = 30
    modifier = {
        factor = 0.5
        has_war = yes
    }
}
```

#### Fire Only Once?
```
fire_only_once = yes  # Event fires only once per game
fire_only_once = no   # Event can fire multiple times
```

#### Immediate Effects (Optional)
```
immediate = {
    # Effects that happen before event shows
    log = "Event fired for [Root.GetName]"
}
```

### Step 1.6: Generate Event Code

Based on user input, generate the complete event:

**Example 1: Simple Country Event**
```
namespace = my_mod

country_event = {
    id = my_mod.1
    title = my_mod.1.t
    desc = my_mod.1.d
    picture = GFX_report_event_german_troops

    is_triggered_only = yes

    option = {
        name = my_mod.1.a
        add_political_power = 50
    }
}
```

**Example 2: Country Event with Multiple Options**
```
namespace = my_mod

country_event = {
    id = my_mod.2
    title = my_mod.2.t
    desc = my_mod.2.d
    picture = GFX_report_event_diplomacy

    is_triggered_only = yes

    option = {
        name = my_mod.2.a  # Accept Alliance
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = alliance_accepted
            }
        }
        ai_chance = {
            factor = 70
        }
    }

    option = {
        name = my_mod.2.b  # Reject Alliance
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = alliance_rejected
            }
        }
        ai_chance = {
            factor = 30
        }
    }
}
```

**Example 3: News Event**
```
namespace = world_news

news_event = {
    id = world_news.1
    title = world_news.1.t
    desc = world_news.1.d
    picture = GFX_news_event_war_declared

    major = yes  # Show to all major powers
    is_triggered_only = yes

    option = {
        name = world_news.1.a  # Interesting...
        trigger = {
            NOT = { tag = GER }
            NOT = { tag = POL }
        }
    }

    option = {
        name = world_news.1.b  # For the Fatherland!
        trigger = { tag = GER }
    }

    option = {
        name = world_news.1.c  # We will resist!
        trigger = { tag = POL }
    }
}
```

**Example 4: Event with Conditional Descriptions**
```
namespace = my_mod

country_event = {
    id = my_mod.3
    title = my_mod.3.t

    desc = {
        text = my_mod.3.d_victory
        trigger = {
            has_war = no
        }
    }

    desc = {
        text = my_mod.3.d_defeat
        trigger = {
            has_war = yes
            surrender_progress > 0.5
        }
    }

    desc = {
        text = my_mod.3.d_default
    }

    picture = GFX_report_event_generic
    is_triggered_only = yes

    option = {
        name = my_mod.3.a
    }
}
```

**Example 5: Event Chain**
```
namespace = event_chain

# First event in chain
country_event = {
    id = event_chain.1
    title = event_chain.1.t
    desc = event_chain.1.d
    picture = GFX_report_event_generic

    is_triggered_only = yes

    option = {
        name = event_chain.1.a
        set_country_flag = event_chain_started
        country_event = {
            id = event_chain.2
            days = 7
        }
    }

    option = {
        name = event_chain.1.b
        # Chain ends here
    }
}

# Second event in chain
country_event = {
    id = event_chain.2
    title = event_chain.2.t
    desc = event_chain.2.d
    picture = GFX_report_event_generic

    is_triggered_only = yes

    trigger = {
        has_country_flag = event_chain_started
    }

    immediate = {
        clr_country_flag = event_chain_started
    }

    option = {
        name = event_chain.2.a
        add_political_power = 100
    }
}
```

### Step 1.7: Create Localization

Generate the localization file content for the event:

```yml
l_english:
    my_mod.1.t:0 "Event Title"
    my_mod.1.d:0 "Event description text goes here. You can use [Root.GetName] to reference the country name."
    my_mod.1.a:0 "Option A Text"
    my_mod.1.b:0 "Option B Text"
```

**Localization Tips:**
- Use `:0` suffix for version number
- Reference countries: `[Root.GetName]`, `[From.GetName]`
- Reference leaders: `[Root.GetLeader]`
- Use color codes: `§Y` (yellow), `§R` (red), `§G` (green)
- Line breaks: Use actual newlines in YAML

### Step 1.8: Choose File Location

Ask the user where to save the event:

**Options:**

- **Namespace file**: `events/[namespace]_events.txt`
  - Use for events grouped by theme/country
  - Example: `events/german_events.txt`, `events/my_mod_events.txt`

- **Country file**: `events/[TAG]_events.txt`
  - Use for country-specific events
  - Example: `events/GER_events.txt`

- **System file**: `events/_[system]_events.txt`
  - Use for custom system events
  - Example: `events/_economic_alliance_events.txt`

**Localization Location:**
- `localisation/english/[namespace]_l_english.yml`
- Example: `localisation/english/my_mod_events_l_english.yml`

### Step 1.9: Add to Files

Use the Write or Edit tool to:

1. Add event code to the appropriate events file
2. Add localization to the appropriate localization file

**For new event file:**
```
add_namespace = [namespace]

country_event = {
    # Event code here
}
```

**For existing event file:**
- Add the new event after existing events in the same namespace

### Step 1.10: Trigger the Event

Provide guidance on how to trigger the event:

**From Console (Testing):**
```
event my_mod.1
```

**From On_Actions:**
```
on_actions = {
    on_startup = {
        events = {
            my_mod.1
        }
    }
}
```

**From Effect:**
```
country_event = {
    id = my_mod.1
    days = 7
}
```

**From National Focus:**
```
completion_reward = {
    country_event = {
        id = my_mod.1
    }
}
```

**From Decision:**
```
complete_effect = {
    country_event = {
        id = my_mod.1
    }
}
```

---

## Action 2: Find Existing Events

### Search for Events

Use Grep to find existing events in your mod:

#### Find All Event Files
```
Pattern: country_event|news_event|state_event
Path: events/
Output: files_with_matches
```

#### Find Events by Namespace
```
Pattern: namespace = my_mod
Path: events/
Output: content
-A: 3
```

#### Find Events by ID
```
Pattern: id = my_mod\\.1
Path: events/
Output: content
-B: 2
-A: 20
```

#### Find Events with Specific Effects
```
Pattern: add_political_power
Path: events/
Output: content
-B: 5
```

#### Find Events with Specific Triggers
```
Pattern: has_war = yes
Path: events/
Output: content
-B: 10
```

#### Find News Events
```
Pattern: news_event\\s*=\\s*\\{
Path: events/
Output: content
-A: 15
```

### Read Specific Event File

Once you've found relevant files, use Read to examine them:

```
Read events/[filename].txt
```

---

## Action 3: Explain Event Mechanics

### Event Structure

**Basic Structure:**
```
namespace = [namespace]

[event_type] = {
    id = [namespace].[number]
    title = [localization_key]
    desc = [localization_key]
    picture = [GFX_reference]

    # Triggers (optional)
    trigger = {
        # Conditions
    }

    # Properties
    is_triggered_only = yes/no
    fire_only_once = yes/no
    major = yes/no  # News events only

    # Immediate effects (optional)
    immediate = {
        # Effects before event shows
    }

    # Mean time to happen (if not triggered only)
    mean_time_to_happen = {
        days = [number]
    }

    # Options (at least one required)
    option = {
        name = [localization_key]
        # Effects
        # AI chance
        # Trigger
    }
}
```

### Event Scopes

Understanding scopes is critical:

#### Country Events
```
country_event = {
    id = my_mod.1
    # ROOT = country receiving the event
    # FROM = country that triggered the event (if applicable)

    option = {
        name = my_mod.1.a
        ROOT = {
            # This country
        }
        FROM = {
            # Triggering country
        }
    }
}
```

#### News Events
```
news_event = {
    id = news.1
    # ROOT = varies by option
    # Each country sees the event and can have different options

    option = {
        name = news.1.a
        trigger = { tag = GER }
        # This option only appears for Germany
    }

    option = {
        name = news.1.b
        trigger = { NOT = { tag = GER } }
        # This option appears for everyone else
    }
}
```

#### State Events
```
state_event = {
    id = state.1
    # ROOT = state
    # FROM = country (usually state owner)

    option = {
        name = state.1.a
        FROM = {
            # Country scope
        }
        ROOT = {
            # State scope
        }
    }
}
```

### Event Triggering

#### From Effect (Immediate)
```
country_event = {
    id = my_mod.1
}
```

#### From Effect (Delayed)
```
country_event = {
    id = my_mod.1
    days = 7
}
```

#### From Effect (Random Delay)
```
country_event = {
    id = my_mod.1
    days = 7
    random_days = 3  # 7-10 days
}
```

#### Hidden Event
```
country_event = {
    id = my_mod.1
    hidden = yes  # Event fires but doesn't show to player
}
```

#### Target Different Country
```
# Trigger event for another country
GER = {
    country_event = {
        id = my_mod.1
    }
}
```

#### MTTH Events
```
country_event = {
    id = my_mod.1

    mean_time_to_happen = {
        days = 30  # Average 30 days

        modifier = {
            factor = 0.5  # Half the time
            has_war = yes
        }

        modifier = {
            factor = 2  # Twice as long
            has_idea = pacifism
        }
    }
}
```

### AI Behavior

**AI Chance:**
```
option = {
    name = my_mod.1.a

    ai_chance = {
        factor = 70  # Base 70% chance

        modifier = {
            factor = 2  # Double chance
            has_government = fascism
        }

        modifier = {
            factor = 0  # Never choose
            is_historical_focus_on = yes
        }
    }
}
```

**AI Historical Focus:**
```
option = {
    name = my_mod.1.a

    ai_chance = {
        base = 10
        modifier = {
            add = 90  # 100% total
            is_historical_focus_on = yes
        }
    }
}
```

### Conditional Descriptions

Events can have multiple descriptions based on conditions:

```
country_event = {
    id = my_mod.1
    title = my_mod.1.t

    desc = {
        text = my_mod.1.d_victory
        trigger = {
            has_war = no
            has_country_flag = won_war
        }
    }

    desc = {
        text = my_mod.1.d_defeat
        trigger = {
            has_war = no
            has_country_flag = lost_war
        }
    }

    desc = {
        text = my_mod.1.d_default
        # Default - always shown if no other desc triggers
    }
}
```

### Event Timeouts

Events can have timeouts that auto-select an option:

```
country_event = {
    id = my_mod.1

    timeout_days = 30

    option = {
        name = my_mod.1.a
        # Player's choice
    }

    option = {
        name = my_mod.1.b
        default = yes  # Auto-selected on timeout
    }
}
```

---

## Common Patterns

### Pattern 1: Simple Notification Event

Just inform the player, no meaningful choice:

```
country_event = {
    id = notification.1
    title = notification.1.t
    desc = notification.1.d
    picture = GFX_report_event_generic

    is_triggered_only = yes

    option = {
        name = notification.1.a  # "Understood"
    }
}
```

### Pattern 2: Choice Event with Trade-offs

Player chooses between different benefits:

```
country_event = {
    id = choice.1
    title = choice.1.t
    desc = choice.1.d
    picture = GFX_report_event_generic

    is_triggered_only = yes

    option = {
        name = choice.1.a  # Military focus
        add_political_power = -50
        army_experience = 25
    }

    option = {
        name = choice.1.b  # Economic focus
        add_political_power = -50
        add_stability = 0.05
    }

    option = {
        name = choice.1.c  # Do nothing
    }
}
```

### Pattern 3: Event Chain

Events that lead to other events:

```
# Start of chain
country_event = {
    id = chain.1
    title = chain.1.t
    desc = chain.1.d

    is_triggered_only = yes

    option = {
        name = chain.1.a
        set_country_flag = chain_path_a
        country_event = {
            id = chain.2
            days = 7
        }
    }

    option = {
        name = chain.1.b
        set_country_flag = chain_path_b
        country_event = {
            id = chain.3
            days = 7
        }
    }
}

# Path A continuation
country_event = {
    id = chain.2
    title = chain.2.t
    desc = chain.2.d

    is_triggered_only = yes

    trigger = {
        has_country_flag = chain_path_a
    }

    option = {
        name = chain.2.a
        clr_country_flag = chain_path_a
        # Effects
    }
}

# Path B continuation
country_event = {
    id = chain.3
    title = chain.3.t
    desc = chain.3.d

    is_triggered_only = yes

    trigger = {
        has_country_flag = chain_path_b
    }

    option = {
        name = chain.3.a
        clr_country_flag = chain_path_b
        # Effects
    }
}
```

### Pattern 4: Interactive Diplomacy Event

One country sends event to another:

```
# Trigger this from focus/decision/on_action
# GER = {
#     country_event = { id = diplomacy.1 }
# }
# POL = {
#     country_event = { id = diplomacy.2 }
# }

# Event for sender (GER)
country_event = {
    id = diplomacy.1
    title = diplomacy.1.t
    desc = diplomacy.1.d

    is_triggered_only = yes

    option = {
        name = diplomacy.1.a  # "We have sent the proposal"
    }
}

# Event for receiver (POL)
country_event = {
    id = diplomacy.2
    title = diplomacy.2.t
    desc = diplomacy.2.d

    is_triggered_only = yes

    option = {
        name = diplomacy.2.a  # Accept
        GER = {
            country_event = {
                id = diplomacy.3  # Acceptance notification
            }
        }
        # Accept effects
    }

    option = {
        name = diplomacy.2.b  # Reject
        GER = {
            country_event = {
                id = diplomacy.4  # Rejection notification
            }
        }
        # Reject effects
    }
}
```

### Pattern 5: Recurring MTTH Event

Event that can fire multiple times:

```
country_event = {
    id = recurring.1
    title = recurring.1.t
    desc = recurring.1.d
    picture = GFX_report_event_generic

    trigger = {
        has_war = yes
        manpower > 100000
    }

    mean_time_to_happen = {
        days = 60
    }

    option = {
        name = recurring.1.a
        add_manpower = -50000
        army_experience = 10
    }
}
```

### Pattern 6: Hidden Event (Script Only)

Event that fires but player doesn't see:

```
country_event = {
    id = hidden.1

    is_triggered_only = yes
    hidden = yes

    immediate = {
        # All effects in immediate
        set_variable = { check_counter += 1 }

        if = {
            limit = { check_var = { check_counter > 5 } }
            country_event = {
                id = visible.1  # Trigger visible event
            }
        }
    }

    option = {
        # Empty option required
    }
}
```

---

## Best Practices

1. **Localization**
   - Always use localization keys, never hardcode text
   - Keep localization files organized by namespace
   - Use descriptive key names (e.g., `my_mod.1.t` for title)

2. **Naming Conventions**
   - Use clear namespace names
   - Number events sequentially
   - Group related events (e.g., `war_events.1`, `war_events.2`)

3. **AI Behavior**
   - Always set AI chances for important choices
   - Consider historical AI behavior
   - Test AI decisions in game

4. **Performance**
   - Avoid heavy MTTH events
   - Use `is_triggered_only = yes` when possible
   - Optimize triggers for MTTH events

5. **Player Experience**
   - Provide meaningful choices
   - Avoid false choices (options with no real difference)
   - Use appropriate event pictures
   - Write engaging descriptions

6. **Testing**
   - Test all event paths
   - Verify localization displays correctly
   - Check scope context (ROOT/FROM)
   - Test AI behavior

7. **Event Chains**
   - Use flags to track chain progress
   - Clean up flags when chain ends
   - Provide clear narrative flow

---

## Reference Files

For detailed information, consult:
- `references/event_types_reference.md` - Complete event type documentation
- `references/event_effects_reference.md` - Common event effects and patterns
- `references/event_pictures_reference.md` - Available event pictures

---

## Tips

- Events are the primary way to create narrative content
- Use immediate effects for setup before event shows
- Hidden events are useful for scripting
- Event chains create compelling narratives
- News events create world atmosphere
- Always test events thoroughly before release
- Use flags to track player choices across events
- Consider both player and AI experience
