# CLAUDE.md

Do not modify any `.wav` or `.ogg` files.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **HOI4-Bakasekaitizu-MOD** (バカ世界地図MOD), a comprehensive Hearts of Iron IV modification based on the "Foolish World Map Project" from Chakuwiki. It's a total conversion mod that reimagines the world with alternative history, geography, and countries.

## Key Development Information

### Performance Optimization Commands
Use the in-game profiler to identify performance bottlenecks:
```
imgui show profiler
```
Enable collection and use the Script tab to analyze processing times. Focus on optimizing `hourly` processes which impact performance most.

### Project Structure

**Core Directories:**
- `bakasekai/` - Main mod content (HOI4 standard structure)
- `documents/00_coding_contexts/` - Development documentation and optimization guides
- `flags/` - Country flag assets organized by number prefixes (00/, 01/, 02/, 03/)

**Critical HOI4 Mod Structure:**
- `bakasekai/common/` - Game rules, countries, focuses, decisions, ideas, etc.
- `bakasekai/events/` - Event definitions for countries and mechanics
- `bakasekai/history/` - Initial game state (countries, states, units)
- `bakasekai/localisation/` - Text translations (primarily Japanese)
- `bakasekai/gfx/` - Graphics and interface files
- `bakasekai/map/` - Map data, provinces, terrain
- `bakasekai/interface/` - UI definitions and scripted GUIs

### Mod Configuration
- **Version:** Alpha 0.1
- **Supported HOI4 Version:** 1.13.*
- **Dependencies:** Japanese Language mod
- **Steam Workshop ID:** 2585391890

### Custom Systems

**BSM (Bakasekai) Systems:**
- Harvest System (`_bsm_Harvest_System.*`)
- Mine Development System (`_bsm_mine_system.*`) 
- Mercenary System (`_bsm_mercenary_system.*`)
- Custom diplomatic actions and scripted GUIs

**Modified Vanilla Systems:**
- **Ideologies:** Vanilla ideology names have been changed to avoid conflicts:
  - `communism` → `communism_ideology`
  - `democratic` → `democratic_ideology`
  - `fascism` → `fascism_ideology`
  - `neutrality` → `neutrality_ideology`

**Performance Considerations:**
- Use early returns in triggers (check lightweight conditions first)
- Avoid `any_state` in frequently-executed code
- Leverage caching with country flags for state-dependent decisions
- Mission-type decisions are heavy - consider alternatives where possible

### Country Tags and Scope
The mod includes hundreds of custom countries with unique 3-letter tags:
- Major powers: USA, GBR, GER, SOV, JPN, etc.
- Custom nations: BKK (Bangkok), MAC (McDonald's), WES (Western Sahara), etc.
- Formable nations and dynamic countries supported

### Development Workflow

**File Organization:**
- Country-specific files use 3-letter country codes (e.g., `JPN.txt`, `USA.txt`)
- System files prefixed with `_bsm_`
- Generic/shared content in files like `generic.txt`

**Localization:**
- Primary language: Japanese (`localisation/japanese/`)
- Organized by feature area (countries, events, focuses)
- Uses `.yml` format with proper encoding

**Testing:**
- Custom test scenarios in `tests/` directory
- Debug events and decisions available
- Performance profiler integration for optimization

### Variable System
The mod uses HOI4's variable system extensively for dynamic content. Key commands:
- `set_variable = { var = name value = X }`
- `add_to_variable`, `subtract_from_variable`, `multiply_variable`, `divide_variable`
- `check_variable` for triggers
- Visualization in localization: `[?variable_name]`

### Character and Leader System
Extensive character definitions in `common/characters/` organized by country, including:
- Country leaders with custom traits
- Military advisors and field marshals  
- Custom portrait assignments in `portraits/`

## Development Best Practices

1. **Performance First:** Always consider the performance impact of triggers and effects, especially those that run hourly
2. **Consistent Naming:** Follow the established country code conventions and BSM prefixing
3. **Localization:** Ensure all new content has proper Japanese localization
4. **Testing:** Use debug tools and test scenarios to verify functionality
5. **Documentation:** Complex systems should include documentation files in appropriate directories
6. **Effects and Triggers:** When implementing logic, consult the coding context references:
   - Effects: `documents/00_coding_contexts/01_effects/effects.json`
   - Triggers: `documents/00_coding_contexts/04_triggers/triggers.json`

## Asset References
- For a complete list of goal interface graphics, see [goals_file_list.md](goals_file_list.md).
