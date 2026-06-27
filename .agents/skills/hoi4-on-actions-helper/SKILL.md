---
name: hoi4-on-actions-helper
version: 1.0.0
description: Helper for creating and managing on_actions in Hearts of Iron IV mods - event handlers that trigger automatically on game events
tags: [hoi4, modding, on_actions, events, triggers]
---

# HOI4 On Actions Helper

This skill helps you create and manage **on_actions** in Hearts of Iron IV mods. On_actions are event handlers that automatically trigger effects or events when specific game events occur (e.g., game start, war declaration, capitulation).

## What are On Actions?

On_actions are automatic event triggers that:
- Execute effects when specific game events occur
- Can trigger country events, news events, or immediate effects
- Work with specific scopes (ROOT and FROM)
- Are defined in `common/on_actions/`
- Can be time-based (daily, weekly, monthly) or event-based

## File Structure

On_actions are defined in `.txt` files in `common/on_actions/`:

```
on_actions = {
    on_[event_name] = {
        effect = {
            # Immediate effects
        }
        random_events = {
            # Weighted random events
        }
        events = {
            # Sequential events
        }
    }
}
```

---

## Using This Skill

### Step 1: Choose Action

Ask the user what they want to do:

1. **Create new on_action handler** - Add effects/events to a game event
2. **Find existing on_actions** - Search for on_actions in your mod
3. **Explain on_action types** - Learn about available on_actions and their scopes

---

## Action 1: Create New On_Action Handler

### Step 1.1: Choose On_Action Type

Ask the user which type of on_action they want to use:

#### Game Lifecycle Events
- `on_startup` - Fires once when game starts
- `on_daily` - Fires every day for every country
- `on_weekly` - Fires every week for every country
- `on_monthly` - Fires every month for every country

#### War and Diplomacy Events
- `on_declare_war` - When a country declares war (ROOT = attacker, FROM = defender)
- `on_war` - When war starts (ROOT = country at war)
- `on_war_relation_added` - When war relation is added (always fires)
- `on_capitulation` - When a country capitulates (ROOT = loser, FROM = winner)
- `on_capitulation_immediate` - Fires before capitulation processing
- `on_uncapitulation` - When a country recovers from capitulation
- `on_peace` - When peace is made
- `on_peaceconference_started` - When peace conference begins
- `on_peaceconference_ended` - When peace conference ends

#### Faction Events
- `on_create_faction` - When a faction is created (ROOT = creator)
- `on_faction_formed` - When a faction is formed
- `on_join_faction` - When a country joins a faction (ROOT = joiner, FROM = faction leader)
- `on_offer_join_faction` - When a country is invited to join (ROOT = inviter, FROM = invitee)
- `on_leave_faction` - When a country leaves a faction

#### Puppet and Subject Events
- `on_puppet` - When a country becomes a puppet (ROOT = puppet, FROM = overlord)
- `on_release_as_puppet` - When a country is released as puppet
- `on_release_as_free` - When a country is released as free nation
- `on_subject_free` - When a subject becomes free
- `on_subject_autonomy_level_change` - When autonomy level changes
- `on_subject_annexed` - When subject is annexed

#### Government Events
- `on_government_change` - When government ideology changes
- `on_ruling_party_change` - When ruling party changes
- `on_coup_succeeded` - When a coup succeeds
- `on_civil_war_end` - When civil war ends (ROOT = winner, FROM = loser)
- `on_civil_war_end_before_annexation` - Before civil war loser is annexed

#### State and Territory Events
- `on_state_control_changed` - When state control changes (ROOT = state, FROM = new controller)
- `on_annex` - When a country is annexed (ROOT = annexed, FROM = annexer)

#### Military Events
- `on_nuke_drop` - When a nuke is dropped (ROOT = state, FROM = country that dropped)
- `on_naval_invasion` - When naval invasion lands
- `on_paradrop` - When paratroopers drop
- `on_units_paradropped_in_state` - When units paradrop into state
- `on_border_war_lost` - When border war is lost

