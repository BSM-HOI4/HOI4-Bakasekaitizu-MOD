# Repository Guidelines

## Project Structure & Modules
- `bakasekai/`: Core HOI4 content. Key subdirs: `common/`, `events/`, `history/`, `localisation/japanese/`, `gfx/`, `interface/`, `map/`.
- `documents/00_coding_contexts/`: Effect/trigger references and development notes.
- `flags/00/, 01/, 02/, 03/`: Country flag assets by shard.
- `tests/`: Custom scenarios and debug setups.

## Build, Test, and Development
- Run locally: load the folder as a mod in the Paradox Launcher (supports HOI4 1.13.*; depends on Japanese Language mod).
- Profiling: open console and run `imgui show profiler`, use the Script tab; focus on hourly processes.
- Debugging: use `tdebug`, `event <id> <TAG>`, `reload interface`, and (when safe) `reload localisation`.

## Coding Style & Naming
- Indentation: 2 spaces, no tabs; one statement per line.
- File naming: country-specific files use 3-letter tags (e.g., `common/national_focus/JPN.txt`, `events/USA.txt`).
- System files: prefix with `_bsm_` (e.g., `_bsm_mine_system.txt`).
- Ideologies: use renamed keys (`communism_ideology`, `democratic_ideology`, `fascism_ideology`, `neutrality_ideology`).
- Localisation: in `localisation/japanese/*.yml` with `l_japanese:` header; UTF-8 with BOM; keep keys consistent and use variables like `[?var]` when needed.

## Testing Guidelines
- Prefer minimal, isolated test content under `_bsm_*_test.*` and scenarios in `tests/`.
- Verify performance: early-return triggers, avoid `any_state` in frequent scopes, cache via flags.
- Use console to fire debug events; include cleanup effects and reversible changes.

## Commit & Pull Request Guidelines
- Commits: imperative mood, concise scope prefix (e.g., `focus:`, `events:`, `localisation:`, `perf:`).
- Include in PRs: clear description, linked issues, affected paths, screenshots for UI, list of new/changed localisation keys, save-compatibility notes, and profiler observations when relevant.
- Assets: do not modify `.wav` or `.ogg` files; optimize images where applicable.

## Security & Configuration
- No secrets in repo or configs. Keep Workshop ID `2585391890` referenced only in publishing flow.
- Versioning: Alpha 0.1; target HOI4 1.13.*. Align changes with this baseline.
