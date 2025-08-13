# Task Completion Checklist

## When a Development Task is Completed

### 1. Performance Validation
- [ ] **Run profiler check:** Use `imgui show profiler` in HOI4 console
- [ ] **Check hourly processes:** Ensure no performance regressions in Script tab
- [ ] **Validate triggers:** Confirm early returns and lightweight condition ordering

### 2. Code Quality Checks
- [ ] **File naming:** Follow BSM prefix conventions for system files
- [ ] **Indentation:** Use tabs consistently throughout the file
- [ ] **Comments:** Add Japanese context comments where needed
- [ ] **Scoping:** Verify proper ROOT/FROM scope usage in triggers

### 3. Functionality Testing
- [ ] **Load in-game:** Verify mod loads without errors in HOI4
- [ ] **Test scenarios:** Run relevant test files from `bakasekai/tests/`
- [ ] **Debug logging:** Check HOI4 error logs for any issues

### 4. Localization Check (if applicable)
- [ ] **Japanese localization:** Ensure proper .yml format in `localisation/japanese/`
- [ ] **UTF-8 encoding:** Verify file encoding supports Japanese characters
- [ ] **Key consistency:** Match localization keys with game script references

### 5. Integration Validation
- [ ] **File structure:** Confirm files are in correct HOI4 directory structure
- [ ] **Dependencies:** Verify any cross-system references are valid
- [ ] **Country tags:** Ensure 3-letter country codes are properly defined

### 6. Documentation Updates (if major changes)
- [ ] **Context documentation:** Update files in `documents/00_coding_contexts/` if needed
- [ ] **CLAUDE.md:** Update project instructions if workflow changes
- [ ] **Comments:** Add inline documentation for complex systems

## Common Issues to Avoid
- **Performance:** Avoid `any_state` in frequently-executed code
- **Caching:** Use country flags for expensive state-dependent decisions
- **Mission decisions:** Consider alternatives as they are performance-heavy
- **Early returns:** Always check lightweight conditions first in triggers

## Final Verification
- [ ] **Game loads:** Mod loads in HOI4 without crashing
- [ ] **No errors:** Check HOI4 error.log for any script errors
- [ ] **Performance:** No significant slowdown in profiler
- [ ] **Functionality:** Core features work as expected in test scenarios