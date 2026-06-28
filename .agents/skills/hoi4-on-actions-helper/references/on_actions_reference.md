# On Actions Complete Reference

## Understanding On_Actions

On_actions are automatic event handlers that fire when specific game events occur. They execute in the context of specific scopes (ROOT and FROM), which vary by on_action type.

---

## Game Lifecycle Events

### on_startup

**Fires:** Once when the game starts

**Scope:**
- ROOT: Each country (fires for every country)
- FROM: Not defined

**Use Cases:**
- Initialize mod systems
- Set initial variables and flags
- Setup arrays and data structures
- Configure starting conditions

**Example:**
```
on_startup = {
    effect = {
        every_country = {
            set_variable = { initialized = 1 }
        }

        set_variable = { global.mod_version = 1 }
    }
}
```

**Real Example from SSW_mod:**
```
on_startup = {
    effect = {
        set_variable = { global.function_amount = 3 }
        set_variable = { global.partner_amount = 14 }

        every_country = {
            limit = { is_ai = no }
            set_variable = { sde_window = 1 }
        }

        add_to_array = { global.indian_warlord = AZH }
        add_to_array = { global.indian_warlord = HND }
    }
}
```

---

### on_daily

**Fires:** Every day for every country

**Scope:**
- ROOT: Current country
- FROM: Not defined

**Use Cases:**
- Daily stat updates
- Frequent checks
- Time-sensitive systems

**Performance Warning:** Executes for ALL countries EVERY day. Use sparingly and with tight limits.

