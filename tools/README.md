# Mod validation tools

## `validate_mod.py`

Static validation for the `bakasekai` HoI4 mod — the practical analogue of a
test suite for a data-driven Paradox mod. It catches classes of errors that
otherwise only surface as silent failures in the game's `error.log`, without
needing to launch the game.

```bash
python3 tools/validate_mod.py            # validates ./bakasekai
python3 tools/validate_mod.py path/to/mod
```

Exit code is non-zero when any **ERROR**-level issue is found, so it gates CI
(see `.github/workflows/validate-mod.yml`). **WARN**-level issues are reported
but do not fail the build.

### Checks

| Check | Level | What it catches |
|-------|-------|-----------------|
| filename hygiene | ERROR (space before extension) / WARN (double space) | files the engine may skip or that break tooling, e.g. `GER_scripted_effects .txt` |
| brace balance | ERROR | unbalanced `{ }` in `common/`, `events/`, `history/`, `map/` script files — a parse-breaking bug |
| duplicate event id | ERROR | the same `namespace.N` **defined** more than once (invocations at deeper nesting are correctly ignored) |
| country-tag files | ERROR | a `TAG = "countries/..."` whose file is missing (`dynamic_tags = yes` files are skipped — their countries are runtime-generated) |
| duplicate focus id | ERROR | the same focus `id` defined twice (focus ids must be globally unique; the engine otherwise drops one silently) |
| localisation | ERROR (missing BOM / malformed header) / WARN (empty file, duplicate key) | `.yml` files the engine silently drops, and duplicate keys |
| duplicate scripted effect/trigger | WARN | a `name = { ... }` defined in two files, where one silently overrides the other |

This complements the existing **CWTools CI** (`.github/workflows/cwtools.yml`),
which already covers undefined references and type/syntax checking — these
checks target classes of bug CWTools does not flag well (duplicate
definitions, filename hygiene, localisation file integrity).

## `loc_coverage.py`

Reports English translation coverage by diffing the Japanese (source) and
English (target) localisation key sets. Useful for driving the Paratranz
translation effort.

```bash
python3 tools/loc_coverage.py                 # summary, always exit 0
python3 tools/loc_coverage.py --list          # also list missing/orphaned keys
python3 tools/loc_coverage.py --strict 0.95   # exit 1 if coverage < 95%
```

It is informational by default (exit 0) so it can run as a non-blocking CI
step; switch to `--strict` once coverage is high enough to gate on.

## Roadmap

These checks are deliberately high-confidence / low-false-positive. Natural
next steps to grow coverage (see the test-coverage analysis):

- focus-tree reachability (no unreachable or cyclic `prerequisite` focuses);
- per-entity localisation coverage (every focus/idea/event/decision id resolves
  to a key), building on `loc_coverage.py`;
- native in-engine [Scripted Event Test Bundles](../bakasekai/tests/_documentation.info)
  for AI / focus-tree regression testing (currently all empty) — these assert
  alt-history gameplay outcomes and need mod-specific design before authoring.
