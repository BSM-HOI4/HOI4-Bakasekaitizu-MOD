---
name: hoi4-techtree-creator
description: Create or revise Hearts of Iron IV technology trees in the current mod repository - technology definitions, folder layout, countrytechtreeview GUI entries, technology GFX sprites, icons, categories, unlocks, and Japanese localisation. Use when adding technologies, creating a new tech folder/tab, or wiring tech tree GUI.
---

# HOI4 Techtree Creator

Use this skill when adding or changing technology folders, technologies, or technology tree GUI wiring in the current mod repository.

## Required Context

- Read `AGENTS.md` before changing files; follow its branch policy (work on a proper branch, never edit on `main`).
- Mod root: this repo's mod content lives under `bakasekai/` (e.g. `bakasekai/common/technologies/`). All paths below are relative to the mod root.
- Preserve repository style: 2 spaces, no tabs, one statement per line, nearby naming patterns. BSM system files use `_bsm_`/`bsm_` prefixes.
- Prefer existing technology folders, GUI container patterns, GFX sprites, categories, and localisation keys. Locate them token-efficiently with the `hoi4-searcher` skill (`--type tech`, `--type gfx`).
- Add or update visible text in `localisation/japanese/`.
- Do not port other repositories' (Tsareich2, SSW_mod) mod-specific IDs, tags, lore, or systems unless the user explicitly asks; they are reference repos only (see CLAUDE.md).

## Workflow

1. Inspect existing technology and GUI patterns:

```bash
rg -n 'technologies\s*=\s*\{|folder\s*=\s*\{|categories\s*=' common/technologies
rg -n 'containerWindowType|techtree_.*folder|countrytechtreeview' interface
rg -n -i 'GFX_.*tech|spriteType|technolog' interface gfx localisation/japanese
```

2. Choose a reference folder from the current mod itself:

- Use the closest existing folder for canvas size, orientation, year spacing, category spacing, item sizes, and tab patterns.
- Do not use template numbers blindly; measure from `interface/countrytechtreeview.gui` and nearby `.gfx` files.

3. Define technologies:

- Place under the closest `common/technologies/` file or a focused new file.
- Use local variable names for rows, columns, years, and categories when the nearby file does.
- Set `folder`, `position`, `categories`, `research_cost`, `start_year`, prerequisites, and unlocks deliberately.
- Prefer existing equipment, modules, bonuses, or scripted effects over inventing disconnected unlocks.

4. Wire GUI and GFX:

- Add folder, tab, and item entries using the reference folder's structure.
- Define technology sprites in the closest existing `.gfx` file or a focused new one.
- Put new icons under an existing `gfx/interface/technologies/` pattern when assets are supplied.

5. Add localisation:

```yaml
l_japanese:
 tech_id:0 "..."
 tech_id_desc:0 "..."
 tech_folder_name:0 "..."
```

6. Verify:

```bash
rg -n 'tech_id|folder_name|GFX_.*tech_id' common/technologies interface localisation/japanese
rg -n '\t' common/technologies interface localisation/japanese
```

## References

- GUI template notes: `references/gui-templates.md`
