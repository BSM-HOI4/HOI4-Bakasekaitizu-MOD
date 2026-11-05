#!/usr/bin/env python3
"""Static contracts for the BSM British tree; not a HOI4 runtime test."""
from pathlib import Path
import re
from verify_london_scenario import parse, walk, values

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "bakasekai"


def load(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


tree = next(e.value for e in load("common/national_focus/uk.txt") if e.key == "focus_tree")
focuses = [e.value for e in tree if e.key == "focus"]
by_id = {values(f, "id")[0]: f for f in focuses}
assert len(focuses) == len(by_id) == 41
assert len({(values(f, "x")[0], values(f, "y")[0]) for f in focuses}) == 41
edges = {}
for name, focus in by_id.items():
    dependencies = []
    for entry in focus:
        if entry.key in ("prerequisite", "mutually_exclusive"):
            for other in values(entry.value, "focus"):
                assert other in by_id, (name, other)
                if entry.key == "prerequisite":
                    dependencies.append(other)
                else:
                    reverse = [e.value for e in by_id[other] if e.key == "mutually_exclusive"]
                    assert any(name in values(e, "focus") for e in reverse), (name, other)
    edges[name] = dependencies


def visit(node, stack):
    assert node not in stack, (node, stack)
    for parent in edges[node]:
        visit(parent, stack | {node})


for node in edges:
    visit(node, set())
events = [e.value for e in load("events/GBR_bsm_events.txt") if e.key == "country_event"]
event_ids = [values(e, "id")[0] for e in events]
assert len(events) == len(set(event_ids)) == 10
for event in events:
    assert values(event, "timeout_days") == ["14"]
    options = [e.value for e in event if e.key == "option"]
    assert len(options) == 2
    # Declining never changes sovereignty, state ownership or the diplomatic outcome.
    assert all(e.key in ("name", "ai_chance") for e in options[1])
    assert any(e.key == "if" for e in options[0]), "Recheck agreement conditions at execution"

all_entries = list(walk(load("events/GBR_bsm_events.txt")))
transfers = [e.value for e in all_entries if e.key == "transfer_state"]
assert transfers == ["835"], transfers
dover = next(e for e in events if values(e, "id") == ["GBR_bsm.10"])
assert any(e.key == "owns_state" and e.value == "835" for e in walk(dover))
assert any(e.key == "controls_state" and e.value == "835" for e in walk(dover))
assert not any(e.key in ("annex_country", "release", "declare_war_on", "puppet", "set_autonomy") for e in all_entries)
known_london = {values(e.value, "id")[0] for e in load("events/LON_scenario_events.txt") if e.key == "country_event"}
for entry in all_entries:
    if entry.key == "country_event":
        for call in values(entry.value, "id"):
            assert call in known_london or call in event_ids, call
loc_path = MOD / "localisation/japanese/GBR_bsm_l_japanese.yml"
assert loc_path.read_bytes().startswith(b"\xef\xbb\xbf")
keys = re.findall(r"^ ([^:]+):", loc_path.read_text(encoding="utf-8-sig"), re.M)
assert len(keys) == len(set(keys))
for name in by_id:
    assert name in keys and name + "_desc" in keys
for event_id in event_ids:
    assert all(event_id + suffix in keys for suffix in (".t", ".d", ".a", ".b"))
print("PASS 41 unique focuses, graph/positions, symmetric political choices")
print("PASS 10 consent events, refusal inert, execution guards, restricted territorial transfer")
print("PASS London event calls and Japanese BOM/labels")
print("SKIP HOI4 execution, AI, NF UI and save migration (static verification only)")
