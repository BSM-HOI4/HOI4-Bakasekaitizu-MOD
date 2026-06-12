---
name: hoi4-unit-design-creator
description: Create or revise Hearts of Iron IV ship, aircraft, and tank equipment variants in the current mod repository - create_equipment_variant effects, OOB unit design setup, module selections, upgrades, and Japanese localisation. For BSM naval variants using the hidden_slot (NVRW) system, prefer the hoi4-naval-oob-editor skill.
---

# HOI4 Unit Design Creator

Use this skill when adding or changing equipment variants or starting designs for ships, aircraft, or tanks in the current mod repository.

## Required Context

- Read `AGENTS.md` before changing files; follow its branch policy (work on a proper branch, never edit on `main`).
- Mod root: this repo's mod content lives under `bakasekai/` (e.g. `bakasekai/common/scripted_effects/`, `bakasekai/history/units/`). All paths below are relative to the mod root.
- **BSM naval variants**: this mod uses the SSW-derived hidden_slot (NVRW) system for ships. For ship variants and naval OOB, use the `hoi4-naval-oob-editor` skill instead; use this skill for tanks, aircraft, and plain vanilla-style setups.
- **AI-designed equipment**: if the goal is to let the AI design equipment itself, that is `common/ai_equipment/` - use the `hoi4-ai-modding` skill.
- Preserve repository style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing hulls, chassis, airframes, modules, scripted effects, OOB patterns, and localisation keys. Locate them token-efficiently with the `hoi4-searcher` skill.
- Add or update visible names in `localisation/japanese/` when needed.
- Do not port other repositories' (Tsareich2, SSW_mod) mod-specific IDs, tags, lore, or systems unless the user explicitly asks; they are reference repos only (see CLAUDE.md).

## Workflow

1. Identify target country, equipment type, and existing patterns:

```bash
rg -n -i -B 10 -A 35 'create_equipment_variant|variant_name|TAG_|ship|tank|airframe|equipment' common/scripted_effects history/units history/countries localisation/japanese
rg -n -i 'ship_hull|tank_chassis|airframe|_equipment' common/units common/technologies
```

2. Choose implementation method:

- Use `create_equipment_variant` when exact modules or upgrades matter.
- Use existing OOB variant levels only for simple vanilla-style setups.
- Put repeated or startup-created variants in a scripted effect rather than duplicating OOB blocks.

3. Validate base equipment and modules:

- Ships: confirm hull, fixed slots, custom slots, role, modules, armor, engine, and tech availability.
- Aircraft: confirm airframe, role modules, engine modules, weapon modules, and DLC-era syntax.
- Tanks: confirm chassis, turret/weapon/armor/engine modules, role, and equipment archetype.

4. Place definitions:

- Scripted effects: closest country or system file under `common/scripted_effects/`.
- Starting units or production: closest matching file under `history/units/` or country history, following the current mod's existing patterns.
- Localisation: `localisation/japanese/` when a player-visible variant name needs a key.

5. Keep IDs and names clear:

```hoi4
create_equipment_variant = {
  name = "Example Class"
  type = ship_hull_light_1
  parent_version = 0
  modules = {
    fixed_ship_battery_slot = ship_light_battery_1
  }
}
```

6. Verify:

```bash
rg -n 'variant_id|Example Class|create_equipment_variant' common/scripted_effects history/units history/countries localisation/japanese
rg -n '\t' common/scripted_effects history/units history/countries localisation/japanese
```

## Guardrails

- Do not invent module IDs; search existing equipment and technology definitions first.
- Do not port external naval module formulas or external mod-specific naval assumptions into Tsareich2.
- Keep balance and starting OOB changes scoped to the requested country or system.