#### Army Leader Events
- `on_army_leader_daily` - Daily for each army leader
- `on_army_leader_won_combat` - When army leader wins combat
- `on_army_leader_lost_combat` - When army leader loses combat
- `on_army_leader_promoted` - When army leader is promoted
- `on_unit_leader_promote_from_ranks_veteran` - When veteran is promoted
- `on_unit_leader_promote_from_ranks_green` - When green unit is promoted

#### Operative Events (La Résistance DLC)
- `on_operative_on_mission_spotted` - When operative is spotted
- `on_operative_captured` - When operative is captured
- `on_operative_death` - When operative dies
- `on_operative_detected_during_operation` - When operative detected during operation
- `on_operation_completed` - When operation completes

#### Other Events
- `on_new_term_election` - When election occurs
- `on_ace_promoted` - When ace pilot is promoted
- `on_ace_killed` - When ace is killed
- `on_justifying_wargoal_pulse` - During war goal justification
- `on_wargoal_expire` - When war goal expires

### Step 1.2: Determine Execution Type

Ask how the on_action should execute:

1. **Immediate effect** - Execute effects directly
   ```
   on_[event_name] = {
       effect = {
           # Effects here
       }
   }
   ```

2. **Trigger events** - Fire one or more events
   ```
   on_[event_name] = {
       events = {
           event_id.1
           event_id.2
       }
   }
   ```

3. **Random events** - Fire weighted random events
   ```
   on_[event_name] = {
       random_events = {
           100 = event_id.1
           50 = event_id.2
       }
   }
   ```

### Step 1.3: Understand Scopes

**Critical**: Different on_actions have different scopes for ROOT and FROM.

Ask user to confirm scope understanding:

**Common Scope Patterns:**

**Country → Country:**
- `on_declare_war`: ROOT = attacker, FROM = defender
- `on_capitulation`: ROOT = capitulated country, FROM = winner
- `on_puppet`: ROOT = puppet, FROM = overlord
- `on_join_faction`: ROOT = joiner, FROM = faction leader

**Country Scope Only:**
- `on_startup`: ROOT = each country
- `on_daily/weekly/monthly`: ROOT = each country
- `on_war`: ROOT = country at war

**State Scope:**
- `on_state_control_changed`: ROOT = state, FROM = new controller
- `on_nuke_drop`: ROOT = state, FROM = nuking country

### Step 1.4: Write the Effect/Event Trigger

Based on user requirements, generate the on_action code:

**Example 1: Immediate Effect (Startup)**
```
on_actions = {
    on_startup = {
        effect = {
            every_country = {
                limit = { tag = GER }
                add_political_power = 100
            }
        }
    }
}
```

**Example 2: Trigger Events (War Declaration)**
```
on_actions = {
    on_declare_war = {
        events = {
            my_mod.1  # ROOT = attacker, FROM = defender
        }
    }
}
```

**Example 3: Random Events (Capitulation)**
```
on_actions = {
    on_capitulation = {
        random_events = {
            100 = capitulation.1
            50 = capitulation.2
            25 = capitulation.3
        }
    }
}
```

**Example 4: Weekly Update (BSM Pattern)**
```
on_actions = {
    on_weekly = {
        effect = {
            bsm_update_economic_alliance_power_share = yes
        }
    }
}
```

**Example 5: Complex Conditional (SSW Pattern)**
```
on_actions = {
    on_peaceconference_ended = {
        effect = {
            ROOT = {
                if = {
                    limit = {
                        is_ai = yes
                        has_government = democratic_ideology
                    }
                    # Switch to peacetime economy
                    add_ideas = partial_economic_mobilisation
                }
            }
        }
    }
}
```

### Step 1.5: Choose File Location

Ask the user where to save the on_action:

**Options:**

- **System-specific file**: `common/on_actions/_[system]_on_actions.txt`
  - Use for custom systems (e.g., `_bsm_economic_alliance_on_actions.txt`)
  - Example: Economic alliance update system

