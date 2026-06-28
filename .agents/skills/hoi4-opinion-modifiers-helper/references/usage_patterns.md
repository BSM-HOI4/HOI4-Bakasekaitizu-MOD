# Opinion Modifiers - Usage Patterns and Examples

## Pattern Categories

### 1. Simple Permanent Modifiers

Basic modifiers that last until manually removed.

#### Positive Permanent

```
TAG_friendship = {
    value = 50
}

alliance_member = {
    value = 25
}

anti_comintern_pact_opinion = {
    value = 25
}
```

**Use Cases:**
- Alliance bonuses
- Pact memberships
- Permanent diplomatic agreements
- Core territorial disputes

#### Negative Permanent

```
holds_our_cores = {
    value = -30
}

holds_our_claims = {
    value = -15
}

claims_on_us = {
    value = -10
}

pact_against_us = {
    value = -50
}
```

**Use Cases:**
- Territorial disputes
- Permanent hostility
- Ideological opposition
- Historical grievances

---

### 2. Decaying Modifiers

Temporary modifiers that decrease over time.

#### Standard Decay

```
protest_action = {
    value = -25
    months = 12
    decay = 1
}

SSW_friendly = {
    value = 50
    months = 12
    decay = 1
}
```

**Behavior:**
- Starts at specified value
- Decays by `decay` amount per month
- Continues after `months` duration until reaching 0

**Example Timeline:**
```
SSW_friendly:
Month 0: +50
Month 1: +49
Month 2: +48
...
Month 12: +38
Month 13: +37
...
Month 50: 0 (removed)
```

#### Fast Decay

```
ssw_emb_lifted = {
    value = 20
    decay = 10
}
```

**Use Case:**
- Quick diplomatic gestures
- Short-term bonuses
- Rapid forgiveness

**Timeline:**
```
Month 0: +20
Month 1: +10
Month 2: 0 (removed)
```

#### Slow Decay

```
condemn_aggression = {
    value = -50
    months = 24
}

western_betrayal = {
    value = -50
    months = 48
}
```

**Use Case:**
- Long-term grudges
- Major diplomatic events
- Historical incidents

---

### 3. Time-Limited Fixed Value

Modifiers that stay constant for a duration, then disappear.

```
GER_bought_fighter = {
    value = 10
    months = 2
}

GER_bought_art = {
    value = 8
    months = 2
}
```

**Behavior:**
- Stays at constant value
- Removed after duration expires
- No gradual decay

**Timeline:**
```
Month 0: +10
Month 1: +10
Month 2: Removed
```

**Use Cases:**
- Temporary trade bonuses
- Short-term cooperation
- Event-based boosts

---

### 4. Trade Restriction Modifiers

Modifiers that block trade between countries.

#### Pure Embargo

```
faction_traitor_trade = {
    trade = yes
    value = -40
}
```

#### Combined Embargo + Opinion

```
ssw_new_emb = {
    trade = yes
    value = -90
}

ssw_new_emb_opinion = {
    value = -75
}

# Applied together for total -165 opinion + trade block
```

**Pattern:**
1. Create trade-blocking modifier
2. Create additional opinion-only modifier
3. Apply both for severe sanctions

**Lifting Embargo:**
```
# Remove embargo modifiers
remove_opinion_modifier = {
    target = FROM
    modifier = ssw_new_emb
}
remove_opinion_modifier = {
    target = FROM
    modifier = ssw_new_emb_opinion
}

# Add forgiveness modifier
add_opinion_modifier = {
    target = FROM
    modifier = ssw_emb_lifted  # +20, decays fast
}
```

---

### 5. Trust-Affecting Modifiers

Modifiers that impact trust levels.

```
justifying_war_goal = {
    value = -10
    min_trust = -10
    days = 10
    decay = 1
}
```

**Use Cases:**
- War justification
- Broken promises
- Espionage discovery
- Alliance violations

**Effect:**
- Reduces both opinion and trust
- Makes AI less likely to cooperate
- Affects long-term relations

---

### 6. Tiered Modifier Systems

Multiple variants for different intensities.

#### SSW Mod: OAS System

```
OAS_hostility_25 = {
    value = -25
}

OAS_hostility_30 = {
    value = -30
}

OAS_hostility_50 = {
    value = -50
}

OAS_friendship_15 = {
    value = 15
}

OAS_friendship_25 = {
    value = 25
}

OAS_friendship_30 = {
    value = 30
}

OAS_friendship_35 = {
    value = 35
}
```

**Use Case:**
- Progressive relationship system
- Varying levels of cooperation/hostility
- Event chains with multiple outcomes

**Implementation:**
```
# In event:
if = {
    limit = { check_variable = { relationship_level = 3 } }
    add_opinion_modifier = {
        target = FROM
        modifier = OAS_friendship_35
    }
}
else_if = {
    limit = { check_variable = { relationship_level = 2 } }
    add_opinion_modifier = {
        target = FROM
        modifier = OAS_friendship_25
    }
}
```

---

### 7. Faction/Alliance Systems

Modifiers for custom alliance mechanics.

#### BSM Economic Alliance

