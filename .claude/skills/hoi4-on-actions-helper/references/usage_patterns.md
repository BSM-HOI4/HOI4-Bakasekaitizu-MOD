# On Actions - Usage Patterns and Examples

## Pattern Categories

### 1. Startup Initialization Patterns

These patterns initialize mod systems when the game starts.

#### Basic Initialization

```
on_startup = {
    effect = {
        # Set global variables
        set_variable = { global.mod_version = 1 }
        set_variable = { global.system_enabled = 1 }
    }
}
```

#### Country Initialization

```
on_startup = {
    effect = {
        every_country = {
            set_variable = { country_points = 0 }
            set_variable = { initialized = 1 }
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        # Startup desk event variables
        set_variable = { global.function_amount = 3 }
        set_variable = { global.partner_amount = 14 }

        # Initialize player countries
        every_country = {
            limit = { is_ai = no }
            set_variable = { sde_window = 1 }
            dts_sort_timeline_list = yes
        }
    }
}
```

#### Array Initialization

```
on_startup = {
    effect = {
        # Initialize arrays
        add_to_array = { global.major_powers = USA }
        add_to_array = { global.major_powers = GER }
        add_to_array = { global.major_powers = SOV }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        add_to_array = { global.indian_warlord = AZH }
        add_to_array = { global.indian_warlord = HND }
        add_to_array = { global.indian_warlord = IND }
        add_to_array = { global.indian_warlord = IRF }
        add_to_array = { global.indian_warlord = RAJ }
        add_to_array = { global.indian_warlord = TRV }
    }
}
```

#### State Flag Setup

```
on_startup = {
    effect = {
        every_state = {
            limit = { is_coastal = yes }
            set_state_flag = coastal_state
        }

        every_state = {
            limit = {
                OR = {
                    state = 123
                    state = 456
                }
            }
            set_state_flag = strategic_location
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        every_state = {
            limit = {
                OR = {
                    is_fully_controlled_by = AKS
                    is_fully_controlled_by = ALF
                    is_fully_controlled_by = FSA
                    state = 463
                    state = 650
                }
            }
            set_state_flag = maybe_core_AMERICA
        }

        every_state = {
            limit = {
                OR = {
                    is_owned_by = HUN
                    is_owned_by = ROM
                    is_owned_by = BUL
                }
            }
            set_state_flag = Balkan_fede_must_need_states
        }
    }
}
```

#### Coalition Party Setup

```
on_startup = {
    effect = {
        GER = {
            set_temp_variable = { coalition_patry = token:social_democracy }
            add_coalition_patry = yes
            set_temp_variable = { coalition_patry = token:liberal_democracy }
            add_coalition_patry = yes
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        FIN = {
            set_temp_variable = { coalition_patry = token:social_democracy }
            add_coalition_patry = yes
            set_temp_variable = { coalition_patry = token:liberal_democracy }
            add_coalition_patry = yes
            set_temp_variable = { coalition_patry = token:authoritarian_democracy }
            add_coalition_patry = yes
        }

        JAP = {
            set_temp_variable = { coalition_patry = token:authoritarian_democracy }
            add_coalition_patry = yes
        }
    }
}
```

---

### 2. War Declaration Patterns

Handle war declarations and war start effects.

#### Simple War Tracking

```
on_declare_war = {
    effect = {
        ROOT = {
            set_country_flag = declared_war_on_@FROM
        }
        FROM = {
            set_country_flag = war_declared_by_@ROOT
        }
    }
}
```

#### War Event Trigger

```
on_declare_war = {
    events = {
        war_events.1  # ROOT = attacker, FROM = defender
    }
}
```

#### Diplomatic Penalty

```
on_declare_war = {
    effect = {
        every_other_country = {
            limit = {
                is_in_faction_with = FROM
                NOT = { is_in_faction_with = ROOT }
            }
            add_opinion_modifier = {
                target = ROOT
                modifier = attacked_our_ally
            }
        }
    }
}
```

---

### 3. Capitulation Patterns

Handle country defeat and cleanup.

#### Puppet Liberation

```
on_capitulation = {
    effect = {
        if = {
            limit = { ROOT = { num_subjects > 0 } }
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
        if = {
            limit = { ROOT = { num_subjects > 0 } }
            log = "[GetDate]: on_capitulation"
            every_other_country = {
                limit = { is_subject_of = ROOT }
                ROOT = { end_puppet = PREV }
            }
        }
    }
}
```

#### System Cleanup