- **Country-specific file**: `common/on_actions/[TAG]_on_actions.txt`
  - Use for country-specific handlers
  - Example: `GER_on_actions.txt` for German events

- **Event-specific file**: `common/on_actions/_[event_type]_on_actions.txt`
  - Use for specific event categories
  - Example: `_capitulations.txt` for all capitulation handlers

- **Main file**: `common/on_actions/00_on_actions.txt`
  - Use for mod-wide general handlers
  - Example: Startup initialization

### Step 1.6: Add to File

Use the Edit tool to add the on_action to the chosen file:

1. If file doesn't exist, create it with:
   ```
   on_actions = {
       [new on_action here]
   }
   ```

2. If file exists, add the new on_action inside the `on_actions = { }` block

**Important**: If the on_action already exists in the file, you're **adding** to it, not replacing it. Multiple effects/events can coexist in the same on_action.

### Step 1.7: Test the On_Action

Provide testing guidance:

**For `on_startup`:**
```
Start a new game and check console logs or observe effects
```

**For war events:**
```
Use console command:
tag GER
declare_war_on FRA
# Observe if on_declare_war fires
```

**For time-based events:**
```
Use console command:
observe
# Watch logs as time passes
```

**Debugging:**
```
Add log statements to track execution:
on_capitulation = {
    effect = {
        log = "[GetDateText]: [ROOT.GetName] capitulated to [FROM.GetName]"
        # Your effects here
    }
}
```

---

## Action 2: Find Existing On_Actions

### Search for On_Actions

Use Grep to find existing on_actions in your mod:

#### Find All On_Action Files

```
Pattern: on_actions
Path: common/on_actions/
Output: files_with_matches
```

#### Find Specific On_Action Type

**Find startup handlers:**
```
Pattern: on_startup\s*=\s*\{
Path: common/on_actions/
Output: content
-B: 2
```

**Find capitulation handlers:**
```
Pattern: on_capitulation\s*=\s*\{
Path: common/on_actions/
Output: content
-B: 2
```

**Find war declaration handlers:**
```
Pattern: on_declare_war\s*=\s*\{
Path: common/on_actions/
Output: content
-B: 2
```

#### Find On_Actions by Effect

**Find on_actions that trigger events:**
```
Pattern: events\s*=\s*\{
Path: common/on_actions/
Output: content
-B: 5
```

**Find on_actions with immediate effects:**
```
Pattern: effect\s*=\s*\{
Path: common/on_actions/
Output: content
-B: 3
```

### Read Specific File

Once you've found relevant files, use Read to examine them:

```
Read common/on_actions/[filename].txt
```

---

## Action 3: Explain On_Action Mechanics

### Execution Order

When an on_action fires, it executes in this order:

1. **Immediate effects** in `effect = { }`
2. **Sequential events** in `events = { }`
3. **Random events** in `random_events = { }` (one selected randomly based on weights)

**Example:**
```
on_startup = {
    effect = {
        # Executes first
        set_variable = { initialized = 1 }
    }
    events = {
        # Executes second (all events)
        startup.1
        startup.2
    }
    random_events = {
        # Executes third (one random event)
        100 = startup.10
        50 = startup.11
    }
}
```

### Scope Context

Understanding ROOT and FROM is critical:

#### Country-to-Country Events

```
on_declare_war = {
    effect = {
        # ROOT = attacker
        # FROM = defender

        ROOT = {
            log = "We declared war!"
        }
        FROM = {
            log = "War was declared on us!"
        }
    }
}
```

#### Country Events

```
on_startup = {
    effect = {
        # Runs for EVERY country
        # ROOT = current country
        # FROM = not defined

        if = {
            limit = { tag = GER }
            log = "Germany starting up"
        }
    }
}
```

#### State Events

