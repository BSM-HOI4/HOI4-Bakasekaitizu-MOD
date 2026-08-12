#!/usr/bin/env python3
"""現行BSMのATRMRW影響面をJSONへ棚卸しする。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Iterator

from inventory_atrm_slots import Block, parse_document, strip_comments


HULL_PATHS = (
    "bakasekai/common/units/equipment/ship_hull_carrier.txt",
    "bakasekai/common/units/equipment/ship_hull_cruiser.txt",
    "bakasekai/common/units/equipment/ship_hull_heavy.txt",
    "bakasekai/common/units/equipment/ship_hull_light.txt",
    "bakasekai/common/units/equipment/ship_hull_submarine.txt",
    "bakasekai/common/units/equipment/repair_ships.txt",
    "bakasekai/common/units/equipment/support_ships.txt",
)
MODULE_PATH = "bakasekai/common/units/equipment/modules/00_ship_modules.txt"
TECHNOLOGY_PATHS = (
    "bakasekai/common/technologies/naval.txt",
    "bakasekai/common/technologies/MTG_naval.txt",
    "bakasekai/common/technologies/MTG_naval_Support.txt",
)


def git_revision(repo: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def named_blocks(path: Path, root_key: str) -> list[str]:
    document = parse_document(path.read_text(encoding="utf-8-sig"))
    root = document.first(root_key)
    if not isinstance(root, Block):
        raise ValueError(f"{path}: {root_key} block not found")
    return [a.key for a in root.assignments if isinstance(a.value, Block) and a.key != "limit"]


def iter_assignments(block: Block) -> Iterator[tuple[str, str | Block]]:
    for assignment in block.assignments:
        yield assignment.key, assignment.value
        if isinstance(assignment.value, Block):
            yield from iter_assignments(assignment.value)


def scalar(block: Block, key: str) -> str:
    value = block.first(key)
    return value if isinstance(value, str) else ""


def inventory_variants(repo: Path, paths: Iterator[Path], hull_ids: set[str]) -> dict[str, object]:
    total = 0
    naval = 0
    files: Counter[str] = Counter()
    types: Counter[str] = Counter()
    parse_failures: list[str] = []
    for path in paths:
        try:
            document = parse_document(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, ValueError):
            parse_failures.append(str(path))
            continue
        for key, value in iter_assignments(document):
            if key != "create_equipment_variant" or not isinstance(value, Block):
                continue
            total += 1
            variant_type = scalar(value, "type")
            if variant_type in hull_ids or variant_type.startswith("ship_hull_"):
                naval += 1
                files[str(path.relative_to(repo))] += 1
                types[variant_type] += 1
    return {
        "all_equipment_variants": total,
        "naval_variants": naval,
        "naval_variant_files": dict(sorted(files.items())),
        "naval_variant_types": dict(sorted(types.items())),
        "parse_failures": parse_failures,
    }


def reference_files(repo: Path, hull_ids: set[str], roots: tuple[str, ...]) -> dict[str, list[str]]:
    pattern = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(map(re.escape, sorted(hull_ids, key=len, reverse=True))) + r")(?![A-Za-z0-9_])")
    result: dict[str, list[str]] = {}
    for root in roots:
        for path in sorted((repo / root).rglob("*.txt")):
            text = strip_comments(path.read_text(encoding="utf-8-sig", errors="replace"))
            hits = sorted(set(pattern.findall(text)))
            if hits:
                result[str(path.relative_to(repo))] = hits
    return result


def oob_inventory(repo: Path) -> dict[str, object]:
    files: dict[str, int] = {}
    pattern = re.compile(r"(?m)^\s*ship\s*=\s*\{")
    for path in sorted((repo / "bakasekai/history/units").rglob("*.txt")):
        count = len(pattern.findall(strip_comments(path.read_text(encoding="utf-8-sig", errors="replace"))))
        if count:
            files[str(path.relative_to(repo))] = count
    return {"ship_entries": sum(files.values()), "files": files}


def input_digest(repo: Path) -> str:
    paths = {repo / path for path in (*HULL_PATHS, MODULE_PATH, *TECHNOLOGY_PATHS)}
    for root in (
        "bakasekai/common/scripted_effects",
        "bakasekai/history",
        "bakasekai/interface",
        "bakasekai/gfx/interface/equipmentdesigner",
    ):
        root_path = repo / root
        if root_path.exists():
            paths.update(path for path in root_path.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(str(path.relative_to(repo)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()

    hulls_by_file = {
        path: named_blocks(repo / path, "equipments") for path in HULL_PATHS
    }
    hull_ids = {hull for hulls in hulls_by_file.values() for hull in hulls}
    modules = named_blocks(repo / MODULE_PATH, "equipment_modules")
    technologies = {
        path: named_blocks(repo / path, "technologies") for path in TECHNOLOGY_PATHS
    }
    variant_roots = (
        repo / "bakasekai/common/scripted_effects",
        repo / "bakasekai/history",
    )
    variants = inventory_variants(
        repo,
        (path for root in variant_roots for path in root.rglob("*.txt")),
        hull_ids,
    )
    references = reference_files(
        repo,
        hull_ids,
        (
            "bakasekai/common/scripted_effects",
            "bakasekai/common/technologies",
            "bakasekai/history/countries",
            "bakasekai/history/units",
        ),
    )
    gui_files = sorted(
        str(path.relative_to(repo))
        for path in (repo / "bakasekai/interface").rglob("*")
        if path.is_file() and "equipmentdesigner" in str(path).lower()
    )
    gfx_files = sorted(
        str(path.relative_to(repo))
        for path in (repo / "bakasekai/gfx/interface/equipmentdesigner").rglob("*")
        if path.is_file()
    ) if (repo / "bakasekai/gfx/interface/equipmentdesigner").exists() else []
    payload = {
        "source_commit": git_revision(repo),
        "input_sha256": input_digest(repo),
        "hulls": {
            "count": len(hull_ids),
            "by_file": hulls_by_file,
        },
        "modules": {
            "count": len(modules),
            "source_path": MODULE_PATH,
            "ids": modules,
        },
        "technologies": {
            "count": sum(len(ids) for ids in technologies.values()),
            "by_file": technologies,
        },
        "variants": variants,
        "oob": oob_inventory(repo),
        "hull_reference_files": {
            "count": len(references),
            "files": references,
        },
        "equipment_designer": {
            "interface_files": gui_files,
            "gfx_asset_count": len(gfx_files),
            "gfx_assets": gfx_files,
        },
    }
    if args.check:
        existing = json.loads(args.json.read_text(encoding="utf-8"))
        if existing != payload:
            print(f"ATRMRW BSM inventory FAILED: snapshot drifted: {args.json}")
            return 1
    else:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "ATRMRW BSM inventory: "
        f"{len(hull_ids)} hulls, {len(modules)} modules, "
        f"{variants['naval_variants']} naval variants, {len(references)} reference files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