```
on_capitulation = {
    effect = {
        # Leave economic sphere
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

**Real Example from SSW_mod:**
```
on_capitulation = {
    effect = {
        if = {
            limit = { ROOT = { tag = ALF } }
            every_country = {
                limit = { is_in_es_ALF_economic_spheres = yes }
                es_leave_economic_sphere_single = yes
            }
        }
        else_if = {
            limit = { ROOT = { tag = FSA } }
            every_country = {
                limit = { is_in_es_FSA_economic_spheres = yes }
                es_leave_economic_sphere_single = yes
            }
        }
    }
}
```

#### News Event

```
on_capitulation = {
    effect = {
        if = {
            limit = { has_civil_war = no }
            news_event = country_capitulated.0
            FROM = { save_global_event_target_as = winning_country }
            ROOT = { save_global_event_target_as = losing_country }
        }
    }
}
```

---

### 4. Peace Conference Patterns

Handle post-war transitions.

#### AI Economy Adjustment

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
                    add_political_power = -150
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
                        has_government = social_democracy
                        has_government = conservative_democracy
                    }
                }
                if = {
                    limit = {
                        OR = {
                            has_idea = war_economy
                            has_idea = tot_economic_mobilisation
                        }
                        NOT = { has_country_flag = economic_law_cannot_change }
                    }
                    add_ideas = partial_economic_mobilisation
                    add_political_power = -150
                    log = "[ROOT.GetName]:自由化完了"
                }
            }
        }
        FROM = {
            # Same logic for FROM
        }
    }
}
```

#### Mobilization Adjustment

```
on_peaceconference_ended = {
    effect = {
        ROOT = {
            if = {
                limit = {
                    is_ai = yes
                    has_government = democratic_ideology
                }
                if = {
                    limit = { has_idea = extensive_conscription }
                    add_ideas = limited_conscription
                    add_political_power = -150
                }
            }
        }
    }
}
```

---

### 5. Faction Management Patterns

Handle faction membership and bonuses.

#### Faction Member Bonuses

```
on_join_faction = {
    effect = {
        ROOT = {
            add_opinion_modifier = {
                target = FROM
                modifier = faction_member_bonus
            }
        }
        FROM = {
            reverse_add_opinion_modifier = {
                target = ROOT
                modifier = faction_member_bonus
            }
        }
    }
}
```

#### Faction Leave Penalty

```
on_leave_faction = {
    effect = {
        every_country = {
            limit = { is_in_faction_with = FROM }
            add_opinion_modifier = {
                target = ROOT
                modifier = faction_betrayal
            }
        }
    }
}
```

---

### 6. Government Change Patterns

Handle ideology and ruling party changes.