```
on_state_control_changed = {
    effect = {
        # ROOT = state
        # FROM = new controller (country)

        FROM = {
            # Country scope
            log = "[This.GetName] took control of [ROOT.GetName]"
        }
    }
}
```

### Multiple Handlers

You can have multiple handlers for the same on_action across different files. They **all execute**.

**Example:**
```
# In file A:
on_actions = {
    on_startup = {
        effect = {
            log = "Handler A"
        }
    }
}

# In file B:
on_actions = {
    on_startup = {
        effect = {
            log = "Handler B"
        }
    }
}

# Result: Both handlers execute
```

### Time-Based On_Actions

Time-based on_actions fire for **every country**:

```
on_daily = {
    effect = {
        # Fires EVERY DAY for EVERY COUNTRY
        # Use limits to restrict execution

        if = {
            limit = {
                tag = GER
                has_war = yes
            }
            add_war_support = 0.001
        }
    }
}
```

**Performance Warning**: Time-based on_actions (especially `on_daily`) can impact performance if they execute heavy logic for all countries. Use limits and early returns.

### Event Firing from On_Actions

**Direct event firing:**
```
on_capitulation = {
    events = {
        my_mod.1  # Fires immediately
    }
}
```

**Delayed event firing:**
```
on_capitulation = {
    effect = {
        ROOT = {
            country_event = {
                id = my_mod.1
                days = 7
            }
        }
    }
}
```

**Random event selection:**
```
on_capitulation = {
    random_events = {
        100 = my_mod.1   # 100/(100+50) = 66.7% chance
        50 = my_mod.2    # 50/(100+50) = 33.3% chance
    }
}
```

---

## Common Patterns

### Pattern 1: Startup Initialization

Initialize variables, arrays, and game state when game starts.

```
on_startup = {
    effect = {
        # Set global variables
        set_variable = { global.system_initialized = 1 }

        # Initialize all countries
        every_country = {
            set_variable = { country_points = 0 }
        }

        # Set state flags
        every_state = {
            limit = { is_coastal = yes }
            set_state_flag = is_coastal_state
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        # Setup arrays
        add_to_array = { global.indian_warlord = AZH }
        add_to_array = { global.indian_warlord = HND }
        add_to_array = { global.indian_warlord = IND }

        # Coalition setup
        FIN = {
            set_temp_variable = { coalition_patry = token:social_democracy }
            add_coalition_patry = yes
        }
    }
}
```

### Pattern 2: War Cleanup on Capitulation

Clean up systems when a country capitulates.

```
on_capitulation = {
    effect = {
        if = {
            limit = {
                ROOT = { num_subjects > 0 }
            }
            every_other_country = {
                limit = { is_subject_of = ROOT }
                ROOT = { end_puppet = PREV }
            }
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_capitulation = {
    effect = {
        # Free all puppets
        if = {
            limit = { ROOT = { num_subjects > 0 } }
            every_other_country = {
                limit = { is_subject_of = ROOT }
                ROOT = { end_puppet = PREV }
            }
        }

        # Leave economic spheres
        if = {
            limit = { ROOT = { tag = ALF } }
            every_country = {
                limit = { is_in_es_ALF_economic_spheres = yes }
                es_leave_economic_sphere_single = yes
            }
        }
    }
}
```

### Pattern 3: Periodic System Updates

Update custom systems on a schedule.

```
on_weekly = {
    effect = {
        # Update economic alliance system
        bsm_update_economic_alliance_power_share = yes

        # Update state variables
        every_state = {
            limit = { has_state_flag = tracked_state }
            owner = {
                # Update owner's tracking
            }
        }
    }
}
```

**Real Example from BSM_mod:**
```
on_weekly = {
    effect = {
        bsm_update_economic_alliance_power_share = yes
    }
}
```

### Pattern 4: AI Behavior Adjustment

Adjust AI behavior based on game events.