```
bsm_economic_alliance_relation_boost = {
    value = 15
    decay = 0
}
```

**Usage:**
```
# On joining alliance:
every_country = {
    limit = {
        is_in_economic_alliance_with = ROOT
    }
    add_opinion_modifier = {
        target = ROOT
        modifier = bsm_economic_alliance_relation_boost
    }
    ROOT = {
        add_opinion_modifier = {
            target = PREV
            modifier = bsm_economic_alliance_relation_boost
        }
    }
}

# On leaving alliance:
every_country = {
    limit = {
        has_opinion_modifier = {
            target = ROOT
            modifier = bsm_economic_alliance_relation_boost
        }
    }
    remove_opinion_modifier = {
        target = ROOT
        modifier = bsm_economic_alliance_relation_boost
    }
}
```

---

### 8. Event Response Patterns

Modifiers for event choices and outcomes.

#### Binary Choice

```
SSW_thanks = {
    value = 30
}

SSW_rejection = {
    value = -20
}
```

**Event Structure:**
```
country_event = {
    id = example.1

    option = {
        name = accept
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = SSW_thanks
            }
        }
    }

    option = {
        name = reject
        FROM = {
            add_opinion_modifier = {
                target = ROOT
                modifier = SSW_rejection
            }
        }
    }
}
```

#### Positive/Negative Outcomes

```
GER_returned_north_france = {
    value = 100
}

GER_not_returned_north_france = {
    value = -200
}
```

**Use Case:**
- Major diplomatic promises
- Territory returns
- Critical decisions

---

### 9. Progressive Relationship Decay

Modifiers that simulate gradual cooling of relations.

```
our_liberators = {
    value = 40
    months = 18
    decay = 1
}
```

**Real-World Behavior:**
- Liberation creates strong positive opinion
- Gratitude fades over time (1 per month)
- After 18 months, still moderately positive (+22)
- Eventually returns to neutral

**Similar Pattern:**
```
GER_conference_in_berlin = {
    value = 30
}

# Could be extended with decay:
GER_conference_in_berlin = {
    value = 30
    months = 24
    decay = 1
}
# Ensures diplomatic success fades over time
```

---

### 10. Reciprocal Modifiers

Applying modifiers in both directions.

```
# In effect:
add_opinion_modifier = {
    target = GER
    modifier = SSW_friendly
}

reverse_add_opinion_modifier = {
    target = GER
    modifier = SSW_friendly
}

# Result: Both countries have +50 opinion of each other
```

**Alternative Pattern:**
```
GER = {
    add_opinion_modifier = {
        target = ROOT
        modifier = SSW_friendly
    }
}

ROOT = {
    add_opinion_modifier = {
        target = GER
        modifier = SSW_friendly
    }
}
```

---

## Real-World System Examples

### SSW Mod: Technology Licensing

```
SSW_generic_technology_licensing = {
    value = 20
}
```

**Implementation:**
```
# In technology sharing decision:
FROM = {
    add_opinion_modifier = {
        target = ROOT
        modifier = SSW_generic_technology_licensing
    }
}
```

### SSW Mod: Civil War Support

```
SSW_support_civil_war = {
    value = 20
}
```

**Context:**
- Supporting a faction in civil war
- Positive opinion from supported faction
- Can lead to alliance

### SSW Mod: Territory Disputes

```
Papua_war_reject_return_territory = {
    value = -20
}

SSW_Return_Territory = {
    value = 60
}

SSW_not_Return_Territory = {
    value = 25
}
```

**Usage Pattern:**
```
# Event: Will you return captured territory?
option = {
    name = "Return it"
    FROM = {
        add_opinion_modifier = {
            target = ROOT
            modifier = SSW_Return_Territory  # +60
        }
    }
    transfer_state = [state_id]
}

option = {
    name = "Keep it"
    FROM = {
        add_opinion_modifier = {
            target = ROOT
            modifier = Papua_war_reject_return_territory  # -20
        }
    }
}
```

### SSW Mod: Equipment Trade System

```
GER_trade_with = {
    value = 20
}

GER_bought_fighter = {
    value = 10
    months = 2
}

GER_bought_MBT = {
    value = 15
    months = 2
}
```

**System:**
```
# Base trade agreement
add_opinion_modifier = {
    target = GER
    modifier = GER_trade_with  # Permanent +20
}

# Per-transaction bonuses
add_opinion_modifier = {
    target = GER
    modifier = GER_bought_fighter  # +10 for 2 months
}
```

### SSW Mod: Diplomatic Conference System

```
GER_conference_in_berlin = {
    value = 30
}

GER_washington_conference = {
    value = 25
}

GER_vienna_conference = {
    value = 25
}

GER_geneva_breakdown = {
    value = -50
}
```

**Pattern:**
- Successful conference: +25-30 opinion
- Failed conference: -50 opinion
- Creates diplomatic momentum

### SSW Mod: Anti-Communist System

```
GER_implementation_anticommunist_agreement = {
    value = 100
}

GER_reject_anticommunist_agreement = {
    value = -50
}

GER_unfulfillment_of_anti_comintern_agreement = {
    value = -50
}
```

