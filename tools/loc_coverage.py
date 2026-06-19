#!/usr/bin/env python3
"""Localisation coverage report for the bakasekai HoI4 mod.

Japanese is the source language; English is the translation target (see the
README / Paratranz project). This compares the set of keys defined in each
language and reports translation coverage, without needing to parse focus /
idea / event definitions.

  - keys in Japanese but missing in English  -> untranslated
  - keys in English but missing in Japanese  -> orphaned / obsolete

Usage:
    python3 tools/loc_coverage.py [MOD_ROOT]
    python3 tools/loc_coverage.py --list            # also list missing keys
    python3 tools/loc_coverage.py --strict 0.95     # exit 1 if coverage < 0.95

Default is informational (always exit 0) so it can run as a non-blocking CI
step. Use --strict to turn it into a gate once coverage is high enough.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_KEY_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s+"')


def collect_keys(lang_dir: Path) -> dict[str, str]:
    """Map loc key -> first file that defines it, for one language tree."""
    keys: dict[str, str] = {}
    if not lang_dir.exists():
        return keys
    for path in sorted(lang_dir.rglob("*.yml")):
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("l_"):
                continue
            m = _KEY_RE.match(line)
            if m and m.group(1) not in keys:
                keys[m.group(1)] = path.name
    return keys


def main(argv: list[str]) -> int:
    list_missing = "--list" in argv
    strict = None
    if "--strict" in argv:
        i = argv.index("--strict")
        strict = float(argv[i + 1])
        del argv[i : i + 2]
    args = [a for a in argv[1:] if not a.startswith("--")]
    root = Path(args[0]) if args else Path("bakasekai")

    loc = root / "localisation"
    jp = collect_keys(loc / "japanese")
    en = collect_keys(loc / "english")

    if not jp:
        print(f"no Japanese localisation found under {loc/'japanese'}", file=sys.stderr)
        return 2

    untranslated = sorted(set(jp) - set(en))
    orphaned = sorted(set(en) - set(jp))
    translated = len(jp) - len(untranslated)
    coverage = translated / len(jp)

    print("Localisation coverage (Japanese -> English)")
    print("-" * 44)
    print(f"  Japanese keys : {len(jp)}")
    print(f"  English keys  : {len(en)}")
    print(f"  Translated    : {translated}")
    print(f"  Untranslated  : {len(untranslated)}")
    print(f"  Orphaned (EN) : {len(orphaned)}")
    print(f"  Coverage      : {coverage:.1%}")

    if list_missing:
        if untranslated:
            print(f"\n::group::Untranslated keys ({len(untranslated)})")
            for k in untranslated:
                print(f"  {k}  ({jp[k]})")
            print("::endgroup::")
        if orphaned:
            print(f"\n::group::Orphaned English keys ({len(orphaned)})")
            for k in orphaned:
                print(f"  {k}  ({en[k]})")
            print("::endgroup::")

    if strict is not None and coverage < strict:
        print(f"\nFAILED: coverage {coverage:.1%} below threshold {strict:.1%}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
