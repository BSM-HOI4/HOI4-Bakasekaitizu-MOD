#!/usr/bin/env python3
"""Static contracts for the LON/GBR/IRE scenario; does not run HOI4.

Run from any directory: python3 tools/verify_london_scenario.py
The small parser retains nested scopes and duplicate keys, unlike a dict or
brace-only regex. Checks inspect the authored scripts, not a copy of the story.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "bakasekai"
TOKEN = re.compile(r'\s+|#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[<>=!]+|[^\s{}<>=!"#]+')
LOC = re.compile(r'^\s*([^\s:#]+):\d*\s+"', re.M)


@dataclass
class Entry:
    key: str
    op: str = ""
    value: str | list["Entry"] = ""


def parse(text: str) -> list[Entry]:
    tokens = []
    cursor = 0
    for match in TOKEN.finditer(text):
        if match.start() != cursor:
            raise ValueError(f"unrecognized input at {cursor}")
        cursor = match.end()
        token = match[0]
        if not token.isspace() and not token.startswith("#"):
            tokens.append(token)
    if cursor != len(text):
        raise ValueError(f"unrecognized trailing input at {cursor}")
    index = 0

    def block(nested=False):
        nonlocal index
        result = []
        while index < len(tokens):
            key = tokens[index]
            index += 1
            if key == "}":
                if not nested:
                    raise ValueError("unmatched closing brace")
                return result
            if key == "{" or key in ("=", "<", ">", "<=", ">=", "!="):
                raise ValueError(f"expected key, got {key}")
            if index == len(tokens) or tokens[index] not in ("=", "<", ">", "<=", ">=", "!="):
                result.append(Entry(key))  # Bare values in arrays.
                continue
            op = tokens[index]
            index += 1
            if index == len(tokens):
                raise ValueError(f"missing value for {key}")
            value = tokens[index]
            index += 1
            if value == "{":
                value = block(True)
            elif value in ("}", "=", "<", ">", "<=", ">=", "!="):
                raise ValueError(f"invalid value for {key}: {value}")
            result.append(Entry(key, op, value))
        if nested:
            raise ValueError("unclosed brace")
        return result

    return block()


def walk(entries):
    for entry in entries:
        yield entry
        if isinstance(entry.value, list):
            yield from walk(entry.value)


def values(entries, key):
    return [entry.value for entry in entries if entry.key == key]


def positive_conditions(entries, negated=False):
    for entry in entries:
        if isinstance(entry.value, list):
            yield from positive_conditions(entry.value, not negated if entry.key == "NOT" else negated)
        elif not negated:
            yield entry


def scalar(entries, key, default=None):
    found = values(entries, key)
    return found[0] if found else default


def bare(value):
    return value.strip('"') if isinstance(value, str) else value


def scenario_key(key):
    return key.startswith("LON_ts_") or bool(re.fullmatch(r"LON\.(?:[3-9]\d|\d{3,})\..+", key))


class TerritorialModel:
    """Limited effect interpreter for ownership safety, never engine evidence.

    Unknown conditions/effects raise instead of silently passing. Political and
    economic effects are recorded without attempting to emulate their game math.
    """

    def __init__(self, effects):
        self.effects = effects
        self.owner = {}
        self.controller = {}
        self.cores = defaultdict(set)
        self.provinces = {}
        self.flags = defaultdict(set)
        self.capital = {}
        self.subjects = {"LON": "GBR"}
        self.wars = set()
        self.loads = Counter()
        self.queue = []
        self.recorded = []
        for state_id in (113, 119, 126, 131, 134, 135):
            paths = list((MOD / "history/states").glob(f"{state_id}-*.txt"))
            if len(paths) != 1:
                raise ValueError(f"cannot locate initial state {state_id}")
            state = values(parse(paths[0].read_text(encoding="utf-8-sig")), "state")[0]
            history = values(state, "history")[0]
            self.owner[state_id] = scalar(history, "owner")
            self.controller[state_id] = self.owner[state_id]
            self.cores[state_id].update(values(history, "add_core_of"))
            for province in values(state, "provinces")[0]:
                self.provinces[int(province.key)] = state_id

    def test(self, entries, scope):
        def one(node):
            key, value = node.key, node.value
            if key in ("AND", "limit"):
                return self.test(value, scope)
            if key == "OR":
                return any(one(child) for child in value)
            if key == "NOT":
                return not self.test(value, scope)
            if re.fullmatch(r"[A-Z]{3}", key) and isinstance(value, list):
                return self.test(value, key)
            if key == "tag":
                return scope == value
            if key == "country_exists":
                return value in self.owner.values()
            if key in ("owns_state", "controls_state"):
                return (self.owner if key == "owns_state" else self.controller).get(int(value)) == scope
            if key == "has_country_flag":
                return value in self.flags[scope]
            if key == "has_war":
                return any(scope in pair for pair in self.wars) == (value == "yes")
            if key == "has_war_with":
                return frozenset((scope, value)) in self.wars
            if key == "is_subject_of":
                return self.subjects.get(scope) == value
            if key == "is_subject":
                return (scope in self.subjects) == (value == "yes")
            if key == "always":
                return value == "yes"
            raise ValueError(f"territorial model unsupported condition: {key}")
        return all(one(node) for node in entries)

    def execute(self, entries, scope):
        branch_taken = False
        for node in entries:
            key, value = node.key, node.value
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch_taken = False
                condition = values(value, "limit")
                if not branch_taken and (key == "else" or not condition or self.test(condition[0], scope)):
                    self.execute([entry for entry in value if entry.key != "limit"], scope)
                    branch_taken = True
                continue
            if key in ("name", "ai_chance", "trigger", "limit"):
                continue
            if isinstance(value, list) and (re.fullmatch(r"[A-Z]{3}", key) or key.isdigit()):
                self.execute(value, int(key) if key.isdigit() else key)
            elif key in self.effects and value == "yes":
                self.execute(self.effects[key], scope)
            elif key == "add_core_of":
                self.cores[scope].add(value)
            elif key == "remove_core_of":
                self.cores[scope].discard(value)
            elif key == "release":
                for state_id in self.owner:
                    if self.owner[state_id] == scope and value in self.cores[state_id]:
                        self.owner[state_id] = value
                        self.controller[state_id] = value
            elif key == "transfer_state":
                self.owner[int(value)] = scope
                self.controller[int(value)] = scope
            elif key == "set_capital":
                if not isinstance(value, list) or scalar(value, "state") is None:
                    raise ValueError("set_capital requires { state = ... }")
                state_id = int(scalar(value, "state"))
                if self.owner[state_id] != scope:
                    raise ValueError(f"capital {state_id} is not owned by {scope}")
                self.capital[scope] = state_id
            elif key == "set_country_flag":
                self.flags[scope].add(scalar(value, "flag") if isinstance(value, list) else value)
            elif key == "clr_country_flag":
                self.flags[scope].discard(value)
            elif key == "load_oob":
                name = bare(value)
                path = MOD / "history/units" / f"{name}.txt"
                if not path.is_file():
                    raise ValueError(f"missing OOB {name}")
                oob = parse(path.read_text(encoding="utf-8-sig"))
                for units in values(oob, "units"):
                    for division in values(units, "division"):
                        location = int(scalar(division, "location"))
                        state_id = self.provinces.get(location)
                        if state_id is None or self.owner[state_id] != scope:
                            raise ValueError(f"{name}: division spawns in unowned province {location}")
                self.loads[(scope, name)] += 1
            elif key in ("country_event", "news_event"):
                self.queue.append((scope, scalar(value, "id")))
            elif key == "set_autonomy":
                target = scalar(value, "target")
                if scalar(value, "autonomous_state") == "autonomy_free":
                    self.subjects.pop(target, None)
                else:
                    self.subjects[target] = scope
            elif key == "white_peace":
                target = scalar(value, "tag") if isinstance(value, list) else value
                self.wars.discard(frozenset((scope, target)))
            elif key == "declare_war_on":
                self.wars.add(frozenset((scope, scalar(value, "target"))))
            elif key in ("add_ideas", "remove_ideas", "add_timed_idea", "add_political_power",
                         "add_stability", "set_stability", "set_war_support", "add_war_support",
                         "set_politics", "set_popularities", "set_variable", "add_opinion_modifier",
                         "custom_effect_tooltip"):
                self.recorded.append((scope, key))
            else:
                raise ValueError(f"territorial model unsupported effect: {key}")


def check_territorial_effects(effect_bodies, events, require):
    """Execute real authored effects against initial and adversarial ownership."""
    effect = effect_bodies.get("LON_ts_establish_ireland")
    require(effect is not None, "missing Ireland establishment effect")
    if effect is None:
        return 0
    count = 0
    world = TerritorialModel(effect_bodies)
    world.execute(effect, "LON")
    require({s for s, owner in world.owner.items() if owner == "IRE"} == {134, 135},
            "Ireland release must grant exactly Connaught and Munster")
    require(world.owner[113] == world.owner[119] == "LON", "Ireland release removed London's remaining territory")
    require("IRE" in world.cores[113] and world.capital.get("IRE") == 135,
            "Ireland missing Leinster core or Munster capital")
    before = (dict(world.owner), dict(world.loads), len(world.recorded))
    world.execute(effect, "LON")
    require(before == (dict(world.owner), dict(world.loads), len(world.recorded)),
            "Ireland release can repeat its rewards or OOB")
    count += 2
    for name in ("foreign_owner", "foreign_controller", "wartime", "existing_ireland"):
        world = TerritorialModel(effect_bodies)
        if name == "foreign_owner":
            world.owner[135] = world.controller[135] = "FRA"
        elif name == "foreign_controller":
            world.controller[135] = "FRA"
        elif name == "wartime":
            world.wars.add(frozenset(("LON", "FRA")))
        else:
            world.owner[134] = world.controller[134] = "IRE"
        before = (dict(world.owner), dict(world.controller), dict(world.loads))
        world.execute(effect, "LON")
        require(before == (dict(world.owner), dict(world.controller), dict(world.loads)),
                f"Ireland release mutated ownership/OOB during {name}")
        count += 1
    # Britain can consent to relocation only while it still owns and controls 126.
    if "LON.44" in events:
        option = values(events["LON.44"], "option")[0]
        conditions = values(option, "trigger")
        for foreign in (False, True):
            world = TerritorialModel(effect_bodies)
            world.execute(effect, "LON")
            world.flags["LON"].add("LON_ts_republic")
            if foreign:
                world.owner[126] = world.controller[126] = "FRA"
            allowed = bool(conditions) and world.test(conditions[0], "GBR")
            require(allowed != foreign, "relocation consent fails to check current owner/controller")
            if allowed:
                world.execute(option, "GBR")
                require(world.owner[126] == "LON" and world.capital.get("LON") == 126,
                        "accepted relocation failed to move London first")
                require(world.owner[113] == "IRE" and world.capital.get("IRE") == 113,
                        "accepted relocation failed to give Leinster to Ireland")
            count += 1
    return count


def check_diplomatic_paths(effect_bodies, events, require):
    def option(world, event_id, scope, choice=0):
        event = events[event_id]
        guards = values(event, "trigger")
        if guards and not world.test(guards[0], scope):
            raise ValueError(f"{event_id}: event trigger prevents expected path")
        selected = values(event, "option")[choice]
        guards = values(selected, "trigger")
        if guards and not world.test(guards[0], scope):
            raise ValueError(f"{event_id}: option trigger prevents expected path")
        for immediate in values(event, "immediate"):
            world.execute(immediate, scope)
        world.execute(selected, scope)

    def available(world, event_id, scope, choice=0):
        event = events[event_id]
        checks = values(event, "trigger") + values(values(event, "option")[choice], "trigger")
        return all(world.test(guard, scope) for guard in checks)

    def opening():
        world = TerritorialModel(effect_bodies)
        world.flags["LON"].update(("LON_ts_assembly_completed", "LON_ts_bridge_settled"))
        return world

    count = 0
    outcomes = {"LON_ts_accord", "LON_ts_republic", "LON_ts_city", "LON_ts_hardline"}
    for choice, expected in enumerate(("LON_ts_accord", "LON_ts_republic", "LON_ts_city", "LON_ts_hardline")):
        world = opening()
        option(world, "LON.36", "LON", choice)
        if choice < 3:
            require(not (world.flags["LON"] & outcomes), "conference route settled before foreign consent")
            require(not available(world, "LON.39", "LON"), "conference ratifiable before IRE/GBR consent")
            option(world, "LON.37", "IRE")
            require(not available(world, "LON.39", "LON"), "conference ratifiable before GBR consent")
            option(world, "LON.38", "GBR")
            option(world, "LON.39", "LON")
        require(world.flags["LON"] & outcomes == {expected}, f"conference choice {choice} sets multiple/wrong endings")
        require("LON_ts_conference_pending" not in world.flags["LON"], f"conference choice {choice} leaves pending flag")
        count += 1
    # A counteroffer must ask IRE again rather than silently turn a refusal into a treaty.
    world = opening()
    option(world, "LON.36", "LON")
    option(world, "LON.37", "IRE", 1)
    option(world, "LON.40", "LON")
    require(not (world.flags["LON"] & outcomes) and ("IRE", "LON.37") in world.queue,
            "counteroffer imposes an ending instead of asking Ireland again")
    count += 1

    def northern_opening():
        world = TerritorialModel(effect_bodies)
        world.execute(effect_bodies["LON_ts_establish_ireland"], "LON")
        world.flags["GBR"].add("LON_ts_north_pending")
        option(world, "LON.53", "GBR")
        return world

    world = northern_opening()
    option(world, "LON.54", "LON")
    option(world, "LON.55", "IRE")
    require(world.owner[119] == "IRE" and "IRE" in world.cores[119], "northern agreement failed to transfer/core 119")
    require("LON_ts_north_pending" not in world.flags["GBR"], "northern agreement leaves pending flag")
    require(all("LON_ts_north_transfer_consent" not in world.flags[tag] for tag in ("LON", "GBR")),
            "northern agreement leaves reusable transfer consent")
    count += 1
    world = TerritorialModel(effect_bodies)
    world.execute(effect_bodies["LON_ts_establish_ireland"], "LON")
    world.owner[119] = world.controller[119] = "GBR"
    world.flags["GBR"].add("LON_ts_north_pending")
    world.flags["LON"].add("LON_ts_north_transfer_consent")
    option(world, "LON.53", "GBR")
    require("LON_ts_north_transfer_consent" not in world.flags["LON"], "new northern request retains stale London consent")
    option(world, "LON.55", "IRE")
    require(world.owner[119] == "IRE", "British-owned north cannot follow the British/Irish consent path")
    count += 1
    world = northern_opening()
    option(world, "LON.54", "LON")
    option(world, "LON.55", "IRE", 1)
    require(world.owner[119] == "LON" and "LON_ts_north_pending" not in world.flags["GBR"],
            "Irish refusal either transfers the north or leaves the request locked")
    require(all("LON_ts_north_transfer_consent" not in world.flags[tag] for tag in ("LON", "GBR")),
            "Irish refusal leaves reusable northern transfer consent")
    count += 1
    for change in ("foreign_owner", "foreign_controller", "british_war", "irish_war"):
        world = northern_opening()
        option(world, "LON.54", "LON")
        if change == "foreign_owner":
            world.owner[119] = world.controller[119] = "FRA"
        elif change == "foreign_controller":
            world.controller[119] = "FRA"
        else:
            world.wars.add(frozenset(("GBR" if change == "british_war" else "IRE", "FRA")))
        require(not available(world, "LON.55", "IRE"), f"northern transfer allows stale consent after {change}")
        count += 1
    # Test the authored white_peace targets in isolation. Real alliance-war
    # behavior still requires the HOI4 engine, so this is a pair-target contract.
    wars = {frozenset(pair) for pair in (("LON", "IRE"), ("LON", "GBR"), ("IRE", "GBR"))}
    for event_id, scope, target in (("LON.50", "LON", "IRE"), ("LON.51", "GBR", "LON"), ("LON.52", "GBR", "IRE")):
        world = TerritorialModel(effect_bodies)
        world.execute(effect_bodies["LON_ts_establish_ireland"], "LON")
        world.wars = wars.copy()
        option(world, event_id, scope)
        require(world.wars == wars - {frozenset((scope, target))}, f"{event_id}: ceasefire targets the wrong pair")
        count += 1
    return count


def check():
    failures = []
    reports = []

    def require(ok, message):
        if not ok:
            failures.append(message)

    # Explicit required entry points prevent a partial checkout from reporting PASS.
    required = [
        MOD / "common/national_focus/london.txt",
        MOD / "events/LON_scenario_events.txt",
        MOD / "common/scripted_effects/LON_scenario_effects.txt",
        MOD / "common/ideas/LON_scenario.txt",
        MOD / "common/decisions/LON_scenario.txt",
        MOD / "common/decisions/categories/LON_scenario.txt",
    ]
    scoped = set(required)
    scoped.update((MOD / "events").glob("LON*.txt"))
    scoped.update((MOD / "common/decisions").glob("LON*.txt"))
    scoped.update((MOD / "common/decisions/categories").glob("LON*.txt"))
    scoped.update((MOD / "common/scripted_triggers").glob("LON_scenario*.txt"))
    parsed = {}
    for path in sorted(scoped):
        require(path.is_file(), f"missing scenario file: {path.relative_to(ROOT)}")
        if not path.is_file():
            continue
        try:
            parsed[path] = parse(path.read_text(encoding="utf-8-sig"))
        except ValueError as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if any(path not in parsed for path in required):
        return failures, reports
    reports.append(f"nested syntax parsed: {len(parsed)} script files")

    locs = defaultdict(list)
    for path in (MOD / "localisation/japanese").rglob("*.yml"):
        text = path.read_text(encoding="utf-8-sig")
        for key in LOC.findall(text):
            locs[key].append(path)
        if path.name.startswith("LON_scenario"):
            require(path.read_bytes().startswith(b"\xef\xbb\xbf"), f"missing BOM: {path.name}")
            require(text.splitlines()[0].strip() == "l_japanese:", f"bad language header: {path.name}")
            for number, line in enumerate(text.splitlines()[1:], 2):
                if line.strip() and not line.lstrip().startswith("#"):
                    require(bool(re.fullmatch(r'\s*[^\s:#]+:\d*\s+"(?:\\.|[^"\\])*"\s*', line)),
                            f"malformed localisation: {path.name}:{number}")

    refs = set()
    events = {}
    # Count definitions globally; a nested country_event call is not a definition.
    definitions = Counter()
    for path in (MOD / "events").glob("*.txt"):
        text = path.read_text(encoding="utf-8-sig")
        if "LON." not in text:
            continue
        try:
            top_level = parsed[path] if path in parsed else parse(text)
        except ValueError as exc:
            failures.append(f"cannot audit LON definitions in {path.name}: {exc}")
            continue
        for entry in top_level:
            if entry.key in ("country_event", "news_event", "state_event", "unit_leader_event") and isinstance(entry.value, list):
                event_id = scalar(entry.value, "id", "")
                if re.fullmatch(r"LON\.\d+", event_id):
                    definitions[event_id] += 1
    for name, count in definitions.items():
        require(count == 1, f"duplicate event ID: {name} ({count})")
    for path, entries in parsed.items():
        if path.parent.name != "events":
            continue
        for event in entries:
            if event.key not in ("country_event", "news_event", "state_event") or not isinstance(event.value, list):
                continue
            name = scalar(event.value, "id")
            if name:
                events[name] = event.value
                for field in ("title", "desc"):
                    for entry in values(event.value, field):
                        if isinstance(entry, str):
                            refs.add(bare(entry))
                for node in event.value:
                    if node.key == "option" and isinstance(node.value, list):
                        label = scalar(node.value, "name")
                        require(bool(label), f"{name}: option without name")
                        if label:
                            refs.add(bare(label))
    reports.append(f"event IDs unique: {len(definitions)} LON definitions")

    script_effects = set()
    script_names = {"scripted_effects": set(), "scripted_triggers": set()}
    effect_bodies = {}
    for directory in ("scripted_effects", "scripted_triggers"):
        for path in (MOD / "common" / directory).glob("*.txt"):
            names = re.findall(r"(?m)^([A-Za-z_][\w]*)\s*=\s*\{", path.read_text(encoding="utf-8-sig"))
            script_effects.update(names)
            script_names[directory].update(names)
            if path in parsed:
                effect_bodies.update({entry.key: entry.value for entry in parsed[path]
                                      if isinstance(entry.value, list)})
    ideas = set()
    for path in (MOD / "common/ideas").glob("*.txt"):
        ideas.update(re.findall(r"(?m)^\s*(LON_[\w]+)\s*=\s*\{", path.read_text(encoding="utf-8-sig")))
    calls = defaultdict(set)
    for path, entries in parsed.items():
        for node in walk(entries):
            if node.key in ("country_event", "news_event", "state_event") and isinstance(node.value, list):
                event_id = scalar(node.value, "id", "")
                if event_id.startswith("LON."):
                    require(event_id in definitions, f"{path.name}: unresolved event {event_id}")
                    calls[path.name].add(event_id)
            if node.key.startswith("LON_ts_") and node.value == "yes":
                require(node.key in script_effects, f"{path.name}: unresolved scripted effect/trigger {node.key}")
            if node.key in ("add_ideas", "remove_ideas", "has_idea", "idea"):
                candidates = [node.value] if isinstance(node.value, str) else [entry.key for entry in node.value]
                for idea in candidates:
                    if idea.startswith("LON_ts_"):
                        require(idea in ideas, f"{path.name}: unresolved idea {idea}")
            if node.key in ("custom_effect_tooltip", "custom_trigger_tooltip", "localization", "text") and isinstance(node.value, str):
                if scenario_key(node.value):
                    refs.add(node.value)

    def dictionary_names(path):
        names = set()

        def collect(value):
            if isinstance(value, dict):
                if isinstance(value.get("name"), str):
                    names.add(value["name"])
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)

        collect(json.loads(path.read_text()))
        return names

    effect_only = ((dictionary_names(ROOT / "documents/01_effects/effects.json")
                    | script_names["scripted_effects"])
                   - dictionary_names(ROOT / "documents/04_triggers/triggers.json")
                   - script_names["scripted_triggers"])
    trigger_blocks = {"trigger", "available", "visible", "allowed", "limit", "target_trigger", "cancel_trigger"}
    for path, entries in parsed.items():
        for node in walk(entries):
            if node.key in trigger_blocks and isinstance(node.value, list):
                for condition in walk(node.value):
                    require(condition.key not in effect_only,
                            f"{path.name}: effect {condition.key} inside {node.key}")
            if node.key in ("clamp_variable", "clamp_temp_variable") and isinstance(node.value, list):
                require(bool(scalar(node.value, "var")), f"{path.name}: {node.key} missing explicit var")
            if node.key == "set_country_flag" and isinstance(node.value, list):
                require(bool(scalar(node.value, "flag")), f"{path.name}: timed country flag missing flag")
            if node.key == "set_capital":
                require(isinstance(node.value, list) and bool(scalar(node.value, "state")),
                        f"{path.name}: set_capital requires {{ state = ... }}")
    reports.append("trigger/effect boundaries and explicit variable/flag arguments")

    focus_entries = parsed[required[0]]
    trees = values(focus_entries, "focus_tree")
    require(len(trees) == 1, "london.txt: expected one focus tree")
    focuses = {}
    positions = defaultdict(list)
    if trees:
        for block in values(trees[0], "focus"):
            name = scalar(block, "id")
            require(name not in focuses, f"duplicate focus ID: {name}")
            focuses[name] = block
            label = scalar(block, "text", name)
            refs.update((label, label + "_desc"))
            positions[(scalar(block, "x", "0"), scalar(block, "y", "0"))].append(name)
    for position, names in positions.items():
        require(len(names) == 1, f"focus nodes overlap at {position}: {', '.join(names)}")
    prerequisites = {}
    for name, block in focuses.items():
        prerequisites[name] = []
        for node in block:
            if node.key in ("prerequisite", "mutually_exclusive") and isinstance(node.value, list):
                for ref in values(node.value, "focus"):
                    require(ref in focuses, f"{name}: unresolved {node.key} focus {ref}")
                    if node.key == "prerequisite":
                        prerequisites[name].append(ref)
        for node in walk(block):
            if node.key == "has_completed_focus":
                require(node.value in focuses, f"{name}: unresolved eligibility focus {node.value}")

    def visit(name, stack=()):
        require(name not in stack, f"focus prerequisite cycle: {' -> '.join(stack + (name,))}")
        if name in stack:
            return
        for ref in prerequisites.get(name, []):
            visit(ref, stack + (name,))

    for name in focuses:
        visit(name)
    # The opening and financial path must remain usable before IRE has territory.
    for name in ("LON_ts_census", "LON_financial_hub", "LON_commonwealth_relations", "LON_global_influence"):
        require(name in focuses, f"missing opening/financial focus {name}")
        if name in focuses:
            required_refs = set()
            todo = [name]
            while todo:
                current = todo.pop()
                if current in required_refs:
                    continue
                required_refs.add(current)
                todo.extend(prerequisites.get(current, []))
            require("LON_celtic_unification" not in required_refs,
                    f"{name}: financial/opening path still gated by Celtic unification")
            for ancestor in required_refs:
                for condition in values(focuses[ancestor], "available"):
                    require(not any(node.value == "IRE" and node.key in ("country_exists", "is_neighbor_of") for node in positive_conditions(condition)),
                            f"{name}: requires landless IRE before constitution")
    reports.append(f"focus graph and distinct positions: {len(focuses)} nodes")

    # Walk real event/effect call edges from focus rewards, decisions, and MTTH
    # events. A defined triggered-only event with no caller is dead content.
    def outgoing(entries, seen=()):
        result = set()
        for node in walk(entries):
            if node.key in ("country_event", "news_event", "state_event") and isinstance(node.value, list):
                target = scalar(node.value, "id", "")
                if target.startswith("LON."):
                    result.add(target)
            if node.key in effect_bodies and node.value == "yes":
                require(node.key not in seen, f"recursive scenario effect: {' -> '.join(seen + (node.key,))}")
                if node.key not in seen:
                    result.update(outgoing(effect_bodies[node.key], seen + (node.key,)))
        return result

    reachable = set()
    for path, entries in parsed.items():
        if path.parent.name != "events" and path.parent.name != "scripted_effects":
            reachable.update(outgoing(entries))
    for name, entries in events.items():
        if scalar(entries, "is_triggered_only") != "yes":
            reachable.add(name)
    pending = list(reachable)
    while pending:
        name = pending.pop()
        for target in outgoing(events.get(name, [])):
            if target not in reachable:
                reachable.add(target)
                pending.append(target)
    for name in events:
        if int(name.partition(".")[2]) >= 30:
            require(name in reachable, f"triggered-only scenario event has no reachable caller: {name}")
    reports.append(f"event call reachability: {len(reachable)} LON events reachable from authored entry points")

    for path, entries in parsed.items():
        if path.parent == MOD / "common/ideas":
            for node in walk(entries):
                if node.key.startswith("LON_ts_") and isinstance(node.value, list):
                    refs.update((node.key, node.key + "_desc"))
        if path.parent in (MOD / "common/decisions", MOD / "common/decisions/categories"):
            for node in walk(entries):
                if node.key.startswith("LON_ts_") and isinstance(node.value, list):
                    refs.update((node.key, node.key + "_desc"))
    new_refs = {key for key in refs if scenario_key(key)}
    for key in sorted(new_refs):
        require(len(locs[key]) == 1, f"localisation {key}: expected one definition, found {len(locs[key])}")
    for key, paths in locs.items():
        if scenario_key(key):
            require(len(paths) == 1, f"duplicate scenario localisation: {key}")
    reports.append(f"Japanese UI references resolved once: {len(new_refs)} keys")

    produced_flags = set()
    consumed_flags = set()
    for entries in parsed.values():
        for node in walk(entries):
            if node.key in ("set_country_flag", "set_global_flag"):
                flag = scalar(node.value, "flag", "") if isinstance(node.value, list) else node.value
                produced_flags.add(flag)
            elif node.key in ("has_country_flag", "has_global_flag") and isinstance(node.value, str):
                consumed_flags.add(node.value)
    for flag in consumed_flags:
        if flag.startswith("LON_ts_"):
            require(flag in produced_flags, f"scenario flag checked but never set: {flag}")
    reports.append(f"scenario flag producers: {len([f for f in produced_flags if f.startswith('LON_ts_')])}")
    try:
        model_cases = check_territorial_effects(effect_bodies, events, require)
        reports.append(f"territorial effect model: {model_cases} normal/adversarial cases (not game execution)")
        diplomatic_cases = check_diplomatic_paths(effect_bodies, events, require)
        reports.append(f"diplomatic effect model: {diplomatic_cases} consent/stale-state/pair-target cases (not game execution)")
    except (ValueError, KeyError, IndexError) as exc:
        failures.append(f"territorial model: {exc}")
    return failures, reports


def main():
    failures, reports = check()
    for report in reports:
        print("CHECK" if failures else "PASS", report)
    for failure in failures:
        print("FAIL", failure)
    print("SKIP HOI4 runtime, UI, AI behavior and save compatibility (static verification only)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
