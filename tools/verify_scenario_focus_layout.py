#!/usr/bin/env python3
"""Validate the FRA/ESP/NSI scenario layouts, including imported shared focuses.

Run from the repository root: python3 tools/verify_scenario_focus_layout.py
"""
from pathlib import Path
import re
import json

def blocks(text, key='focus'):
    for m in re.finditer(r'(?m)^\s*'+key+r'\s*=\s*\{',text):
        start=m.start(); opening=text.index('{',m.start()); depth=0
        for t in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text[opening:]):
            if t[0]=='{': depth+=1
            elif t[0]=='}':
                depth-=1
                if depth==0:
                    end=opening+t.end(); yield start,end,text[start:end]; break

def get(b,k,default=None):
    m=re.search(r'(?m)^\s*'+k+r'\s*=\s*([^\s#{}]+)',b)
    return m[1] if m else default

def load(path):
    txt=Path(path).read_text(encoding='utf-8-sig'); fs={}
    for s,e,b in blocks(txt):
        fid=get(b,'id'); fs[fid]={'s':s,'e':e,'b':b,'rel':get(b,'relative_position_id'),'x':int(get(b,'x',0)),'y':int(get(b,'y',0)),'pre':re.findall(r'prerequisite\s*=\s*\{\s*focus\s*=\s*(\w+)',b)}
    return txt,fs

def resolve(fs,fid,seen=()):
    f=fs[fid]; x,y=f['x'],f['y']
    if f['rel']:
        assert fid not in seen
        px,py=resolve(fs,f['rel'],seen+(fid,));x+=px;y+=py
    return x,y

LAYOUT = json.loads((Path(__file__).parent / "scenario_focus_layout.json").read_text())
GEOMETRY = LAYOUT["geometry"]


def boxes_too_close(a, b):
    dx = abs(a[0] - b[0]) * GEOMETRY["x_step"]
    dy = abs(a[1] - b[1]) * GEOMETRY["y_step"]
    return (dx < GEOMETRY["node_width"] + GEOMETRY["horizontal_gap"]
            and dy < GEOMETRY["node_height"] + GEOMETRY["vertical_gap"])


def verify():
    base = Path(__file__).resolve().parents[1] / "bakasekai/common/national_focus"
    loc_keys = {}
    for path in (base.parents[1] / "localisation/japanese").rglob("*.yml"):
        for key in re.findall(r'^\s*([^\s:#]+):\d*\s+"', path.read_text(encoding="utf-8-sig"), re.M):
            loc_keys[key] = loc_keys.get(key, 0) + 1
    shared = {}
    for path in base.glob("*.txt"):
        for _, _, block in blocks(path.read_text(encoding="utf-8-sig"), "shared_focus"):
            fid = get(block, "id")
            shared[fid] = {
                "rel": get(block, "relative_position_id"),
                "x": int(get(block, "x", 0)),
                "y": int(get(block, "y", 0)),
                "pre": [ref for _, _, part in blocks(block, "prerequisite")
                        for ref in re.findall(r"\bfocus\s*=\s*(\w+)", part)],
            }
    for name in ("france", "spain", "nsi"):
        text, focuses = load(base / (name + ".txt"))
        assert len(focuses) == len(list(blocks(text))), f"{name}: duplicate focus ID"
        for focus in focuses.values():
            focus["pre"] = [ref for _, _, part in blocks(focus["b"], "prerequisite")
                            for ref in re.findall(r"\bfocus\s*=\s*(\w+)", part)]
        imported = set(re.findall(r"(?m)^\s*shared_focus\s*=\s*(\w+)", text))
        assert imported <= shared.keys(), f"{name}: missing shared focus"
        # Shared root imports include their prerequisite-dependent descendants.
        while True:
            extra = {fid for fid, focus in shared.items()
                     if any(ref in imported for ref in focus["pre"])}
            if extra <= imported:
                break
            imported |= extra
        combined = {fid: shared[fid] for fid in imported} | focuses
        def group(fid):
            x, _ = resolve(combined, fid)
            industry, military = LAYOUT["countries"][name]["category_bounds"]
            return "political" if x < industry else "industry" if x < military else "military"

        roots = {"political": [], "industry": [], "military": []}
        for fid, focus in focuses.items():
            assert all(group(ref) == group(fid) for ref in focus["pre"]), (
                f"{fid}: prerequisite crosses independent groups")
            if focus["rel"]:
                assert group(focus["rel"]) == group(fid), f"{fid}: relative anchor crosses groups"
            if not focus["pre"] and resolve(combined, fid)[1] == 0:
                roots[group(fid)].append(fid)
            for ref in re.findall(r"\bhas_completed_focus\s*=\s*(\w+)", focus["b"]):
                assert ref in combined, f"{fid}: missing eligibility reference {ref}"
            loc_key = get(focus["b"], "text", fid)
            assert loc_keys.get(loc_key) == 1, f"{fid}: missing/duplicate Japanese name"
            assert loc_keys.get(loc_key + "_desc") == 1, f"{fid}: missing/duplicate Japanese description"
            references = focus["pre"] + re.findall(
                r"mutually_exclusive\s*=\s*\{\s*focus\s*=\s*(\w+)", focus["b"])
            assert all(ref in combined for ref in references), f"{fid}: missing reference"
            if focus["rel"]:
                assert focus["rel"] in combined, f"{fid}: missing relative anchor"
            x, y = resolve(combined, fid)
            assert all(y > resolve(combined, ref)[1] for ref in focus["pre"]), (
                f"{fid}: prerequisite is not above its child")
            assert all(y - resolve(combined, ref)[1] == 1 for ref in focus["pre"]), (
                f"{fid}: excessive vertical distance from prerequisite")
            for other in combined:
                if fid == other:
                    continue
                ox, oy = resolve(combined, other)
                assert not boxes_too_close((x, y), (ox, oy)), f"{fid}: rendered box overlaps/too close to {other}"
        columns = sorted({resolve(combined, fid)[0] for fid in combined})
        assert all(right - left <= 8 for left, right in zip(columns, columns[1:])), (
            f"{name}: excessive empty horizontal band")
        for category in roots:
            rows = sorted({resolve(combined, fid)[1] for fid in focuses if group(fid) == category})
            assert all(bottom - top <= 3 for top, bottom in zip(rows, rows[1:])), (
                f"{name}: excessive vertical gap in {category}")
        assert all(roots.values()), f"{name}: each group needs an independent top-level root"
        print(f"PASS {name}: {len(focuses)} focuses, {len(imported)} shared; "
              "IDs, references, rendered boxes, short prerequisite links, independent groups, Japanese text")


if __name__ == "__main__":
    verify()
