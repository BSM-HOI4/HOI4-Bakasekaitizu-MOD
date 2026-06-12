#!/usr/bin/env python3
"""HOI4 map integrity checker (BSM mod).

Checks the invariants whose violation causes DELAYED crashes
(works on 1st launch, SIGSEGV on 2nd launch via naval_dist.cache):
  1. strategic region id duplicates
  2. province assigned to >1 strategic region
  3. definition.csv: duplicate province ids / duplicate RGB colors
  4. province assigned to >1 state
  5. state/strategic-region provinces missing from definition.csv

Usage: python3 check_map.py [--base /path/to/repo_or_mod_root]
Exit code 0 = all OK, 1 = violations found.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

PROV_BLOCK_RE = re.compile(r'provinces\s*=\s*\{([^}]*)\}')
ID_RE = re.compile(r'\bid\s*=\s*(\d+)')


def strip_comments(text):
    return re.sub(r'#[^\n]*', '', text)


def read(path):
    return path.read_text(encoding='utf-8-sig', errors='replace')


def collect_provinces(text):
    out = []
    for m in PROV_BLOCK_RE.finditer(text):
        out.extend(int(n) for n in re.findall(r'\d+', m.group(1)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base', default='.', help='repo or mod root')
    ap.add_argument('--details', type=int, default=10,
                    help='max detail lines per violation type')
    args = ap.parse_args()

    base = Path(args.base).resolve()
    if (base / 'bakasekai').is_dir():
        base = base / 'bakasekai'
    bad = 0
    D = args.details

    def report(label, problems):
        nonlocal bad
        if problems:
            bad += 1
            print(f'NG {label}: {len(problems)}')
            for p in problems[:D]:
                print(f'   - {p}')
            if len(problems) > D:
                print(f'   - ... {len(problems) - D} more')
        else:
            print(f'OK {label}')

    # --- definition.csv ---
    defids = set()
    dup_ids, dup_rgb = [], []
    rgb_seen = {}
    def_csv = base / 'map' / 'definition.csv'
    if def_csv.exists():
        for ln, line in enumerate(read(def_csv).splitlines(), 1):
            parts = line.split(';')
            if len(parts) < 4 or not parts[0].strip().isdigit():
                continue
            pid = int(parts[0])
            if pid in defids:
                dup_ids.append(f'province {pid} (line {ln})')
            defids.add(pid)
            rgb = tuple(parts[1:4])
            if pid != 0:
                if rgb in rgb_seen:
                    dup_rgb.append(f'RGB {";".join(rgb)}: province {rgb_seen[rgb]} and {pid}')
                else:
                    rgb_seen[rgb] = pid
        report('definition.csv duplicate ids', dup_ids)
        report('definition.csv duplicate colors', dup_rgb)
    else:
        print(f'?? definition.csv not found under {base}/map')

    # --- strategic regions ---
    sr_dir = base / 'map' / 'strategicregions'
    region_ids = defaultdict(list)   # id -> [files]
    prov_region = defaultdict(list)  # province -> [region files]
    missing_sr = []
    for f in sorted(sr_dir.glob('*.txt')):
        text = strip_comments(read(f))
        m = ID_RE.search(text)
        if m:
            region_ids[int(m.group(1))].append(f.name)
        for p in collect_provinces(text):
            prov_region[p].append(f.name)
            if defids and p not in defids:
                missing_sr.append(f'province {p} in {f.name}')
    report('strategic region id duplicates',
           [f'id {i}: {" / ".join(fs)}' for i, fs in sorted(region_ids.items()) if len(fs) > 1])
    report('province in multiple strategic regions',
           [f'province {p}: {" / ".join(sorted(set(fs)))}'
            for p, fs in sorted(prov_region.items()) if len(set(fs)) > 1 or len(fs) > 1])
    report('strategic region provinces missing from definition.csv', missing_sr)

    # --- states ---
    st_dir = base / 'history' / 'states'
    prov_state = defaultdict(list)
    missing_st = []
    for f in sorted(st_dir.glob('*.txt')):
        text = strip_comments(read(f))
        for p in collect_provinces(text):
            prov_state[p].append(f.name)
            if defids and p not in defids:
                missing_st.append(f'province {p} in {f.name}')
    report('province in multiple states',
           [f'province {p}: {" / ".join(sorted(set(fs)))}'
            for p, fs in sorted(prov_state.items()) if len(fs) > 1])
    report('state provinces missing from definition.csv', missing_st)

    print(f'## {"NG: fix before launching" if bad else "all map invariants OK"}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