**Example:**
```
on_daily = {
    effect = {
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

---

### on_weekly

**Fires:** Every week for every country

**Scope:**
- ROOT: Current country
- FROM: Not defined

**Use Cases:**
- Regular system updates
- Economic calculations
- Periodic checks

**Example:**
```
on_weekly = {
    effect = {
        bsm_update_economic_alliance_power_share = yes
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

---

### on_monthly

**Fires:** Every month for every country

**Scope:**
- ROOT: Current country
- FROM: Not defined

**Use Cases:**
- Monthly economic updates
- Long-term tracking
- Less frequent calculations

**Example:**
```
on_monthly = {
    effect = {
        if = {
            limit = { has_idea = custom_economy }
            add_political_power = 10
        }
    }
}
```

**Real Example from BBA DLC:**
```
on_monthly = {
    effect = {
        # Monthly political power updates
        # Economic calculations
    }
}
```

---

## War and Combat Events

### on_declare_war

**Fires:** When a country declares war (fires BEFORE on_war_relation_added)

**Scope:**
- ROOT: Attacker (country declaring war)
- FROM: Defender (target of declaration)

**Use Cases:**
- Track war declarations
- Apply diplomatic penalties
- Trigger war-start events
- Modify relations

**Example:**
```
on_declare_war = {
    effect = {
        ROOT = {
            log = "[This.GetName] declared war on [FROM.GetName]"
        }
        FROM = {
            add_war_support = 0.1
        }
    }
}
```

**Real Example from SSW_mod:**
```
on_declare_war = {
    events = {
        ssw_war.1  # Trigger war notification
    }
}
```

---

### on_war

**Fires:** When war starts (alternative to on_declare_war)

**Scope:**
- ROOT: Country at war
- FROM: Not consistently defined

**Use Cases:**
- Track war state changes
- Apply war modifiers
- Initialize war systems

**Example:**
```
on_war = {
    effect = {
        if = {
            limit = { tag = GER }
            add_ideas = total_war_economy
        }
    }
}
```

---

### on_war_relation_added

**Fires:** When war relation is added (ALWAYS fires, after on_declare_war)

**Scope:**
- ROOT: Country entering war
- FROM: Enemy country

**Use Cases:**
- Guaranteed war tracking
- Apply war effects
- Track all war participants

**Example:**
```
on_war_relation_added = {
    effect = {
        ROOT = {
            set_country_flag = at_war_with_@FROM
        }
    }
}
```

**Difference from on_declare_war:**
- on_declare_war: Fires only for initial declaration
- on_war_relation_added: Fires for ALL war participants (including those joining existing wars)

---

### on_capitulation

**Fires:** When a country capitulates

**Scope:**
- ROOT: Capitulated country (loser)
- FROM: Winning country (country that caused capitulation)

**Use Cases:**
- Clean up defeated country's systems
- Free puppets
- Trigger defeat events
- Award victory bonuses

**Example:**
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

        # News event
        news_event = country_capitulated.0
    }
}
```

**Real Example from SSW_mod:**
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

---

### on_capitulation_immediate

**Fires:** Before capitulation is processed (before on_capitulation)

**Scope:**
- ROOT: Capitulating country
- FROM: Winning country

**Use Cases:**
- Pre-capitulation cleanup
- Save state before defeat
- Emergency actions

**Example:**
```
on_capitulation_immediate = {
    effect = {
        ROOT = {
            save_event_target_as = capitulated_country
        }
    }
}
```

---

### on_uncapitulation

**Fires:** When a country recovers from capitulation

**Scope:**
- ROOT: Country recovering
- FROM: Not defined

**Use Cases:**
- Restore systems
- Remove capitulation penalties
- Trigger recovery events

**Example:**
```
on_uncapitulation = {
    effect = {
        ROOT = {
            remove_ideas = capitulated_nation
            add_stability = 0.1
        }
    }
}
```

---

### on_peace

**Fires:** When peace is made

**Scope:**
- ROOT: Country making peace
- FROM: Former enemy

**Use Cases:**
- Transition to peacetime
- Remove war modifiers
- Trigger peace events

**Example:**
```
on_peace = {
    effect = {
        ROOT = {
            remove_ideas = total_war
        }
    }
}
```

---

### on_peaceconference_started

**Fires:** When peace conference begins

**Scope:**
- ROOT: Participant country
- FROM: Not defined

**Use Cases:**
- Pre-conference setup
- Calculate war scores
- Initialize peace systems

**Example:**
```
on_peaceconference_started = {
    effect = {
        ROOT = {
            log = "[This.GetName] entering peace conference"
        }
    }
}
```

---

### on_peaceconference_ended

**Fires:** When peace conference ends

**Scope:**
- ROOT: Participant country
- FROM: Not defined

**Use Cases:**
- Post-war cleanup
- Adjust AI economy
- Remove war-time ideas

**Example:**
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

## Faction Events

### on_create_faction

**Fires:** When a faction is created

**Scope:**
- ROOT: Faction creator
- FROM: Not defined

**Use Cases:**
- Track faction creation
- Apply faction bonuses
- Initialize faction systems

**Example:**
```
on_create_faction = {
    effect = {
        ROOT = {
            add_political_power = 50
            set_country_flag = faction_leader
        }
    }
}
```

---

### on_faction_formed

**Fires:** When a faction is formed (similar to on_create_faction)

**Scope:**
- ROOT: Faction leader
- FROM: Not defined

**Use Cases:**
- Alternative to on_create_faction
- Faction initialization

**Example:**
```
on_faction_formed = {
    effect = {
        ROOT = {
            log = "[This.GetName] formed a faction"
        }
    }
}
```

---

### on_join_faction

**Fires:** When a country joins a faction

**Scope:**
- ROOT: Country joining faction
- FROM: Faction leader

**Use Cases:**
- Apply faction member bonuses
- Update faction systems
- Trigger diplomatic events

**Example:**
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

---

### on_offer_join_faction

**Fires:** When a country is invited to join a faction

**Scope:**
- ROOT: Country sending invite (faction leader)
- FROM: Country being invited

**Use Cases:**
- Track faction invitations
- Pre-join checks
- Diplomatic events

**Example:**
```
on_offer_join_faction = {
    effect = {
        FROM = {
            country_event = {
                id = faction_invite.1
                days = 1
            }
        }
    }
}
```

---

### on_leave_faction

**Fires:** When a country leaves a faction

**Scope:**
- ROOT: Country leaving
- FROM: Faction leader (former)

**Use Cases:**
- Remove faction bonuses
- Apply betrayal penalties
- Clean up faction systems

**Example:**
```
on_leave_faction = {
    effect = {
        ROOT = {
            remove_opinion_modifier = {
                target = FROM
                modifier = faction_member_bonus
            }
        }
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = faction_betrayal
            }
        }
    }
}
```

---

## Puppet and Subject Events

### on_puppet

**Fires:** When a country becomes a puppet

**Scope:**
- ROOT: Country becoming puppet
- FROM: Overlord

**Use Cases:**
- Apply puppet bonuses/penalties
- Update diplomatic relations
- Initialize puppet systems

**Example:**
```
on_puppet = {
    effect = {
        ROOT = {
            add_opinion_modifier = {
                target = FROM
                modifier = puppet_overlord
            }
        }
        FROM = {
            reverse_add_opinion_modifier = {
                target = ROOT
                modifier = puppet_subject
            }
        }
    }
}
```

---

### on_release_as_puppet

**Fires:** When a country is released as a puppet

**Scope:**
- ROOT: Country being released
- FROM: Overlord (releaser)

**Use Cases:**
- Initialize released puppet
- Set starting conditions
- Apply release bonuses

**Example:**
```
on_release_as_puppet = {
    effect = {
        ROOT = {
            add_stability = -0.2
            add_political_power = 100
        }
    }
}
```

---

### on_release_as_free

**Fires:** When a country is released as independent

**Scope:**
- ROOT: Country being released
- FROM: Releaser

**Use Cases:**
- Initialize independent nation
- Set starting conditions
- Diplomatic adjustments

**Example:**
```
on_release_as_free = {
    effect = {
        ROOT = {
            add_opinion_modifier = {
                target = FROM
                modifier = granted_independence
            }
        }
    }
}
```

---

### on_subject_free

**Fires:** When a subject becomes free

**Scope:**
- ROOT: Former subject
- FROM: Former overlord

**Use Cases:**
- Remove puppet effects
- Update relations
- Trigger independence events

**Example:**
```
on_subject_free = {
    effect = {
        ROOT = {
            remove_ideas = puppet_nation
            add_stability = 0.1
        }
    }
}
```

---

### on_subject_autonomy_level_change

**Fires:** When a subject's autonomy level changes

**Scope:**
- ROOT: Subject
- FROM: Overlord

**Use Cases:**
- Adjust bonuses based on autonomy
- Track autonomy progression
- Trigger autonomy events

**Example:**
```
on_subject_autonomy_level_change = {
    effect = {
        ROOT = {
            if = {
                limit = { has_autonomy_state = autonomy_free }
                add_stability = 0.05
            }
        }
    }
}
```

---

### on_subject_annexed

**Fires:** When a subject is annexed by overlord

**Scope:**
- ROOT: Subject being annexed
- FROM: Overlord

**Use Cases:**
- Pre-annexation cleanup
- Transfer resources
- Trigger events

**Example:**
```
on_subject_annexed = {
    effect = {
        FROM = {
            add_political_power = 50
        }
    }
}
```

---

## Government Events

### on_government_change

**Fires:** When government ideology changes

**Scope:**
- ROOT: Country changing government
- FROM: Not defined

**Use Cases:**
- Adjust national spirits
- Update relations
- Trigger ideology events

**Example:**
```
on_government_change = {
    effect = {
        ROOT = {
            if = {
                limit = { has_government = fascism_ideology }
                add_ideas = fascist_government
            }
        }
    }
}
```

---

### on_ruling_party_change

**Fires:** When ruling party changes

**Scope:**
- ROOT: Country changing ruling party
- FROM: Not defined

**Use Cases:**
- Update coalition parties
- Adjust government composition
- Political system updates

**Example:**
```
on_ruling_party_change = {
    effect = {
        if = {
            limit = { has_government = totalitarian_socialism }
            set_temp_variable = { coalition_patry = token:totalitarian_socialism }
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
        # ... continues for all ideologies
    }
}
```

---

### on_coup_succeeded

**Fires:** When a coup succeeds

**Scope:**
- ROOT: Country where coup succeeded
- FROM: Not defined

**Use Cases:**
- Apply coup effects
- Change government
- Trigger instability

**Example:**
```
on_coup_succeeded = {
    effect = {
        ROOT = {
            add_stability = -0.3
            add_war_support = -0.2
        }
    }
}
```

---

### on_civil_war_end

**Fires:** When civil war ends

**Scope:**
- ROOT: Winner
- FROM: Loser (before annexation)

**Use Cases:**
- Apply victory/defeat effects
- Clean up civil war systems
- Unify country

**Example:**
```
on_civil_war_end = {
    effect = {
        ROOT = {
            add_stability = -0.1
            add_political_power = 100
        }
    }
}
```

---

### on_civil_war_end_before_annexation

**Fires:** Before civil war loser is annexed

**Scope:**
- ROOT: Winner
- FROM: Loser

**Use Cases:**
- Save loser's state
- Transfer resources
- Pre-annexation cleanup

**Example:**
```
on_civil_war_end_before_annexation = {
    effect = {
        FROM = {
            save_event_target_as = civil_war_loser
        }
    }
}
```

---

## State and Territory Events

### on_state_control_changed

**Fires:** When state control changes (occupation, liberation, capture)

**Scope:**
- ROOT: State
- FROM: New controller (country)

**Use Cases:**
- Track state captures
- Apply occupation effects
- Trigger state events

**Example:**
```
on_state_control_changed = {
    effect = {
        ROOT = {
            set_state_flag = recently_captured
        }
        FROM = {
            log = "[This.GetName] captured [ROOT.GetName]"
        }
    }
}
```

---

### on_annex

**Fires:** When a country is annexed

**Scope:**
- ROOT: Country being annexed
- FROM: Annexing country

**Use Cases:**
- Pre-annexation cleanup
- Transfer resources
- Trigger annexation events

**Example:**
```
on_annex = {
    effect = {
        FROM = {
            add_political_power = 50
        }
        ROOT = {
            # Clean up before annexation
            clr_country_flag = all_flags
        }
    }
}
```

---

## Military Events

### on_nuke_drop

**Fires:** When a nuclear bomb is dropped

**Scope:**
- ROOT: State where nuke was dropped
- FROM: Country that dropped the nuke

**Use Cases:**
- Track nuclear strikes
- Apply nuke effects
- Trigger war crime events

**Example:**
```
on_nuke_drop = {
    effect = {
        FROM = {
            add_war_support = -0.2
        }
        ROOT = {
            add_resistance = 10
        }
    }
}
```

---

### on_naval_invasion

**Fires:** When naval invasion lands

**Scope:**
- ROOT: Invading country
- FROM: Target state

**Use Cases:**
- Track invasions
- Apply invasion effects
- Trigger events

**Example:**
```
on_naval_invasion = {
    effect = {
        ROOT = {
            log = "[This.GetName] launched naval invasion"
        }
    }
}
```

---

### on_paradrop

**Fires:** When paratroopers drop

**Scope:**
- ROOT: Country dropping paratroopers
- FROM: Not consistently defined

**Use Cases:**
- Track paradrop operations
- Apply paradrop effects

**Example:**
```
on_paradrop = {
    effect = {
        ROOT = {
            log = "Paradrop operation initiated"
        }
    }
}
```

---

### on_units_paradropped_in_state

**Fires:** When units paradrop into a state

**Scope:**
- ROOT: State
- FROM: Country that paradropped

**Use Cases:**
- Track state-specific paradrops
- Apply state effects

**Example:**
```
on_units_paradropped_in_state = {
    effect = {
        ROOT = {
            set_state_flag = paradrop_occurred
        }
    }
}
```

---

### on_border_war_lost

**Fires:** When a border war is lost

**Scope:**
- ROOT: Loser
- FROM: Winner

**Use Cases:**
- Apply defeat effects
- Trigger border war events

**Example:**
```
on_border_war_lost = {
    effect = {
        ROOT = {
            add_stability = -0.05
        }
    }
}
```

---

## Army Leader Events

### on_army_leader_daily

**Fires:** Daily for each army leader

**Scope:**
- ROOT: Army leader (unit leader scope)
- FROM: Not defined

**Use Cases:**
- Daily leader updates
- Track leader stats
- Apply daily effects

**Example:**
```
on_army_leader_daily = {
    effect = {
        # Unit leader scope
        if = {
            limit = { skill > 5 }
            # Effects for skilled leaders
        }
    }
}
```

---

### on_army_leader_won_combat

**Fires:** When army leader wins combat

**Scope:**
- ROOT: Winning army leader
- FROM: Enemy army leader (if applicable)

**Use Cases:**
- Award victory bonuses
- Increase skill/traits
- Track victories

**Example:**
```
on_army_leader_won_combat = {
    effect = {
        ROOT = {
            add_unit_leader_trait = victorious_leader
        }
    }
}
```

---

### on_army_leader_lost_combat

**Fires:** When army leader loses combat

**Scope:**
- ROOT: Losing army leader
- FROM: Enemy army leader (if applicable)

**Use Cases:**
- Apply defeat penalties
- Track losses
- Trigger events

**Example:**
```
on_army_leader_lost_combat = {
    effect = {
        ROOT = {
            # Penalize leader
        }
    }
}
```

---

### on_army_leader_promoted

**Fires:** When army leader is promoted

**Scope:**
- ROOT: Promoted leader
- FROM: Country

**Use Cases:**
- Apply promotion bonuses
- Track promotions

**Example:**
```
on_army_leader_promoted = {
    effect = {
        ROOT = {
            add_unit_leader_trait = promoted_officer
        }
    }
}
```

---

### on_unit_leader_promote_from_ranks_veteran

**Fires:** When veteran unit is promoted to leader

**Scope:**
- ROOT: New unit leader
- FROM: Unit

**Use Cases:**
- Apply veteran bonuses
- Track promotions from ranks

**Example:**
```
on_unit_leader_promote_from_ranks_veteran = {
    effect = {
        ROOT = {
            add_unit_leader_trait = veteran_experience
        }
    }
}
```

---

### on_unit_leader_promote_from_ranks_green

**Fires:** When green unit is promoted to leader

**Scope:**
- ROOT: New unit leader
- FROM: Unit

**Use Cases:**
- Apply new leader effects
- Track promotions

**Example:**
```
on_unit_leader_promote_from_ranks_green = {
    effect = {
        ROOT = {
            # Green leader effects
        }
    }
}
```

---

## Operative Events (La Résistance DLC)

### on_operative_on_mission_spotted

**Fires:** When operative is spotted on mission

**Scope:**
- ROOT: Operative
- FROM: Country that spotted

**Use Cases:**
- Track operative exposure
- Apply penalties

**Example:**
```
on_operative_on_mission_spotted = {
    effect = {
        ROOT = {
            # Reduce operative effectiveness
        }
    }
}
```

---

### on_operative_captured

**Fires:** When operative is captured

**Scope:**
- ROOT: Captured operative
- FROM: Capturing country

**Use Cases:**
- Handle capture
- Trigger rescue missions

**Example:**
```
on_operative_captured = {
    effect = {
        FROM = {
            log = "Operative captured"
        }
    }
}
```

---

### on_operative_death

**Fires:** When operative dies

**Scope:**
- ROOT: Dead operative
- FROM: Killing country (if applicable)

**Use Cases:**
- Clean up operative
- Trigger events

**Example:**
```
on_operative_death = {
    effect = {
        # Clean up operative data
    }
}
```

---

### on_operative_detected_during_operation

**Fires:** When operative is detected during operation

**Scope:**
- ROOT: Operative
- FROM: Detecting country

**Use Cases:**
- Apply detection penalties
- Trigger counterintelligence

**Example:**
```
on_operative_detected_during_operation = {
    effect = {
        FROM = {
            add_intel = 5
        }
    }
}
```

---

### on_operation_completed

**Fires:** When intelligence operation completes

**Scope:**
- ROOT: Operative
- FROM: Target country

**Use Cases:**
- Apply operation results
- Award bonuses

**Example:**
```
on_operation_completed = {
    effect = {
        ROOT = {
            # Operative gains experience
        }
    }
}
```

---

## Other Events

### on_new_term_election

**Fires:** When election occurs (US focus tree mechanic)

**Scope:**
- ROOT: Country having election
- FROM: Not defined

**Use Cases:**
- Trigger election events
- Change government

**Example:**
```
on_new_term_election = {
    random_events = {
        100 = usa.6
        100 = usa.7
    }
}
```

---

### on_ace_promoted

**Fires:** When ace pilot is promoted

**Scope:**
- ROOT: Country
- FROM: Not defined

**Use Cases:**
- Track ace promotions
- Award bonuses

**Example:**
```
on_ace_promoted = {
    effect = {
        ROOT = {
            add_political_power = 10
        }
    }
}
```

---

### on_ace_killed

**Fires:** When ace pilot is killed

**Scope:**
- ROOT: Country that lost ace
- FROM: Not defined

**Use Cases:**
- Apply morale penalties
- Trigger events

**Example:**
```
on_ace_killed = {
    effect = {
        ROOT = {
            add_war_support = -0.01
        }
    }
}
```

---

### on_justifying_wargoal_pulse

**Fires:** Periodically during war goal justification

**Scope:**
- ROOT: Country justifying
- FROM: Target country

**Use Cases:**
- Track justification progress
- Apply diplomatic effects

**Example:**
```
on_justifying_wargoal_pulse = {
    effect = {
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = justifying_against_us
            }
        }
    }
}
```

---

### on_wargoal_expire

**Fires:** When war goal expires

**Scope:**
- ROOT: Country with war goal
- FROM: Target country

**Use Cases:**
- Clean up expired war goals
- Remove modifiers

**Example:**
```
on_wargoal_expire = {
    effect = {
        ROOT = {
            remove_opinion_modifier = {
                target = FROM
                modifier = wargoal_active
            }
        }
    }
}
```

---

## Quick Reference Table

| On_Action | ROOT | FROM | Frequency |
|-----------|------|------|-----------|
| on_startup | Each country | - | Once |
| on_daily | Each country | - | Daily |
| on_weekly | Each country | - | Weekly |
| on_monthly | Each country | - | Monthly |
| on_declare_war | Attacker | Defender | Event |
| on_war | Country at war | - | Event |
| on_war_relation_added | Country | Enemy | Event |
| on_capitulation | Loser | Winner | Event |
| on_peace | Country | Former enemy | Event |
| on_peaceconference_ended | Participant | - | Event |
| on_create_faction | Creator | - | Event |
| on_join_faction | Joiner | Leader | Event |
| on_leave_faction | Leaver | Leader | Event |
| on_puppet | Puppet | Overlord | Event |
| on_state_control_changed | State | New controller | Event |
| on_annex | Annexed | Annexer | Event |
| on_government_change | Country | - | Event |
| on_ruling_party_change | Country | - | Event |

---

## Performance Considerations

**Heavy Operations (Use with Caution):**
- `on_daily` - Fires for ALL countries EVERY day
- `on_army_leader_daily` - Fires for ALL leaders EVERY day
- `on_state_control_changed` - Can fire frequently during wars

**Recommended Alternatives:**
- Use `on_weekly` instead of `on_daily` when possible
- Use limits to restrict execution
- Use early returns to skip unnecessary processing
- Cache results with variables instead of recalculating

**Performance Tips:**
```
on_daily = {
    effect = {
        # BAD: No limits, runs for all countries
        add_political_power = 1

        # GOOD: Limited scope
        if = {
            limit = {
                tag = GER
                has_country_flag = special_system_enabled
            }
            add_political_power = 1
        }
    }
}
```
