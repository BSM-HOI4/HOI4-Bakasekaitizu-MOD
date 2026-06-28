#!/usr/bin/env python3
"""HOI4 definition locator - token-efficient search for mod definitions.

List mode   : prints "name<TAB>path:line" (one line per definition)
Def mode    : prints only the brace-balanced block of one definition
Check mode  : quick syntax sanity (brace balance, BOM, loc format)

Examples:
  search_defs.py --type scripted_effect --name bsm_ea          # locate
  search_defs.py --type decision --grep add_political_power    # by content
  search_defs.py --def bsm_ea_ai_update_policy                 # extract one block
  search_defs.py --check common/scripted_effects/foo.txt       # sanity check
"""

import argparse
import re
import sys
from pathlib import Path

# type -> (search dirs, definition depth, exclude subdirs)
# depth: brace depth at which definition names appear (None = special handler)
TYPES = {
    "event":             (["events"], None, []),
    "focus":             (["common/national_focus"], None, []),
    "decision":          (["common/decisions"], 1, ["categories"]),
    "decision_category": (["common/decisions/categories"], 0, []),
    "idea":              (["common/ideas"], 2, []),
    "scripted_effect":   (["common/scripted_effects"], 0, []),
    "scripted_trigger":  (["common/scripted_triggers"], 0, []),
    "dynamic_modifier":  (["common/dynamic_modifiers"], 0, []),
    "on_action":         (["common/on_actions"], 1, []),
    "opinion_modifier":  (["common/opinion_modifiers"], 1, []),
    "ai_strategy":       (["common/ai_strategy"], 0, []),
    "ai_strategy_plan":  (["common/ai_strategy_plans"], 0, []),
    "tech":              (["common/technologies"], 1, []),
    "character":         (["common/characters"], 1, []),
    "gfx":               (["interface", "gfx"], None, []),
    "loc":               (["localisation"], None, []),
}

EVENT_KINDS = {"country_event", "news_event", "state_event",
               "unit_leader_event", "operative_leader_event"}
KEY_RE = re.compile(r'([A-Za-z0-9_.@\-]+)\s*=\s*\{')
ID_RE = re.compile(r'\bid\s*=\s*([A-Za-z0-9_.]+)')
GFX_RE = re.compile(r'\bname\s*=\s*"?((?:GFX_|gfx_)[A-Za-z0-9_.\-]+)"?')
LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"')


def strip_comment(line):
    """Remove # comments (quote-aware)."""
    out, in_q = [], False
    for ch in line:
        if ch == '"':
            in_q = not in_q
        elif ch == '#' and not in_q:
            break
        out.append(ch)
    return ''.join(out)


def read_text(path):
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None


def iter_files(base, dirs, exclude):
    for d in dirs:
        root = base / d
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if p.suffix not in (".txt", ".gfx", ".yml"):
                continue
            if any(e in p.parts for e in exclude):
                continue
            yield p


def scan_paradox(text, depth_want, event_mode=False, focus_mode=False):
    """Yield (name, lineno, start_depth) for definitions in a paradox file."""
    depth = 0
    stack = []  # (key, open_depth)
    for ln, raw in enumerate(text.splitlines(), 1):
        line = strip_comment(raw)
        pos = 0
        for m in KEY_RE.finditer(line):
            d_here = depth + line.count('{', pos, m.start()) - line.count('}', pos, m.start())
            key = m.group(1)
            stack.append((key, d_here))
            if not event_mode and not focus_mode and d_here == depth_want:
                yield (key, ln, d_here)
        if (event_mode or focus_mode) and stack:
            mid = ID_RE.search(line)
            if mid:
                top = stack[-1][0]
                if event_mode and top in EVENT_KINDS and stack[-1][1] == 0:
                    yield (mid.group(1), ln, stack[-1][1])
                elif focus_mode and top in ("focus", "shared_focus", "joint_focus"):
                    yield (mid.group(1), ln, stack[-1][1])
        depth += line.count('{') - line.count('}')
        while stack and stack[-1][1] >= depth:
            stack.pop()


def extract_block(text, name, typ=None):
    """Return (start_line, block_lines) of `name = {...}` or event with id=name."""
    lines = text.splitlines()
    depth = 0
    start = None
    start_depth = 0
    block_re = re.compile(r'(?:^|[\s{])' + re.escape(name) + r'\s*=\s*\{')
    pend_event = None  # (line_idx, open_depth) of event block awaiting id
    for i, raw in enumerate(lines):
        line = strip_comment(raw)
        if start is None:
            m = block_re.search(line)
            if m:
                start = i
                start_depth = depth + line.count('{', 0, m.start()) - line.count('}', 0, m.start())
            else:
                km = KEY_RE.search(line)
                if km and km.group(1) in EVENT_KINDS:
                    d_open = depth + line.count('{', 0, km.start()) - line.count('}', 0, km.start())
                    # definitions are top-level only; nested = fire-effect call site
                    pend_event = (i, d_open) if d_open == 0 else None
                elif pend_event is not None:
                    mid = ID_RE.search(line)
                    if mid:
                        if mid.group(1) == name:
                            start, start_depth = pend_event
                        else:
                            pend_event = None
        depth += line.count('{') - line.count('}')
        if start is not None and depth <= start_depth:
            return start + 1, lines[start:i + 1]
        if pend_event is not None and depth <= pend_event[1]:
            pend_event = None
    return None, None


