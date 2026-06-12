# HOI4 Modifier Block Templates

## Template Categories

Pre-built modifier combinations for common use cases.

## Economic Templates

### Economic Boom
```
modifier = {
    stability_factor = 0.10
    production_speed_industrial_complex_factor = 0.15
    industrial_capacity_factory = 0.10
}
```

### Industrial Focus
```
modifier = {
    production_speed_industrial_complex_factor = 0.20
    production_speed_arms_factory_factor = 0.20
    production_factory_efficiency_gain_factor = 0.10
}
```

### Resource Efficiency
```
modifier = {
    local_resources_factor = 0.15
    production_factory_max_efficiency_factor = 0.10
    industrial_capacity_factory = 0.05
}
```

### Economic Depression
```
modifier = {
    consumer_goods_factor = 0.10
    stability_factor = -0.15
    production_speed_buildings_factor = -0.10
    industrial_capacity_factory = -0.10
}
```

## Military Templates

### Military Readiness
```
modifier = {
    conscription_factor = 0.10
    training_time_factor = -0.10
    army_org_factor = 0.05
    experience_gain_factor = 0.05
}
```

### Offensive Doctrine
```
modifier = {
    army_attack_factor = 0.15
    planning_speed = 0.10
    max_planning = 0.10
}
```

### Defensive Posture
```
modifier = {
    army_defence_factor = 0.20
    army_org_factor = 0.10
    land_reinforce_rate = 0.05
}
```

### Total Mobilization
```
modifier = {
    conscription_factor = 0.20
    war_support_factor = 0.10
    training_time_factor = -0.20
    consumer_goods_factor = -0.05
}
```

## Naval Templates

### Naval Supremacy
```
modifier = {
    navy_org_factor = 0.10
    naval_coordination_factor = 0.15
    convoy_escort_efficiency = 0.10
}
```

### Submarine Warfare
```
modifier = {
    convoy_raiding_efficiency_factor = 0.20
    naval_speed_factor = 0.10
}
```

### Fleet Expansion
```
modifier = {
    production_speed_dockyard_factor = 0.20
    industrial_capacity_dockyard = 0.15
    navy_org_factor = 0.05
}
```

## Air Force Templates

### Air Superiority
```
modifier = {
    air_attack_factor = 0.15
    air_defence_factor = 0.10
    air_superiority_attack_factor = 0.10
}
```

### Strategic Bombing Focus
```
modifier = {
    air_attack_factor = 0.20
    air_range_factor = 0.15
}
```

## Political Templates

### Internal Stability
```
modifier = {
    stability_factor = 0.15
    war_support_factor = 0.10
    political_power_gain = 0.15
}
```

### Political Turmoil
```
modifier = {
    stability_factor = -0.20
    political_power_gain = -0.25
    drift_defence_factor = -0.30
}
```

### Ideological Shift (Democratic)
```
modifier = {
    democratic_drift = 0.05
    drift_defence_factor = -0.20
    political_power_factor = -0.10
}
```

## Hybrid Templates

### Total War Economy
```
modifier = {
    war_support_factor = 0.15
    conscription_factor = 0.15
    consumer_goods_factor = -0.05
    production_speed_arms_factory_factor = 0.10
    industrial_capacity_factory = 0.10
}
```

### Peacetime Prosperity
```
modifier = {
    stability_factor = 0.15
    consumer_goods_factor = -0.05
    production_speed_industrial_complex_factor = 0.10
    political_power_gain = 0.10
}
```

### Military-Industrial Complex
```
modifier = {
    production_speed_arms_factory_factor = 0.15
    production_speed_dockyard_factor = 0.15
    industrial_capacity_factory = 0.10
    conscription_factor = 0.05
}
```

### Research Focus
```
modifier = {
    experience_gain_factor = 0.10
    political_power_gain = 0.10
    stability_factor = 0.05
}
```

## Negative Effect Templates

### War Exhaustion
```
modifier = {
    war_support_factor = -0.20
    stability_factor = -0.10
    conscription_factor = -0.15
    army_morale_factor = -0.10
}
```

### Economic Crisis
```
modifier = {
    consumer_goods_factor = 0.15
    stability_factor = -0.20
    production_speed_buildings_factor = -0.15
    political_power_gain = -0.20
}
```

### Internal Strife
```
modifier = {
    stability_factor = -0.25
    political_power_gain = -0.30
    conscription_factor = -0.10
    war_support_factor = -0.15
}
```

## Balanced Templates

### Moderate Growth
```
modifier = {
    stability_factor = 0.05
    production_speed_industrial_complex_factor = 0.05
    political_power_gain = 0.05
}
```

### Military Preparedness
```
modifier = {
    conscription_factor = 0.05
    training_time_factor = -0.05
    production_speed_arms_factory_factor = 0.05
}
```

## Customization Guidelines

When building custom modifiers:

1. **Keep it themed** - Related modifiers work better together
2. **Balance values** - Typical range: 0.05 to 0.20 for buffs
3. **Consider trade-offs** - Mix positive and negative for realism
4. **Don't overload** - 3-5 modifiers per idea is ideal
5. **Test balance** - Large values can break gameplay

## Value Recommendations

**Minor effects:** ±0.05
**Standard effects:** ±0.10
**Major effects:** ±0.15 to ±0.20
**Extreme effects:** ±0.25+ (use sparingly)