#### Coalition Party Cleanup

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
        else_if = {
            limit = { has_government = gradual_socialism }
            set_temp_variable = { coalition_patry = token:gradual_socialism }
            remove_coalition_patry = yes
        }
        # ... continues for all ideologies
        else = {
            set_temp_variable = { coalition_patry = token:ultranationalism }
            remove_coalition_patry = yes
        }
    }
}
```

#### Government-Specific Ideas

```
on_government_change = {
    effect = {
        ROOT = {
            if = {
                limit = { has_government = fascism_ideology }
                add_ideas = fascist_government
                remove_ideas = democratic_government
            }
            else_if = {
                limit = { has_government = democratic_ideology }
                add_ideas = democratic_government
                remove_ideas = fascist_government
            }
        }
    }
}
```

---

### 7. Periodic Update Patterns

Handle weekly/monthly system updates.

#### Weekly System Update

```
on_weekly = {
    effect = {
        # Update economic alliance
        bsm_update_economic_alliance_power_share = yes

        # Update state tracking
        every_state = {
            limit = { has_state_flag = tracked }
            owner = {
                # Update owner stats
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

#### Monthly Economic Update

```
on_monthly = {
    effect = {
        every_country = {
            limit = { has_country_flag = economic_system_active }
            # Calculate monthly income
            add_political_power = 5
        }
    }
}
```

---

### 8. State Control Patterns

Handle state capture and occupation.

#### State Capture Tracking

```
on_state_control_changed = {
    effect = {
        # ROOT = state
        # FROM = new controller

        ROOT = {
            set_state_flag = recently_captured
        }

        FROM = {
            log = "[This.GetName] captured [ROOT.GetName]"
        }
    }
}
```

#### Occupation Event

```
on_state_control_changed = {
    effect = {
        FROM = {
            country_event = {
                id = occupation.1
                days = 1
            }
        }
    }
}
```

---

### 9. Puppet Management Patterns

Handle puppet creation and autonomy.

#### Puppet Bonuses

```
on_puppet = {
    effect = {
        ROOT = {
            add_opinion_modifier = {
                target = FROM
                modifier = our_overlord
            }
        }
        FROM = {
            reverse_add_opinion_modifier = {
                target = ROOT
                modifier = our_puppet
            }
        }
    }
}
```

#### Release as Puppet

```
on_release_as_puppet = {
    effect = {
        ROOT = {
            add_stability = -0.2
            add_war_support = -0.1
            add_political_power = 100
        }
    }
}
```

---

### 10. Custom System Initialization Patterns

Initialize complex custom systems on startup.

#### Economic Alliance System

```
on_startup = {
    effect = {
        ESP = { bsm_initialize_spain_alliance = yes }
    }
}
```

**Real Example from BSM_mod:**
```
on_startup = {
    effect = {
        ESP = { bsm_initialize_spain_alliance = yes }
    }
}
```

#### Variable Initialization

```
on_startup = {
    effect = {
        every_country = {
            limit = { NOT = { original_tag = MYS } }
            set_variable = { Cultural_Degree = modifier@base_Cultural_Degree }
            set_variable = { National_Unity_Power = 10 }
        }

        every_country = {
            limit = { original_tag = MYS }
            set_variable = { Cultural_Degree = modifier@base_Cultural_Degree }
            set_variable = { National_Unity_Power = 100 }
        }
    }
}
```

**Real Example from BSM_mod:**
```
on_startup = {
    effect = {
        every_country = {
            limit = { NOT = { original_tag = MYS } }
            set_variable = { var = COUNTRY_resource_minor_artifacts value = 0 }
            set_variable = { Cultural_Degree = modifier@base_Cultural_Degree }
            set_variable = { var = National_Unity_Power value = 10 }
        }

        every_country = {
            limit = { original_tag = MYS }
            set_variable = { Cultural_Degree = modifier@base_Cultural_Degree }
            set_variable = { var = National_Unity_Power value = 100 }
        }
    }
}
```

#### Dynamic Modifier Application

```
on_startup = {
    effect = {
        every_country = {
            limit = { is_ai = no }
            clamp_variable = { var = Cultural_Degree min = -1 max = 1 }
            add_dynamic_modifier = { modifier = civ_research_buff }
            add_dynamic_modifier = { modifier = bsm_uc_factor }
        }
    }
}
```

**Real Example from BSM_mod:**
```
on_startup = {
    effect = {
        every_country = {
            limit = { is_ai = no }
            clamp_variable = { var = Cultural_Degree min = -1 }
            clamp_variable = { var = Cultural_Degree max = 1 }
            clamp_variable = { var = National_Unity_Power min = -10000 }
            clamp_variable = { var = National_Unity_Power max = 10000 }
            add_dynamic_modifier = { modifier = civ_research_buff }
            add_dynamic_modifier = { modifier = bsm_uc_factor }
        }
    }
}
```

---

## Template: Complete War System

```
# War declaration
on_declare_war = {
    effect = {
        ROOT = {
            set_country_flag = at_war_with_@FROM
            log = "[This.GetName] declared war on [FROM.GetName]"
        }
        FROM = {
            add_war_support = 0.1
            country_event = { id = war_declared.1 days = 1 }
        }
    }
}

# War relation added (guaranteed to fire)
on_war_relation_added = {
    effect = {
        ROOT = {
            set_country_flag = in_war_with_@FROM
        }
    }
}

# Capitulation
on_capitulation = {
    effect = {
        # Free puppets
        if = {
            limit = { ROOT = { num_subjects > 0 } }
            every_other_country = {
                limit = { is_subject_of = ROOT }
                ROOT = { end_puppet = PREV }
            }
        }

        # Clean up systems
        ROOT = {
            clr_country_flag = all_flags
        }

        # News event
        news_event = country_capitulated.0
    }
}

# Peace conference
on_peaceconference_ended = {
    effect = {
        ROOT = {
            # AI economy adjustment
            if = {
                limit = {
                    is_ai = yes
                    has_government = democratic_ideology
                }
                if = {
                    limit = { has_idea = war_economy }
                    add_ideas = partial_economic_mobilisation
                }
            }

            # Clean up war flags
            clr_country_flag = at_war_with_@FROM
        }
    }
}
```

---

## Template: Economic System

```
# Initialize on startup
on_startup = {
    effect = {
        # Setup economic alliance
        ESP = { bsm_initialize_spain_alliance = yes }

        # Initialize country variables
        every_country = {
            set_variable = { economic_power = 0 }
            set_variable = { trade_balance = 0 }
        }
    }
}

# Weekly update
on_weekly = {
    effect = {
        # Update economic calculations
        bsm_update_economic_alliance_power_share = yes

        # Update trade balances
        every_country = {
            limit = { has_country_flag = in_economic_system }
            calculate_trade_balance = yes
        }
    }
}

# Monthly income
on_monthly = {
    effect = {
        every_country = {
            limit = { has_country_flag = in_economic_system }
            add_political_power = 10
        }
    }
}
```

---

## Template: Faction System

```
# Faction created
on_create_faction = {
    effect = {
        ROOT = {
            add_political_power = 50
            set_country_flag = faction_leader
        }
    }
}

# Member joins
on_join_faction = {
    effect = {
        # Apply bonuses to both countries
        ROOT = {
            add_opinion_modifier = {
                target = FROM
                modifier = faction_member_bonus
            }
        }
        FROM = {
            reverse_add_opinion_modifier = {
                target = ROOT
                modifier = faction_member_bonus
            }
        }

        # Update faction system
        every_country = {
            limit = { is_in_faction_with = FROM }
            add_opinion_modifier = {
                target = ROOT
                modifier = faction_ally
            }
        }
    }
}

# Member leaves
on_leave_faction = {
    effect = {
        # Remove bonuses
        ROOT = {
            remove_opinion_modifier = {
                target = FROM
                modifier = faction_member_bonus
            }
        }

        # Apply betrayal penalty
        every_country = {
            limit = { is_in_faction_with = FROM }
            add_opinion_modifier = {
                target = ROOT
                modifier = faction_betrayal
            }
        }
    }
}
```

---

## Common Mistakes

### ❌ Wrong: No Scope Awareness

```
# BAD - Doesn't check scope context
on_declare_war = {
    effect = {
        add_war_support = 0.1  # Which country?
    }
}
```

### ✅ Correct: Explicit Scopes

```
# GOOD - Explicit scope
on_declare_war = {
    effect = {
        ROOT = {
            # Attacker
            add_war_support = -0.05
        }
        FROM = {
            # Defender
            add_war_support = 0.1
        }
    }
}
```

---

### ❌ Wrong: Heavy Daily Operations

```
# BAD - Runs for all countries every day
on_daily = {
    effect = {
        every_owned_state = {
            # Heavy calculation
            owner = {
                # More heavy stuff
            }
        }
    }
}
```

### ✅ Correct: Limited and Optimized

```
# GOOD - Limited scope, weekly instead of daily
on_weekly = {
    effect = {
        if = {
            limit = {
                tag = GER
                has_country_flag = system_enabled
            }
            every_owned_state = {
                limit = { has_state_flag = tracked }
                # Calculation
            }
        }
    }
}
```

---

### ❌ Wrong: Forgetting Multiple Handlers Execute

```
# In file A:
on_startup = {
    effect = {
        set_variable = { global.initialized = 1 }
    }
}

# In file B:
on_startup = {
    effect = {
        # Assumes global.initialized doesn't exist
        set_variable = { global.initialized = 2 }  # Overwrites!
    }
}
```

### ✅ Correct: Coordinated Handlers

```
# In file A:
on_startup = {
    effect = {
        set_variable = { global.system_a_initialized = 1 }
    }
}

# In file B:
on_startup = {
    effect = {
        set_variable = { global.system_b_initialized = 1 }
    }
}
```

---

## Best Practices Summary

1. **Always document ROOT and FROM scopes** in comments
2. **Use limits to restrict execution** to relevant countries/states
3. **Avoid heavy operations in on_daily** - use on_weekly or on_monthly
4. **Log important actions** for debugging
5. **Remember multiple handlers execute** - don't duplicate logic
6. **Use early returns** to optimize performance
7. **Test scope context** before implementing complex logic
8. **Organize by system** - group related on_actions in same file
9. **Clean up on capitulation/annexation** - remove flags, variables
10. **Use scripted effects** for code shared across on_actions

---

## Debugging Tips

### Add Logging

```
on_capitulation = {
    effect = {
        log = "[GetDateText]: [ROOT.GetName] capitulated to [FROM.GetName]"

        # Your effects here
    }
}
```

### Test Scopes

```
on_declare_war = {
    effect = {
        ROOT = {
            log = "ROOT: [This.GetName]"
        }
        FROM = {
            log = "FROM: [This.GetName]"
        }
    }
}
```

### Check Execution

```
on_startup = {
    effect = {
        log = "Startup on_action executing"
        every_country = {
            log = "Initializing [This.GetName]"
        }
    }
}
```
