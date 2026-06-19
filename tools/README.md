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
| localisation | ERROR (missing BOM / malformed header) / WARN (empty file, duplicate key) | `.yml` files the engine silently drops, and duplicate keys |

### Roadmap

These checks are deliberately high-confidence / low-false-positive. Natural
next steps to grow coverage (see the test-coverage analysis):

- broken reference checks (undefined state / province / country tag / idea /
  focus references) — the closest thing to a full `error.log` clone;
- localisation **key coverage** (every focus/idea/event/decision has a loc
  entry, per language) to drive the English translation effort;
- focus-tree reachability (no unreachable or cyclic `prerequisite` focuses);
- native in-engine [Scripted Event Test Bundles](../bakasekai/tests/_documentation.info)
  for AI / focus-tree regression testing (currently all empty).
