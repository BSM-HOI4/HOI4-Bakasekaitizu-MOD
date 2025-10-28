# Suggested Commands for Development

## Performance Analysis Commands
```bash
# In-game profiler (use in HOI4 console)
imgui show profiler
```
**Usage:** Enable collection in profiler, use Script tab to analyze processing times. Focus on optimizing `hourly` processes which impact performance most.

## Git Commands (Standard)
```bash
# Basic git operations
git status
git add .
git commit -m "Commit message"
git push origin feature/branch-name

# Branch management
git checkout -b feature/new-feature
git merge main
```

## File Operations (macOS/Darwin)
```bash
# Directory listing
ls -la
find . -name "*.txt" -type f

# File search and content
grep -r "pattern" bakasekai/
find bakasekai/ -name "*bsm*" -type f

# File editing
nano filename.txt
code filename.txt  # VS Code
```

## HOI4 Testing Commands
- **Test scenarios:** Located in `bakasekai/tests/`
- **Test execution:** Run through HOI4 game with test scenarios loaded
- **Debug logging:** Test results logged to HOI4 user directory under `logs/tests/`

## Project-Specific Utilities
```bash
# Search for BSM system files
find bakasekai/ -name "*_bsm_*" -type f

# Find country-specific files
find bakasekai/common/ -name "[A-Z][A-Z][A-Z].txt" -type f

# Search for localization keys
grep -r "l_japanese" bakasekai/localisation/
```

## Development Workflow Commands
```bash
# Check mod descriptor
cat bakasekai/descriptor.mod

# Validate file structure
ls -la bakasekai/common/
ls -la bakasekai/events/
ls -la bakasekai/history/

# Search for performance-critical code
grep -r "any_state" bakasekai/common/decisions/
grep -r "hourly" bakasekai/
```

## System-Specific Commands (Darwin/macOS)
```bash
# File permissions (if needed)
chmod +x script.sh

# Archive operations
tar -czf backup.tar.gz bakasekai/

# System info
uname -a
sw_vers  # macOS version
```

## Quality Assurance
- **No automated linting:** HOI4 mods don't use traditional linters
- **Testing:** Use in-game test scenarios in `bakasekai/tests/`
- **Performance:** Monitor with `imgui show profiler`
- **Validation:** Check game loading and error logs