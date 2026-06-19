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


_TAG_REF_RE = re.compile(r'^\s*([A-Z0-9]{3})\s*=\s*"([^"]+)"')


def check_country_tag_files() -> None:
    """Every tag in country_tags must point to an existing country file.

    A tag whose file is missing makes the country fail to load. CWTools also
    covers this, but it is cheap and unambiguous, so we keep it as a fast gate.
    Paths in country_tags are relative to `common/`.
    """
    base = MOD_ROOT / "common" / "country_tags"
    if not base.exists():
        return
    common = MOD_ROOT / "common"
    dynamic_re = re.compile(r"^\s*dynamic_tags\s*=\s*yes")
    for path in base.glob("*.txt"):
        rel = str(path.relative_to(MOD_ROOT.parent))
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        # Dynamic-tag files reference runtime-generated placeholder countries
        # (civil wars etc.) whose files need not exist on disk.
        if any(dynamic_re.match(ln) for ln in lines):
            continue
        for n, line in enumerate(lines, 1):
            if line.lstrip().startswith("#"):
                continue
            m = _TAG_REF_RE.match(line)
            if not m:
                continue
            tag, ref = m.group(1), m.group(2)
            if tag == "dynamic_tags":  # `dynamic_tags = yes`, not a path
                continue
            if not (common / ref).is_file():
                err(f"[country-tag] {tag} -> missing file 'common/{ref}' ({rel}:{n})")


_FOCUS_OPEN_RE = re.compile(r"^\s*(?:shared_)?focus\s*=\s*\{")
_PLAIN_ID_RE = re.compile(r"^\s*id\s*=\s*([A-Za-z0-9_.\-]+)")


def check_duplicate_focus_ids() -> None:
    """Focus ids must be globally unique; duplicates make the engine pick one
    and silently drop the other. We capture the first `id =` inside each
    `focus = {` / `shared_focus = {` block (the focus_tree's own id and any
    `relative_position_id` / `prerequisite { focus = X }` are not matched)."""
    base = MOD_ROOT / "common" / "national_focus"
    if not base.exists():
        return
    seen: dict[str, str] = {}
    for path in base.rglob("*.txt"):
        rel = str(path.relative_to(MOD_ROOT.parent))
        depth = 0
        focus_depth = None  # brace depth at which the current focus block opened
        captured = False
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            clean = strip_noise(line)
            if focus_depth is None and _FOCUS_OPEN_RE.match(clean):
                focus_depth = depth
                captured = False
            elif focus_depth is not None and not captured:
                m = _PLAIN_ID_RE.match(clean)
                if m:
                    fid = m.group(1)
                    captured = True
                    if fid in seen:
                        err(f"[focus-id] duplicate focus id '{fid}' in {rel} (first in {seen[fid]})")
                    else:
                        seen[fid] = rel
            depth += clean.count("{") - clean.count("}")
            if focus_depth is not None and depth <= focus_depth:
                focus_depth = None


_DEF_NAME_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*\{")


def check_duplicate_definitions(subdir: str, label: str) -> None:
    """Flag top-level definitions (depth 0 `name = {`) declared more than once
    within a directory. Applies to scripted_effects / scripted_triggers, where
    a redefinition silently overrides the earlier one."""
    base = MOD_ROOT / "common" / subdir
    if not base.exists():
        return
    seen: dict[str, str] = {}
    for path in sorted(base.rglob("*.txt")):
        rel = str(path.relative_to(MOD_ROOT.parent))
        depth = 0
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            clean = strip_noise(line)
            if depth == 0:
                m = _DEF_NAME_RE.match(clean)
                if m:
                    name = m.group(1)
                    if name in seen:
                        warn(f"[{label}] duplicate definition '{name}' in {rel} (first in {seen[name]})")
                    else:
                        seen[name] = rel
            depth += clean.count("{") - clean.count("}")


def main() -> int:
    if not MOD_ROOT.exists():
        print(f"mod root not found: {MOD_ROOT}", file=sys.stderr)
        return 2
    check_filenames()
    check_brace_balance()
    check_event_ids()
    check_localisation()
    check_country_tag_files()
    check_duplicate_focus_ids()
    check_duplicate_definitions("scripted_effects", "scripted-effect")
    check_duplicate_definitions("scripted_triggers", "scripted-trigger")

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
