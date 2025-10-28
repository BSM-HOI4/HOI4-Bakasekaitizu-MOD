# Codebase Structure

## Root Directory Structure
```
/
├── bakasekai/          # Main mod content (HOI4 standard structure)
├── flags/              # Country flag assets (organized by number prefixes: 00/, 01/, 02/, 03/)
├── documents/          # Development documentation and optimization guides
│   └── 00_coding_contexts/  # Context-specific documentation
├── CLAUDE.md           # Project instructions for AI assistants
├── README.md           # Project documentation
└── .gitignore          # Git ignore patterns
```

## Core Bakasekai Directory (Main Mod Content)
```
bakasekai/
├── common/             # Game rules, countries, focuses, decisions, ideas
│   ├── decisions/      # Decision definitions and categories
│   ├── national_focus/ # Country focus trees
│   ├── ideas/          # National spirits and advisors
│   ├── characters/     # Leader and character definitions
│   ├── scripted_triggers/ # Custom trigger definitions
│   ├── scripted_effects/  # Custom effect definitions
│   ├── scripted_guis/  # Custom GUI scripting
│   └── country_tags/   # Country tag definitions
├── events/             # Event definitions for countries and mechanics
├── history/            # Initial game state (countries, states, units)
├── localisation/       # Text translations (primarily Japanese)
│   └── japanese/       # Japanese language files (.yml)
├── gfx/                # Graphics and interface files
│   ├── interface/      # UI graphics and icons
│   └── fonts/          # Custom font files
├── interface/          # UI definitions and scripted GUIs
├── map/                # Map data, provinces, terrain
├── tests/              # Test scenarios for different countries
└── descriptor.mod      # Mod metadata and configuration
```

## File Organization Patterns
- **Country-specific files:** Use 3-letter country codes (e.g., `JPN.txt`, `USA.txt`)
- **System files:** Prefixed with `_bsm_` (Bakasekai System Modules)
- **Generic/shared content:** Named generically (e.g., `generic.txt`)
- **Localization:** Organized by feature area in `localisation/japanese/`

## Custom Systems (BSM Prefix)
All custom systems use the `_bsm_` prefix to distinguish them from base game files:
- `_bsm_Harvest_System.*` - Food production and agriculture
- `_bsm_mine_system.*` - Mining and resource extraction
- `_bsm_mercenary_system.*` - Mercenary recruitment and management