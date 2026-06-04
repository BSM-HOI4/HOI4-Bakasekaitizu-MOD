# Opencode Instructions for bsm_test (HOI4-Bakasekaitizu-MOD)

Read `../AGENTS.md` before making changes. It is the shared source of truth for AI agents in this repository.

## Workflow

- Check branch and status before editing.
- Use a proper branch name: `type/scope_name`.
- Do not push directly to `main`.
- Merge completed work into `develop`.
- Split unrelated tasks into separate branches.

## Branch Examples

```text
feature/JPN_project
feature/_map_africa
feature/_system_harvest
fix/crash_JAP_event
archive/1.0
```

## Coding Rules

- Use 2 spaces, no tabs.
- Match existing bsm_test file structure and naming (`_bsm_` prefix for systems).
- Keep changes scoped.
- Preserve user changes.
- Add Japanese localisation for visible content.
- Do not modify `.wav` or `.ogg` files unless explicitly requested.
- Use `communism_ideology`, `democratic_ideology`, `fascism_ideology`, `neutrality_ideology` for ideology keys.
- Primary localisation path: `bakasekai/localisation/japanese/*.yml`.
