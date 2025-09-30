# GitHub Copilot Instructions

This repository contains the **HOI4-Bakasekaitizu-MOD** (バカ世界地図MOD), a Hearts of Iron IV total conversion mod. This file provides GitHub Copilot with essential context for effective code assistance.

## Project Context

- **Type**: Hearts of Iron IV modification/mod
- **Language**: Primarily Paradox scripting languages, with Japanese localization
- **Target Version**: Hearts of Iron IV 1.13.*
- **Dependencies**: Japanese Language mod
- **Status**: Alpha 0.1

## Repository Structure

```
bakasekai/                 # Main mod content (HOI4 standard structure)
├── common/               # Game rules, countries, focuses, decisions, ideas
├── events/               # Event definitions for countries and mechanics
├── history/              # Initial game state (countries, states, units)
├── localisation/japanese/ # Text translations (Japanese primary)
├── gfx/                  # Graphics and interface files
├── interface/            # UI definitions and scripted GUIs
└── map/                  # Map data, provinces, terrain

documents/00_coding_contexts/ # Development documentation and references
flags/                    # Country flag assets (organized by number prefixes)
```

## Coding Standards & Conventions

### File Naming
- **Country-specific files**: Use 3-letter country codes (e.g., `JPN.txt`, `USA.txt`)
- **System files**: Prefix with `_bsm_` (e.g., `_bsm_mine_system.txt`)
- **Generic content**: Use descriptive names like `generic.txt`

### Scripting Style
- **Indentation**: 2 spaces, no tabs
- **Format**: One statement per line
- **Performance**: Use early returns in triggers, avoid `any_state` in frequent scopes
- **Caching**: Leverage country flags for state-dependent decisions

### Modified Vanilla Systems
- **Ideologies**: Renamed to avoid conflicts:
  - `communism` → `communism_ideology`
  - `democratic` → `democratic_ideology`
  - `fascism` → `fascism_ideology`
  - `neutrality` → `neutrality_ideology`

## Custom Systems (BSM Prefixed)

The mod includes several custom systems:
- Harvest System (`_bsm_Harvest_System.*`)
- Mine Development System (`_bsm_mine_system.*`)
- Mercenary System (`_bsm_mercenary_system.*`)
- Custom diplomatic actions and scripted GUIs

## Variable System Usage

HOI4's variable system is extensively used:
```
set_variable = { var = name value = X }
add_to_variable, subtract_from_variable, multiply_variable, divide_variable
check_variable = { var > value } # for triggers
```
- Visualization in localization: `[?variable_name]`

## Localization Standards

- **Primary language**: Japanese (`localisation/japanese/`)
- **Format**: `.yml` files with `l_japanese:` header
- **Encoding**: UTF-8 with BOM
- **Organization**: By feature area (countries, events, focuses)
- **Variables**: Use `[?var]` for dynamic content

## Performance Optimization

- **Early returns**: Check lightweight conditions first in triggers
- **Avoid heavy operations**: `any_state` in frequently-executed code
- **Use caching**: Country flags for state-dependent decisions
- **Mission decisions**: Heavy operations - consider alternatives
- **Profiling**: Use `imgui show profiler` in-game, focus on Script tab

## Testing & Development

- **Debug commands**: `tdebug`, `event <id> <TAG>`, `reload interface`
- **Test scenarios**: Located in `tests/` directory
- **Performance verification**: Monitor hourly processes
- **Cleanup**: Include reversible changes in debug content

## Asset Guidelines

- **DO NOT modify**: `.wav` or `.ogg` files
- **Flag organization**: Use number-prefixed directories (00/, 01/, 02/, 03/)
- **Graphics**: Optimize images where applicable
- **Portraits**: Custom assignments in `portraits/` directory

## Documentation References

For detailed information, consult these comprehensive guides:
- **[CLAUDE.md](../CLAUDE.md)**: Complete development guidance for AI assistants
- **[AGENTS.md](../AGENTS.md)**: Repository guidelines and workflow
- **Effects/Triggers**: `documents/00_coding_contexts/01_effects/effects.json` and `documents/00_coding_contexts/04_triggers/triggers.json`

## Country Tags & Scope

The mod includes hundreds of custom countries with unique 3-letter tags:
- **Major powers**: USA, GBR, GER, SOV, JPN
- **Custom nations**: BKK (Bangkok), MAC (McDonald's), WES (Western Sahara)
- **Formable nations**: Dynamic countries supported

## Commit Guidelines

- **Format**: Imperative mood with scope prefix (`focus:`, `events:`, `localisation:`, `perf:`)
- **Description**: Include affected paths, UI screenshots, localization changes
- **Compatibility**: Note save-compatibility impact
- **Performance**: Include profiler observations when relevant