def cmd_list(base, typ, name_pat, grep_pat, limit):
    dirs, depth_want, exclude = TYPES[typ]
    name_re = re.compile(name_pat, re.I) if name_pat else None
    grep_re = re.compile(grep_pat, re.I) if grep_pat else None
    results, total = [], 0
    for path in iter_files(base, dirs, exclude):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(base)
        if typ == "gfx":
            found = [(m.group(1), ln) for ln, l in enumerate(text.splitlines(), 1)
                     for m in [GFX_RE.search(l)] if m]
        elif typ == "loc":
            if path.suffix != ".yml":
                continue
            found = [(m.group(1), ln) for ln, l in enumerate(text.splitlines(), 1)
                     for m in [LOC_RE.match(l)] if m]
        else:
            found = [(n, ln) for n, ln, _ in scan_paradox(
                text, depth_want,
                event_mode=(typ == "event"), focus_mode=(typ == "focus"))]
        for n, ln in found:
            if name_re and not name_re.search(n):
                continue
            if grep_re:
                _, block = extract_block(text, n)
                if not block or not any(grep_re.search(b) for b in block):
                    continue
            total += 1
            if len(results) < limit:
                results.append(f"{n}\t{rel}:{ln}")
    print("\n".join(results))
    print(f"## {total} match(es), showing {len(results)} (type={typ})")


def cmd_def(base, name, typ, max_lines):
    if typ:
        dirs, _, exclude = TYPES[typ]
    else:
        dirs, exclude = ["common", "events"], []
    for path in iter_files(base, dirs, exclude):
        if path.suffix == ".yml":
            continue
        text = read_text(path)
        if text is None or name not in text:
            continue
        ln, block = extract_block(text, name)
        if block:
            rel = path.relative_to(base)
            print(f"# {rel}:{ln}-{ln + len(block) - 1}")
            if len(block) > max_lines:
                print("\n".join(block[:max_lines]))
                print(f"# ... truncated ({len(block)} lines total, use --max-lines)")
            else:
                print("\n".join(block))
            return
    print(f"## not found: {name}", file=sys.stderr)
    sys.exit(1)


def cmd_check(paths):
    bad = 0
    for p in map(Path, paths):
        issues = []
        try:
            raw = p.read_bytes()
        except OSError as e:
            print(f"NG {p}: {e}")
            bad += 1
            continue
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        if p.suffix == ".yml" and not has_bom:
            issues.append("missing UTF-8 BOM (required for localisation)")
        text = raw.decode("utf-8-sig", errors="replace")
        if p.suffix == ".yml":
            for ln, l in enumerate(text.splitlines(), 1):
                s = l.strip()
                if not s or s.startswith("#") or re.match(r'^l_\w+:', s):
                    continue
                if not LOC_RE.match(l):
                    issues.append(f"line {ln}: malformed loc entry")
        else:
            depth = 0
            for ln, l in enumerate(text.splitlines(), 1):
                line = strip_comment(l)
                if line.count('"') % 2 == 1:
                    issues.append(f"line {ln}: unbalanced quotes")
                depth += line.count('{') - line.count('}')
                if depth < 0:
                    issues.append(f"line {ln}: unexpected '}}'")
                    depth = 0
            if depth != 0:
                issues.append(f"EOF: {depth} unclosed brace(s)")
        if issues:
            bad += 1
            print(f"NG {p}")
            for i in issues[:10]:
                print(f"   - {i}")
            if len(issues) > 10:
                print(f"   - ... {len(issues) - 10} more")
        else:
            print(f"OK {p}")
    sys.exit(1 if bad else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=".", help="mod root (auto-descends into bakasekai/)")
    ap.add_argument("--type", choices=sorted(TYPES), help="definition type")
    ap.add_argument("--name", help="filter by name (regex, case-insensitive)")
    ap.add_argument("--grep", help="filter by block content (regex; slower)")
    ap.add_argument("--def", dest="defname", help="print one definition block")
    ap.add_argument("--check", nargs="+", help="syntax-sanity check file(s)")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--max-lines", type=int, default=200)
    ap.add_argument("--list-types", action="store_true")
    args = ap.parse_args()

    if args.list_types:
        print(" ".join(sorted(TYPES)))
        return
    if args.check:
        cmd_check(args.check)
        return

    base = Path(args.base).resolve()
    if (base / "bakasekai").is_dir():
        base = base / "bakasekai"

    if args.defname:
        cmd_def(base, args.defname, args.type, args.max_lines)
    elif args.type:
        cmd_list(base, args.type, args.name, args.grep, args.limit)
    else:
        ap.error("need --type, --def, --check or --list-types")


if __name__ == "__main__":
    main()
