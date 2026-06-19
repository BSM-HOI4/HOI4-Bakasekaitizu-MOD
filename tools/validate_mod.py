#!/usr/bin/env python3
"""Static validation for the bakasekai HoI4 mod.

This is the practical analogue of "tests" for a data-driven Paradox mod:
it catches whole classes of errors that otherwise only surface as silent
failures in the game's error.log. None of the checks require the game to run.

Checks (high-confidence, low false-positive):
  1. filename hygiene  - stray/trailing whitespace in file names
  2. brace balance     - unbalanced { } in script files (breaks parsing)
  3. duplicate event id - same `namespace.N` defined more than once
  4. localisation       - missing UTF-8 BOM, missing `l_<lang>:` header,
                          and duplicate keys within a file

Exit code is non-zero if any ERROR-level issue is found, so it can gate CI.
WARN-level issues are reported but do not fail the build.

Usage:
    python3 tools/validate_mod.py [MOD_ROOT]
MOD_ROOT defaults to "bakasekai".
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MOD_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("bakasekai")

# Directories that contain Paradox script (where brace balance matters).
SCRIPT_DIRS = ["common", "events", "history", "map"]

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def iter_files(*suffixes: str):
    for path in MOD_ROOT.rglob("*"):
        if path.is_file() and path.suffix in suffixes:
            yield path


# Match an inline # comment and any double-quoted string so they are ignored
# when counting braces.
_STRIP_RE = re.compile(r'"(?:\\.|[^"\\])*"|#.*')


def strip_noise(line: str) -> str:
    return _STRIP_RE.sub("", line)


def check_filenames() -> None:
    for path in MOD_ROOT.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        rel = path.relative_to(MOD_ROOT.parent)
        if name != name.strip():
            err(f"[filename] leading/trailing whitespace in name: {rel}")
        elif "  " in name:
            warn(f"[filename] double space in name: {rel}")
        elif re.search(r"\s\.[^.]+$", name):
            err(f"[filename] space before extension: {rel}")


def check_brace_balance() -> None:
    for sub in SCRIPT_DIRS:
        base = MOD_ROOT / sub
        if not base.exists():
            continue
        for path in base.rglob("*.txt"):
            try:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            except OSError as exc:  # pragma: no cover - unexpected IO error
                err(f"[io] cannot read {path}: {exc}")
                continue
            depth = 0
            bad = False
            for line in text.splitlines():
                clean = strip_noise(line)
                depth += clean.count("{") - clean.count("}")
                if depth < 0:
                    bad = True
                    break
            rel = path.relative_to(MOD_ROOT.parent)
            if bad or depth != 0:
                err(f"[braces] unbalanced {{}} (net {depth:+d}): {rel}")


_ID_RE = re.compile(r"^\s*id\s*=\s*([A-Za-z0-9_]+\.[0-9]+)\s*(#.*)?$")


def check_event_ids() -> None:
    """Flag duplicate event *definitions*.

    An event definition's `id` sits at brace depth 1 (directly inside the
    top-level `country_event = { ... }` block). The identical `id = ns.N`
    line also appears in event *invocations* like
    `country_event = { id = ns.N days = 3 }`, but those are nested deeper
    (depth >= 3). Only depth-1 ids are real definitions, so we count those.
    """
    base = MOD_ROOT / "events"
    if not base.exists():
        return
    seen: dict[str, str] = {}
    for path in base.rglob("*.txt"):
        rel = str(path.relative_to(MOD_ROOT.parent))
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        depth = 0
        for line in text.splitlines():
            clean = strip_noise(line)
            m = _ID_RE.match(line)
            # depth here is the depth *inside* which this line sits, i.e. the
            # depth established by previous lines' braces.
            if m and depth == 1:
                eid = m.group(1)
                if eid in seen:
                    err(
                        f"[event-id] duplicate definition '{eid}' in {rel} "
                        f"(first in {seen[eid]})"
                    )
                else:
                    seen[eid] = rel
            depth += clean.count("{") - clean.count("}")


_KEY_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s+".*')
_HEADER_RE = re.compile(r"^﻿?l_[a-z_]+:\s*$")


def check_localisation() -> None:
    base = MOD_ROOT / "localisation"
    if not base.exists():
        return
    for path in base.rglob("*.yml"):
        rel = str(path.relative_to(MOD_ROOT.parent))
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            err(f"[loc] missing UTF-8 BOM (game will skip file): {rel}")
        text = raw.decode("utf-8-sig", errors="replace")
        lines = text.splitlines()
        # First non-empty, non-comment line must be the language header.
        header_ok = False
        has_body = False
        for line in lines:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            has_body = True
            header_ok = bool(re.match(r"^l_[a-z_]+:\s*$", s))
            break
        if not header_ok:
            if has_body:
                err(f"[loc] missing or malformed 'l_<lang>:' header: {rel}")
            else:
                warn(f"[loc] empty localisation file (only BOM, no header): {rel}")
        keys: dict[str, int] = {}
        for n, line in enumerate(lines, 1):
            m = _KEY_RE.match(line)
            if not m:
                continue
            key = m.group(1)
            if key in keys:
                warn(f"[loc] duplicate key '{key}' in {rel} (lines {keys[key]} & {n})")
            else:
                keys[key] = n


def main() -> int:
    if not MOD_ROOT.exists():
        print(f"mod root not found: {MOD_ROOT}", file=sys.stderr)
        return 2
    check_filenames()
    check_brace_balance()
    check_event_ids()
    check_localisation()

    if warnings:
        print(f"::group::Warnings ({len(warnings)})")
        for w in warnings:
            print(f"WARN  {w}")
        print("::endgroup::")
    if errors:
        print(f"\n{len(errors)} ERROR(s):")
        for e in errors:
            print(f"ERROR {e}")
        print(f"\nValidation FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"\nValidation PASSED: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
