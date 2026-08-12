#!/usr/bin/env python3
"""旧ATRMブランチの艦船スロットを継承込みで棚卸しする。"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence


DEFAULT_REF = "origin/future/Navy_rework"
DEFAULT_PATHS = (
    "bakasekai/common/units/ship_hull_carrier.txt",
    "bakasekai/common/units/ship_hull_cruiser.txt",
    "bakasekai/common/units/ship_hull_heavy.txt",
    "bakasekai/common/units/ship_hull_light.txt",
    "bakasekai/common/units/ship_hull_submarine.txt",
)


@dataclass(frozen=True)
class Assignment:
    key: str
    value: str | "Block"


@dataclass(frozen=True)
class Block:
    assignments: tuple[Assignment, ...]

    def first(self, key: str) -> str | "Block" | None:
        for assignment in self.assignments:
            if assignment.key == key:
                return assignment.value
        return None


@dataclass(frozen=True)
class Hull:
    hull_id: str
    source_path: str
    block: Block


TOKEN_RE = re.compile(r'"(?:\\.|[^"\\])*"|[{}=]|[^\s{}=]+')


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        quoted = False
        escaped = False
        kept: list[str] = []
        for char in line:
            if char == '"' and not escaped:
                quoted = not quoted
            if char == "#" and not quoted:
                break
            kept.append(char)
            escaped = char == "\\" and not escaped
            if char != "\\":
                escaped = False
        lines.append("".join(kept))
    return "\n".join(lines)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(strip_comments(text))


def parse_block(tokens: Sequence[str], index: int) -> tuple[Block, int]:
    if tokens[index] != "{":
        raise ValueError(f"expected '{{' at token {index}, got {tokens[index]!r}")
    index += 1
    assignments: list[Assignment] = []
    while index < len(tokens) and tokens[index] != "}":
        key = tokens[index]
        index += 1
        if index >= len(tokens) or tokens[index] != "=":
            # category list等の裸値はスロット抽出に不要。
            continue
        index += 1
        if index >= len(tokens):
            raise ValueError(f"missing value for {key!r}")
        if tokens[index] == "{":
            value, index = parse_block(tokens, index)
        else:
            value = tokens[index].strip('"')
            index += 1
        assignments.append(Assignment(key, value))
    if index >= len(tokens):
        raise ValueError("unclosed block")
    return Block(tuple(assignments)), index + 1


def parse_document(text: str) -> Block:
    tokens = tokenize(text)
    assignments: list[Assignment] = []
    index = 0
    while index < len(tokens):
        key = tokens[index]
        index += 1
        if index >= len(tokens) or tokens[index] != "=":
            continue
        index += 1
        if tokens[index] == "{":
            value, index = parse_block(tokens, index)
        else:
            value = tokens[index].strip('"')
            index += 1
        assignments.append(Assignment(key, value))
    return Block(tuple(assignments))


def git_text(repo: Path, ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def git_revision(repo: Path, ref: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", ref],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def load_hulls(repo: Path, ref: str, paths: Sequence[str]) -> dict[str, Hull]:
    hulls: dict[str, Hull] = {}
    for path in paths:
        document = parse_document(git_text(repo, ref, path))
        equipments = document.first("equipments")
        if not isinstance(equipments, Block):
            raise ValueError(f"equipments block not found: {path}")
        for assignment in equipments.assignments:
            if not isinstance(assignment.value, Block):
                continue
            if assignment.key in hulls:
                raise ValueError(f"duplicate equipment id: {assignment.key}")
            hulls[assignment.key] = Hull(assignment.key, path, assignment.value)
    return hulls


def scalar(block: Block, key: str) -> str:
    value = block.first(key)
    return value if isinstance(value, str) else ""


def inheritance_source(hull: Hull, hulls: dict[str, Hull]) -> str:
    parent = scalar(hull.block, "parent")
    if parent in hulls:
        return parent
    archetype = scalar(hull.block, "archetype")
    if archetype and archetype != hull.hull_id and archetype in hulls:
        return archetype
    return ""


def slot_map(
    hull_id: str,
    hulls: dict[str, Hull],
    memo: dict[str, dict[str, str]],
    stack: tuple[str, ...] = (),
) -> dict[str, str]:
    if hull_id in memo:
        return memo[hull_id]
    if hull_id in stack:
        raise ValueError(f"inheritance cycle: {' -> '.join((*stack, hull_id))}")
    hull = hulls[hull_id]
    slots = hull.block.first("module_slots")
    source = inheritance_source(hull, hulls)
    if slots == "inherit":
        if not source:
            raise ValueError(f"{hull_id}: module_slots=inherit without parent/archetype")
        effective = dict(slot_map(source, hulls, memo, (*stack, hull_id)))
    elif isinstance(slots, Block):
        source_slots = (
            slot_map(source, hulls, memo, (*stack, hull_id)) if source else {}
        )
        effective = {}
        for assignment in slots.assignments:
            if assignment.key in effective:
                raise ValueError(f"{hull_id}: duplicate slot {assignment.key}")
            if assignment.value == "inherit":
                if assignment.key not in source_slots:
                    raise ValueError(
                        f"{hull_id}: slot {assignment.key}=inherit is absent from {source}"
                    )
                effective[assignment.key] = f"inherit:{source}"
            elif isinstance(assignment.value, Block):
                effective[assignment.key] = "declared"
            else:
                # 別スロット名を値に取る短縮定義も1物理枠として数える。
                effective[assignment.key] = f"alias:{assignment.value}"
        for slot_id, provenance in effective.items():
            if provenance.startswith("alias:"):
                target = provenance.removeprefix("alias:")
                if target not in effective:
                    raise ValueError(f"{hull_id}: slot {slot_id} aliases missing {target}")
    else:
        effective = {}
    memo[hull_id] = effective
    return effective


def zone(slot_id: str) -> str:
    if slot_id.startswith("front_") or "_bow_" in slot_id:
        return "front"
    if slot_id.startswith("mid_"):
        return "mid"
    if slot_id.startswith("rear_"):
        return "rear"
    if slot_id.startswith("optional_"):
        return "optional"
    return "fixed" if slot_id.startswith("fixed_") else "other"


def iter_rows(hulls: dict[str, Hull]) -> Iterator[dict[str, object]]:
    memo: dict[str, dict[str, str]] = {}
    for hull_id in sorted(hulls):
        hull = hulls[hull_id]
        raw_slots = hull.block.first("module_slots")
        effective = slot_map(hull_id, hulls, memo)
        source = inheritance_source(hull, hulls)
        source_slots = slot_map(source, hulls, memo) if source else {}
        explicit_assignments = raw_slots.assignments if isinstance(raw_slots, Block) else ()
        inherited_entries = sum(a.value == "inherit" for a in explicit_assignments)
        overridden_entries = sum(
            a.key in source_slots and a.value != "inherit" for a in explicit_assignments
        )
        new_entries = sum(a.key not in source_slots for a in explicit_assignments)
        counts = {name: 0 for name in ("fixed", "front", "mid", "rear", "optional", "other")}
        for slot_id in effective:
            counts[zone(slot_id)] += 1
        yield {
            "hull_id": hull_id,
            "source_path": hull.source_path,
            "parent_id": scalar(hull.block, "parent"),
            "archetype_id": scalar(hull.block, "archetype"),
            "inheritance_source": source,
            "module_slots_mode": "inherit" if raw_slots == "inherit" else "block" if isinstance(raw_slots, Block) else "absent",
            "declared_slots": len(explicit_assignments),
            "inherited_slot_entries": inherited_entries,
            "overridden_slots": overridden_entries,
            "new_slots": new_entries,
            "effective_slots": len(effective),
            "fixed_slots": counts["fixed"],
            "custom_slots": len(effective) - counts["fixed"],
            "front_slots": counts["front"],
            "mid_slots": counts["mid"],
            "rear_slots": counts["rear"],
            "optional_slots": counts["optional"],
            "other_slots": counts["other"],
            "effective_slot_ids": ";".join(effective),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--path", action="append", dest="paths")
    args = parser.parse_args()
    paths = tuple(args.paths or DEFAULT_PATHS)
    hulls = load_hulls(args.repo.resolve(), args.ref, paths)
    rows = list(iter_rows(hulls))
    revision = git_revision(args.repo.resolve(), args.ref)
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(
                {
                    "source_ref": args.ref,
                    "source_commit": revision,
                    "source_paths": paths,
                    "hulls": rows,
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
    if not args.csv and not args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"ATRMRW slot inventory: {len(rows)} hulls, ref={args.ref}, commit={revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
