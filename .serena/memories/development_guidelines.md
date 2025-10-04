# Development Guidelines and Best Practices

## Performance Optimization Guidelines

### Priority: Hourly Process Optimization
The most critical performance consideration is optimizing code that runs hourly in HOI4:

1. **Avoid heavy operations in hourly triggers**
   - `any_state` is extremely expensive
   - Mission-type decisions are performance-heavy
   - Use alternatives like events or standard decisions when possible

2. **Implement early returns in triggers**
   ```hoi4
   # GOOD: Check lightweight conditions first
   trigger = {
       has_war_with = ITA
       any_state = { is_controlled_by = ITA }
   }
   
   # BAD: Heavy operation first
   trigger = {
       any_state = { is_controlled_by = ITA }
       has_war_with = ITA
   }
   ```

3. **Use caching with country flags**
   ```hoi4
   # Set flag only when state changes
   on_actions = {
       on_state_control_changed = {
           set_country_flag = {
               flag = should_check_decision
               days = 1
           }
       }
   }
   
   # Check flag before expensive operations
   trigger = {
       has_country_flag = should_check_decision
       any_state = { ... }
   }
   ```

## Code Design Patterns

### BSM System Architecture
- **Prefix convention:** All custom systems use `_bsm_` prefix
- **Modular design:** Each system (Harvest, Mine, Mercenary) is self-contained
- **Scripted GUIs:** Custom interfaces for enhanced user experience
- **Variable system:** Extensive use of HOI4's variable system for dynamic content

### Scoping Best Practices
- **ROOT scope:** The country executing the trigger/effect
- **FROM scope:** The target country in diplomatic actions
- **PREV scope:** Previous scope in nested contexts
- **Clear documentation:** Comment complex scope chains

## File Organization Standards

### Directory Structure
- **common/decisions/** - Decision definitions
- **common/decisions/categories/** - Decision category definitions
- **events/** - Event files with country-specific prefixes
- **localisation/japanese/** - All Japanese text translations

### Naming Conventions
- **System files:** `_bsm_<SystemName>.txt`
- **Country files:** `<TAG>.txt` (three-letter country codes)
- **Categories:** Separate directory for decision categories
- **Localization:** Feature-area organization

## Testing and Quality Assurance

### Built-in Testing Framework
- **Test scenarios:** Located in `bakasekai/tests/`
- **Country-specific tests:** Individual files for major powers
- **AI testing:** `test_AI.txt` for AI behavior validation
- **Documentation:** `_documentation.info` explains test syntax

### Performance Monitoring
- **Profiler integration:** Use `imgui show profiler` for analysis
- **Script timing:** Monitor processing times in Script tab
- **Hourly focus:** Pay special attention to hourly process performance

## Localization Standards

### Japanese Primary Support
- **Encoding:** UTF-8 with BOM for Japanese character support
- **Structure:** YAML format with proper key-value pairs
- **Organization:** Feature-based file organization
- **Translation:** English translation project via Paratranz

## Version Control Practices
- **Branch strategy:** Feature branches for development
- **Commit messages:** Clear, descriptive commit messages
- **File management:** Proper .gitignore for IDE and system files
- **Integration:** Regular merging with main branch

## Custom System Guidelines

### Variable System Usage
- **Dynamic content:** Use variables for changing game states
- **Localization integration:** Display variables with `[?variable_name]`
- **Mathematical operations:** Support for add, subtract, multiply, divide
- **Condition checking:** `check_variable` for trigger conditions

### Character and Leader System
- **Organization:** Files organized by country in `common/characters/`
- **Portraits:** Custom portrait assignments in `portraits/`
- **Traits:** Custom leader traits and advisor definitions
- **Military leaders:** Field marshals and military advisors