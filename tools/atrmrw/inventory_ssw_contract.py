#!/usr/bin/env python3
"""固定SSWコミットからATRMRWが同期するroleと船体archetypeを抽出する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

try:
    from .inventory_atrm_slots import Block, git_revision, git_text, parse_document, scalar
except ImportError:  # 直接スクリプト実行時
    from inventory_atrm_slots import Block, git_revision, git_text, parse_document, scalar


DEFAULT_COMMIT = "4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1"
ROLE_PATH = "common/units/equipment/modules/00_S_role.txt"
EQUIPMENT_ROOT = "common/units/equipment"
ROLE_RE = re.compile(r"^\s*(SRM_[A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
NAVAL_ARCHETYPE_FILES = {
    "ocean_surveillance_ship.txt",
    "submarine_oiler.txt",
}


def is_naval_archetype_path(path: str) -> bool:
    name = Path(path).name
    return name.startswith("ship_hull_") or name in NAVAL_ARCHETYPE_FILES


def git_paths(repo: Path, ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--", EQUIPMENT_ROOT],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return [path for path in result.stdout.splitlines() if path.endswith(".txt")]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ssw-repo", type=Path, required=True)
    parser.add_argument("--commit", default=DEFAULT_COMMIT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    revision = git_revision(args.ssw_repo, args.commit)
    role_text = git_text(args.ssw_repo, revision, ROLE_PATH)
    role_ids = sorted(set(ROLE_RE.findall(role_text)))
    archetypes = []
    input_hash = hashlib.sha256()
    input_hash.update(role_text.encode())
    for path in git_paths(args.ssw_repo, revision):
        text = git_text(args.ssw_repo, revision, path)
        input_hash.update(path.encode())
        input_hash.update(text.encode())
        document = parse_document(text)
        equipments = document.first("equipments")
        if not isinstance(equipments, Block):
            continue
        for assignment in equipments.assignments:
            if not isinstance(assignment.value, Block):
                continue
            block = assignment.value
            if scalar(block, "is_archetype") != "yes" or not is_naval_archetype_path(path):
                continue
            slots = block.first("module_slots")
            slot_ids = [a.key for a in slots.assignments] if isinstance(slots, Block) else []
            archetypes.append({
                "archetype_id": assignment.key,
                "source_path": path,
                "module_slot_count": len(slot_ids),
                "visible_base_slot_count": sum(not slot_id.startswith("hidden_") for slot_id in slot_ids),
                "hidden_base_slot_count": sum(slot_id.startswith("hidden_") for slot_id in slot_ids),
                "module_slot_ids": slot_ids,
            })

    payload = {
        "source_repository": str(args.ssw_repo.resolve()),
        "source_commit": revision,
        "role_source_path": ROLE_PATH,
        "input_sha256": input_hash.hexdigest(),
        "role_count": len(role_ids),
        "role_ids": role_ids,
        "equipment_archetype_count": len(archetypes),
        "equipment_archetypes": sorted(archetypes, key=lambda row: row["archetype_id"]),
        "atrmrw_contract": {
            "sync_role_ids": True,
            "copy_hidden_operation": False,
            "all_atrmrw_slots_visible": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"SSW contract inventory: {len(role_ids)} roles, {len(archetypes)} archetypes, "
        f"commit={revision}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
