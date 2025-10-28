# Code Style and Conventions

## General HOI4 Modding Conventions
- Use tabs for indentation (consistent with HOI4 standard)
- Curly braces `{}` for code blocks
- Comments use `#` prefix
- File encoding: UTF-8 (important for Japanese text)

## Naming Conventions

### Files
- **System files:** `_bsm_<system_name>.txt` (e.g., `_bsm_Harvest_System.txt`)
- **Country-specific:** `<three_letter_tag>.txt` (e.g., `JPN.txt`, `USA.txt`)
- **Generic content:** Descriptive names (e.g., `generic.txt`, `common.txt`)
- **Categories:** `categories/` subdirectory for decision categories

### Variables and Flags
- **Country flags:** Descriptive snake_case (e.g., `should_check_decision`, `HS_AF`)
- **Variables:** CamelCase for complex systems (e.g., `Unified_Currency`)
- **BSM prefixes:** Used for custom system identifiers

### Code Structure
- **Triggers:** Logical grouping with AND/OR operators
- **Effects:** Sequential execution with proper scoping
- **Early returns:** Lightweight conditions checked first for performance
- **Comments:** Japanese comments for context, English for technical notes

## Performance Optimization Patterns
```hoi4
# GOOD: Early return pattern
trigger = {
    has_war_with = ITA          # Check lightweight condition first
    any_state = {               # Then expensive operations
        is_controlled_by = ITA
    }
}

# BAD: Heavy operation first
trigger = {
    any_state = {               # Expensive check
        is_controlled_by = ITA
    }
    has_war_with = ITA          # Should be first
}
```

## Localization Conventions
- **File format:** `.yml` with proper YAML structure
- **Key naming:** Consistent with feature area
- **Language:** Primary in Japanese, with English translation support
- **Encoding:** UTF-8 with BOM for proper Japanese character support

## Documentation Standards
- **Context files:** Stored in `documents/00_coding_contexts/`
- **Inline comments:** Explain complex logic and performance considerations
- **System documentation:** Comprehensive guides for custom BSM systems