```
on_peaceconference_ended = {
    effect = {
        ROOT = {
            if = {
                limit = {
                    is_ai = yes
                    has_government = democratic_ideology
                }
                # Switch to peacetime economy
                if = {
                    limit = { has_idea = war_economy }
                    add_ideas = partial_economic_mobilisation
                }
            }
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_peaceconference_ended = {
    effect = {
        ROOT = {
            if = {
                limit = {
                    is_ai = yes
                    OR = {
                        has_government = authoritarian_democracy
                        has_government = liberal_democracy
                    }
                }
                if = {
                    limit = { has_idea = war_economy }
                    add_ideas = partial_economic_mobilisation
                    add_political_power = -150
                }
            }
        }
    }
}
```

### Pattern 5: State Control Tracking

Track when states change hands.

```
on_state_control_changed = {
    effect = {
        # ROOT = state
        # FROM = new controller

        FROM = {
            # New controller scope
            country_event = {
                id = state_captured.1
                days = 1
            }
        }

        # Set state flag
        ROOT = {
            set_state_flag = recently_captured
        }
    }
}
```

### Pattern 6: Government Change Cleanup

Clean up coalition parties when government changes.

```
on_ruling_party_change = {
    effect = {
        if = {
            limit = { has_government = totalitarian_socialism }
            set_temp_variable = { coalition_patry = token:totalitarian_socialism }
            remove_coalition_patry = yes
        }
        # ... other ideologies
    }
}
```

**Real Example from SSW_mod:**
```
on_ruling_party_change = {
    effect = {
        if = {
            limit = { has_government = totalitarian_socialism }
            set_temp_variable = { coalition_patry = token:totalitarian_socialism }
            remove_coalition_patry = yes
        }
        else_if = {
            limit = { has_government = radical_socialism }
            set_temp_variable = { coalition_patry = token:radical_socialism }
            remove_coalition_patry = yes
        }
        # ... continues for all ideologies
    }
}
```

---

## Best Practices

1. **Performance First**
   - Avoid heavy operations in `on_daily` (use `on_weekly` or `on_monthly` instead)
   - Use limits to restrict execution to relevant countries
   - Use early returns to skip unnecessary processing

2. **Scope Awareness**
   - Always document which scope is ROOT and FROM
   - Test scope context with log statements
   - Remember that time-based on_actions run for every country

3. **File Organization**
   - Group related on_actions in the same file
   - Use descriptive file names (e.g., `_capitulations.txt`, `_faction_system.txt`)
   - Country-specific on_actions in country files

4. **Debugging**
   - Add log statements to track execution
   - Use `log = "[GetDateText]: [event description]"`
   - Test thoroughly in different scenarios

5. **Multiple Handlers**
   - Remember that multiple handlers for the same on_action all execute
   - Don't duplicate logic across files
   - Consider using scripted effects for shared code

6. **Event Triggers**
   - Use `events = {}` for sequential events
   - Use `random_events = {}` for weighted random selection
   - Use `effect = {}` for immediate execution

---

## Common Use Cases

### Game Initialization
```
on_startup = {
    effect = {
        # Initialize systems, variables, flags
    }
}
```

### War System Hooks
```
on_declare_war = {
    # Track war declarations
}

on_capitulation = {
    # Clean up systems on defeat
}
```

### Faction Management
```
on_join_faction = {
    # Grant bonuses to faction members
}

on_leave_faction = {
    # Remove bonuses, trigger events
}
```

### Periodic Updates
```
on_weekly = {
    # Update custom systems
}
```

### State Control Tracking
```
on_state_control_changed = {
    # Track occupied states
}
```

---

## Reference Files

For detailed information, consult:
- `references/on_actions_reference.md` - Complete list of all on_actions with scopes
- `references/usage_patterns.md` - Common patterns and examples

---

## Tips

- On_actions are powerful for automatic systems
- Multiple files can define handlers for the same on_action
- Time-based on_actions run for every country - optimize carefully
- ROOT and FROM scopes vary by on_action type
- Use logs to debug scope and execution
- Consider performance impact of daily/weekly handlers