**Workflow:**
1. Offer anti-communist pact
2. Accept: +100 opinion
3. Reject: -50 opinion
4. Break pact: -50 opinion

---

## Template: Complete Diplomatic System

```
# Positive escalation
TAG_minor_cooperation = {
    value = 10
}

TAG_significant_cooperation = {
    value = 30
}

TAG_major_alliance = {
    value = 50
    decay = 0  # Permanent
}

# Negative escalation
TAG_minor_dispute = {
    value = -15
    months = 12
    decay = 1
}

TAG_diplomatic_incident = {
    value = -40
    months = 24
}

TAG_major_hostility = {
    value = -100
    decay = 0
}

# Trade integration
TAG_trade_agreement = {
    value = 20
}

TAG_trade_sanctions = {
    trade = yes
    value = -60
    months = 12
}

# Event outcomes
TAG_promise_kept = {
    value = 75
}

TAG_promise_broken = {
    value = -150
}

TAG_mediation_success = {
    value = 40
    months = 18
    decay = 1
}
```

---

## Template: Alliance Entry/Exit System

```
# Alliance membership
alliance_TAG_member_bonus = {
    value = 25
    decay = 0
}

# Joining alliance
on_join_alliance_TAG = {
    every_country = {
        limit = { is_in_alliance_TAG = yes }
        add_opinion_modifier = {
            target = ROOT
            modifier = alliance_TAG_member_bonus
        }
        reverse_add_opinion_modifier = {
            target = PREV
            modifier = alliance_TAG_member_bonus
        }
    }
}

# Leaving alliance (betrayal)
alliance_TAG_betrayal = {
    value = -100
    months = 36
}

on_leave_alliance_TAG = {
    every_country = {
        limit = { is_in_alliance_TAG = yes }

        # Remove friendship bonus
        remove_opinion_modifier = {
            target = ROOT
            modifier = alliance_TAG_member_bonus
        }

        # Add betrayal penalty
        add_opinion_modifier = {
            target = ROOT
            modifier = alliance_TAG_betrayal
        }
    }
}
```

---

## Template: Progressive Relationship System

```
# Stage 1: Neutral
neutral_relations = {
    value = 0
}

# Stage 2: Warming
warming_relations = {
    value = 20
    months = 12
}

# Stage 3: Friendly
friendly_relations = {
    value = 40
    months = 24
    decay = 1
}

# Stage 4: Close Allies
close_allies = {
    value = 75
    decay = 0
}

# Cooling stages
cooling_relations = {
    value = -20
    months = 12
    decay = 2
}

hostile_relations = {
    value = -60
    months = 24
}
```

**Implementation:**
```
# Upgrade relationship
if = {
    limit = {
        has_opinion_modifier = {
            target = FROM
            modifier = warming_relations
        }
    }
    remove_opinion_modifier = {
        target = FROM
        modifier = warming_relations
    }
    add_opinion_modifier = {
        target = FROM
        modifier = friendly_relations
    }
}
```

---

## Common Mistakes

### ❌ Wrong: No Fallback

```
# BAD - What if player keeps territory?
option = {
    name = "Return territory"
    add_opinion_modifier = { modifier = returned_territory }
}
# Missing option for keeping territory!
```

### ✅ Correct: All Outcomes Covered

```
option = {
    name = "Return territory"
    add_opinion_modifier = { modifier = returned_territory }
}

option = {
    name = "Keep territory"
    add_opinion_modifier = { modifier = kept_territory }
}
```

### ❌ Wrong: Conflicting Decay

```
# BAD - Decay makes duration meaningless
long_term_modifier = {
    value = 50
    months = 24  # Says "24 months"
    decay = 10   # But decays in 5 months!
}
```

### ✅ Correct: Matching Decay and Duration

```
# GOOD - Decay aligns with duration
long_term_modifier = {
    value = 50
    months = 50
    decay = 1  # Decays over 50 months
}
```

### ❌ Wrong: Forgetting Removal

```
# BAD - Permanent embargo without removal mechanism
permanent_embargo = {
    trade = yes
    value = -100
    # How do you lift this?
}
```

### ✅ Correct: Removal Path

```
# Add embargo
add_opinion_modifier = {
    modifier = temporary_embargo
}

# Later: Lift embargo decision
remove_opinion_modifier = {
    modifier = temporary_embargo
}
add_opinion_modifier = {
    modifier = embargo_lifted
}
```

---

## Best Practices Summary

1. **Use Descriptive Names**: `GER_returned_territory` not `good_thing`
2. **Provide Counterparts**: For every positive modifier, consider a negative version
3. **Plan Decay Carefully**: Match duration to decay rate
4. **Document Intent**: Use comments to explain modifier purpose
5. **Test AI Behavior**: Verify AI responds appropriately to opinion changes
6. **Balance Values**: Don't overuse extreme values (±100+)
7. **Clean Up**: Remove obsolete modifiers in events
8. **Reciprocal When Needed**: Use `reverse_add_opinion_modifier` for mutual feelings
9. **Localize Everything**: Players need to see why opinion changed
10. **Consider Stacking**: Multiple modifiers add up - plan accordingly
