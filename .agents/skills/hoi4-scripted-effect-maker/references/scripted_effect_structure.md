# HOI4 Scripted Effect Structure Reference

## Basic Structure

Scripted effects are defined in `common/scripted_effects/<filename>.txt`:

```
effect_name = {
    # Effect contents
    add_political_power = 100
    add_stability = 0.05
}
```

## Scopes

Effects can work in different scopes:

- **Country Scope** - Most common, affects a country
- **State Scope** - Affects a state
- **Character Scope** - Affects a character
- **Unit Leader Scope** - Affects a unit leader

Always document the required scope in a comment:

```
# Country scope
effect_name = {
    # ...
}
```

## Custom Tooltips

Provide user-facing tooltips:

```
effect_name = {
    custom_effect_tooltip = effect_name_tt
    hidden_effect = {
        # Actual effects
        add_political_power = 100
    }
}
```

Localization entry:
```yaml
effect_name_tt:0 "Grants +100 Political Power"
```

## Parameters

Effects can accept parameters:

```
add_cores_on_state = {
    add_core_of = PREV
    add_claim_by = ROOT
}
```

## Common Patterns

### Grant Resources

```
grant_industrial_bonus = {
    random_owned_controlled_state = {
        add_building_construction = {
            type = industrial_complex
            level = 2
            instant_build = yes
        }
    }
}
```

### Add Multiple Ideas

```
add_economic_ideas = {
    add_ideas = economic_boom
    add_ideas = industrial_expansion
    add_ideas = trade_focus
}
```

### Conditional Effects

```
conditional_stability_boost = {
    if = {
        limit = { has_war = no }
        add_stability = 0.10
    }
    else = {
        add_war_support = 0.10
    }
}
```

### Cleanup Effects

```
remove_temporary_modifiers = {
    remove_ideas = temp_modifier_1
    remove_ideas = temp_modifier_2
    remove_ideas = temp_modifier_3
}
```

## Calling Scripted Effects

In other files (events, focuses, etc.):

```
# Simple call
effect_name = yes

# Or just
effect_name
```

## Best Practices

1. **Name clearly** - Use descriptive names
2. **Document scope** - Add comment specifying required scope
3. **Use tooltips** - For user-visible effects
4. **Group related effects** - Keep similar effects in same file
5. **Avoid duplication** - Reuse existing scripted effects
6. **Test thoroughly** - Ensure effects work in all cases

## Example: Complete Effect

```
# Country scope
# Grants economic bonuses and removes depression
enact_new_deal = {
    custom_effect_tooltip = enact_new_deal_tt
    hidden_effect = {
        # Remove depression
        if = {
            limit = { has_idea = great_depression }
            remove_ideas = great_depression
        }

        # Add recovery ideas
        add_ideas = economic_recovery
        add_ideas = public_works_program

        # Grant factories
        random_owned_controlled_state = {
            add_building_construction = {
                type = industrial_complex
                level = 2
                instant_build = yes
            }
        }

        # Add stability
        add_stability = 0.05
        add_political_power = 50
    }
}
```

Localization:
```yaml
enact_new_deal_tt:0 "Implement New Deal economic reforms"
```
