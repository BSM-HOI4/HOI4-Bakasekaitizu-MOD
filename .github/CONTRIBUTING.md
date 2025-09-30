# Contributing to HOI4-Bakasekaitizu-MOD

Thank you for your interest in contributing to the Bakasekaitizu MOD! This guide will help you get started with development.

## Development Setup

1. **Prerequisites:**
   - Hearts of Iron IV (version 1.13.*)
   - Japanese Language mod (dependency)
   - Text editor with Paradox script support (recommended: VS Code with HOI4 extensions)

2. **Local Development:**
   - Clone the repository
   - Copy/symlink the `bakasekai/` folder to your HOI4 mod directory
   - Enable the mod in HOI4 launcher alongside the Japanese Language mod

## Project Structure

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for detailed structure information.

## Development Workflow

### Before Making Changes
1. Test the current mod to understand existing behavior
2. Use in-game profiler (`imgui show profiler`) to establish performance baselines
3. Review related files in `documents/00_coding_contexts/` for reference

### Making Changes
1. Follow the coding standards outlined in the Copilot instructions
2. Use appropriate file naming conventions (3-letter country codes, `_bsm_` prefixes)
3. Test changes incrementally using debug commands
4. Add/update Japanese localisation for new content

### Performance Considerations
- Use early returns in triggers
- Avoid `any_state` in frequently-executed code
- Cache with country flags for expensive operations
- Monitor hourly processes impact

## Testing

### In-Game Testing
```
# Debug commands
tdebug                    # Enable debug mode
event <event_id> <TAG>   # Fire specific events
reload interface         # Reload UI changes
reload localisation      # Reload text changes (use carefully)
```

### Performance Testing
```
imgui show profiler      # Open performance profiler
# Focus on Script tab for mod impact analysis
```

## Localization

- **Primary**: Japanese (`localisation/japanese/`)
- **Format**: `.yml` files with proper UTF-8 BOM encoding
- **Header**: Must include `l_japanese:` line
- **Variables**: Use `[?variable_name]` for dynamic content

## Asset Guidelines

- **DO NOT** modify audio files (`.wav`, `.ogg`)
- Flag images go in numbered directories (`flags/00/`, `flags/01/`, etc.)
- Optimize graphics where possible
- Follow existing naming patterns

## Submitting Changes

1. **Commit Messages:**
   - Use imperative mood
   - Include scope prefix: `focus:`, `events:`, `localisation:`, `perf:`
   - Example: `focus: Add new Japanese industrial tree`

2. **Pull Request Information:**
   - Clear description of changes
   - List affected file paths
   - Include screenshots for UI changes
   - Note new/changed localisation keys
   - Mention save-compatibility impact
   - Include profiler observations if performance-related

## Community

- **Development Discord**: [Join here](https://discord.gg/nNYQGeePpR)
- **General Community**: [Discord Server](https://discord.com/invite/dykkFfVEp8)
- **Translation Project**: [Paratranz](https://paratranz.cn/projects/9454)

## Documentation

For comprehensive development information:
- **[CLAUDE.md](../CLAUDE.md)**: Detailed development guidance
- **[AGENTS.md](../AGENTS.md)**: Repository guidelines
- **[README.md](../README.md)**: Project overview and installation

## Questions?

Join our Discord servers or open an issue on GitHub for development questions.